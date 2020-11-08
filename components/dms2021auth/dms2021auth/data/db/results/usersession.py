""" UserSession class module.
"""

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey  # type: ignore
from sqlalchemy import String, Boolean, DateTime  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from dms2021auth.data.db.results.resultbase import ResultBase


class UserSession(ResultBase):
    """ Definition and storage of user session ORM records.
    """

    def __init__(self, username: str, token: str, active: bool,
                 created: datetime, updated: datetime):
        """ Constructor method.

        Initializes a user session record.
        ---
        Parameters:
            - username: The username owning the session.
            - token: A string with the session token.
            - active: Whether the session is active or not.
            - created: The datetime of the time of creation.
            - updated: The datetime of the time of update.
        """
        self.token: str = token
        self.username: str = username
        self.active: bool = active
        self.created: datetime = created
        self.updated: datetime = updated

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
            'user_sessions',
            metadata,
            Column('token', String(36), primary_key=True),
            Column('username', String(32),
                   ForeignKey('users.username'), nullable=False),
            Column('active', Boolean, nullable=False, default=True),
            Column('created', DateTime, nullable=False),
            Column('updated', DateTime, nullable=False)
        )

    def touch(self, session: Session, timestamp: datetime):
        """ Updates the update time.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The Session object that was used to retrieve this UserSession.
            - timestamp: A datetime with the timestamp to use.
        """
        try:
            self.updated = timestamp
            session.commit()
        except:
            session.rollback()
            raise

    def deactivate(self, session: Session):
        """ Deactivates the session.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The Session object that was used to retrieve this UserSession.
        """
        try:
            self.active = False
            session.commit()
        except:
            session.rollback()
            raise
