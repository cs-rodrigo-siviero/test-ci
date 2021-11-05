import main

def test_random(monkeypatch):
    assert type(main.random_num()) is int