import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DNS = 'postgresql://postgres:admin@localhost:5432/VK_BOT'
Base = declarative_base()
engine = sq.create_engine(DNS)
Session = sessionmaker(bind=engine)


class Quests_Users(Base):
    __tablename__ = "quests_users"

    id = sq.Column(sq.Integer, primary_key=True)
    users_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    quests_id = sq.Column(sq.Integer, sq.ForeignKey("quests.id"))
    favorites = sq.Column(sq.Integer)


class Users(Base):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    quests = relationship('quests_users', backref='users')


class Quests(Base):
    __tablename__ = "quests"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    fist_name = sq.Column(sq.String(length=15))
    last_name = sq.Column(sq.String(length=15))
    city = sq.Column(sq.String(length=15))
    sex = sq.Column(sq.String(length=5))
    relation = sq.Column(sq.String(length=5))
    url_profile = sq.Column(sq.String, unique=True)
    url_photo_1 = sq.Column(sq.String, unique=True)
    url_photo_2 = sq.Column(sq.String, unique=True)
    url_photo_3 = sq.Column(sq.String, unique=True)
    users = relationship('quests_users', backref='quests')


def create_tables():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables()

