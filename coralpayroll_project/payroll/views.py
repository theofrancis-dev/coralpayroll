from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

from .models import Business
from .models import Address, Person, Employment

from .forms import AddressForm, PersonForm
from .forms import BusinessUpdateForm, BusinessCreateForm


#======================== BUSINESS SECTION =========================================
class BusinessListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'business_list.html'  # Ensure you have a template named business_list.html
    context_object_name = 'businesses'
    paginate_by = 10  # Number of businesses per page

    def get_queryset(self):
        # Retrieve all businesses and order them by entity_name
        return Business.objects.all().order_by('entity_name')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the selected business_id from the session
        business_id = self.request.session.get('selected_business_id')
        if business_id:
            # Retrieve the business instance or return None if not found
            context['selected_business'] = get_object_or_404(Business, pk=business_id)
        else:
            context['selected_business'] = None
        return context
    
@login_required
def business_detail(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    
    # Save the business ID in the session
    request.session['selected_business_id'] = business_id

    context = {
        'business': business,
        'staff': Person.objects.filter(business=business),
    }
    return render(request, 'business_detail.html', context)

@login_required
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

@login_required
def create_business(request):
    if request.method == 'POST':
        form = BusinessCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business-list')  # Redirect to the business list view after creating a new business
    else:
        form = BusinessCreateForm()
    return render(request, 'create_business.html', {'form': form})

#===================== CLIENT SECTION ==================================================
@login_required
def create_client(request):
    PersonFormSet = inlineformset_factory(Address, Person, form=PersonForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        formset = PersonFormSet(request.POST)
        
        if address_form.is_valid() and formset.is_valid():
            address = address_form.save()
            persons = formset.save(commit=False)
            for person in persons:
                person.address = address
                person.save()
            return redirect('list-clients')  # Adjust this to your desired redirect target
    else:
        address_form = AddressForm()
        formset = PersonFormSet()

    return render(request, 'create_client.html', {'address_form': address_form, 'formset': formset})

@login_required
def list_clients(request):
    business_id = request.session.get('selected_business_id')
    business = get_object_or_404(Business, pk=business_id) if business_id else None
    

    clients_list = Person.objects.all().order_by('first_name')  # Order by first name
    paginator = Paginator(clients_list, 10)  # Show 10 clients per page

    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)

    context = {
        'clients': clients,
        'business': business,
    }
    return render(request, 'list_clients.html', context)

# client(Person) detailed view
@login_required
def client_detail(request, pk):
    client = get_object_or_404(Person, pk=pk)
    return render(request, 'client_detail.html', {'client': client})

#client update and delete views
# Update view
@login_required
def update_client(request, pk):
    client = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-detail', pk=client.pk)
    else:
        form = PersonForm(instance=client)
    return render(request, 'update_client.html', {'form': form})

# Delete view
@login_required
def delete_client(request, pk):
    client = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('list-clients')
    return render(request, 'delete_client.html', {'client': client})


#=========================   STAFF SECTION ================================================
#staff list view
@login_required
def list_staff(request, business_id):
    #get current business
    business_id = request.session.get('selected_business_id')
    business = get_object_or_404(Business, pk=business_id) if business_id else None
    staff = Person.objects.filter(businesses__id=business_id)  # Filter by the many-to-many relationship

    context = {
        'staff': staff,
        'business' : business,
    }
    return render(request, 'list_staff.html', context)

@login_required
def add_staff(request, person_id):
    business_id = request.session.get('selected_business_id')
    business = get_object_or_404(Business, pk=business_id)
    client = get_object_or_404(Person, pk=person_id)
    
    # Add the client to the business (create the relationship)
    Employment.objects.create(person=client, business=business)
    
    return redirect('list_staff', business_id=business.id)
