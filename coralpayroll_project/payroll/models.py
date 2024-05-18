from django.db import models
from django.utils.translation import gettext_lazy as _

#from encrypted_fields import EncryptedCharField

# Define choices for states
STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
        ]


class Address(models.Model):
    address1 = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, blank=True, null=True)
    address3 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=100, default='Hialeah')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='FL')
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20, default='33012')
    lastupdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address1}, {self.city}, {self.state}, {self.country}, {self.postal_code}"

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_ssn = models.CharField(max_length=12, blank=True, null=True)
    
    #ssn = EncryptedCharField(max_length=100)  # Encrypted SSN field
    email1 = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    phone3 = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    lastupdate = models.DateTimeField(auto_now_add=True)
    
    businesses = models.ManyToManyField('Business', through='Employment')
    # Many-to-many relationship with Business

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

BUSINESS_TYPE = [
    ('sole_proprietorship', 'Sole Proprietorship'),
    ('partnership', 'Partnership'),
    ('llc', 'LLC'),
    ('c_corp', 'C Corp'),
    ('s_corp', 'S Corp'),
    ('benefit_corporation', 'Benefit Corporation'),
    ('close_corporation', 'Close Corporation'),
    ('nonprofit_corporation', 'Nonprofit Corporation'),
    ('fl_profit_corp','Florida Profit Corp'),
]

class Business(models.Model):
    entity_name = models.CharField(max_length=250)
    business_type = models.CharField(max_length=100, choices=BUSINESS_TYPE, default='fl_profit_corp')  
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    fei_ein_number = models.CharField(max_length=20)  
    date_filed = models.DateField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='FL')  
    status_active = models.BooleanField(default=True)
    principal_address = models.ForeignKey(Address, related_name='principal_businesses', on_delete=models.CASCADE)
    mailing_address = models.ForeignKey(Address, related_name='mailing_businesses', on_delete=models.CASCADE)
    registered_agent = models.ForeignKey(Person, related_name='registered_agent_for', on_delete=models.CASCADE)
    registered_agent_address = models.ForeignKey(Address, related_name='registered_agent_addresses', on_delete=models.CASCADE)

    def get_business_type_display(self):
        for choice in BUSINESS_TYPE:
            if choice[0] == self.business_type:
                return choice[1]
        return self.business_type

    def __str__(self):
        return self.entity_name


class Employment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

class Earnings(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateField()
    earnings = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("earnings (USD)"))

    def __str__(self):
        return f"Earnings for {self.person} at {self.business} on {self.date}"



