from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractHour
from transactions.models import Transaction
from banks.models import Bank
from customers.models import Customer
from django.utils.timezone import now
from datetime import timedelta


def transactions_monthly(request):
    # Ensure there is at least demo data for charts if DB is empty
    qs = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    data = {
        'labels': [x['month'].strftime('%b %Y') if x['month'] else '' for x in qs],
        'values': [float(x['total'] or 0) for x in qs],
    }
    return JsonResponse(data)


def banks_top15(request):
    created_after = request.GET.get('year_after')
    min_clients = request.GET.get('min_clients')
    qs = Bank.objects.annotate(num_customers=Count('customers'))
    if created_after and created_after.isdigit():
        qs = qs.filter(created_at__year__gt=int(created_after))
    if min_clients and min_clients.isdigit():
        qs = qs.filter(num_customers__gte=int(min_clients))
    qs = qs.order_by('-num_customers')[:15].values('id','name','country','city','num_customers')
    return JsonResponse({'items': list(qs)})


def transactions_monthly_by_type(request):
    qs = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            dep=Sum('amount', filter=Q(type='DEPOSIT')),
            wit=Sum('amount', filter=Q(type='WITHDRAW')),
        )
        .order_by('month')
    )
    data = {
        'labels': [x['month'].strftime('%b %Y') if x['month'] else '' for x in qs],
        'deposit': [float(x['dep'] or 0) for x in qs],
        'withdraw': [float(x['wit'] or 0) for x in qs],
    }
    return JsonResponse(data)


def activity_by_hour(request):
    qs = (
        Transaction.objects
        .annotate(h=ExtractHour('created_at'))
        .values('h')
        .annotate(n=Count('id'))
    )
    counts = {x['h']: x['n'] for x in qs if x['h'] is not None}
    labels = list(range(0,24))
    values = [int(counts.get(h, 0)) for h in labels]
    return JsonResponse({'labels': labels, 'values': values})


def fraud_alerts(request):
    # Démo: retraits > 400 considérés suspects
    suspicious = (
        Transaction.objects
        .select_related('account','account__customer')
        .filter(type='WITHDRAW', amount__gt=400)
        .order_by('-created_at')[:50]
    )
    items = [
        {
            'date': t.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': t.type,
            'amount': float(t.amount),
            'account': t.account.number,
            'customer': str(t.account.customer),
            'reason': 'Retrait élevé (>400)'
        }
        for t in suspicious
    ]
    return JsonResponse({'items': items})


def client_balance_evolution(request):
    """Évolution du solde du client connecté"""
    from django.db.models import Sum
    from django.db.models.functions import TruncDate
    
    # Récupérer les comptes du client
    user_accounts = request.user.customer.accounts.all()
    
    # Calculer l'évolution du solde par jour
    balance_data = (
        Transaction.objects
        .filter(account__in=user_accounts)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(
            deposits=Sum('amount', filter=Q(type='DEPOSIT')),
            withdrawals=Sum('amount', filter=Q(type='WITHDRAW')),
            transfers_in=Sum('amount', filter=Q(type='TRANSFER', destination_account__in=user_accounts)),
            transfers_out=Sum('amount', filter=Q(type='TRANSFER', account__in=user_accounts))
        )
        .order_by('date')
    )
    
    # Calculer le solde cumulé
    current_balance = 0
    labels = []
    values = []
    
    for data in balance_data:
        net_change = (
            (data['deposits'] or 0) - 
            (data['withdrawals'] or 0) + 
            (data['transfers_in'] or 0) - 
            (data['transfers_out'] or 0)
        )
        current_balance += net_change
        labels.append(data['date'].strftime('%d/%m'))
        values.append(float(current_balance))
    
    return JsonResponse({
        'labels': labels,
        'values': values
    })


def client_transactions_by_type(request):
    """Répartition des transactions par type pour le client"""
    from django.db.models import Sum
    
    user_accounts = request.user.customer.accounts.all()
    
    data = (
        Transaction.objects
        .filter(account__in=user_accounts)
        .values('type')
        .annotate(total=Sum('amount'))
    )
    
    labels = []
    values = []
    colors = {
        'DEPOSIT': '#4CAF50',
        'WITHDRAW': '#F44336',
        'TRANSFER': '#2196F3'
    }
    
    for item in data:
        labels.append(item['type'])
        values.append(float(item['total'] or 0))
    
    return JsonResponse({
        'labels': labels,
        'values': values,
        'colors': [colors.get(label, '#9E9E9E') for label in labels]
    })


def client_recent_transactions(request):
    """Dernières transactions du client"""
    user_accounts = request.user.customer.accounts.all()
    
    transactions = (
        Transaction.objects
        .filter(account__in=user_accounts)
        .select_related('account')
        .order_by('-created_at')[:10]
    )
    
    items = [
        {
            'date': t.created_at.strftime('%d/%m/%Y %H:%M'),
            'type': t.type,
            'amount': float(t.amount),
            'account': t.account.number,
            'reference': t.reference,
            'description': t.description or ''
        }
        for t in transactions
    ]
    
    return JsonResponse({'items': items})


def client_savings_progress(request):
    """Progression vers l'objectif d'épargne (démo)"""
    user_accounts = request.user.customer.accounts.all()
    total_balance = sum(account.balance or 0 for account in user_accounts)
    
    # Objectif d'épargne fictif (10 000€)
    savings_goal = 10000
    progress = min(100, (total_balance / savings_goal) * 100)
    
    return JsonResponse({
        'current': float(total_balance),
        'goal': savings_goal,
        'progress': progress
    })


def account_types_distribution(request):
    """Répartition des comptes par type"""
    from accounts.models import Account
    
    data = (
        Account.objects
        .values('type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    labels = []
    values = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
    
    for i, item in enumerate(data):
        labels.append(item['type'])
        values.append(item['count'])
    
    return JsonResponse({
        'labels': labels,
        'values': values,
        'colors': colors[:len(labels)]
    })


def customer_growth(request):
    """Croissance du nombre de clients par mois"""
    from customers.models import Customer
    from django.db.models.functions import TruncMonth
    
    data = (
        Customer.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    labels = []
    values = []
    cumulative = 0
    
    for item in data:
        cumulative += item['count']
        labels.append(item['month'].strftime('%b %Y') if item['month'] else '')
        values.append(cumulative)
    
    return JsonResponse({
        'labels': labels,
        'values': values
    })