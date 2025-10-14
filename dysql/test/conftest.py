"""
Copyright 2021 Adobe
All Rights Reserved.

NOTICE: Adobe permits you to use, modify, and distribute this file in accordance
with the terms of the Adobe license agreement accompanying it.
"""

from unittest.mock import patch
import pytest


@pytest.fixture(name="mock_create_engine")
def mock_create_engine_fixture():
    create_mock = patch("dysql.databases.sqlalchemy.create_engine")
    try:
        yield create_mock.start()
    finally:
        create_mock.stop()
