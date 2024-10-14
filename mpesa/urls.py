from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [
    path('b2b/transaction/', views.CreateBToBTransaction.as_view(), name="create_b_2_b_transaction"),
    path('b2c/transaction/', views.CreateBToCTransaction.as_view(), name="create_b_2_c_transaction"),
    path('register/c2b/url/', views.RegisterCToBUrl.as_view(), name="register_c_2_b_url"),
    path('accountbalance/transaction/', views.CheckAccountBalance.as_view(), name="check_account_balance"),
    path('check/transaction/status/', views.CheckTransactionStatus.as_view(), name="check_transaction_status"),
    path('reversal/transaction/', views.TransactionReversal.as_view(), name="transaction_reversal"),
    path('lipanampesa/online/', views.InitiateLipaNaMpesaTransaction.as_view(), name="initiate_lipa_na_mpesa_online_transaction"),
    path('lipanampesa/online/transaction/status/', views.QueryLipaNaMpesaOnlineTransactionStatus.as_view(), name="query_lipa_na_mpesa_online_transaction_status"),
    path('create/occassion/', views.CreateOccassion.as_view(), name="create_occasion"),
    path('create/mpesa/command/id/', views.CreateMpesaCommandId.as_view(), name="create_mpesa_command_id"),
    path('create/company/shortcodeornumber/', views.CreateCompanyShortCodeOrNumber.as_view(), name="create_company_short_code_or_number"),
    path('create/initiator/name/', views.CreateInitiatorName.as_view(), name="create_initiator_name"),
    path('create/transaction/type/', views.CreateTransactionType.as_view(), name="create_transaction_type"),
    path('create/initiator/type/', views.CreateInitiatorType.as_view(), name="create_initiator_type"),

    path('occassion/detail/<int:pk>/', views.OccasionDetailAPIView.as_view(), name='occasion-detail'),
    path('mpesa/commandid/detail/<int:pk>/', views.MpesaCommandIdDetailAPIView.as_view(), name='mpesa-commandid-detail'),
    path('mpesa/shortcodeornumber/detail/<int:pk>/', views.MpesaShortCodeOrNumberDetailAPIView.as_view(), name='mpesa-shortcodeornumber-detail'),
    path('initiator/name/detail/<int:pk>/', views.InitiatorNameDetailAPIView.as_view(), name='initiatorname-detail'),
    path('transaction/type/detail/<int:pk>/', views.TransactionTypeDetailAPIView.as_view(), name='transactiontype-detail'),
    path('identifier/type/detail/<int:pk>/', views.IdentifierTypeDetailAPIView.as_view(), name='identifiertype-detail'),

    path('occassion/list/', views.OccasionListView.as_view(), name='occassion-list'),
    path('mpesacommandid/list/', views.MpesaCommandIdListView.as_view(), name='mpesa-commandid-list'),
    path('shortcodeornumber/list/', views.MpesaShortCodeOrNumberListView.as_view(), name='shortcodeornumber-list'),
    path('initiatorname/list/', views.InitiatorNameListView.as_view(), name='initiatorname-list'),
    path('transactiontype/list/', views.TransactionTypeListView.as_view(), name='transactiontype-list'),
    path('identifiertype/list/', views.IdentifierTypeListView.as_view(), name='identifiertype-list'),
    path('transaction/list/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactionresponse/list/', views.TransactionResponseListView.as_view(), name='transactionresponse-list'),
    path('registration/list/', views.RegistrationListView.as_view(), name='registration-list'),
]

