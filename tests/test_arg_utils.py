import ghpkgadmin as g


def testArgListOfNonesAllNones():

    # Given
    args = [None, None]

    # When
    res = g._argListOfNonesToNone(args)

    # Then
    assert res is None


def testArgListOfNotAllNones():

    # Given
    args = [None, "t", None]

    # When
    res = g._argListOfNonesToNone(args)

    # Then
    assert res is not None
    assert res == args


def testArgStringNONE():

    # Given
    arg = "__NONE__"

    # When
    res = g._argString(arg)

    # Then
    assert res is None


def testArgStringNone():

    # Given
    arg = None

    # When
    res = g._argString(arg)

    # Then
    assert res is None


def testArgStringnotNone():

    # Given
    arg = "test"

    # When
    res = g._argString(arg)

    # Then
    assert res == "test"


def testArgIsTrue():

    # Given
    arg = "true"

    # When
    res = g._isTrue(arg)

    # Then
    assert res is True


def testArgIsTrueCaseInsensitive():

    # Given
    arg = "TrUe"

    # When
    res = g._isTrue(arg)

    # Then
    assert res is True


def testArgIsFalse():

    # Given
    arg = "false"

    # When
    res = g._isTrue(arg)

    # Then
    assert res is False


def testArgIsFalseCaseInsensitive():

    # Given
    arg = "FalSE"

    # When
    res = g._isTrue(arg)

    # Then
    assert res is False


def testArgIsFalseWhenGarbage():

    # Given
    arg = "foo"

    # When
    res = g._isTrue(arg)

    # Then
    assert res is False


def testArgIsFalseWhenNone():

    # Given
    arg = None

    # When
    res = g._isTrue(arg)

    # Then
    assert res is False


# def testIncludeMatchesAtChildLEvel(itemList):

#     # Given
#     preCount = len(itemList)
#     summary = {}


#     # When
#     result = g._includeFilter(itemList=itemList, include=("children[*]", "a0"), summary=summary)

#     # Then
#     assert len(result) == 1
