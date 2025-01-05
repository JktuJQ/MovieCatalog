from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from films.models import Film

from django.forms import modelformset_factory
from django.forms.utils import ErrorList
from .forms import PollForm, QuestionForm, ChoiceForm, ChoiceFormSet, ChoiceUpdateFormSet
from .models import Poll, Question, Choice


@login_required
def create_poll(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user
            poll.film = film
            poll.save()
            return redirect('films:film_detail', id=poll.film.id)
    else:
        form = PollForm(initial={'film': film})
    return render(request, 'polls/create_poll.html', {'form': form})


@login_required
def create_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.author:
        return redirect('films:film_detail', id=poll.film.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.poll = poll
            question.save()

            for form in formset.forms:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()

            return redirect('films:film_detail', id=poll.film.id)
    else:
        form = QuestionForm(initial={'poll': poll})
        formset = ChoiceFormSet()

    return render(request, 'polls/create_question.html', {
        'form': form,
        'formset': formset,
        'poll': poll,
    })


@login_required
def create_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.poll.author:
        return redirect('films:film_detail', id=question.poll.film.id)

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('films:film_detail', id=question.poll.film.id)
    else:
        form = ChoiceForm()

    return render(request, 'polls/create_choice.html', {
        'form': form,
        'question': question,
    })


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.poll.author:
        return redirect('films:film_detail', id=question.poll.film.id)
    if request.method == 'POST':
        question.delete()
        return redirect('films:film_detail', id=question.poll.film.id)
    return render(request, 'polls/confirm_delete_question.html', {'question': question})


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
def update_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.user != poll.author:
        return redirect('films:film_detail', id=poll.film.id)

    QuestionFormSet = modelformset_factory(Question, fields=('position',), extra=0)

    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, queryset=poll.questions.all())
        if formset.is_valid():
            formset.save()

            return redirect('films:film_detail', id=poll.film.id)
    else:
        formset = QuestionFormSet(queryset=poll.questions.all())

    return render(request, 'polls/update_poll.html', {
        'formset': formset,
        'poll': poll,
    })


@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.poll.author:
        return redirect('films:film_detail', id=question.poll.film.id)

    ChoiceFormSet = modelformset_factory(
        Choice,
        formset=ChoiceUpdateFormSet,
        fields=('position',),
        extra=0,
    )

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, queryset=question.choice_set.all())
        if formset.is_valid():
            non_deleted_choices = sum(1 for form in formset if not form.cleaned_data.get('DELETE'))
            if non_deleted_choices < 2:
                formset._non_form_errors = ErrorList(["A question must have at least two choices."])
            else:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.save()
                for form in formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                return redirect('films:film_detail', id=question.poll.film.id)
    else:
        formset = ChoiceFormSet(queryset=question.choice_set.all())

    return render(request, 'polls/update_question.html', {
        'formset': formset,
        'question': question,
    })


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
