
# tests/test_loader.py
from busbidder.loader import call_files




def test_bad_key_is_skipped():
    data = call_files(["comp", "xyz"])
    assert "comp" in data        # companies were loaded
    assert "xyz" not in data     # bad key was skipped


def test_only_bad_keys_gives_error():
    result = call_files(["xyz"])
    assert result == "error"

def test_no_keys_gives_error():
    result = call_files()
    assert result == "you failed to enter a calling list"


def test_empty_list_gives_error():
    assert call_files([]) == "error"

def test_all_five_keys():
    data = call_files(["prof", "comp", "dest", "bad", "off"])
    assert len(data) == 5