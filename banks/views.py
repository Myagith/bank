from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.db.models import Count, Sum

from .models import Bank
from .forms import BankForm
from .filters import BankFilter


class BankListView(FilterView):
    model = Bank
    template_name = 'banks/list.html'
    context_object_name = 'banks'
    filterset_class = BankFilter
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par nombre de clients
        customer_count = self.request.GET.get('customer_count')
        if customer_count:
            if customer_count == '0':
                queryset = queryset.filter(customers__isnull=True)
            elif customer_count == '1-10':
                queryset = queryset.annotate(
                    customer_count=Count('customers')
                ).filter(customer_count__gte=1, customer_count__lte=10)
            elif customer_count == '11-50':
                queryset = queryset.annotate(
                    customer_count=Count('customers')
                ).filter(customer_count__gte=11, customer_count__lte=50)
            elif customer_count == '51-100':
                queryset = queryset.annotate(
                    customer_count=Count('customers')
                ).filter(customer_count__gte=51, customer_count__lte=100)
            elif customer_count == '100+':
                queryset = queryset.annotate(
                    customer_count=Count('customers')
                ).filter(customer_count__gt=100)
        
        return queryset.prefetch_related('customers', 'customers__accounts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banks = self.get_queryset()
        
        # Statistiques
        context.update({
            'total_banks': banks.count(),
            'total_customers': sum(bank.customers.count() for bank in banks),
            'total_accounts': sum(
                sum(customer.accounts.count() for customer in bank.customers.all())
                for bank in banks
            ),
            'total_balance': sum(
                sum(
                    sum(account.balance or 0 for account in customer.accounts.all())
                    for customer in bank.customers.all()
                )
                for bank in banks
            ),
        })
        
        return context


class BankCreateView(CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'banks/form.html'
    success_url = reverse_lazy('banks:list')


class BankUpdateView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'banks/form.html'
    success_url = reverse_lazy('banks:list')


class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'
    context_object_name = 'bank'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank = self.get_object()
        
        # Statistiques de la banque
        customers = bank.customers.all()
        total_accounts = sum(customer.accounts.count() for customer in customers)
        total_balance = sum(
            sum(account.balance or 0 for account in customer.accounts.all())
            for customer in customers
        )
        
        context.update({
            'total_customers': customers.count(),
            'total_accounts': total_accounts,
            'total_balance': total_balance,
            'customers': customers.prefetch_related('accounts'),
        })
        
        return context


class BankDeleteView(DeleteView):
    model = Bank
    success_url = reverse_lazy('banks:list')
    template_name = 'banks/confirm_delete.html'


class BankTop15View(ListView):
    model = Bank
    template_name = 'banks/top15.html'
    context_object_name = 'banks'

    def get_queryset(self):
        return Bank.objects.annotate(num_customers=Count('customers')).order_by('-num_customers')[:15]
