from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_balance(accounts):
    """
    Calcule la somme des soldes de tous les comptes
    Usage: {{ customer.accounts.all|sum_balance }}
    """
    if not accounts:
        return 0
    return accounts.aggregate(total=Sum('balance'))['total'] or 0

@register.filter
def sum_accounts(customers):
    """
    Calcule le nombre total de comptes pour une liste de clients
    Usage: {{ bank.customers.all|sum_accounts }}
    """
    if not customers:
        return 0
    total = 0
    for customer in customers:
        total += customer.accounts.count()
    return total