#!/usr/bin/env python3
import pytest
import sys

sys.path.insert(0, "..")
from skills.skill_search import SearchSkill


def test_search_duckduckgo():
    ss = SearchSkill()
    results = ss.search("Python pytest", use_cache=False)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]


def test_search_cache():
    ss = SearchSkill()
    results1 = ss.search("test cache")
    results2 = ss.search("test cache")
    assert results1 == results2  # Cached
