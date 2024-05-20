from django import forms
from .models import Business
from .models import Address, Person, Earnings


# ModelForm to create a form that is automatically generated from the Business model.
# specify the Business model as the model attribute in the Meta class.

#update form
class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['entity_name', 'business_type', 'fei_ein_number', 'date_filed', 'state', 'status_active', 'principal_address', 'mailing_address', 'registered_agent', 'registered_agent_address']


#create form
class BusinessCreateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'  # Use all fields from the Business model


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address1', 'city', 'state', 'country', 'postal_code']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'middle_name', 'last_ssn','email1', 'phone1', 'phone2']

class EarningsForm(forms.ModelForm):
    employee_name = forms.CharField(label='Employee', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Earnings
        fields = ['employee_name', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }