from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add custom fields as needed
    email_verified = models.BooleanField(default=False)

    # Define the many-to-many relationship with groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users', # Custom related name to resolve the clash with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_users', # Custom related name to resolve the clash with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        # Add a related_name argument to resolve the conflict
        # with the reverse accessors in the default User model
        default_related_name = 'accounts_%(class)s'

    # Note: The Clash Explanation
    # The clash occurs due to the reverse accessors 'Group.user_set' and 'Permission.user_set'
    # defined in the default User model ('auth.User') conflicting with the same reverse accessors
    # in the 'accounts.User' model we defined.
    #
    # By default, Django's authentication system creates 'auth.User' with its own 'groups'
    # and 'user_permissions' fields. When we define our custom 'accounts.User' model with the
    # same fields, a clash arises because both models try to use the same reverse accessors,
    # causing the system check error.
    #
    # To resolve this clash, we provide custom related names ('accounts_users') for the many-to-many
    # relationships with groups and user permissions. This ensures that the reverse accessors are unique
    # and do not conflict with the accessors in 'auth.User'.
    #
    # The related names 'accounts_users' are used to access the groups and user permissions of a 'User'
    # instance, allowing us to differentiate them from the accessors in 'auth.User'.