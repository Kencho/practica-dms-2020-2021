""" User class module.
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2021auth.data.db.results.resultbase import ResultBase
from dms2021auth.data.db.results.usersession import UserSession
from dms2021auth.data.db.results.userright import UserRight


class User(ResultBase):
    """ Definition and storage of user ORM records.
    """

    def __init__(self, username: str, password: str):
        """ Constructor method.

        Initializes a user record.
        ---
        Parameters:
            - username: A string with the user name.
            - password: A string with the password hash.
        """
        self.username: str = username
        self.password: str = password

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.
        ---
        Parameters:
            - metadata: The database schema metadata
                        (used to gather the entities' definitions and mapping)
        Returns:
            A Table object with the table definition.
        """
        return Table(
            'users',
            metadata,
            Column('username', String(32), primary_key=True),
            Column('password', String(64), nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.
        ---
        Returns:
            A dictionary with the mapping properties.
        """
        return {
            'sessions': relationship(UserSession, backref='user'),
            'rights': relationship(UserRight, backref='user')
        }
