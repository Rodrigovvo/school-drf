from django.db import models
from django.utils.translation import gettext_lazy as _

from validate_docbr import CPF

from apps.base.models import User


class Student(User):
    """ Model for students """

    enrollment_number = models.AutoField(
        verbose_name=_('Enrolment number'), 
        help_text=_('Unique number for identify a student'),
        primary_key=True,
        unique=True
    )
    nickname = models.CharField(
        max_length=24, 
        verbose_name=_('Nickname'), 
        help_text=_('Name to display in the interface')
    )
    address = models.CharField(
        max_length=128,
        verbose_name=_('Address'),
        help_text=_('Student Address')
    )
    age = models.CharField(
        max_length=128,
        verbose_name=_('Age'),
        help_text=_('Student Age')
    )
    doc = models.CharField(
        max_length=18,
        verbose_name=_('Identity document'), 
        unique=True
    )
    course = models.CharField(
        max_length=120,
        verbose_name=_('Course')
    )

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def __str__(self) -> str:
        return f'Student: {self.nickname}'

    @classmethod
    def validate_cpf(kls, cpf:str) -> bool:    
        """ Validate the CPF, for lenght and for verifies digits.
        
        :param cpf: (str) The CPF number 
        :returns: (bool) Returns True if CPF is valid or False if is invalid
        """
        valid_cpf = CPF()
        return valid_cpf.validate(cpf)

    def save(self, *args, **kwargs) -> None:
        """
        Save the current instance of Student. 
        Save the numbers of doc like a string.
        Save is_active as True by default.
        """
        self.doc = ''.join(list(filter(lambda x : x.isdigit(), self.doc)))
        return super().save(*args, **kwargs)
