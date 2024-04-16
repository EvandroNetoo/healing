from typing import Any
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.http.request import HttpRequest
from .models import User


class CustomBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: str = None,
        password: str = None,
        **kwargs: Any,
    ) -> User | None:
        try:
            user = UserModel.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None

        if user.exists():
            my_user = user.first()
            if my_user.check_password(password):
                return my_user
        return None