from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp=datetime.now()):
        return (
                str(user.pk) + str(timestamp) +
                str(user.is_active)
        )

account_activation_token = TokenGenerator()
