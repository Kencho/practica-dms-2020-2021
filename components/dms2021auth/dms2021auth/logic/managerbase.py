""" ManagerBase class module.
"""

from dms2021auth.data.config import AuthConfiguration
from dms2021auth.data.db import Schema


class ManagerBase():
    """ Base class for all logic manager classes.
    """

    def __init__(self, config: AuthConfiguration, schema: Schema):
        """ Constructor method.

        Initializes the manager.
        ---
        Parameters:
            - config: An AuthConfiguration instance with the manager configurable parameters.
            - schema: The database schema instance to use.
        """
        self.__set_configuration(config)
        self.__set_schema(schema)

    def get_schema(self) -> Schema:
        """ Gets the schema being used by this instance.
        ---
        Returns:
            The DB schema object used by the manager.
        """
        return self.__schema

    def __set_schema(self, schema: Schema):
        """ Sets the schema to be used by this instance.
        ---
        Parameters:
            - schema: The database schema instance to use.
        """
        self.__schema = schema

    def get_configuration(self) -> AuthConfiguration:
        """ Gets the configuration being used by this instance.
        ---
        Returns:
            The configuration object used by the manager.
        """
        return self.__configuration

    def __set_configuration(self, config: AuthConfiguration):
        """ Sets the configuration to be used by this instance.
        ---
        Parameters:
            - config: The configuration instance to use.
        """
        self.__configuration = config
