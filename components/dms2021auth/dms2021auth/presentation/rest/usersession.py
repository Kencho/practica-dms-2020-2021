""" UserSession class module.
"""

import json
from dms2021core.data.rest import RestResponse
from dms2021auth.data.db.exc import SessionNotFoundError
from dms2021auth.logic import UserSessionManager
from dms2021auth.logic.exc import InvalidCredentialsError

class UserSession():
    """ Class responsible of handling the user-related REST requests.
    """
    def __init__(self, user_session_manager: UserSessionManager):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - user_session_manager: Instance responsible of the user session logic operations.
        """
        self.__set_user_session_manager(user_session_manager)

    def get_user_session_manager(self) -> UserSessionManager:
        """ Gets the user session manager object being used by this instance.
        ---
        Returns:
            The user session manager instance in use.
        """
        return self.__user_session_manager

    def __set_user_session_manager(self, user_session_manager: UserSessionManager):
        """ Sets the new user session manager object to be used by this instance.
        ---
        Parameters:
            - user_session_manager: The new user manager instance.
        """
        self.__user_session_manager = user_session_manager

    def login(self, username: str, password: str) -> RestResponse:
        """ Logs in a user.
        ---
        Parameters:
            - username: The user name string.
            - password: The user password string.
        Returns:
            A RestResponse object with the request response.
        """
        try:
            session_id = self.get_user_session_manager().login(username, password)
            res_content = {
                'session_id': session_id
            }
            res_content_json = json.dumps(res_content, separators=(',', ':'))
            return RestResponse(res_content_json, mime_type='application/json')
        except InvalidCredentialsError:
            return RestResponse(code=401, mime_type='text/plain')

    def logout(self, token: str) -> RestResponse:
        """ Logs out a user/session.
        ---
        Parameters:
            - token: The session token string.
        Returns:
            A RestResponse object with the request response.
        """
        try:
            self.get_user_session_manager().logout(token)
            return RestResponse(mime_type='text/plain')
        except SessionNotFoundError:
            return RestResponse(code=401, mime_type='text/plain')
