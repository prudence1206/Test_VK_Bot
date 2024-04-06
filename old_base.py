
from Constants import DNS
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()
engine = sq.create_engine(DNS)
Session = sessionmaker(bind=engine)


class Bot_guests(Base):
    __tablename__ = "bot_guests"
    id = sq.Column(sq.Integer, primary_key=True)
    guest_vk_id = sq.Column(sq.Integer, nullable=False, unique=True)

    def __str__(self):
        return f'guest: {self.id}: {self.guest_vk_id}'


class VK_users(Base):
    __tablename__ = "vk_users"
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.String(length=55))
    last_name = sq.Column(sq.String(length=55))
    birth_year = sq.Column(sq.Integer)
    sq.CheckConstraint("1950<=birth_year<=2010")
    city = sq.Column(sq.String(length=80))
    sex = sq.Column(sq.Integer)
    sq.CheckConstraint("sex in (0, 1, 2,)")
    link = sq.Column(sq.String(length=255))
    in_relation = sq.Column(sq.Integer)
    sq.CheckConstraint("0<=in_relation<=8")
    photo_1 = sq.Column(sq.String(length=255))
    photo_2 = sq.Column(sq.String(length=255))
    photo_3 = sq.Column(sq.String(length=255))

    def __str__(self):
        return f'user: {self.vk_id}: ({self.first_name}, {self.last_name}, {self.link}, {self.photo_1}, {self.photo_2}, {self.photo_3})'


class Guest_vk_users(Base):
    __tablename__ = "guest_vk_users"
    id = sq.Column(sq.Integer, primary_key=True)
    guest_id = sq.Column(sq.Integer, sq.ForeignKey("bot_guests.id"), nullable=False)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey("vk_users.id"), nullable=False)
    like = sq.Column(sq.Boolean)
    blacklist = sq.Column(sq.Boolean)

    bot_guests = relationship(Bot_guests, backref="guest_vk_users")
    vk_users = relationship(VK_users, backref="guest_vk_users")

    def __str__(self):
        return f'guest_vk_users: {self.id}: (guest_id - {self.guest_id}, vk_user_id - {self.vk_user_id}, like - {self.like}, dislike - {self.blacklist})'


def create_tables():
#    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_quests():
    session = Session()
    guest01 = Bot_guests(guest_vk_id=257332170)
    session.add_all([guest01])
    session.commit()
    session.close()


if __name__ == '__main__':
    create_tables()
    add_quests()

