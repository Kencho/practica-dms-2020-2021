""" Module containing the dms2021core.data.config.configuration.Configuration class.
"""

import os
from abc import ABC, abstractmethod
from typing import Union, Dict, List, Tuple, Optional
from appdirs import user_config_dir  # type: ignore
import yaml

ConfigurationValueType = Optional[
    Union[str, int, float, bool, Dict, List, Tuple]
]


class Configuration(ABC):
    """ Class responsible of storing a specific service configuration.
    """

    @abstractmethod
    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.
        ---
        Returns:
            A string identifying the component which will categorize the configuration.
        """

        return ''

    def default_config_file(self) -> str:
        """ Path of the default configuration file.
        ---
        Returns:
            A string with the path of the default configuration file.
        """

        return os.path.join(user_config_dir(self._component_name()), 'config.yml')

    def __init__(self):
        """ Initialization/constructor method.
        """

        self.__values: dict

        self._set_values({})

    def load_from_file(self, path: str = 'config.yml') -> None:
        """ Loads the configuration values from a given file.

        This operation will override any previously existing configuration parameters.
        ---
        Parameters:
            - path: A string with the path of the configuration file to load.
        """

        with open(path, 'r') as stream:
            self._set_values(yaml.load(stream, Loader=yaml.SafeLoader))

    def _set_values(self, values: dict) -> None:
        """ Overrides the configuration values with a given dictionary.
        ---
        Parameters:
            - values: The dictionary of configuration values.
        """

        self._validate_values(values)
        self.__values = values

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

    def set_value(self, key: str, value: ConfigurationValueType) -> None:
        """ Sets a single value into the configuration in this object.
        ---
        Parameters:
            - key: A string with the name of the configuration parameter to set.
            - value: An optional string, integer, float, boolean, tuple, list
                     or dictionary contained in the parameter.
        """
        self.__values[key] = value

    def get_value(self, key: str) -> ConfigurationValueType:
        """ Retrieves a single value from the configuration in this object.
        ---
        Parameters:
            - key: A string with the name of the configuration parameter to retrieve.
        Returns:
            A string, integer, float, boolean, tuple, list or dictionary contained
            in the parameter, or None if no such key was found or its value is
            deliberately set to None.
        """

        try:
            return self.__values[key]
        except KeyError:
            return None
