
# tests/test_loader.py
import pytest
from busbidder.loader import call_files




def test_bad_key_is_skipped():
    data = call_files(["comp", "xyz"])
    assert "comp" in data        # companies were loaded
    assert "xyz" not in data     # bad key was skipped


def test_only_bad_keys_gives_error():
    with pytest.raises(ValueError):
        call_files(["xyz"])

def test_no_keys_gives_error():
    with pytest.raises(ValueError):
        call_files()


def test_empty_list_gives_error():
    with pytest.raises(ValueError):
        call_files([])

def test_all_five_keys():
    data = call_files(["prof", "comp", "dest", "bad", "off"])
    assert len(data) == 5