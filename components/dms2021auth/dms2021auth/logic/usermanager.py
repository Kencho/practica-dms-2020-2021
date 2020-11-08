""" UserManager class module.
"""

from dms2021core.data import UserRightName
from dms2021auth.data.db.resultsets import Users
from dms2021auth.logic.managerbase import ManagerBase
from dms2021auth.logic.userrightvalidator import UserRightValidator


class UserManager(ManagerBase):
    """ Class responsible of the user management logic.
    """

    def create_user(
        self,
        username: str,
        password: str,
        session_token: str,
        right_validator: UserRightValidator,
        superuser: bool = False
    ):
        """ Creates a user.
        ---
        Parameters:
            - username: A non-empty user name string.
            - password: A non-empty user password string.
            - session_token: The token of the session, used to verify that
                             the requestor has sufficient rights.
            - right_validator: The user right validator to use.
            - superuser: If set, will not validate the requestor rights.
                         Use ONLY for administrative purposes.
        Throws:
            - InsufficientRightsError: If the requestor does not have the required rights.
            - ValueError: if either the username or the password is empty.
        """
        if not username:
            raise ValueError('A non-empty username is required.')
        if not password:
            raise ValueError('A non-empty password is required.')
        session = self.get_schema().new_session()
        if not superuser:
            right_validator.enforce_rights(session_token, [UserRightName.AdminUsers])
        password_hash = self.__calculate_password_hash(username, password)
        Users.create(session, username, password_hash)

    def user_exists(self, username: str, password: str) -> bool:
        """ Verifies whether a user with the given credentials exists or not.
        ---
        Parameters:
            - username: The user name string.
            - password: The user password string.
        Returns:
            True if the user exists and the credentials are correct; false otherwise.
        """
        session = self.get_schema().new_session()
        password_hash = self.__calculate_password_hash(username, password)
        return Users.user_exists(session, username, password_hash)

    def __calculate_password_hash(self, username: str, password: str) -> str:
        """ Calculates the password hash of a user.
        ---
        Parameters:
            - username: The username (it is used as a suffix to the password)
            - password: The password itself.
        Returns:
            A string with the password hash.
        """
        salt = self.get_configuration().get_password_salt()
        return Users.hash_password(password, suffix=username, salt=salt)
