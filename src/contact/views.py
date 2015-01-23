from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm


def contact(request):
    title = 'Contact us'
    form = ContactForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        message = form.cleaned_data['message']
        name = form.cleaned_data['name']
        sbj = 'Message from the Blog.com'
        msg = '%s %s' %(message, name)
        frm = form.cleaned_data['email']
        to_us = [settings.EMAIL_HOST_USER]
        send_mail(sbj, msg, frm, to_us, fail_silently=True)

        title = 'Thank you'
        confirm_message = """
        Thank you for your message. We have received it and we are reviewing it.
        """
        form = None

    context = {'form': form,
               'title': title,
               'confirm_message': confirm_message}
    return render(request, 'blog/contact.html', context)
