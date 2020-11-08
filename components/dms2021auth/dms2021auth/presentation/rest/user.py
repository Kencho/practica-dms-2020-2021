""" User class module.
"""

from dms2021core.data.rest import RestResponse
from dms2021auth.logic import UserManager, UserRightValidator
from dms2021auth.data.db.exc import UserExistsError
from dms2021auth.logic.exc import InsufficientRightsError


class User():
    """ Class responsible of handling the user-related REST requests.
    """

    def __init__(self, user_manager: UserManager, user_right_validator: UserRightValidator):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - user_manager: Instance responsible of the user logic operations.
            - user_right_validator: The validator used to check the user rights.
        """
        self.__set_user_manager(user_manager)
        self.__set_user_right_validator(user_right_validator)

    def get_user_manager(self) -> UserManager:
        """ Gets the user manager object being used by this instance.
        ---
        Returns:
            The user manager instance in use.
        """
        return self.__user_manager

    def __set_user_manager(self, user_manager: UserManager):
        """ Sets the new user manager object to be used by this instance.
        ---
        Parameters:
            - user_manager: The new user manager instance.
        """
        self.__user_manager = user_manager

    def get_user_right_validator(self) -> UserRightValidator:
        """ Gets the user rights validator object being used by this instance.
        ---
        Returns:
            The user validator instance in use.
        """
        return self.__user_right_validator

    def __set_user_right_validator(self, user_right_validator: UserRightValidator):
        """ Sets the new user rights validator object to be used by this instance.
        ---
        Parameters:
            - user_right_validator: The new user rights validator instance.
        """
        self.__user_right_validator = user_right_validator

    def create(self, username: str, password: str, token: str) -> RestResponse:
        """ Creates a new user.
        ---
        Parameters:
            - username: The user name string.
            - password: The password string.
            - token: The session token string.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            self.get_user_manager().create_user(
                username, password, token, self.get_user_right_validator()
            )
        except ValueError:
            return RestResponse(code=400, mime_type='text/plain')
        except InsufficientRightsError:
            return RestResponse(code=401, mime_type='text/plain')
        except UserExistsError:
            return RestResponse(code=409, mime_type='text/plain')
        return RestResponse(mime_type='text/plain')
