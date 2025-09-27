from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

def home_view(request):
    return render(request, 'frontend/index.html')

def about_view(request):
    return render(request, 'frontend/about.html')

def service_view(request):
    return render(request, 'frontend/service.html')

def contact_view(request):

    if request.method == 'POST':
        name = request.POST.get('contact-name')
        email = request.POST.get('contact-email')
        subject = request.POST.get('contact-subject')
        message = request.POST.get('contact-message')

        final_message = render_to_string('frontend/emails/customer_care_email.html', 
        {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject
        })

        # try:
        #     emailsend.email_send(
        #         'Email From '+name,
        #         final_message,
        #         'deliveries@mundoswift.com',
        #     )
        #     messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
        # except:
        #     messages.error(request, 'There was an error while trying to send your email, please try again')

        # finally:
        #     return redirect('frontend:contact_us')
    return render(request, 'frontend/contact.html')