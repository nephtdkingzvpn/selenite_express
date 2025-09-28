from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from . import emailsend
from account.models import Shipment, LiveUpdate
from .forms import ContactForm
def home_view(request):
    return render(request, 'frontend/index.html')

def about_view(request):
    return render(request, 'frontend/about.html')

def service_view(request):
    return render(request, 'frontend/service.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            print('goinggone')
            print(message)
            print(subject)

            final_message = render_to_string('frontend/emails/customer_care_email.html', 
            {
                'name': fullname,
                'email': email,
                'message': message,
                'subject': subject
            })

            try:
                emailsend.email_send(
                    'Email From '+fullname,
                    final_message,
                    'deliveries@selenitexpress.com',
                )
                messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
            except:
                messages.error(request, 'There was an error while trying to send your email, please try again')

            finally:
                return redirect('frontend:contact')
    else:
        form = ContactForm()
    return render(request, 'frontend/contact.html', {'form':form})


# def contact_view(request):

#     if request.method == 'POST':
#         name = request.POST.get('fullname')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')

#         print(message)

#         final_message = render_to_string('frontend/emails/customer_care_email.html', 
#         {
#             'name': name,
#             'email': email,
#             'message': message,
#             'subject': subject
#         })

#         try:
#             emailsend.email_send(
#                 'Email From '+name,
#                 final_message,
#                 'deliveries@selenitexpress.com',
#             )
#             messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
#         except:
#             messages.error(request, 'There was an error while trying to send your email, please try again')

#         finally:
#             return redirect('frontend:contact')
#     return render(request, 'frontend/contact.html')



def tracking_view(request):
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        shipments = Shipment.objects.filter(tracking_number=tracking_code)

        if shipments.exists():
            shipment_single = shipments.first()
            live_update_qs = LiveUpdate.objects.filter(shipment=shipment_single).order_by('created_on')

            # Serialize live updates to a list of dicts for the map
            live_updates = []
            for update in live_update_qs:
                if update.latitude and update.longitude:
                    live_updates.append({
                        'latitude': update.latitude,
                        'longitude': update.longitude,
                        'status': update.status,
                        'remark': update.remark,
                        'created_on': update.created_on.isoformat(),
                        'country': update.country.country_name if update.country else None,
                    })

            live_update_count = live_update_qs.count()
            latest_update = live_update_qs.last()

            return render(request, 'frontend/tracking.html', {
                'shipments': shipments,
                'shipment_single': shipment_single,
                'update_count': live_update_count,
                'latest_update': latest_update,
                'live_update': live_update_qs,
                'live_updates_json': live_updates,  
            })
        else:
            messages.error(request, "Invalid tracking code. Please check the code and try again.")
            return redirect('frontend:tracking')

    return render(request, 'frontend/tracking.html')