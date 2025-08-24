from django import template
from django.db.models import Sum
from django.core.exceptions import FieldError

register = template.Library()

@register.filter
def sum_balance(items):
    """
    Calcule la somme des soldes.
    - Si 'items' est un queryset de Account: SUM(balance)
    - Si 'items' est un queryset de Customer: SUM(accounts__balance)
    - Si 'items' est une liste/iterable: calcule via itération
    """
    if not items:
        return 0

    # QuerySet-like: utilise aggregate
    if hasattr(items, 'aggregate'):
        try:
            return items.aggregate(total=Sum('balance'))['total'] or 0
        except FieldError:
            return items.aggregate(total=Sum('accounts__balance'))['total'] or 0

    # Iterable/list fallback
    total = 0
    iterator = iter(items)
    try:
        first = next(iterator)
    except StopIteration:
        return 0

    # Recompense le premier élément puis itère
    def iter_with_first(first_item, rest_iter):
        yield first_item
        for x in rest_iter:
            yield x

    for obj in iter_with_first(first, iterator):
        if hasattr(obj, 'balance'):
            total += (obj.balance or 0)
        elif hasattr(obj, 'accounts'):
            # Suppose Customer-like avec related_name 'accounts'
            total += (obj.accounts.aggregate(total=Sum('balance'))['total'] or 0)
    return total

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