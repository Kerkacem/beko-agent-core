import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_search():
    mock_ss = Mock()
    mock_ss.search.return_value = [{"title": "mock", "snippet": "test"}]
