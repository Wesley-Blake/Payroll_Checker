from helpers.weekend_overtime import weekend_overtime

def test_return_dict():
    assert isinstance(weekend_overtime(""),dict)