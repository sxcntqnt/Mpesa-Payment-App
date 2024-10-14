from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import  *


urlpatterns = [
    path('b2b/transaction/', CreateBToBTransaction.as_view(), name="create_b_2_b_transaction"),
    path('b2c/transaction/', CreateBToCTransaction.as_view(), name="create_b_2_c_transaction"),
    path('register/c2b/url/', RegisterCToBUrl.as_view(), name="register_c_2_b_url"),
    path('accountbalance/transaction/', CheckAccountBalance.as_view(), name="check_account_balance"),
    path('check/transaction/status/', CheckTransactionStatus.as_view(), name="check_transaction_status"),
    path('reversal/transaction/', TransactionReversal.as_view(), name="transaction_reversal"),
    path('lipanampesa/online/', InitiateLipaNaMpesaTransaction.as_view(), name="initiate_lipa_na_mpesa_online_transaction"),
    path('lipanampesa/online/transaction/status/', QueryLipaNaMpesaOnlineTransactionStatus.as_view(), name="query_lipa_na_mpesa_online_transaction_status"),
    path('create/occassion/', CreateOccassion.as_view(), name="create_occasion"),
    path('create/mpesa/command/id/', CreateMpesaCommandId.as_view(), name="create_mpesa_command_id"),
    path('create/company/shortcodeornumber/', CreateCompanyShortCodeOrNumber.as_view(), name="create_company_short_code_or_number"),
    path('create/initiator/name/', CreateInitiatorName.as_view(), name="create_initiator_name"),
    path('create/transaction/type/', CreateTransactionType.as_view(), name="create_transaction_type"),
    path('create/initiator/type/', CreateInitiatorType.as_view(), name="create_initiator_type"),

    path('occassion/detail/<int:pk>/', OccasionDetailAPIView.as_view(), name='occasion-detail'),
    path('mpesa/commandid/detail/<int:pk>/', MpesaCommandIdDetailAPIView.as_view(), name='mpesa-commandid-detail'),
    path('mpesa/shortcodeornumber/detail/<int:pk>/', MpesaShortCodeOrNumberDetailAPIView.as_view(), name='mpesa-shortcodeornumber-detail'),
    path('initiator/name/detail/<int:pk>/', InitiatorNameDetailAPIView.as_view(), name='initiatorname-detail'),
    path('transaction/type/detail/<int:pk>/', TransactionTypeDetailAPIView.as_view(), name='transactiontype-detail'),
    path('identifier/type/detail/<int:pk>/', IdentifierTypeDetailAPIView.as_view(), name='identifiertype-detail'),

    path('occassion/list/', OccasionListView.as_view(), name='occassion-list'),
    path('mpesacommandid/list/', MpesaCommandIdListView.as_view(), name='mpesa-commandid-list'),
    path('shortcodeornumber/list/', MpesaShortCodeOrNumberListView.as_view(), name='shortcodeornumber-list'),
    path('initiatorname/list/', InitiatorNameListView.as_view(), name='initiatorname-list'),
    path('transactiontype/list/', TransactionTypeListView.as_view(), name='transactiontype-list'),
    path('identifiertype/list/', IdentifierTypeListView.as_view(), name='identifiertype-list'),
    path('transaction/list/', TransactionListView.as_view(), name='transaction-list'),
    path('transactionresponse/list/', TransactionResponseListView.as_view(), name='transactionresponse-list'),
    path('registration/list/', RegistrationListView.as_view(), name='registration-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
