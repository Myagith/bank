from django.urls import path
from . import views, api
from . import exports

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.dashboard_admin, name='admin'),
    path('client/', views.dashboard_client, name='client'),
    path('users/', views.manage_users, name='manage_users'),
    path('api/transactions/monthly/', api.transactions_monthly, name='transactions_monthly'),
    path('api/transactions/monthly-by-type/', api.transactions_monthly_by_type, name='transactions_monthly_by_type'),
    path('api/banks/top15/', api.banks_top15, name='banks_top15'),
    path('api/activity-by-hour/', api.activity_by_hour, name='activity_by_hour'),
    path('api/fraud-alerts/', api.fraud_alerts, name='fraud_alerts'),
    # APIs pour le dashboard client
    path('api/client/balance-evolution/', api.client_balance_evolution, name='client_balance_evolution'),
    path('api/client/transactions-by-type/', api.client_transactions_by_type, name='client_transactions_by_type'),
    path('api/client/recent-transactions/', api.client_recent_transactions, name='client_recent_transactions'),
    path('api/client/savings-progress/', api.client_savings_progress, name='client_savings_progress'),
    # APIs supplémentaires pour le dashboard admin
    path('api/account-types-distribution/', api.account_types_distribution, name='account_types_distribution'),
    path('api/customer-growth/', api.customer_growth, name='customer_growth'),
    path('export/top-banks.csv', exports.top_banks_csv, name='export_top_banks_csv'),
    path('export/top-banks.xlsx', exports.top_banks_xlsx, name='export_top_banks_xlsx'),
]