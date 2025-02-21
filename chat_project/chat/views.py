from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from allauth.account.views import ConfirmEmailView
from django.http import JsonResponse
from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation

def index(request):
    return HttpResponse("Hello, world. You're at the chat index.")


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        print("GET")
        key = kwargs.get("key")
        confirmation = None

        # Kiểm tra email confirmation
        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
        except:
            pass

        if confirmation is None:
            try:
                confirmation = EmailConfirmation.objects.get(key=key)
            except EmailConfirmation.DoesNotExist:
                return JsonResponse({"error": "Invalid or expired confirmation key"}, status=400)

        # Xác nhận email
        confirmation.confirm(self.request)
        return JsonResponse({"message": "Email successfully confirmed"}, status=200)

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )