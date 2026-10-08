import pytest

from mangafire.requests import (
    InvalidSelectionError,
    parse_selections,
)


def test_parse_single_selection():
    assert parse_selections("1") == (
        (1.0, 1.0),
    )


def test_parse_multiple_selections_with_commas():
    assert parse_selections("1, 6, 12") == (
        (1.0, 1.0),
        (6.0, 6.0),
        (12.0, 12.0),
    )


def test_parse_multiple_selections_with_semicolons():
    assert parse_selections("1; 6; 12") == (
        (1.0, 1.0),
        (6.0, 6.0),
        (12.0, 12.0),
    )


def test_parse_range_selection():
    assert parse_selections("1-12") == (
        (1.0, 12.0),
    )


def test_parse_decimal_selection():
    assert parse_selections("636.5") == (
        (636.5, 636.5),
    )


def test_parse_mixed_selections():
    assert parse_selections(
        "1-5, 8, 12-15, 636.5"
    ) == (
        (1.0, 5.0),
        (8.0, 8.0),
        (12.0, 15.0),
        (636.5, 636.5),
    )


def test_parse_selection_with_spaces():
    assert parse_selections(
        " 1 - 5 , 8 , 636.5 "
    ) == (
        (1.0, 5.0),
        (8.0, 8.0),
        (636.5, 636.5),
    )


def test_parse_empty_selection():
    with pytest.raises(InvalidSelectionError):
        parse_selections("")


def test_parse_whitespace_only_selection():
    with pytest.raises(InvalidSelectionError):
        parse_selections("   ")


def test_parse_invalid_selection():
    with pytest.raises(InvalidSelectionError):
        parse_selections("abc")


def test_parse_invalid_range():
    with pytest.raises(InvalidSelectionError):
        parse_selections("12-1")


def test_parse_incomplete_range():
    with pytest.raises(InvalidSelectionError):
        parse_selections("1-")


def test_parse_empty_item():
    with pytest.raises(InvalidSelectionError):
        parse_selections("1,,3")


def test_parse_multiple_hyphens():
    with pytest.raises(InvalidSelectionError):
        parse_selections("1-2-3")