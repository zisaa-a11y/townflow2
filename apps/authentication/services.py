from datetime import timedelta
from hashlib import sha256
from secrets import randbelow

from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import OtpSession, User


def blacklist_refresh_token(refresh_token: str) -> None:
    token = RefreshToken(refresh_token)
    token.blacklist()


def issue_otp_session(user: User, channel: str) -> OtpSession:
    plain_code = str(randbelow(900000) + 100000)
    code_hash = sha256(f"{user.id}:{channel}:{plain_code}".encode("utf-8")).hexdigest()
    ttl = timedelta(minutes=getattr(settings, "OTP_EXPIRY_MINUTES", 10))

    OtpSession.objects.filter(user=user, channel=channel, is_used=False).update(is_used=True)
    session = OtpSession.objects.create(
        user=user,
        channel=channel,
        code_hash=code_hash,
        expires_at=timezone.now() + ttl,
    )
    session._plain_code = plain_code
    return session


def verify_otp_session(user: User, channel: str, code: str) -> bool:
    now = timezone.now()
    session = (
        OtpSession.objects.filter(user=user, channel=channel, is_used=False, expires_at__gte=now)
        .order_by("-created_at")
        .first()
    )
    if not session:
        return False

    incoming_hash = sha256(f"{user.id}:{channel}:{code}".encode("utf-8")).hexdigest()
    if incoming_hash != session.code_hash:
        return False

    session.is_used = True
    session.save(update_fields=["is_used", "updated_at"])
    user.is_verified = True
    user.save(update_fields=["is_verified", "updated_at"])
    return True
