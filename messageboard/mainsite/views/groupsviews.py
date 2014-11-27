from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from mainsite.forms import GroupForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from mainsite.models import Topic, Message, Group
from mainsite.views import helperviews

@login_required(login_url='/mainsite/login')
def create_group(request):
    if request.method == 'POST':
        user = request.user
        try:
            existing_group = Group.objects.get(group_name__iexact=request.POST['group_name'])
        except Group.DoesNotExist:
            group = Group(group_name=request.POST['group_name'],
                          group_password=request.POST['group_password'], creator=request.user)
            group.save()
            group.user_set.add(user)
            user.joined_groups.add(group)
        return redirect(reverse('mainsite:messageboard'))
    else:
        return render(request, 'groups/create_group.html', {'form': GroupForm})

    
@login_required(login_url='/mainsite/login')
def group(request, groupid):
    this_group = Group.objects.get(id=groupid)
    if request.method == 'POST':
        if "INVITE" in request.POST:
            return redirect('inviteuser/')
        if "REMOVE" in request.POST:
            this_group.delete()
            return redirect(reverse('mainsite:messageboard'))
        elif "ADDMOD" in request.POST:
            mod_name = request.POST['mod_name']
            try:
                if mod_name != this_group.creator.username:
                    mod_user = this_group.user_set.get(username=mod_name)
                    this_group.mod_set.add(mod_user)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('mainsite:group', args=(groupid,)))                    
            return HttpResponseRedirect(reverse('mainsite:group', args=(groupid,)))
        elif "POSTMSG" in request.POST:
            helperviews.post_message(request.POST['message_content'], Topic.objects.get(id=request.POST['topic_id']), request.user)
            return HttpResponseRedirect(reverse('mainsite:group', args=(groupid,)))
    else:
        group_creator = this_group.creator
        user_list = this_group.user_set.all()
        mod_list = this_group.mod_set.all()
        topic_list = this_group.viewable_topics.all()
        message_list = Message.objects.all()
        return render(request, 'groups/group.html', {'group': this_group,
                                                     'creator': group_creator,
                                                     'mods': mod_list,
                                                     'users': user_list,
                                                     'topics': topic_list,
                                                     'messages': message_list})

@login_required(login_url='/mainsite/login')
def joined_groups(request):
    user = request.user
    group_list = user.joined_groups.all()
    return render(request, 'groups/joined_groups.html', {'groups': group_list})


@login_required(login_url='/mainsite/login')
def join_group(request):
    all_groups = Group.objects.all()
    if request.method == 'POST':
        # Get the user and group object
        user = request.user
        try:
            this_group = Group.objects.get(group_name=request.POST['group_name'])
        except Group.DoesNotExist:
            return helperviews.response(request,
                            'Nonexistent Group',
                            'Group does not exist.',
                            '/mainsite/messageboard/joingroup/',
                            'Back')
        # Add the user to the group if the password is correct
        if this_group.group_password == request.POST['group_password']:
            this_group.user_set.add(user)
            user.joined_groups.add(this_group)
        else:
            return helperviews.response(request,
                            'Incorrect Password',
                            'Password is incorrect.',
                            '/mainsite/messageboard/joingroup/',
                            'Back')
        return redirect(reverse('mainsite:messageboard'))
    else:
        return render(request, 'groups/join_group.html', {'form': GroupForm, 'groups': all_groups})
