from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model

    A placeholder for a custom user model, used in case we need to customize the user model in the future
    """

    pass


class Project(models.Model):
    """
    Project model

    A project is a collection of other things, such as transactions, budget, etc.

    TODO: Think of a better name...
    """

    pass
