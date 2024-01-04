import pytest

from st_server.shared.domain.entity_id import EntityId


def test_generate():
    """Test."""
    entity_id = EntityId.generate()

    assert entity_id.value is not None


def test_from_text():
    """Test."""
    entity_id = EntityId.from_text("1234")

    assert entity_id.value is not None
    assert entity_id.value == "1234"


def test_immutable_generate():
    """Test."""
    entity_id = EntityId.generate()

    assert entity_id.value is not None

    with pytest.raises(AttributeError):
        entity_id.value = "1234"


def test_immutable_from_text():
    """Test."""
    entity_id = EntityId.from_text("1234")

    assert entity_id.value is not None
    assert entity_id.value == "1234"

    with pytest.raises(AttributeError):
        entity_id.value = "12345"
