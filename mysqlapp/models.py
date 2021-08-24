from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,Unicode
from sqlalchemy.orm import relationship , composite
from sqlalchemy_utils import PhoneNumber
import sqlalchemy.types as types

from .database import Base


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]



class User(Base):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    mobile_number = Column(String(15), index=True)
    _phone_number = Column(Unicode(20))
    country_code = Column(Unicode(8))
    # phone_number = composite(
    #             PhoneNumber,
    #             _phone_number,
    #             country_code
    #         )
    gender = Column(String(16),
            ChoiceType({"Male": "Male",  "Female": "Female"}), nullable=False
        )
    age = Column(Integer, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="user")



class Profile(Base):

    __tablename__ = "profile"


    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(100), index=True)
    company_name = Column(String(100), index=True)
    salary = Column(Integer,default=0)
    utr = Column(String(11), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="profile")

