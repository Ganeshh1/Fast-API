

from sqlalchemy.orm import Session



from . import models, schemas

from sqlalchemy_utils import PhoneNumber


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):

    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, first_name=user.first_name,last_name=user.last_name,
                          mobile_number=user.mobile_number,gender=user.gender,
                        #   phone_number=PhoneNumber(user.mobile_number, user.country_code),
                          age = user.age,hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session):
    return db.query(models.Profile).all()


def create_user_item(db: Session, item: schemas.ProfileCreate, user_id: int):
    db_item = models.Profile(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_user_item(db: Session, item: schemas.UserCreate, item_id: int):
    db_item = db.query(models.Profile).filter(models.Profile.id == item_id).first()
    print(db_item)
    db.delete(db_item)
    db.commit()
    return db_item


def delete_user(db:Session,user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    db.refresh()
    return user

