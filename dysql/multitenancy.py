"""
Copyright 2025 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in accordance
with the terms of the Adobe license agreement accompanying it.
"""

import functools
import logging
from typing import Any, Callable, TypeVar
from contextlib import contextmanager

from dysql.exceptions import DBNotPreparedError
from dysql import (
    set_current_database,
    reset_current_database,
)

LOGGER = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


@contextmanager
def tenant_database_manager(database_key: str):
    """
    Context manager for temporarily switching to a different database.

    :param database_key: the database key to switch to
    :raises DBNotPreparedError: if the database key is not set
    """
    if not database_key:
        raise DBNotPreparedError(
            "Cannot switch to database tenant with empty database key"
        )

    try:
        LOGGER.debug(f"Switching to database {database_key}")
        set_current_database(database_key)
        yield
    except Exception as e:
        LOGGER.error(f"Error while using database {database_key}: {e}")
        raise
    finally:
        try:
            reset_current_database()
            LOGGER.debug(f"Reset database context from: {database_key}")
        except Exception as e:
            LOGGER.error(f"Error resetting database context: {e}")
            # Don't re-raise here to avoid masking the original exception


def use_database_tenant(database_key: str):
    """
    Decorator that switches to a specific database for the duration of the function call.
    :param database_key: the database key to use
    :return: the decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with tenant_database_manager(database_key):
                return func(*args, **kwargs)

        return wrapper

    return decorator
