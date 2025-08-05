from swiss_school_holidays import get_school_holidays


def test_get_school_holidays_known_zip():
    holidays = get_school_holidays("2023-04-01", "2023-05-31", "8914")

    assert "8914" in holidays
    assert {
        "type": "spring",
        "start": "2023-04-22",
        "end": "2023-05-07",
    } in holidays["8914"]

