from django.shortcuts import render
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listings.choices import state_choices, bedroom_choices, price_choices


def index(request):
    listings = Listing.objects.all().order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    context = {
        'listing' : listing,
        'range' : range(6)
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(descrption__icontains=keywords)
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)     
    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    
    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    
    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings' : queryset_list,
        'values': request.GET,
        'state_choices' : state_choices,
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices
    }
    return render(request, 'listings/search.html', context)