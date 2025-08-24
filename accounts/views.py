from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Sum, Count, Q

from .models import Account
from .forms import AccountForm
from banks.models import Bank


class AccountListView(FilterView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'
    filterset_fields = {
        'customer__bank__name': ['exact'],
        'status': ['exact'],
        'type': ['exact'],
        'customer__bank__country': ['exact'],
        'customer__bank__city': ['exact'],
    }
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        # Si c'est un client, rediriger vers la vue client
        if request.user.is_authenticated and request.user.role != 'ADMIN':
            return redirect('accounts:client_list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par nombre de clients (approche simplifiée)
        customer_count = self.request.GET.get('customer_count')
        if customer_count:
            # Compter les comptes par client et filtrer
            if customer_count == '1':
                # Clients avec exactement 1 compte
                customers_with_one = Account.objects.values('customer').annotate(
                    account_count=Count('id')
                ).filter(account_count=1).values_list('customer', flat=True)
                queryset = queryset.filter(customer__in=customers_with_one)
            elif customer_count == '2-5':
                # Clients avec 2-5 comptes
                customers_with_multiple = Account.objects.values('customer').annotate(
                    account_count=Count('id')
                ).filter(account_count__gte=2, account_count__lte=5).values_list('customer', flat=True)
                queryset = queryset.filter(customer__in=customers_with_multiple)
            elif customer_count == '6-10':
                # Clients avec 6-10 comptes
                customers_with_many = Account.objects.values('customer').annotate(
                    account_count=Count('id')
                ).filter(account_count__gte=6, account_count__lte=10).values_list('customer', flat=True)
                queryset = queryset.filter(customer__in=customers_with_many)
            elif customer_count == '10+':
                # Clients avec plus de 10 comptes
                customers_with_lots = Account.objects.values('customer').annotate(
                    account_count=Count('id')
                ).filter(account_count__gt=10).values_list('customer', flat=True)
                queryset = queryset.filter(customer__in=customers_with_lots)
        
        return queryset.select_related('customer', 'customer__bank')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = self.get_queryset()
        
        # Statistiques
        context.update({
            'open_accounts_count': accounts.filter(status='OPEN').count(),
            'total_balance': accounts.aggregate(total=Sum('balance'))['total'] or 0,
            'unique_customers_count': accounts.values('customer').distinct().count(),
        })
        
        # Données pour les filtres
        context.update({
            'banks': Bank.objects.all().order_by('name'),
            'countries': Bank.objects.values_list('country', flat=True).distinct().order_by('country'),
            'cities': Bank.objects.values_list('city', flat=True).distinct().order_by('city'),
        })
        
        return context


class ClientAccountListView(LoginRequiredMixin, FilterView):
    """Vue pour les comptes du client connecté"""
    model = Account
    template_name = 'accounts/client_list.html'
    context_object_name = 'accounts'
    paginate_by = 20
    
    def get_queryset(self):
        # Filtrer uniquement les comptes du client connecté
        return Account.objects.filter(customer__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = self.get_queryset()
        
        # Calculer les statistiques
        total_balance = sum(account.balance or 0 for account in accounts)
        open_accounts = accounts.filter(status='OPEN').count()
        
        context.update({
            'total_balance': f"{total_balance:.2f}",
            'open_accounts': open_accounts,
        })
        
        return context


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')


class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/detail.html'


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('accounts:list')
    template_name = 'accounts/confirm_delete.html'
