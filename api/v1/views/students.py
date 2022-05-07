from django.utils.translation import gettext_lazy as _
from django.db.models.query_utils import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.serializers.students import StudentSerializer
from apps.students.models import Student


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for students
    """

    queryset = Student.objects.filter(is_active=True).order_by('-modified_at')
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):

        print(request)
        print(args)
        print(kwargs)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        if instance:
            instance.is_active = False
            print(instance)
            instance.save()
        else:
            raise NotFound(_('Student Not Found.'))
        return Response(status=status.HTTP_204_NO_CONTENT, content_type='json')

    @action(detail=False, methods=['get'], name='all-students',
    url_path='all-students', url_name='all-students')
    def get_students(self, request):
        """ 
        Action to returns serializer for all Students, without pagination.
        
        :returns: (Response)
        """
        persons = Student.objects.all()
        serializer_context = {
            'request': request,
        }

        serializer = self.serializer_class(
            persons, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], name='search',
    url_path='search', url_name='search')
    def search_students(self, request):
        """
        View responsible for search students based on the name and age, with pagination.
        """       
        params = self.request.query_params
        
        serializer_context = {
            'request': request,
        }
        queryset = Student.objects.filter(
            Q(
                Q(nickname__icontains=params.get('name', '')) |
                Q(first_name__icontains=params.get('name', '')) |
                Q(last_name__icontains=params.get('name', '')) 
            ) &
            Q(course__icontains=params.get('course', '')) &
            Q(enrollment_number=params.get('enrollment', ''))
        ).order_by('-modified_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)
        