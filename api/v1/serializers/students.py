from typing import OrderedDict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """ Serializer for Student """
    
    class Meta:
        model = Student
        fields = [
            'enrollment_number', 'nickname', 'address', 'age', 
            'doc', 'email', 'first_name', 'last_name', 'course', 'is_active'
        ]
    
    def validate_age(self, value):
        if not value.isdigit():
            raise ValidationError(_('The age is not a number'))
        elif int(value) < 3 or int(value) > 105:
            raise ValidationError(_('The age is without in the range of valid ages'))
        return value 

    def validate_doc(self, value):
        if not Student.validate_cpf(value):
            raise ValidationError(_('The Identity document is invalid.'))
        return value 
