from sqlalchemy.orm import Session

from recogniser.database.models import UserDB
from recogniser.models import User
from recogniser.settings import get_settings

settings = get_settings()


def get_all_users(db: Session) -> dict:
    users = db.query(UserDB).all()
    result = {user.name: user.face for user in users}
    return result


def save_to_db(db: Session, user: User):
    db_user = UserDB(face=user.face, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
