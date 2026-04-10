from pydantic import BaseModel, EmailStr, Field


# -----------------------------------------
# USER SIGNUP
# -----------------------------------------

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=15)


# -----------------------------------------
# OTP VERIFICATION
# -----------------------------------------

class OTPVerifyRequest(BaseModel):
    username: str
    email: str
    mobile: str
    otp: str
    password: str

# -----------------------------------------
# LOGIN REQUEST
# -----------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


# -----------------------------------------
# REQUEST PASSWORD RESET
# -----------------------------------------

class RequestResetRequest(BaseModel):
    identifier: str  # email or mobile


# -----------------------------------------
# RESET PASSWORD
# -----------------------------------------

class ResetPasswordRequest(BaseModel):
    identifier: str
    otp: str
    new_password: str = Field(..., min_length=6)


# -----------------------------------------
# TOKEN RESPONSE
# -----------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"