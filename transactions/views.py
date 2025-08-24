from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Transaction
from .forms import TransactionForm
from .services import post_transaction
from users.services import get_user_accounts


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/create.html'
    success_url = reverse_lazy('transactions:history')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            post_transaction(self.object)
            messages.success(self.request, 'Transaction posted.')
        except Exception as e:
            messages.error(self.request, str(e))
        return response


class TransactionHistoryView(LoginRequiredMixin, FilterView):
    model = Transaction
    template_name = 'transactions/history.html'
    context_object_name = 'transactions'
    filterset_fields = {
        'created_at': ['date__gte', 'date__lte'],
        'amount': ['gte', 'lte'],
        'type': ['exact'],
        'account__customer__bank': ['exact'],
    }
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        # Si c'est un client, rediriger vers la vue client
        if request.user.is_authenticated and request.user.role != 'ADMIN':
            return redirect('transactions:client_history')
        return super().dispatch(request, *args, **kwargs)


class ClientTransactionHistoryView(LoginRequiredMixin, FilterView):
    """Vue pour l'historique des transactions du client connecté"""
    model = Transaction
    template_name = 'transactions/client_history.html'
    context_object_name = 'transactions'
    filterset_fields = {
        'created_at': ['date__gte', 'date__lte'],
        'amount': ['gte', 'lte'],
        'type': ['exact'],
    }
    paginate_by = 20
    
    def get_queryset(self):
        # Filtrer uniquement les transactions du client connecté
        user_accounts = get_user_accounts(self.request.user)
        return Transaction.objects.filter(account__in=user_accounts)
