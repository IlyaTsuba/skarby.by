from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from accounts.filters import AccountFilter
from accounts.models import Account, SavedAccount, Photos, AccountLikes
from accounts.serializers import AccountSerializer, SavedAccountSerializer, AccountListSerializer


# class AccountListPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 10

# prefetch_related(
#         Prefetch('account_photos', queryset=Photos.objects.all(), to_attr='account_list')

class AccountsListView(ListAPIView):
    """
    This view is to show all published posts.
    """
    queryset = Account.objects.filter(is_published=Account.Status.PUBLISHED).select_related(
        'category')
    # Show only accepted to publish accounts
    serializer_class = AccountListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AccountFilter
    # pagination_class = AccountListPagination


class AccountDetailView(APIView):
    """
    This view is to show exact Account details
    """

    def get(self, request, slug):
        account = get_object_or_404(
            Account.objects.select_related('category').prefetch_related('account_photos', 'account_social_media'),
            slug=slug,
            is_published=Account.Status.PUBLISHED
        )

        serializer = AccountSerializer(account, context={'request': request})
        return Response(serializer.data)


class AccountLikeView(APIView):
    permission_classes = [IsAuthenticated, ]

    # def post(self, request, slug):
    #     user = request.user
    #     account = get_object_or_404(Account, slug=slug)
    #
    #     liked_account, created = AccountLikes.objects.get_or_create(user=user, account=account)
    #
    #     if created:  # True, add like
    #         return Response({'message': 'Падабаечка!'}, status=status.HTTP_201_CREATED)
        # else:  # False, like exists
        #     return Response({'message': 'Ужо спадабалася!'}, status=status.HTTP_200_OK)
    def post(self, request, slug):
        user = request.user
        account = get_object_or_404(Account, slug=slug)

        liked_account, created = AccountLikes.objects.get_or_create(user=user, account=account)

        if created:  # True, add like
            return Response({'message': 'Падабаечка!'}, status=status.HTTP_201_CREATED)
        else:  # False, like exists
            return Response({'message': 'Ужо спадабалася!'}, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        user = request.user
        account = get_object_or_404(Account, slug=slug)
        like_to_delete = get_object_or_404(AccountLikes, user=user, account_id=account.id)
        if like_to_delete:
            like_to_delete.delete()
            return Response({'message': 'Падабаечка выдалена:('}, status=status.HTTP_200_OK)

# Saved account functionality


class SavedAccountsCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        user = request.user

        saved_account, created = SavedAccount.objects.get_or_create(user=user, account=account)
        # get_or_create method creates object if object doesn't exist in saved accounts and returns True,
        # if not returns False

        if created:  # True, new account saved
            return Response({'message': 'Акаўнт захаваны'}, status=status.HTTP_201_CREATED)
        # else:  # False, account already exists in saved
        #     return Response({'message': 'Акаўнт ужо захаваны'}, status=status.HTTP_200_OK)

    def delete(self, request, account_id):
        user = request.user
        account_to_delete = get_object_or_404(SavedAccount, user=user, id=account_id)
        account_to_delete.delete()
        return Response({'message': 'Акаўнт быў выдалены'}, status=status.HTTP_204_NO_CONTENT)


class SavedAccountsListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        saved_accounts = SavedAccount.objects.filter(user=user)
        serializer = SavedAccountSerializer(saved_accounts, many=True)
        return Response(serializer.data)
