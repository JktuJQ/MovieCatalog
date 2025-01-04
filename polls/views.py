from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Poll, Choice


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


@login_required
def poll_statistics(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all()
    statistics = []
    for question in questions:
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
    return render(request, 'polls/poll_statistics.html', {'statistics': statistics})
