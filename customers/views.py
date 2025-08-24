from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.db.models import Sum, Count

from .models import Customer
from .forms import CustomerForm
from .filters import CustomerFilter
from banks.models import Bank


class CustomerListView(FilterView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'
    filterset_class = CustomerFilter
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par nombre de comptes
        account_count = self.request.GET.get('account_count')
        if account_count:
            if account_count == '0':
                queryset = queryset.filter(accounts__isnull=True)
            elif account_count == '1':
                queryset = queryset.annotate(
                    account_count=Count('accounts')
                ).filter(account_count=1)
            elif account_count == '2-5':
                queryset = queryset.annotate(
                    account_count=Count('accounts')
                ).filter(account_count__gte=2, account_count__lte=5)
            elif account_count == '6-10':
                queryset = queryset.annotate(
                    account_count=Count('accounts')
                ).filter(account_count__gte=6, account_count__lte=10)
            elif account_count == '10+':
                queryset = queryset.annotate(
                    account_count=Count('accounts')
                ).filter(account_count__gt=10)
        
        return queryset.select_related('bank').prefetch_related('accounts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = self.get_queryset()
        
        # Statistiques
        context.update({
            'unique_banks_count': customers.values('bank').distinct().count(),
            'total_accounts_count': sum(customer.accounts.count() for customer in customers),
            'total_balance': sum(
                sum(account.balance or 0 for account in customer.accounts.all())
                for customer in customers
            ),
        })
        
        # Données pour les filtres
        context.update({
            'banks': Bank.objects.all().order_by('name'),
        })
        
        return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'
    success_url = reverse_lazy('customers:list')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'
    success_url = reverse_lazy('customers:list')


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Calculer le solde total
        total_balance = sum(account.balance or 0 for account in customer.accounts.all())
        context['total_balance'] = total_balance
        
        return context


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')
    template_name = 'customers/confirm_delete.html'
