""" UserSessions class module.
"""

import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2021auth.data.db.exc import SessionNotFoundError
from dms2021auth.data.db.results import UserSession


class UserSessions():
    """ Class responsible of table-level user sessions operations.
    """
    @staticmethod
    def create(session: Session, username: str) -> UserSession:
        """ Creates a new user session record.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - username: The user name string.
        Returns:
            The created UserSession result.
        """
        if not username:
            raise ValueError('A username and a password hash are required.')
        try:
            new_user_session = UserSession(
                username,
                token=str(uuid.uuid4()),
                active=True,
                created=datetime.now(),
                updated=datetime.now()
            )
            session.add(new_user_session)
            session.commit()
            return new_user_session
        except Exception as ex:
            session.rollback()
            raise ex

    @staticmethod
    def find_session_for_user(session: Session, username: str) -> Optional[UserSession]:
        """ Attempts to find an active session for a given user.
        ---
        Parameters:
            - session: The session object.
            - username: The user name string.
        Returns:
            The UserSession found, or None if no active session existed.
        """
        try:
            query = session.query(UserSession)
            query = query.filter_by(username=username, active=True)
            return query.one()
        except NoResultFound:
            return None

    @staticmethod
    def find_session_by_token(session: Session, session_token: str, active_only: bool = True):
        """ Finds a session by its token.
        ---
        Parameters:
            - session: The session object.
            - session_token: The session token.
            - active_only: Whether only active sessions (default) should be retrieved or not.
        Returns:
            The UserSession found, or None if no matching session was found.
        """
        try:
            query = session.query(UserSession)
            query = query.filter_by(token=session_token)
            if active_only:
                query = query.filter_by(active=True)
            return query.one()
        except NoResultFound:
            return None

    @staticmethod
    def get_active_user_session(session: Session, session_token: str) -> UserSession:
        """ Gets the active user session identified by the given token.
        ---
        Parameters:
            - session_token: The token identifying the session to retrieve.
        Returns:
            The requested UserSession result.
        Throws:
            - SessionNotFound: When the provided session was not found or is inactive.
        """
        user_session: Optional[UserSession] = UserSessions.find_session_by_token(
            session, session_token, active_only=True
        )
        if user_session is None:
            raise SessionNotFoundError()
        return user_session
