from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Account
from .forms import AccountForm


class AccountListView(FilterView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'
    filterset_fields = ['customer__bank', 'status', 'type']
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        # Si c'est un client, rediriger vers la vue client
        if request.user.is_authenticated and request.user.role != 'ADMIN':
            return redirect('accounts:client_list')
        return super().dispatch(request, *args, **kwargs)


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
