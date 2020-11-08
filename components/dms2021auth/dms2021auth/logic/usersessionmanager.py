""" UserSessionManager class module.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session  # type: ignore
from dms2021auth.data.config import AuthConfiguration
from dms2021auth.data.db import Schema
from dms2021auth.data.db.resultsets import UserSessions
from dms2021auth.data.db.results import UserSession
from dms2021auth.logic.managerbase import ManagerBase
from dms2021auth.logic.usermanager import UserManager
from dms2021auth.logic.exc import InvalidCredentialsError


class UserSessionManager(ManagerBase):
    """ Class responsible of the user session management logic.
    """

    def __init__(self, config: AuthConfiguration, schema: Schema, user_manager: UserManager):
        """ Constructor method.

        Initializes the manager.
        ---
        Parameters:
            - config: An AuthConfiguration instance with the manager configurable parameters.
            - schema: The database schema instance to use.
            - user_manager: The user manager to be used internally by the user sessions manager.
        """
        super().__init__(config, schema)
        self.__set_user_manager(user_manager)

    def login(self, username: str, password: str) -> str:
        """ Logs a user in. I.e., creates or reuses a session if the credentials are correct.
        ---
        Parameters:
            - username: The user name string.
            - password: The user password string.
        Returns:
            The user session token.
        Throws:
            - InvalidCredentialsError: When the credentials used to log in are wrong.
        """
        if not self.get_user_manager().user_exists(username, password):
            raise InvalidCredentialsError()
        session: Session = self.get_schema().new_session()
        user_session: Optional[UserSession] = UserSessions.find_session_for_user(
            session, username
        )
        token: str
        if user_session is None:
            token = UserSessions.create(session, username).token
        else:
            user_session.touch(session, datetime.now())
            token = user_session.token
        return token

    def logout(self, session_token: str):
        """ Logs a user out. I.e., deactivates the given session.
        ---
        Parameters:
            - session_token: The token of the session to deactivate.
        Throws:
            - SessionNotFound: When the provided session was not found or is inactive.
        """
        session: Session = self.get_schema().new_session()
        user_session: UserSession = UserSessions.get_active_user_session(
            session, session_token
        )
        user_session.deactivate(session)

    def get_user_manager(self) -> UserManager:
        """ Gets the user manager being used by this instance.
        ---
        Returns:
            The DB user manager object used by the manager.
        """
        return self.__user_manager

    def __set_user_manager(self, user_manager: UserManager):
        """ Sets the user manager to be used by this instance.
        ---
        Parameters:
            - user_manager: The user manager instance to use.
        """
        self.__user_manager = user_manager
