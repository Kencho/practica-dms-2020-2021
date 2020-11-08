""" UserRightValidator class module.
"""

from typing import Optional, List
from sqlalchemy.orm import Session  # type: ignore
from dms2021core.data import UserRightName
from dms2021auth.data.db import Schema
from dms2021auth.data.db.results import UserRight, UserSession
from dms2021auth.data.db.resultsets import UserRights, UserSessions
from dms2021auth.logic.exc import InsufficientRightsError


class UserRightValidator():
    """ Toolkit class to validate user rights.
    """

    def __init__(self, schema: Schema):
        """ Constructor method.

        Initializes the manager.
        ---
        Parameters:
            - schema: The database schema instance to use.
        """
        self.__set_schema(schema)

    def has_right(self, username: str, right: UserRightName) -> bool:
        """ Determines whether a given user has a certain right or not.
        ---
        Parameters:
            - username: The user name string.
            - right: The right name.
        Returns:
            True if the user has the given right; false otherwise.
        """
        session: Session = self.get_schema().new_session()
        user_right: Optional[UserRight] = UserRights.find_right(
            session, username, right)
        if user_right is not None:
            return True
        return False

    def enforce_rights(self, session_token: str, rights: List[UserRightName]):
        """ Raises an error if the owner of session identified by the token
        does not have all of the provided rights.
        ---
        Parameters:
            - session_token: The session token string.
            - rights: A list of user right names.
        Throws:
            - InsufficientRightsError: If the user lacks any of the rights.
        """
        session: Session = self.get_schema().new_session()
        user_session: UserSession = UserSessions.get_active_user_session(
            session, session_token
        )
        for right in rights:
            if not self.has_right(user_session.username, right):
                raise InsufficientRightsError()

    def get_schema(self) -> Schema:
        """ Gets the schema being used by this instance.
        ---
        Returns:
            The DB schema object used by the validator.
        """
        return self.__schema

    def __set_schema(self, schema: Schema):
        """ Sets the schema to be used by this instance.
        ---
        Parameters:
            - schema: The database schema instance to use.
        """
        self.__schema = schema
