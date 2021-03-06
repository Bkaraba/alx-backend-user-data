#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adds a user to thr db and returns the user object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """finds user filtered by kwargs arguments"""
        if kwargs is None:
            raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user found by find_user_by method"""
        if kwargs is not None:
            try:
                user = self.find_user_by(id=user_id)
                for k, v in kwargs.items():
                    if not hasattr(User, k):
                        raise ValueError
                    user.k = str(v)
                    print(user.k)
                    self._session.commit()
            except NoResultFound:
                print("updating failed")

    def up(self, user_id: int, **kwargs) -> None:
        user = self.find_user_by(id=int(user_id))
        for key, value in kwargs.items():
            user.key = str(value)
        self._session.commit()
