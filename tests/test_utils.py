from datetime import date

from swiss_school_holidays.utils import overlap_period


def test_overlap_period_returns_overlap():
    a_start = date(2023, 1, 1)
    a_end = date(2023, 1, 10)
    b_start = date(2023, 1, 5)
    b_end = date(2023, 1, 15)

    assert overlap_period(a_start, a_end, b_start, b_end) == (
        date(2023, 1, 5),
        date(2023, 1, 10),
    )


def test_overlap_period_no_overlap():
    a_start = date(2023, 1, 1)
    a_end = date(2023, 1, 5)
    b_start = date(2023, 1, 6)
    b_end = date(2023, 1, 10)

    assert overlap_period(a_start, a_end, b_start, b_end) is None

