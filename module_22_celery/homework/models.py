from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///my_base.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    order_id = Column(String(20))
    filename = Column(String(100))

    is_subscribed = Column(Boolean, default=False)

    @classmethod
    def set_user_subscribed(cls, email, order_id, filename):
        user = session.query(User).filter(User.email == email).first()

        if not user:
            user = User(email=email, order_id=order_id, filename=filename)
            session.add(user)
            session.commit()

        user.is_subscribed = True

        session.commit()
        session.close()

    @classmethod
    def set_user_unsubscribed(cls, email):
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.is_subscribed = False
            session.commit()
            session.close()

    @classmethod
    def get_subscribed_users(cls):
        users = session.query(User).filter(User.is_subscribed == True).all()
        session.close()
        return users


Base.metadata.create_all(engine)