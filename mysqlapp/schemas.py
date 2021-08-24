from typing import List, Optional


from pydantic import BaseModel




class ProfileBase(BaseModel):

    bio: str
    utr: str
    company_name: Optional[str] = None
    salary: Optional[str] = None


class ProfileCreate(ProfileBase):

    pass



class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):

    first_name : str
    last_name : str
    mobile_number : str
    country_code : str
    gender : str
    age : int
    email: str




class UserCreate(UserBase):

    password: str



class User(UserBase):
    id: int
    is_active: bool
    profile: List[Profile] = []

    class Config:
        orm_mode = True
