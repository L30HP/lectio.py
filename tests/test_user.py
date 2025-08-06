from lectio.models.user import User, UserType


class DummyLectio:
    def _request(self, url):
        raise AssertionError("_request should not be called when lazy=True")


def test_usertype_strings():
    assert UserType.STUDENT.get_str() == "student"
    assert str(UserType.TEACHER) == "laerer"


def test_user_equality():
    lectio = DummyLectio()
    u1 = User(lectio, 1, UserType.STUDENT, lazy=True)
    u2 = User(lectio, 1, UserType.STUDENT, lazy=True)
    u3 = User(lectio, 2, UserType.STUDENT, lazy=True)
    assert u1 == u2
    assert u1 != u3
