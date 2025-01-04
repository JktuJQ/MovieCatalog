from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from films.models import Film

from .forms import PollForm, QuestionForm, ChoiceForm, QuestionFormSet, ChoiceFormSet
from .models import Poll, Question, Choice


@login_required
def create_poll(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    poll_form = PollForm()
    question_formset = QuestionFormSet()
    forms = []
    for i in range(question_formset.total_form_count()):
        choice_formset = ChoiceFormSet(prefix=f'choices_{i}')
        forms.append({
            'question_form': question_formset.forms[i],
            'choice_formset': choice_formset,
        })

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        forms = []
        for i, question_form in enumerate(question_formset):
            choice_formset = ChoiceFormSet(request.POST, prefix=f'choices_{i}')
            forms.append({
                'question_form': question_form,
                'choice_formset': choice_formset,
            })

        if poll_form.is_valid() and question_formset.is_valid() and all(
                cf['choice_formset'].is_valid() for cf in forms):
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.film = film
            poll.save()

            for form in forms:
                question_form = form['question_form']
                choice_formset = form['choice_formset']
                if question_form.is_valid() and choice_formset.is_valid():
                    question = question_form.save(commit=False)
                    question.poll = poll
                    question.save()

                    for choice_form in choice_formset:
                        choice = choice_form.save(commit=False)
                        choice.question = question
                        choice.save()

            return redirect('polls:poll_statistics', poll_id=poll.id)

    return render(request, 'polls/create_poll.html', {
        'poll_form': poll_form,
        'forms': forms,
        'film': film,
    })


@login_required
def confirm_delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.author:
        return redirect('films:film_detail', id=poll.film.id)
    return render(request, 'polls/confirm_delete_poll.html', {'poll': poll})


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == 'POST' and request.user == poll.author:
        poll.delete()

    return redirect('films:film_detail', id=poll.film.id)


@login_required
def submit_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user

    for question in poll.questions.all():
        for choice in question.choice_set.all():
            choice.votes.remove(user)

    for question in poll.questions.all():
        selected_choices = request.POST.getlist('question_{}'.format(question.id))
        for choice_id in selected_choices:
            choice = get_object_or_404(Choice, pk=choice_id)
            choice.votes.add(user)

    return redirect('polls:poll_statistics', poll_id=poll.id)


def has_completed_poll(user, poll):
    for question in poll.questions.all():
        if question.question_type == "Один вариант ответа":
            user_votes = question.choice_set.filter(votes=user)
            if not user_votes.exists() or user_votes.count() != 1:
                return False
        elif question.question_type == "Несколько вариантов ответа":
            user_votes = question.choice_set.filter(votes=user)
            if not user_votes.exists():
                return False
    return True


@login_required
def poll_statistics(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user

    if user == poll.author or has_completed_poll(user, poll):
        statistics = []
        for question in poll.questions.all():
            stats = {
                'question': question,
                'choices': []
            }
            for choice in question.choice_set.all():
                stats['choices'].append({
                    'choice': choice,
                    'vote_count': choice.votes.count()
                })
            statistics.append(stats)
        return render(request, 'polls/poll_statistics.html', {'statistics': statistics, 'poll': poll})
    else:
        return redirect('films:film_detail', film_id=poll.film.id)
