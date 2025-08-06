from pathlib import Path
from unittest import mock

import requests

from lectio.lectio import Lectio, UserType

DATA_DIR = Path(__file__).parent / "data"


def make_response(text: str):
    r = requests.Response()
    r.status_code = 200
    r._content = text.encode("utf-8")
    return r


def test_log_out_creates_new_session():
    lec = Lectio(1)
    old_session = lec._Lectio__session
    lec.log_out()
    assert lec._Lectio__session is not old_session


def test_me_returns_user_id(monkeypatch):
    lec = Lectio(1)
    html = (DATA_DIR / "forside.html").read_text()
    monkeypatch.setattr(lec, "_request", lambda url: make_response(html))

    class DummyMe:
        def __init__(self, lectio, user_id, user_type):
            self.id = user_id
            self.type = user_type

    monkeypatch.setattr("lectio.lectio.Me", DummyMe)

    me = lec.me()
    assert me.id == "42"
    assert me.type == UserType.STUDENT
