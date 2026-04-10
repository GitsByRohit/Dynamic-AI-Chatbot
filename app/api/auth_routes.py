from fastapi import APIRouter, HTTPException

from app.auth.schemas import (
    SignupRequest,
    OTPVerifyRequest,
    LoginRequest,
    RequestResetRequest,
    ResetPasswordRequest
)

from app.auth.auth_service import (
    signup_user,
    verify_signup_otp,
    login_user,
    request_password_reset,
    reset_password
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------------------
# SIGNUP (SEND OTP)
# -----------------------------------------

@router.post("/signup")
def signup(data: SignupRequest):
    try:
        result = signup_user(
            username=data.username,
            email=data.email,
            mobile=data.mobile
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------------------
# VERIFY OTP + CREATE ACCOUNT
# -----------------------------------------

@router.post("/verify-otp")
def verify_otp_route(data: OTPVerifyRequest):

    try:
        result = verify_signup_otp(
            username=data.username,
            email=data.email,
            mobile=data.mobile,
            otp=data.otp,
            password=data.password
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------------------
# LOGIN
# -----------------------------------------

@router.post("/login")
def login(data: LoginRequest):

    try:
        result = login_user(
            email=data.email,
            password=data.password
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# -----------------------------------------
# REQUEST PASSWORD RESET
# -----------------------------------------

@router.post("/request-reset")
def request_reset(data: RequestResetRequest):

    try:
        result = request_password_reset(
            identifier=data.identifier
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------------------
# RESET PASSWORD
# -----------------------------------------

@router.post("/reset-password")
def reset_password_route(data: ResetPasswordRequest):

    try:
        result = reset_password(
            identifier=data.identifier,
            otp=data.otp,
            new_password=data.new_password
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))