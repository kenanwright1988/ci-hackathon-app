from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, reverse, redirect, get_object_or_404

from .helpers import extract_badges_for_hackathon
from accounts.models import UserType, CustomUser
from accounts.decorators import can_access
from hackathon.models import Hackathon, HackTeam


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackadmin_panel(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    hackathons = Hackathon.objects.order_by('-start_date').exclude(
        status='deleted')
    return render(request, 'hackadmin_panel.html', {
        'hackathons': hackathons,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackathon_participants(request, hackathon_id):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    slack_url = None
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    mentors = [{
        'team': team,
        'mentor': team.mentor
        } for team in hackathon.teams.all()]
    if settings.SLACK_ENABLED:
        slack_url = f'https://{settings.SLACK_WORKSPACE}.slack.com/team/'
    badges_csv = 'data:text/csv;charset=utf-8,' + extract_badges_for_hackathon(
            hackathon, date.today().isoformat(), format='csv')
    awardees = [awardee for category, values in extract_badges_for_hackathon(
            hackathon, date.today().isoformat()).items()
            for awardee in values
            if category not in ['participants', 'judges', 'facilitators']]
    return render(request, 'hackadmin_participants.html', {
        'hackathon': hackathon,
        'mentors': mentors,
        'awardees': awardees,
        'slack_url': slack_url,
        'badges_csv': badges_csv,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def all_users(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'all_users.html', {
        'hackathons': hackathons,
        'users': users,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def remove_participant(request, hackathon_id):
    if request.method == 'POST':
        remove_from_hackathon = (request.POST.get('remove_from_hackathon')
                                 == 'True')
        participant = get_object_or_404(
            CustomUser, id=request.POST.get('participant_id'))

        if remove_from_hackathon:
            hackathon = get_object_or_404(Hackathon, id=hackathon_id)
            hackathon.participants.remove(participant)
            teams = hackathon.teams.filter(participants__in=[participant.id])
            for team in teams:
                team.participants.remove(participant)
        else:
            team = get_object_or_404(HackTeam,
                                     id=request.POST.get('team_id'))
            team.participants.remove(participant)

        if request.POST.get('dropoffs'):
            participant.dropoffs += 1
            participant.dropped_off_hackathon = get_object_or_404(Hackathon, id=hackathon_id)
            participant.save()

        messages.success(request, 'Participant successfully removed')
        return redirect(reverse('hackadmin:hackathon_participants',
                                kwargs={'hackathon_id': hackathon_id}))
    else:
        return HttpResponseBadRequest()


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def add_participant(request, hackathon_id):
    if request.method == 'POST':
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        participant = get_object_or_404(
            CustomUser, id=request.POST.get('participant_id'))
        hackathon.participants.add(participant)
        if request.POST.get('team_id'):
            team = get_object_or_404(HackTeam, id=request.POST.get('team_id'))
            team.participants.add(participant)
        return redirect(reverse('hackadmin:all_users'))
    else:
        return HttpResponseBadRequest()


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def add_judge(request):
    if request.method == 'POST':
        hackathon = get_object_or_404(Hackathon,
                                      id=request.POST.get('hackathon_id'))
        judge = get_object_or_404(
            CustomUser, id=request.POST.get('judge_id'))
        if judge.user_type in [
                UserType.SUPERUSER, UserType.STAFF,
                UserType.FACILITATOR_ADMIN, UserType.PARTNER_ADMIN,
                UserType.FACILITATOR_JUDGE, UserType.PARTNER_JUDGE]:
            hackathon.judges.add(judge)
            messages.success(request, ('User successfully added as judge to '
                                       'selected hackathon.'))
        else:
            messages.error(request, ('This user does not have the right '
                                     'priveleges to be a judge.'))
        return redirect(reverse('hackadmin:all_users'))
    else:
        return HttpResponseBadRequest()
