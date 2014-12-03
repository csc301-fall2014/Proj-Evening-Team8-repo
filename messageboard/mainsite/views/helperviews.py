from mainsite.models import Message
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail

# Helper function for subscription notifications.
# No loginrequired header is needed here, its not an actual view function.
def notify_subscriber(topic, subscriber):
    profile = subscriber.user_profile

    if not profile.notifications_enabled:
        return

    # Add a topic to the user's notification queue.
    profile.notification_queue.add(topic)
    profile.save()

    # Check if its been long enough since the last email.
    if datetime.now() > (profile.last_notified.replace(tzinfo=None) + timedelta(seconds=profile.notification_delay)):

        # Start composing the email.
        email_subject = 'Subscription Update!'
        email_body = "Dear %s,\n\nA new message has been posted to a topic you're subscribed to!\n\n" \
                     % subscriber.username

        # Dump all the topic links into the email.
        for t in profile.notification_queue.all():
            email_body += "http://127.0.0.1:8000/mainsite/messageboard/%d\n" % t.id
        email_body += "\n\nYours,\nTeam8s"
        send_mail(email_subject, email_body, 'donotreply@huddle.ca', [subscriber.email], fail_silently=False)

        # Clear the notification queue, set the last_notified time.
        profile.notification_queue.clear()
        profile.last_notified = timezone.now()
        profile.save()

# Not a view, helper function for notices (a richer and more customizable HttpResponse)
def response(request, title, message, link, button):
    return render(request, 'response.html', {
        'title': title,
        'message': message,
        'link': link,
        'button': button})

def post_message(content, topic, creator):
    message = Message()
    message.creator = creator
    message.topic = topic
    content = content.strip()
    if(content != ""):
        message.message_content = content
        message.save()
        # Hand out subscription notifications (currently synchronous)
        subscribers = topic.subscriptions.all()
        for subscriber in subscribers:
            if subscriber != message.creator:
                notify_subscriber(topic, subscriber)



