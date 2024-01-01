"""Views for Staff API"""
from rest_framework import (
    viewsets,
    mixins,
    authentication,
    status
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from staff import models
from staff import serializers
from core.permissions import (
    IsAdmin,
    IsTeacher
)
from core.serializers import UserAccountSerializer


class StaffViewSets(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """View for manage Staff APIs"""
    serializer_class = serializers.StaffSerializer
    queryset = models.Staff.objects.all()
    authentication_classes = (
        authentication.TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated, IsTeacher or IsAdmin,
    )

    def get_queryset(self):
        """Retrieve and return staff list for current admin user"""
        return self.queryset.filter(
            school=self.request.user.staff.school
        ).order_by('-first_name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.StaffDetailSerializer
        if self.action == 'qualifications'\
                or self.action == 'qualification_detail':
            return serializers.QualificationSerializer
        if self.action == 'promotions':
            return serializers.PromotionSerializer
        if self.action == 'promotion_detail':
            return serializers.PromotionSerializer
        if self.action == 'account':
            return UserAccountSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(
            school=self.request.user.staff.school
        )

    @action(
        methods=['POST'], detail=True,
        permission_classes=[IsAdmin]
    )
    def account(self, request, pk=None):
        """Create account for a staff"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                'Account credentials created', status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=('GET', 'POST', ),
        url_name='qualifications',
        url_path='qualifications',
        detail=True,
    )
    def qualifications(self, request, pk=None):
        """List all Qualtifications a specific staff"""
        staff = models.Staff.objects.get(id=pk)
        if request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
            )
            if serializer.is_valid():
                serializer.save(staff=staff)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'GET':
            qualifications = models.Qualification.objects.filter(
                staff=staff
            )
            serializer = self.get_serializer(qualifications, many=True)
            return Response(serializer.data)

    @action(
        methods=('GET', 'PUT', 'PATCH'),
        url_path=r'qualifications/(?P<qid>[^/.]+)',
        url_name='qualification_detail',
        detail=True,
    )
    def qualification_detail(self, request, pk=None, qid=None):
        """Detail page for a qualification object"""
        instance = models.Qualification.objects.get(id=qid)

        if request.method == 'PATCH' or request.method == 'PUT':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'GET':
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=('GET', 'POST', ),
        url_path='promotions',
        url_name='promotions',
        detail=True,
    )
    def promotions(self, request, pk=None, pid=None):
        """Staff promotions"""
        staff = models.Staff.objects.get(id=pk)
        if request.method == 'GET':
            promotions = staff.promotions.all()
            serializer = self.get_serializer(promotions, many=True)
            return Response(serializer.data)
        if request.method == 'POST':

            serializer = serializers.PromotionSerializer(
                data=request.data
            )
            if serializer.is_valid():
                serializer.save(staff=staff)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(
            {'msg': 'Method not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(
        methods=('GET', 'PUT', 'PATCH'),
        url_path=r'promotions/(?P<pid>[^/.]+)',
        url_name='promotion_detail',
        detail=True,
    )
    def promotion_detail(self, request, pk=None, pid=None):
        """Staff promotions detail"""
        promotion = models.Promotion.objects.get(id=pid)
        if promotion:
            serializer = self.get_serializer(promotion)
            if request.method == 'GET':
                return Response(serializer.data, status=status.HTTP_200_OK)
            if request.method == 'PUT' or request.method == 'PATCH':
                serializer = self.get_serializer(
                    promotion, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'msg': 'Not found'}, status=status.HTTP_404_NOT_FOUND
            )
