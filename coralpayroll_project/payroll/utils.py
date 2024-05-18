from django.db.models import Sum
from .models import Earnings

#initial_date = '2024-01-01'
#final_date = '2024-03-31'
#employee = Person.objects.get(id=1)  # Assuming you have a specific employee object
#company = Business.objects.get(id=1)  # Assuming you have a specific company object
#total_earnings = calculate_total_earnings(initial_date, final_date, employee, company)


def calculate_total_earnings(initial_date, final_date, employee, company):
    total_earnings = Earnings.objects.filter(
        person=employee,
        business=company,
        date__range=(initial_date, final_date)
    ).aggregate(total_earnings=Sum('earnings'))['total_earnings']
    return total_earnings or 0