import requests
from datetime import datetime
from pathlib import Path

from lectio.helpers import schedule


DATA_DIR = Path(__file__).parent.parent / "data"


class DummyLectio:
    def __init__(self, html: str):
        self.html = html

    def _request(self, url):
        response = requests.Response()
        response.status_code = 200
        response._content = self.html.encode("utf-8")
        return response


def test_parse_additionalinfo_parses_module():
    info = (
        "Aflyst!\nTest Title\n01/01-2021 08:00 til 09:00"
        "\nHold: 1.a Ma\nLærere: ABC\nLokaler: R1\n\nExtra info"
    )
    module = schedule.parse_additionalinfo(info)
    assert module.status == 2
    assert module.title == "Test Title"
    assert module.subject == "1.a Ma"
    assert module.teacher == "ABC"
    assert module.room == "R1"
    assert module.extra_info == "Extra info"
    assert module.start_time == datetime(2021, 1, 1, 8, 0)
    assert module.end_time == datetime(2021, 1, 1, 9, 0)


def test_get_schedule_returns_modules():
    html = (DATA_DIR / "schedule_single_module.html").read_text()
    dummy = DummyLectio(html)
    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 1)
    modules = schedule.get_schedule(dummy, [], start, end)
    assert len(modules) == 1
    mod = modules[0]
    assert mod.title == "Test Title"
    assert mod.status == 1
    assert mod.subject == "1.a Ma"


def test_get_schedule_handles_no_modules():
    html = (DATA_DIR / "schedule_empty.html").read_text()
    dummy = DummyLectio(html)
    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 1)
    modules = schedule.get_schedule(dummy, [], start, end)
    assert modules == []
