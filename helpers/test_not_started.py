from pathlib import Path
from not_started import not_started_list

class test_not_started_list:
    not_started_csv = Path.home().parent
    def test_not_started_list(self):
        result = not_started_list(not_started_csv)
        assert result == {'manager1@mail.com':['1@mail.com','2@mail.com']}
