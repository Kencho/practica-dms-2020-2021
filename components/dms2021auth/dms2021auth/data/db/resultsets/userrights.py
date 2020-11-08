""" UserRights class module.
"""

from typing import Optional
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2021core.data import UserRightName
from dms2021auth.data.db.results import UserRight
from dms2021auth.data.db.exc import UserNotFoundError


class UserRights():
    """ Class responsible of table-level user rights operations.
    """
    @staticmethod
    def grant(session: Session, username: str, right: UserRightName) -> UserRight:
        """ Grants a right to a user.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - username: The user name string.
            - right: The right name.
        Returns:
            The created UserRight result.
        Throws:
            - ValueError: If either the username or the right name is missing.
            - UserNotFoundError: If the user granted the right does not exist.
        """
        if not username or not right:
            raise ValueError('A username and a right name are required.')
        user_right: Optional[UserRight] = UserRights.find_right(session, username, right)
        if user_right is not None:
            return user_right
        try:
            new_user_right = UserRight(username, right)
            session.add(new_user_right)
            session.commit()
            return new_user_right
        except IntegrityError as ex:
            session.rollback()
            raise UserNotFoundError() from ex
        except:
            session.rollback()
            raise

    @staticmethod
    def revoke(session: Session, username: str, right: UserRightName):
        """ Revokes a right from a user.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - username: The user name string.
            - right: The right name.
        Throws:
            - ValueError: If either the username or the right name is missing.
        """
        if not username or not right:
            raise ValueError('A username and a right name are required.')
        user_right: Optional[UserRight] = UserRights.find_right(session, username, right)
        if user_right is None:
            return
        try:
            session.delete(user_right)
            session.commit()
        except:
            session.rollback()
            raise

    @staticmethod
    def find_right(session: Session, username: str, right: UserRightName) -> Optional[UserRight]:
        """ Finds a right for a user.
        ---
        Parameters:
            - session: The session object.
            - username: The user name string.
            - right: The right name.
        Returns:
            The UserRight result if found, or None if the user does not have the given right.
        Throws:
            - ValueError: If either the username or the right name is missing.
        """
        if not username or not right:
            raise ValueError('A username and a right name are required.')
        try:
            query = session.query(UserRight).filter_by(
                username=username,
                right=right
            )
            return query.one()
        except NoResultFound:
            return None
