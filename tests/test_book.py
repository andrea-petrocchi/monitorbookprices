"""Test functions related to books, schemas, etc."""

import pytest

import monitorbookprices as mbp


def test_schema():
    """Test generated schema."""
    schema = mbp.schema()
    book_info = mbp.book_info()
    list_sites = mbp.list_sites()
    required_info = book_info + list_sites
    assert all([x in schema for x in required_info])
    assert all([x in required_info for x in schema])


def test_isbn():
    """Test checks on isbn."""
    book_1 = {'isbn': 'bad_isbn'}
    with pytest.raises(ValueError):
        mbp.new_book(book_1)
    book_2 = {'title': 'no_isbn'}
    with pytest.raises(ValueError):
        mbp.new_book(book_2)


def test_fill():
    """Test filling function."""
    book = {'isbn': '1234567890123'}
    book_filled_1 = mbp.new_book(book)
    schema = mbp.schema()
    assert all([x in book_filled_1.keys() for x in schema])
    book_filled_2 = mbp.fill_book_schema(**book)
    assert all([x in book_filled_2.keys() for x in schema])
