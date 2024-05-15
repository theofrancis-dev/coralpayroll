from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Business
from django.shortcuts import get_object_or_404, redirect, render

from .models import Business

from .forms import BusinessUpdateForm, BusinessCreateForm  # Assuming you have a form for updating businesses

class BusinessListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'business_list.html'  # Create a template named business_list.html
    context_object_name = 'businesses'
    paginate_by = 10  # Number of businesses per page

    def get_queryset(self):
        return Business.objects.all().order_by('entity_name')  # Order businesses by id (you can change this as needed)

class BusinessDetailView(LoginRequiredMixin,DetailView):
    model = Business
    template_name = 'business_detail.html'  # Create a template named business_detail.html
    context_object_name = 'business'


def business_update(LoginRequiredMixin,request, pk):
    business = get_object_or_404(Business, pk=pk)
    if request.method == 'POST':
        form = BusinessUpdateForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business-detail', pk=pk)  # Redirect to the business detail view after updating
    else:
        form = BusinessUpdateForm(instance=business)
    return render(request, 'business_update.html', {'form': form, 'business': business})

# def business_update(request, pk):
#    business = get_object_or_404(Business, pk=pk)
#    if request.method == 'POST':
#        form = BusinessForm(request.POST, instance=business)
#        if form.is_valid():
#            form.save()
#            return redirect('business-detail', pk=pk)  # Redirect to the business detail view after updating
#    else:
#        form = BusinessForm(instance=business)
#    return render(request, 'business_update.html', {'form': form, 'business': business})

def create_business(request):
    if request.method == 'POST':
        form = BusinessCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business-list')  # Redirect to the business list view after creating a new business
    else:
        form = BusinessCreateForm()
    return render(request, 'create_business.html', {'form': form})

