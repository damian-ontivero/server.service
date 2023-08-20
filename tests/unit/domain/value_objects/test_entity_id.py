"""EntityId tests."""

import pytest

from st_server.shared.domain.value_objects.entity_id import EntityId


def test_generate():
    """Test."""
    entity_id = EntityId.generate()

    assert entity_id.value is not None


def test_from_string():
    """Test."""
    entity_id = EntityId.from_string("1234")

    assert entity_id.value is not None
    assert entity_id.value == "1234"


def test_immutable_generate():
    """Test."""
    entity_id = EntityId.generate()

    assert entity_id.value is not None

    with pytest.raises(AttributeError):
        entity_id.value = "1234"

    with pytest.raises(AttributeError):
        entity_id._value = "12345"


def test_immutable_from_string():
    """Test."""
    entity_id = EntityId.from_string("1234")

    assert entity_id.value is not None
    assert entity_id.value == "1234"

    with pytest.raises(AttributeError):
        entity_id.value = "12345"

    with pytest.raises(AttributeError):
        entity_id._value = "123456"
