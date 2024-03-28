import pytest
# from unittest.mock import Mock
import ghpkgadmin as g
import json



@pytest.fixture
def itemList():
    itemList = [
        json.loads('{"id": 0, "name": "one", "children": [{"id": "a0"},{"id":"a1"}] }'),
        json.loads('{"id": 1, "name": "two", "children": [{"id": "b0"},{"id":"b1"}] }'),
        json.loads('{"id": 2, "name": "three", "children": [{"id": "c0"},{"id":"c1"}] }'),
        json.loads('{"id": 3, "name": "four", "children": [{"id": "d0"},{"id":"d1"}] }'),
    ]
    yield itemList



def testIncludeSimpleMatcheAll(itemList):

    # Given
    summary = {}

    # When
    result, summary = g._includeFilter(itemList=itemList, include=('name', '.*'), summary=summary)

    # Then
    # assert type(result) is list
    assert len(result) == 4


# def testIncludeMatchesAtChildLEvel(itemList):

#     # Given
#     preCount = len(itemList)
#     summary = {}


#     # When
#     result = g._includeFilter(itemList=itemList, include=("children[*]", "a0"), summary=summary)

#     # Then
#     assert len(result) == 1
