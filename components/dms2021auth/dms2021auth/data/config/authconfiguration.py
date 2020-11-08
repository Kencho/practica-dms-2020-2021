""" AuthConfiguration class module.
"""

from dms2021core.data.config import Configuration


class AuthConfiguration(Configuration):
    """ Class responsible of storing a specific authentication service configuration.
    """

    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.
        ---
        Returns:
            A string identifying the component which will categorize the configuration.
        """

        return 'dms2021auth'

    def __init__(self):
        """ Initialization/constructor method.
        """

        Configuration.__init__(self)

    def _validate_values(self, values: dict) -> None:
        """ Validates a set of configuration values.

        Subclasses are expected to override this method and provide their own
        domain-specific validation.
        ---
        Parameters:
            - values: The dictionary of configuration values.
        Throws:
            - A `ValueError` exception if validation is not passed.
        """

    def get_db_connection_string(self) -> str:
        """ Gets the db_connection_string configuration value.
        ---
        Returns:
            A string with the value of db_connection_string.
        """

        return str(self.get_value('db_connection_string'))

    def get_service_host(self) -> str:
        """ Gets the host configuration value.
        ---
        Returns:
            A string with the value of host.
        """

        return str(self.get_value('host'))

    def get_service_port(self) -> int:
        """ Gets the port configuration value.
        ---
        Returns:
            An integer with the value of port.
        """

        value = self.get_value('port')
        return int(str(value))

    def get_debug_flag(self) -> bool:
        """ Gets whether the debug flag is set or not.
        ---
        Returns:
            A boolean with the value of debug.
        """

        return bool(self.get_value('debug'))

    def get_password_salt(self) -> str:
        """ Gets the password salt configuration value.
        ---
        Returns:
            A string with the salt, or '' if no salt is configured.
        """

        return str(self.get_value('salt') or '')
