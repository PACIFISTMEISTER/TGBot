from datetime import datetime

from sqlalchemy import Table, Column, MetaData, Integer, Numeric, create_engine, Text, ForeignKey, BOOLEAN, DateTime, \
    func, BIGINT
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
import psycopg2

engine = create_engine('postgresql+psycopg2://localhost:localhost@localhost/ForTelegramBot')
Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    Id=Column(BIGINT(), primary_key=True)
    User_id = Column(BIGINT())
    LastSeen=Column(DateTime(),default=func.now())
    Type=Column(Text())

def CheckLastUpdate(user_id,Type):
    """проверяет когда в последний раз обновлялись данные от пользователя/зарегистрирован ли он"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user=session.query(Users).filter_by(User_id=user_id,Type=Type).first()
        if user is not None:
            return user.LastSeen
        else:
            user=Users(User_id=user_id,Type=Type)
            session.add(user)
            session.commit()


def UpdateTime(user_id,Type):
    """обнолвнеие таймера"""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user = session.query(Users).filter_by(User_id=user_id, Type=Type).first()
        user.LastSeen=datetime.utcnow()
        session.commit()


