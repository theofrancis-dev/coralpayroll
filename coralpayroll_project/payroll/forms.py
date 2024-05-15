from django import forms
from .models import Business


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
