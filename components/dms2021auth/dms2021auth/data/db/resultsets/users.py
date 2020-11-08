""" Users class module.
"""

import hashlib
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2021auth.data.db.results import User
from dms2021auth.data.db.exc import UserExistsError


class Users():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, username: str, password_hash: str) -> User:
        """ Creates a new user record.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - username: The user name string.
            - password: The password hash string.
        Returns:
            The created User result.
        Throws:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.
        """
        if not username or not password_hash:
            raise ValueError('A username and a password hash are required.')
        try:
            new_user = User(username, password_hash)
            session.add(new_user)
            session.commit()
            return new_user
        except IntegrityError as ex:
            raise UserExistsError(
                'A user with name ' + username + ' already exists.'
                ) from ex

    @staticmethod
    def user_exists(session: Session, username: str, password_hash: str) -> bool:
        """ Determines whether a user exists or not.
        ---
        Parameters:
            - session: The session object.
            - username: The user name string.
            - password_hash: The password hash string.
        Returns:
            True if a user with the given credentials exists; false otherwise.
        """
        try:
            query = session.query(User).filter_by(username=username, password=password_hash)
            query.one()
        except NoResultFound:
            return False
        return True

    @staticmethod
    def hash_password(password: str, suffix: str = '', salt: str = '') -> str:
        """ A password hashing function compatible with the schema.
        ---
        Parameters:
            - password: The password string.
            - suffix: An optional suffix string.
            - salt: An optional salt string.
        Returns:
            A string with the hashed password.
        """
        return hashlib.sha256(bytes(password + suffix + salt, 'utf-8')).hexdigest()
