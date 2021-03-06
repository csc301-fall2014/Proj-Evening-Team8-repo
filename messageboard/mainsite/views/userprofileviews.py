from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from mainsite.forms import UserProfileForm, DirectMessageForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from mainsite.models import UserProfile, Group, Requests, Conversation, DirectMessage


@login_required(login_url='/mainsite/login')
def userprofile(request, userid):
    user_to_display = User.objects.get(id=userid)
    logged_in_user = request.user
    return render(request, 'userprofile/userprofile.html', {'user_to_display': user_to_display,
     'logged_in_user': logged_in_user})


@login_required(login_url='/mainsite/login')
def edituserprofile(request, userid):
    args = {}
    user = request.user
    if User.objects.get(id=userid).id != user.id:
        return render(request, '404error.html')
    userprofile = user.user_profile

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Get data from form
            data = form.cleaned_data
            userprofile.user_description = data['user_description']
            userprofile.school = data['school']
            userprofile.notifications_enabled = data['notifications_enabled']
            userprofile.save()
            return redirect('mainsite:userprofile', userid=userid)
    else:
        form = UserProfileForm(instance=userprofile)

    args['form'] = form
    return render(request, "userprofile/edituserprofile.html", args)

#invite users to a specific group
@login_required(login_url='/mainsite/login')
def groupinvite(request, groupid):
    this_group = Group.objects.get(id=groupid)
    group_creator = this_group.creator
    user_list = User.objects.filter(is_active=True)
    

    return render(request, 'groups/groupinvite.html', {'group': this_group,
                                                 'creator': group_creator,
                                                 'users': user_list})
#confirm invite
@login_required(login_url='/mainsite/login')
def confirmation(request, groupid, userid):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_to_invite = User.objects.get(id=userid)
    user_to_invite_profile = UserProfile.objects.get(user=user_to_invite)

    this_group = Group.objects.get(id=groupid)
    new_request = Requests(user_profile=user_to_invite_profile,
                                  group=this_group,
                                  user_that_invited=user_profile)
    new_request.save()

    return render(request, 'groups/groupinviteconfirmation.html', {'user_to_invite': user_to_invite,
                                                                   'group': this_group})


#view invites
@login_required(login_url='/mainsite/login')
def viewinvites(request, userid):
    user = request.user
    requests  = Requests.objects.all()
    if request.method == "POST":
        if "accept" in request.POST:
            this_request = request.POST['accept_request']
            this_request = Requests.objects.get(id=this_request)
            this_request.group.user_set.add(user)
            this_request.delete()
            #return render(request, 'groups/groupacceptconfirmation.html',
            # {'group': this_request.group})

    return render(request, 'groups/viewgroupinvites.html', {'user': user, 'requests': requests})

#view dm's
@login_required(login_url='/mainsite/login')
def viewdirectmessages(request):
    user = request.user
    conversation_list = user.viewable_conversations.all()
    return render(request, 'topics/direct_message_index.html', {'user': user,
     'conversations': conversation_list})

#view dm
@login_required(login_url='/mainsite/login')
def viewdirectmessage(request, convoid):
    user = request.user
    convo = Conversation.objects.get(id=convoid)
    messagelist = DirectMessage.objects.filter(conversation=convo)



    #post request
    if request.method == 'POST':
        filledForm = DirectMessageForm(request.POST)
        if filledForm.is_valid():
            data = filledForm.cleaned_data
            message = DirectMessage()
            message.creator = request.user
            message.conversation = Conversation.objects.get(id=convo.id)
            message.message_content = data['message_content']
            message.save()

    return render(request, 'topics/direct_message_view.html', {'user': user, 
     'conversation': convo, 'messages': messagelist, 'form': DirectMessageForm()})


#create new dm or view existing
@login_required(login_url='/mainsite/login')
def createmessage(request):
    user = request.user
    all_users = User.objects.all()

    all_existing_users = []
    for x in user.viewable_conversations.all():
        if user != x.recipient:
            all_existing_users.append(x.recipient)

    if request.method == "POST":
        if "new_message" in request.POST:
            #create new dm
            recipient = User.objects.get(id=request.POST['recipient'])
            convo = Conversation(convo_name='testing', recipient=recipient, recipient2 = user)
            convo.save()
            convo.user_set.add(user)
            convo.user_set.add(recipient)
            user.viewable_conversations.add(convo)
            messagelist = DirectMessage.objects.filter(conversation=convo)
            #go to new convo view
            return HttpResponseRedirect(reverse('mainsite:viewdirectmessages'))

    else:   
        #render the create new dm page 
        return render(request, 'topics/create_direct_message.html', {'user': user, 'all_users': all_users,
            'all_existing_users': all_existing_users})

