from pydantic import BaseModel, EmailStr, Field


class LoginCredentials(BaseModel):
    email: EmailStr = Field()
    password: str = Field(min_length=5)


class RegistrationData(LoginCredentials):
    firstName: str = Field(min_length=1)
    lastName: str = Field(min_length=1)
