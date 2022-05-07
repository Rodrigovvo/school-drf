from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ User base model """
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at  = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name=_('Modified at'),
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self) -> str:
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        return f'{self.first_name} {self.last_name}'
