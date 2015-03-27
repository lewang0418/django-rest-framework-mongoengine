import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib import admin

from mongoengine import *
from mongoengine.django.auth import User

from datetime import datetime



# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
# Note that we don't perform this code in the compat module due to
# bug report #1297
# See: https://github.com/tomchristie/django-rest-framework/issues/1297
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Token(Document):
	"""
	The default authorization token model.
	"""
	key = StringField(max_length=40, primary_key=True)
	user = ReferenceField(AUTH_USER_MODEL, unique=True)
	created = DateTimeField(default=datetime.now)

	class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
		abstract = 'rest_framework_mongoengine.authtoken' not in settings.INSTALLED_APPS

	def save(self, *args, **kwargs):
		if not self.key:
			self.key = self.generate_key()
		return super(Token, self).save(*args, **kwargs)

	def generate_key(self):
		return binascii.hexlify(os.urandom(20)).decode()

	def __str__(self):
		return self.key
