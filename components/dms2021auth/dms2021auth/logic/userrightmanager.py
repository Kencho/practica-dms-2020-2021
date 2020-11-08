""" UserRightManager class module.
"""

from sqlalchemy.orm import Session  # type: ignore
from dms2021core.data import UserRightName
from dms2021auth.data.config import AuthConfiguration
from dms2021auth.data.db import Schema
from dms2021auth.data.db.resultsets import UserRights
from dms2021auth.logic.managerbase import ManagerBase
from dms2021auth.logic.usersessionmanager import UserSessionManager
from dms2021auth.logic.userrightvalidator import UserRightValidator


class UserRightManager(ManagerBase):
    """ Class responsible of the user rights management logic.
    """

    def __init__(
        self, config: AuthConfiguration, schema: Schema, user_session_manager: UserSessionManager
    ):
        """ Constructor method.

        Initializes the manager.
        ---
        Parameters:
            - config: An AuthConfiguration instance with the manager configurable parameters.
            - schema: The database schema instance to use.
            - user_session_manager: The user session manager to be used internally by
                                    the user rights manager.
        """
        super().__init__(config, schema)
        self.__set_user_session_manager(user_session_manager)

    def grant(
        self,
        username: str,
        right: UserRightName,
        session_token: str,
        right_validator: UserRightValidator,
        superuser: bool = False
    ):
        """ Grants a right to a user.
        ---
        Parameters:
            - username: The name of the user to grant the rights to.
            - right: The name of the right to grant.
            - session_token: The token of the session, used to verify that
                             the requestor has sufficient rights.
            - right_validator: The user right validator to use.
            - superuser: If set, will not validate the requestor rights.
                         Use ONLY for administrative purposes.
        Throws:
            - InsufficientRightsError: If the requestor does not have the required rights.
        """
        session: Session = self.get_schema().new_session()
        if not superuser:
            right_validator.enforce_rights(session_token, [UserRightName.AdminRights])
        UserRights.grant(session, username, right)

    def revoke(
        self,
        username: str,
        right: UserRightName,
        session_token: str,
        right_validator: UserRightValidator,
        superuser: bool = False
    ):
        """ Revokes a right from a user.
        ---
        Parameters:
            - username: The name of the user to revoke the rights from.
            - right: The name of the right to revoke.
            - session_token: The token of the session, used to verify that
                             the requestor has sufficient rights.
            - right_validator: The user right validator to use.
            - superuser: If set, will not validate the requestor rights.
                         Use ONLY for administrative purposes.
        Throws:
            - InsufficientRightsError: If the requestor does not have the required rights.
        """
        session: Session = self.get_schema().new_session()
        if not superuser:
            right_validator.enforce_rights(session_token, [UserRightName.AdminRights])
        UserRights.revoke(session, username, right)

    def get_user_session_manager(self) -> UserSessionManager:
        """ Gets the user session manager being used by this instance.
        ---
        Returns:
            The DB user session manager object used by the rights manager.
        """
        return self.__user_session_manager

    def __set_user_session_manager(self, user_session_manager: UserSessionManager):
        """ Sets the user session manager to be used by this instance.
        ---
        Parameters:
            - user_session_manager: The user session manager instance to use.
        """
        self.__user_session_manager = user_session_manager
