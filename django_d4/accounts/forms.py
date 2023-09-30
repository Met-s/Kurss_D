from allauth.account.forms import SignupForm
from django.core.mail import send_mail


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,  # Будет использованно значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )
        return user

# -----------------------------------------------------------------------------
    # Эта форма при регистрации автоматически добавляет пользователя
    # в группу "common users"

# from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group

# class CustomSignupForm(SignupForm):
    # def save(self, request):
    #     user = super().save(request)
    #     common_users = Group.objects.get(name="common users")
    #     user.groups.add(common_users)
    #     return user

# -----------------------------------------------------------------------------
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )