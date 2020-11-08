""" UserRight class module.
"""

from sqlalchemy import Table, MetaData, Column, ForeignKey, String, Enum  # type: ignore
from dms2021core.data import UserRightName
from dms2021auth.data.db.results.resultbase import ResultBase


class UserRight(ResultBase):
    """ Definition and storage of user right ORM records.
    """

    def __init__(self, username: str, right: UserRightName):
        """ Constructor method.

        Initializes a user right record.
        ---
        Parameters:
            - username: A string with the user name.
            - right: A string with the right.
        """
        self.username: str = username
        self.right: UserRightName = right

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
            'user_rights',
            metadata,
            Column('username', String(32),
                   ForeignKey('users.username'), primary_key=True),
            Column('right', Enum(UserRightName), primary_key=True)
        )
