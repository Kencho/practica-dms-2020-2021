""" UserRight class module.
"""

from dms2021core.data import UserRightName
from dms2021core.data.rest import RestResponse
from dms2021auth.data.db.exc import UserNotFoundError, SessionNotFoundError
from dms2021auth.logic import UserRightManager, UserRightValidator
from dms2021auth.logic.exc import InsufficientRightsError


class UserRight():
    """ Class responsible of handling the user rights-related REST requests.
    """

    def __init__(
        self,
        user_right_manager: UserRightManager,
        user_right_validator: UserRightValidator
    ):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - user_right_manager: Instance responsible of the user rights logic operations.
            - user_right_validator: The validator used to check the user rights.
        """
        self.__set_user_right_manager(user_right_manager)
        self.__set_user_right_validator(user_right_validator)

    def get_user_right_manager(self) -> UserRightManager:
        """ Gets the user rights manager object being used by this instance.
        ---
        Returns:
            The user manager instance in use.
        """
        return self.__user_right_manager

    def __set_user_right_manager(self, user_right_manager: UserRightManager):
        """ Sets the new user rights manager object to be used by this instance.
        ---
        Parameters:
            - user_right_manager: The new user rights manager instance.
        """
        self.__user_right_manager = user_right_manager

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

    def grant(self, username: str, right_name: str, token: str) -> RestResponse:
        """ Grants a right to a user.
        ---
        Parameters:
            - username: The name of the user to grant the right to.
            - right_name: The name of the right to be granted.
            - token: The session token string.
        Returns:
            A RestResponse object with the request response.
        """
        try:
            right: UserRightName = UserRightName[right_name]
            self.get_user_right_manager().grant(username, right, token,
                                                self.get_user_right_validator())
            return RestResponse(mime_type='text/plain')
        except KeyError:
            return RestResponse(code=404, mime_type='text/plain')
        except UserNotFoundError:
            return RestResponse(code=404, mime_type='text/plain')
        except SessionNotFoundError:
            return RestResponse(code=401, mime_type='text/plain')
        except InsufficientRightsError:
            return RestResponse(code=401, mime_type='text/plain')

    def revoke(self, username: str, right_name: str, token: str) -> RestResponse:
        """ Revokes a right from a user.
        ---
        Parameters:
            - username: The name of the user to revoke the right from.
            - right_name: The name of the right to be revoked.
            - token: The session token string.
        Returns:
            A RestResponse object with the request response.
        """
        try:
            right: UserRightName = UserRightName[right_name]
            self.get_user_right_manager().revoke(username, right, token,
                                                 self.get_user_right_validator())
            return RestResponse(mime_type='text/plain')
        except KeyError:
            return RestResponse(code=404, mime_type='text/plain')
        except UserNotFoundError:
            return RestResponse(code=404, mime_type='text/plain')
        except SessionNotFoundError:
            return RestResponse(code=401, mime_type='text/plain')
        except InsufficientRightsError:
            return RestResponse(code=401, mime_type='text/plain')

    def has_right(self, username: str, right_name: str) -> RestResponse:
        """ Gets whether a user has a given right or not.
        ---
        Parameters:
            - username: The name of the user.
            - right_name: The name of the right.
            - right_validator: The user right validator to use.
        Returns:
            A RestResponse object with the request response.
        """
        try:
            right: UserRightName = UserRightName[right_name]
            if self.get_user_right_validator().has_right(username, right):
                return RestResponse(mime_type='text/plain')
            return RestResponse(code=404, mime_type='text/plain')
        except KeyError:
            return RestResponse(code=404, mime_type='text/plain')
        except UserNotFoundError:
            return RestResponse(code=404, mime_type='text/plain')
