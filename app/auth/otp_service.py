import random
from datetime import datetime, timedelta

from app.db.auth_queries import save_otp, get_otp, delete_otp


# OTP validity duration (minutes)
OTP_EXPIRY_MINUTES = 5


def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP code.
    """
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def send_otp(identifier: str):
    """
    Generate and store OTP for email or mobile.
    In production this would send SMS or email.
    """
    otp = generate_otp()

    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    # Store OTP in database
    save_otp(identifier, otp, expires_at.isoformat())

    # For development: print OTP to console
    print(f"🔐 OTP for {identifier}: {otp} (valid {OTP_EXPIRY_MINUTES} minutes)")

    return otp


def verify_otp(identifier: str, user_otp: str) -> bool:
    """
    Verify OTP entered by user.
    """

    otp_record = get_otp(identifier)

    if not otp_record:
        return False

    stored_otp = otp_record["otp"]
    expires_at = datetime.fromisoformat(otp_record["expires_at"])

    # Check expiration
    if datetime.utcnow() > expires_at:
        delete_otp(identifier)
        return False

    # Check match
    if stored_otp != user_otp:
        return False

    # OTP correct → delete it
    delete_otp(identifier)

    return True