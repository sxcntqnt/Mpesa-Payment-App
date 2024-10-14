# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from rest_framework import status, generics
from rest_framework.decorators import *
from rest_framework.renderers import *
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from django.http import Http404
from . import utils
from . import tasks

class CreateBToCTransaction(APIView):

    def post(self, request, format=None):
        # company to customer transaction based phone no and shortcode
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                occasion = Occasion.objects.get(id=request.data['occasion'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                code_a = CompanyCodeOrNumber.objects.get(
                    id=party_a).name
                code_b = CompanyCodeOrNumber.objects.get(
                    id=party_b).name
                name = InitiatorName.objects.get(
                    id=initiator_name).name
                com_id = MpesaCommandId.objects.get(
                    id=command_id).name
                occ = Occasion.objects.get(
                    id=occasion).name

            except:
                raise Http404
            request = {
                "InitiatorName": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "Amount": amount,
                "PartyA": code_a,
                "PartyB": code_b,
                "Remarks": remarks,
                "QueueTimeOutURL": "/",
                "ResultURL": "/",
                "Occasion": occ
            }
            send_create_b2c_transaction.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateBToBTransaction(APIView):

    def post(self, request, format=None):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                occasion = Occasion.objects.get(id=request.data['occasion'])
                identifier_type_a = IdentifierType.objects.get(
                    id='identifier_type')
                identifier_type_b = IdentifierType.objects.get(
                    id='identifier_type')
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                com_id = command_id.name
                party_a = party_a.name
                party_b = party_b.name
                name = initiator_name.name
                id_type_a = identifier_type_a.name
                id_type_b = identifier_type_b.name
            except:
                raise Http404
            request = {
                "Initiator": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "SenderIdentifierType": id_type_a,
                "RecieverIdentifierType": id_type_b,
                "Amount": amount,
                "PartyA": party_a,
                "PartyB": party_b,
                "AccountReference": com_id,
                "Remarks": remarks,
                "QueueTimeOutURL": "/",
                "ResultURL": "/"
            }
            send_create_b2b_transaction.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class RegisterCToBUrl(APIView):

    def post(self, request, format=None):
        # The C2B Register URL API registers the 3rd party’s confirmation and validation URLs to M-Pesa ;
        # which then maps these URLs to the 3rd party shortcode.
        # Whenever M-Pesa receives a transaction on the shortcode,
        # M-Pesa triggers a validation request against the validation URL.
        # The 3rd party system responds to M-Pesa with a validation response (either a success or an error code).
        # The response expected is the success code the 3rd party
        access_token = authenticate()
        try:
            try:
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                confirmation_url = request.data['confirmation_url']
                validation_url = request.data['confirmation_url']
                Registration.objects.create(
                    company=party_b,
                    initiator_name=initiator_name,
                    confirmation_url=confirmation_url,
                    validation_url=validation_url)
            except:
                raise Http404
            party_b = party_b.name

            request = {"ShortCode": party_b,
                       "ResponseType": "json",
                       "ConfirmationURL": confirmation_url,
                       #"http://ip_address:port/confirmation",
                       "ValidationURL": validation_url,
                       # "http://ip_address:port/validation_url"
                       }
            send_register_c_to_b_url.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CheckAccountBalance(APIView):

    def post(self, request, format=None):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                remarks = request.data['remarks'],
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                transaction = Transaction.objects.create(
                    command_id=command_id,
                    Party_a=Party_a,
                    initiator_name=initiator_name)
                initiator = encryptInitiatorPassword()
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                party_a = party_a.name
                name = initiator_name.name
            except:
                raise Http404

            request = {"Initiator": name,
                       "SecurityCredential": initiator,
                       "CommandID": com_id,
                       "PartyA": party_a,
                       "IdentifierType": "4",
                       "Remarks": remarks,
                       "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                       "ResultURL": "https://ip_address:port/result_url"
                       }
            send_check_account_balance.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CheckTransactionStatus(APIView):

    def post(self, request, format=None):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['create_company_short_code_or_number'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                com_id = command_id.name
                party_a = party_a.name
                party_b = party_b.name
                name = initiator_name.name
            except:
                raise Http404

            request = {
                "Initiator": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "TransactionID": party_b,
                "PartyA": party_a,
                "IdentifierType": "1",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": remarks
            }

            send_check_transaction_status.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class TransactionReversal(APIView):

    def post(self, request, format=None):
        # company to customer transaction based phone no and shortcode
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name)
                initiator = encryptInitiatorPassword()
                code_a = party_a.name
                code_b = party_b.name
                name = initiator_name.name
                com_id = command_id.name

            except:
                raise Http404

            request = {"Initiator": name,
                       "SecurityCredential": initiator,
                       "CommandID": com_id,
                       "TransactionID": code_b,
                       "Amount": amount,
                       "PartyA": code_a,
                       "RecieverIdentifierType": "4",
                       "ResultURL": "https://ip_address:port/result_url",
                       "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                       "Remarks": remarks,
                       "Occasion": " "
                       }

            send_transaction_reversal.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class InitiateLipaNaMpesaTransaction(APIView):

    def post(self, request, format=None):
        # Lipa na M-Pesa Online Payment API is
        # used to initiate a M-Pesa transaction
        # on behalf of a customer using STK Push
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    transaction_description=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name)
                code_a = party_a.name
                code_b = party_b.name
                com_id = command_id.name
                t_type = transaction_type.name
                time = transaction.created

            except:
                raise Http404
            password = Password(code_b=code_b, time=time)

            request = {
                "BusinessShortCode": code_b,
                "Password": password,
                "Timestamp": time,
                "TransactionType": t_type,
                "Amount": amount,
                "PartyA": code_a,
                "PartyB": code_b,
                "PhoneNumber": code_a,
                "CallBackURL": "https://ip_address:port/callback",
                "AccountReference": com_id,
                "TransactionDesc": remarks
            }

            send_initiate_lipa_na_mpesa_online.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class QueryLipaNaMpesaOnlineTransactionStatus(APIView):

    def post(self, request, format=None):
        # Lipa na M-Pesa Online Payment API is
        # used to initiate a M-Pesa transaction
        # on behalf of a customer using STK Push
        access_token = authenticate()
        try:
            try:
                transaction_response = TransactionResponse.objects.get(
                    id=request.data['transaction_response'])
                transaction = Transaction.objects.get(
                    id=transaction_response.transaction_id)
                code_b = CompanyCodeOrNumber.objects.get(
                    id=transaction.party_b).name
                time = transaction.created
                checkout_request_id = transaction_response.checkout_request_id
            except:
                raise Http404
            password = Password(code_b=code_b, time=time)

            request = {
                "BusinessShortCode": code_b,
                "Password": password,
                "Timestamp": time,
                "CheckoutRequestID": checkout_request_id,
            }
            send_query_lipa_na_mpesa_online_status.delay(request,access_token)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateOccassion(APIView):

    def post(self, request, format=None):
        Occassion.objects.create(name=request.data['occasion'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateMpesaCommandId(APIView):

    def post(self, request, format=None):
        MpesaCommandId.objects.create(
            name=request.data['command_id'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateCompanyShortCodeOrNumber(APIView):

    def post(self, request, format=None):
        CompanyShortCodeOrNumber.objects.create(
            name=request.data['short_code'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateInitiatorName(APIView):

    def post(self, request, format=None):
        InitiatorName.objects.create(
            name=request.data['initiator_name'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateTransactionType(APIView):

    def post(self, request, format=None):
        TransactionType.objects.create(
            name=request.data['transaction_type'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateInitiatorType(APIView):

    def post(self, request, format=None):
        IdentifierType.objects.create(
            name=request.data['transaction_type'])
        return Response(response, status=status.HTTP_201_CREATED)


class OccasionListView(generics.ListAPIView):
    serializer_class = serializers.OccassionSerializer
    queryset = serializers.Occassion.objects.all()

    def list(self, request):
        try:
            occassions = serializers.Occassion.objects.all()
        except:
            raise Http404
        serializer = serializers.OccasionSerializer(
            occassions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OccasionDetailAPIView(DestroyModelMixin,
                            UpdateModelMixin,
                            generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            occassion = Occassion.objects.get(pk=pk)
        except Occassion.DoesNotExist:
            raise Http404
        serializer = OccassionSerializer(occassion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            return Occassion.objects.get(pk=pk)
        except Occassion.DoesNotExist:
            raise Http404
        serializer = OccasionSerializer(
            occassion, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            return Occassion.objects.get(pk=pk)
        except Occassion.DoesNotExist:
            raise Http404
        occassion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MpesaCommandIdListView(generics.ListAPIView):
    serializer_class = serializers.MpesaCommandIdSerializer
    queryset = serializers.MpesaCommandId.objects.all()

    def list(self, request):
        try:
            command_ids = MpesaCommandId.objects.all()
        except:
            raise Http404
        serializer = MpesaCommandIdSerializer(
            command_ids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MpesaCommandIdDetailAPIView(DestroyModelMixin,
                                  UpdateModelMixin,
                                  generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            command_id = MpesaCommandId.objects.get(pk=pk)
        except MpesaCommandId.DoesNotExist:
            raise Http404
        serializer = MpesaCommandIdSerializer(command_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            command_id = MpesaCommandId.objects.get(pk=pk)
        except MpesaCommandId.DoesNotExist:
            raise Http404
        serializer = MpesaCommandIdSerializer(
            command_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            command_id = MpesaCommandId.objects.get(pk=pk)
        except MpesaCommandId.DoesNotExist:
            raise Http404
        command_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MpesaShortCodeOrNumberListView(generics.ListAPIView):
    serializer_class = serializers.CompanyShortCodeOrNumberSerializer
    queryset = serializers.CompanyShortCodeOrNumber.objects.all()

    def list(self, request):
        try:
            company_codes_or_nos = serializers.CompanyShortCodeOrNumber.objects.all()
        except:
            raise Http404
        serializer = serializers.CompanyShortCodeOrNumberSerializer(
            company_codes_or_nos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MpesaShortCodeOrNumberDetailAPIView(DestroyModelMixin,
                                          UpdateModelMixin,
                                          generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            companycode_or_no = CompanyShortCodeOrNumber.objects.get(pk=pk)
        except CompanyShortCodeOrNumber.DoesNotExist:
            raise Http404

        serializer = CompanyShortCodeOrNumberSerializer(companycode_or_no)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            companycode_or_no = CompanyShortCodeOrNumber.objects.get(pk=pk)
        except CompanyShortCodeOrNumber.DoesNotExist:
            raise Http404

        serializer = CompanyShortCodeOrNumberSerializer(
            companycode_or_no, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            companycode_or_no = CompanyShortCodeOrNumber.objects.get(pk=pk)
        except CompanyShortCodeOrNumber.DoesNotExist:
            raise Http404
        companycode_or_no.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InitiatorNameListView(generics.ListAPIView):
    serializer_class = serializers.InitiatorNameSerializer
    queryset = serializers.InitiatorName.objects.all()

    def list(self, request):
        try:
            initiator_names = serializers.InitiatorName.objects.all()
        except:
            raise Http404
        serializer = serializers.InitiatorNameSerializer(
            initiator_names, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InitiatorNameDetailAPIView(DestroyModelMixin,
                                 UpdateModelMixin,
                                 generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            initiator_name = InitiatorName.objects.get(pk=pk)
        except InitiatorName.DoesNotExist:
            raise Http404

        serializer = InitiatorNameSerializer(initiator_name)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            initiator_name = InitiatorName.objects.get(pk=pk)
        except InitiatorName.DoesNotExist:
            raise Http404
        serializer = InitiatorNameSerializer(
            initiator_name, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            initiator_name = InitiatorName.objects.get(pk=pk)
        except InitiatorName.DoesNotExist:
            raise Http404
        initiator_name.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionTypeListView(generics.ListAPIView):
    serializer_class = serializers.TransactionTypeSerializer
    queryset = serializers.TransactionType.objects.all()

    def list(self, request):
        try:
            transaction_types = serializers.TransactionType.objects.all()
        except:
            raise Http404
        serializer = serializers.TransactionTypeSerializer(
            transaction_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionTypeDetailAPIView(DestroyModelMixin,
                                   UpdateModelMixin,
                                   generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            transaction_type = TransactionType.objects.get(pk=pk)
        except TransactionType.DoesNotExist:
            raise Http404
        serializer = TransactionTypeSerializer(transaction_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            transaction_type = TransactionType.objects.get(pk=pk)
        except TransactionType.DoesNotExist:
            raise Http404
        serializer = TransactionTypeSerializer(
            transaction_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            transaction_type = TransactionType.objects.get(pk=pk)
        except TransactionType.DoesNotExist:
            raise Http404
        transaction_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IdentifierTypeListView(generics.ListAPIView):
    serializer_class = serializers.IdentifierTypeSerializer
    queryset = serializers.IdentifierType.objects.all()

    def list(self, request):
        try:
            identifier_types = serializers.IdentifierType.objects.all()
        except:
            raise Http404
        serializer = serializers.IdentifierTypeSerializer(
            identifier_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdentifierTypeDetailAPIView(DestroyModelMixin,
                                  UpdateModelMixin,
                                  generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            identifier_type = IdentifierType.objects.get(pk=pk)
        except IdentifierType.DoesNotExist:
            raise Http404
        serializer = IdentifierSerializer(identifier_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            identifier_type = IdentifierType.objects.get(pk=pk)
        except IdentifierType.DoesNotExist:
            raise Http404
        serializer = IdentifierTypeSerializer(
            identifier_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            identifier_type = IdentifierType.objects.get(pk=pk)
        except IdentifierType.DoesNotExist:
            raise Http404
        identifier_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionListView(generics.ListAPIView):
    serializer_class = serializers.TransactionSerializer
    queryset = serializers.Transaction.objects.all()

    def list(self, request):
        try:
            transactions = serializers.Transaction.objects.all()
        except:
            raise Http404
        serializer = serializers.TransactionSerializer(
            transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionDetailAPIView(generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionResponseListView(generics.ListAPIView):
    serializer_class = serializers.TransactionResponseSerializer
    queryset = serializers.TransactionResponse.objects.all()

    def list(self, request):
        try:
            transaction_responses = serializers.TransactionResponse.objects.all()
        except:
            raise Http404
        serializer = serializers.TransactionResponseSerializer(
            transaction_responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionResponseDetailAPIView(generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            transactionresponse = TransactionResponse.objects.get(pk=pk)
        except TransactionResponse.DoesNotExist:
            raise Http404
        serializer = TransactionResponseSerializer(transactionresponse)
        return Response(serializer.data)


class RegistrationListView(generics.ListAPIView):
    serializer_class = serializers.RegistrationSerializer
    queryset = serializers.Registration.objects.all()

    def list(self, request):
        try:
            registrations = serializers.Registration.objects.all()
        except:
            raise Http404
        serializer = serializers.RegistrationSerializer(
            registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationDetailAPIView(generics.RetrieveAPIView):

    def get(self, request, pk, format=None):
        try:
            registration = Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            raise Http404

        serializer = RegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_200_OK)
