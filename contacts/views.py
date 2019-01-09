from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        contact = Contact(listing=listing, listing_id=listing_id, 
                    name=name,email=email, phone=phone, 
                    message=message, user_id=user_id)
        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquare for this listing')
                return redirect('/listings/' + listing_id)
        contact.save()
        messages.success(request, 'Your request has been submited, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)
    else:
        return redirect('/listings/' + listing_id)