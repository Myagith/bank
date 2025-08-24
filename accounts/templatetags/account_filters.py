from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_balance(accounts):
    """
    Calcule la somme des soldes de tous les comptes
    Usage: {{ accounts|sum_balance }}
    """
    if not accounts:
        return 0
    return accounts.aggregate(total=Sum('balance'))['total'] or 0