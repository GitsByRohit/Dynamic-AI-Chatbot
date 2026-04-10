from datetime import timedelta

from app.auth.utils import hash_password, verify_password, create_access_token
from app.auth.otp_service import send_otp, verify_otp

from app.db.auth_queries import (
    create_user,
    get_user_by_email,
    get_user_by_mobile,
    update_password
)

# JWT expiration (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -----------------------------------------
# SIGNUP FLOW
# -----------------------------------------

def signup_user(username: str, email: str, mobile: str):
    """
    Start signup process by sending OTP.
    """

    # Check if user already exists
    if get_user_by_email(email):
        raise ValueError("Email already registered")

    if get_user_by_mobile(mobile):
        raise ValueError("Mobile number already registered")

    # Send OTP
    send_otp(email)

    return {
        "message": "OTP sent to your email"
    }


# -----------------------------------------
# VERIFY OTP + SET PASSWORD
# -----------------------------------------

def verify_signup_otp(username: str, email: str, mobile: str, otp: str, password: str):
    """
    Verify OTP and create user account.
    """

    valid = verify_otp(email, otp)

    if not valid:
        raise ValueError("Invalid or expired OTP")

    hashed_password = hash_password(password)

    create_user(username, email, mobile, hashed_password)

    return {
        "message": "Account created successfully"
    }


# -----------------------------------------
# LOGIN
# -----------------------------------------

def login_user(email: str, password: str):
    """
    Authenticate user and generate JWT token.
    """

    user = get_user_by_email(email)

    if not user:
        raise ValueError("User not found")

    if not verify_password(password, user["password"]):
        raise ValueError("Incorrect password")

    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -----------------------------------------
# REQUEST PASSWORD RESET
# -----------------------------------------

def request_password_reset(identifier: str):
    """
    Send OTP for password reset.
    identifier can be email or mobile
    """

    user = get_user_by_email(identifier) or get_user_by_mobile(identifier)

    if not user:
        raise ValueError("User not found")

    send_otp(identifier)

    return {
        "message": "OTP sent"
    }


# -----------------------------------------
# RESET PASSWORD
# -----------------------------------------

def reset_password(identifier: str, otp: str, new_password: str):
    """
    Verify OTP and update password.
    """

    valid = verify_otp(identifier, otp)

    if not valid:
        raise ValueError("Invalid or expired OTP")

    hashed_password = hash_password(new_password)

    update_password(identifier, hashed_password)

    return {
        "message": "Password updated successfully"
    }