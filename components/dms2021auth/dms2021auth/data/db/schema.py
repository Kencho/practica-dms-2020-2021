""" Schema class module.
"""

from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from dms2021auth.data.config import AuthConfiguration
from dms2021auth.data.db.results import User, UserSession, UserRight


# Required for SQLite to enforce FK integrity when supported
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
    """ Sets the SQLite foreign keys enforcement pragma on connection.
    ---
    Parameters:
        - dbapi_connection: The connection to the database API.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.close()


class Schema():
    """ Class responsible of the schema initialization and session generation.
    """

    def __init__(self, config: AuthConfiguration):
        """ Constructor method.

        Initializes the schema, deploying it if necessary.
        ---
        Parameters:
            - config: The `AuthConfiguration` instance with the schema connection parameters.
        """
        self.__declarative_base = declarative_base()
        if config.get_db_connection_string() is None:
            raise RuntimeError(
                'A value for the configuration parameter `db_connection_string` is needed.'
            )
        db_connection_string: str = config.get_db_connection_string() or ''
        self.__create_engine = create_engine(db_connection_string)
        self.__session_maker = sessionmaker(bind=self.__create_engine)

        User.map(self.__declarative_base.metadata)
        UserSession.map(self.__declarative_base.metadata)
        UserRight.map(self.__declarative_base.metadata)
        self.__declarative_base.metadata.create_all(self.__create_engine)

    def new_session(self) -> Session:
        """ Constructs a new session.
        ---
        Returns:
            A new `Session` object.
        """
        return self.__session_maker()
