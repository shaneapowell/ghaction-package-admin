"""
A simple python script that can run a set of GitHub Package Admin functions.
- list packages
- list package versions
- delete package versions
"""
import sys
import argparse
from typing import Optional, Union, Any
from enum import Enum
import requests
import json
import jsonpath_ng  # type: ignore
import re
from collections import OrderedDict

KEY_ORG = "org"
KEY_USER = "user"

API_ROOT = "https://api.github.com"

# We'll impose a paging limit of 50. GitHub already imposes a limit of 100. And a default of 30
GITHUB_PER_PAGE_LIMIT = 100


LIST_PACKAGES_FOR_ORG = API_ROOT + "/orgs/{org}/packages?package_type={package_type}"
LIST_PACKAGES_FOR_USER = API_ROOT + "/users/{username}/packages?package_type={package_type}"

#DELETE_PACKAGE_FOR_ORG = API_ROOT + "/orgs/{org}/packages/{package_type}/{package_name}"
#DELETE_PACKAGE_FOR_USER = API_ROOT + "/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

LIST_PACKAGE_VERSIONS_FOR_ORG = API_ROOT + "/orgs/{org}/packages/{package_type}/{package_name}/versions"
LIST_PACKAGE_VERSIONS_FOR_USER = API_ROOT + "/users/{username}/packages/{package_type}/{package_name}/versions"

DELETE_PACKAGE_VERSION_FOR_ORG = LIST_PACKAGE_VERSIONS_FOR_ORG + "/{package_version_id}"
DELETE_PACKAGE_VERSION_FOR_USER = LIST_PACKAGE_VERSIONS_FOR_USER + "/{package_version_id}"

PAGING_ARGS = "?per_page={per_page}&page={page}"

_debug = True


def DEBUG_PRINT(msg):
    if _debug:
        print(f"DEBUG: {msg}", file=sys.stderr)


def INFO_PRINT(msg):
    print(msg)


class ACTION(str, Enum):
    LIST_PACKAGES = "listPackages"
    LIST_PACKAGE_VERSIONS = "listPackageVersions"
    DELETE_PACKAGE_VERSIONS = "deletePackageVersions"


def _generateRerquestHeaders(ghtoken: str) -> dict:
    """
    Generate a common basic auth object for all GH interactions
    """
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {ghtoken}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def _findRootIndex(jsonpath: jsonpath_ng.Child | jsonpath_ng.Index | jsonpath_ng.DatumInContext) -> int:
    """
    Given a json path, or path context. find the root index.
    If the root is a list, it'll be the index in that list of this items.
    if the root is a dict/object, return None
    This function is recursive.
    """

    # If we get a datum, pass it's full path recursively into this function
    if type(jsonpath) is jsonpath_ng.DatumInContext:
        return _findRootIndex(jsonpath.full_path)

    # If the child is an Index, we're at the root
    if type(jsonpath) is jsonpath_ng.Index:
        return jsonpath.index

    # If this is a child, navigate left and run this function recursively.
    if type(jsonpath) is jsonpath_ng.Child:
        if jsonpath.left is None:
            raise Exception("Attempt to find root list index, in a non list object")
        else:
            return _findRootIndex(jsonpath.left)

    raise Exception("Attempt to find root list index, found nothing.")


def _includeFilter(itemList: list[dict],
                   include: tuple[str, str],
                   summary: dict) -> tuple[list[dict], dict]:
    """
    Returns a NEW list of filtered items.
    And the origianl summary dict altered
    """
    assert len(include) == 2, "Include Filter must have 2 values.  (jsonpath, regex)"

    includePath = "[*]." + include[0]
    includeRegex = include[1]

    # Item Path Matcher, and it's matching regex value matcher
    fieldPathExpr = jsonpath_ng.parse(includePath)
    fieldValueRegex = re.compile(includeRegex)

    # Needs to be a OrderedDict by rootIndex, so we don't duplicate
    newItemDict: OrderedDict[int, dict] = OrderedDict()

    # Find all/any path matches into this list
    fieldPathList = fieldPathExpr.find(itemList)
    DEBUG_PRINT(f"Found {len(fieldPathList)} value(s) at path '{fieldPathExpr}'")

    # Check each value against the provided value regex
    for fieldPath in fieldPathList:

        fieldValue = str(fieldPath.value)

        # If we get a value match, add to the new root list
        if fieldValueRegex.match(fieldValue) is not None:
            DEBUG_PRINT(f"Regex '{includeRegex} matches Value '{fieldValue}'. Adding to result list")
            rootIndex = _findRootIndex(fieldPath)
            newItemDict[rootIndex] = itemList[rootIndex]

    DEBUG_PRINT(f"Include Filter Result {len(newItemDict)}")
    summary["include_filter_result"] = len(newItemDict)
    return list(newItemDict.values()), summary


def _excludeFilter(itemList: list[dict],
                   exclude: tuple[str, str],
                   summary: dict) -> tuple[list[dict], dict]:
    """
    Run the exclude filter on the item list
    """
    assert len(exclude) == 2, "Exclude Filter must have 2 values.  (jsonpath, regex)"
    excludePath = "[*]." + exclude[0]
    excludeRegex = exclude[1]

    # Item Path Matcher, and it's matching regex value matcher
    fieldPathExpr = jsonpath_ng.parse(excludePath)
    fieldValueExpr = re.compile(excludeRegex)

    newItemList = itemList.copy()
    delItemIndexList: list[int] = []


    # Find all/any path matches into this item
    fieldPathList = fieldPathExpr.find(newItemList)
    DEBUG_PRINT(f"Found {len(fieldPathList)} values at path'{fieldPathExpr}'")
    for fieldPath in fieldPathList:

        fieldValue = str(fieldPath.value)

        # If we get a value match, add to the delete index list. Only if it's not already there
        if fieldValueExpr.match(fieldValue):
            DEBUG_PRINT(f"Regex '{excludeRegex} matches Value '{fieldValue}'. Removing from result list")
            rootIndex = _findRootIndex(fieldPath)
            if rootIndex not in delItemIndexList:
                delItemIndexList.append(rootIndex)

    # Delete our found indexes. In reverse so we don't affect the index lookup in realtime
    for i in sorted(delItemIndexList, reverse=True):
        del newItemList[i]

    DEBUG_PRINT(f"Exclude Filter Result {len(newItemList)}")
    summary["exclude_filter_result"] = len(newItemList)
    return newItemList, summary


def _sortBy(itemList: list[dict],
            sortBy: str,
            sortReverse: bool,
            summary: dict) -> tuple[list[dict], dict]:
    """
    Run the sort by on the provided list
    """

    fieldPathExpr = jsonpath_ng.parse(sortBy)

    newItemList: list[tuple[Any, dict]] = []  # A list of tuples. [0] is the sorting value. [1] is the item

    # Build a list of tuples, with the desired field value in the [0] of the tuple
    for item in itemList:

        fieldValues = [item.value for item in fieldPathExpr.find(item)]
        fieldValues.sort(reverse=sortReverse)
        fieldValue = (fieldValues or [None])[0]
        newItemList.append((fieldValue, item))

    # Sort pushing Nones to the end
    newItemList.sort(key=lambda x: (x[0] is None, x[0]), reverse=sortReverse)

    # Now, extract the list of json values that have been sorted by the typle [0]
    resultList = list(map(lambda x: x[1], newItemList))
    return resultList, summary


def _filterAndSortListResponseJson(itemList: list[dict],
                                   include: Optional[tuple[str, str]],  # path, regex
                                   exclude: Optional[tuple[str, str]],  # path, regex
                                   sortBy: Optional[str],
                                   sortReverse: Optional[bool],
                                   summary: dict) -> tuple[list[dict], dict]:
    """
    Take the raw string json response. This response should contain a root list of items.
    Run the include and exclude filters on it.
    Apply the sorting rule.
    return the result as a json string
    """
    DEBUG_PRINT(f"include filter: {include}")
    DEBUG_PRINT(f"exclude filter: {exclude}")
    DEBUG_PRINT(f"sort by: {sortBy}")

    if include:
        itemList, summary = _includeFilter(itemList=itemList, include=include, summary=summary)

    if exclude:
        itemList, summary = _excludeFilter(itemList=itemList, exclude=exclude, summary=summary)

    if sortBy:
        itemList, summary = _sortBy(itemList=itemList, sortBy=sortBy, sortReverse=bool(sortReverse), summary=summary)

    summary["items_found"] = len(itemList)
    return itemList, summary


def _pagedDataFetch(ghtoken: str,
                    urlWithoutPageParameter: str,
                    totalFetchLimit: int,
                    summary: dict) -> tuple[list, dict]:
    """
    given a PAT token, and a URL, without the 2 paging parameters appended,
    attempt to load all of the data from the URL, up to our max result limit
    if limit is -1 or None. Just do a 1 off fetch, and return the result.
    Otherwise, provide a limit.
    """

    DEBUG_PRINT(urlWithoutPageParameter)
    DEBUG_PRINT(f"limit: {totalFetchLimit}")

    result = []
    page = 1

    while page > 0:

        # Where to get the data
        url = urlWithoutPageParameter

        # Set the page size.  We'll keep adjusting it down to fit the desired result. but 100 is the GH imposed max
        if totalFetchLimit > 0:

            pageArgs = PAGING_ARGS.format(per_page=GITHUB_PER_PAGE_LIMIT, page=page)
            url = url + pageArgs

        DEBUG_PRINT(url)
        response = requests.get(url, headers=_generateRerquestHeaders(ghtoken))
        response.raise_for_status()
        fetched: list = response.json()

        assert type(fetched) is list, f"Fetched Content must be a list. Received {fetched.__class__}"

        fetchCount = len(fetched)
        DEBUG_PRINT(f"Fetched {fetchCount} total items")

        # Add to our return list
        result = result + fetched

        # Stop if there are no more items to fetch. Or if we have a -1 limit for a single fetch
        if totalFetchLimit < 0 or len(fetched) == 0 or len(fetched) < GITHUB_PER_PAGE_LIMIT:
            break

        # Next Page
        page += 1

    # Trim our result incase we exceed our limit
    result = result[:totalFetchLimit]
    summary["items_fetched"] = len(result)

    return result, summary


def _listPackages(summary: dict,
                  ghtoken: str,
                  org: Optional[str],
                  user: Optional[str],
                  packageType: str,
                  fetchLimit: int,
                  include: Optional[tuple[str, str]],
                  exclude: Optional[tuple[str, str]],
                  sortBy: Optional[str],
                  sortReverse: Optional[bool]) -> tuple[list[dict], dict]:
    """
    Get the list of packages, and return the json response
    """
    assert bool(org) != bool(user)
    url = None
    if org:
        url = LIST_PACKAGES_FOR_ORG.format(org=org, package_type=packageType)
    if user:
        url = LIST_PACKAGES_FOR_USER.format(user=user, package_type=packageType)
    assert url is not None, "Failed to generate a valid API url"

    packageList, summary = _pagedDataFetch(ghtoken, url, fetchLimit, summary)
    assert type(packageList) is list
    packageList, summary = _filterAndSortListResponseJson(itemList=packageList, include=include, exclude=exclude, sortBy=sortBy, sortReverse=sortReverse, summary=summary)

    return packageList, summary


def _listPackageVersions(summary: dict,
                         ghtoken: str,
                         org: Optional[str],
                         user: Optional[str],
                         packageType: str,
                         packageName: str,
                         fetchLimit: int,
                         include: Optional[tuple[str, str]],
                         exclude: Optional[tuple[str, str]],
                         sortBy: Optional[str],
                         sortReverse: Optional[bool]) -> tuple[list[dict], dict]:
    """
    Get the list of package versions for the specific package
    """
    assert bool(org) != bool(user)

    url = None
    if org:
        url = LIST_PACKAGE_VERSIONS_FOR_ORG.format(org=org, package_type=packageType, package_name=packageName)
    if user:
        url = LIST_PACKAGE_VERSIONS_FOR_USER.format(user=user, package_type=packageType, package_name=packageName)
    assert url is not None, "Failed to generate a valid API url"

    versionList, summary = _pagedDataFetch(ghtoken, url, fetchLimit, summary)
    assert type(versionList) is list, f"fetched data returned an unexpected type [{type(versionList)}]"
    versionList, summary = _filterAndSortListResponseJson(itemList=versionList, include=include, exclude=exclude, sortBy=sortBy, sortReverse=sortReverse, summary=summary)

    return versionList, summary

def _deletePackageVersions(summary: dict,
                           itemList: list[dict],
                           ghtoken: str,
                           org: Optional[str],
                           user: Optional[str],
                           packageType: str,
                           packageName: str,
                           dryrun: bool) -> tuple[list[dict], dict]:
    """
    Delete the packages identified by the provided item list.
    """

    assert bool(org) != bool(user)
    url = None

    INFO_PRINT(f"Deleting {len(itemList)} package version(s)")

    deleteCount = 0
    for index, item in enumerate(itemList):
        id = item["id"]
        if id is not None:
            deleteCount += 1
            INFO_PRINT(f"Deleting [{index+1}/{len(itemList)}] - id:{id}")

            if org:
                url = DELETE_PACKAGE_VERSION_FOR_ORG.format(org=org, package_type=packageType, package_name=packageName, package_version_id=id)
            if user:
                url = DELETE_PACKAGE_VERSION_FOR_USER.format(user=user, package_type=packageType, package_name=packageName, package_version_id=id)

            assert url is not None, "Failed to generate a valid API url"

            DEBUG_PRINT(url)
            if not dryrun:
                response = requests.delete(url, headers=_generateRerquestHeaders(ghtoken))
                response.raise_for_status()
                if response.status_code == 204:
                    INFO_PRINT("Ok")
                else:
                    INFO_PRINT(f"Fail [{response.status_code}]")
            else:
                INFO_PRINT("Ok[dryrun]")

        else:
            INFO_PRINT(f"Skipping {index+1} of {len(itemList)} id not found")

    summary['deleted'] = len(itemList)

    return itemList, summary

# ***************************************
# MAIN
# ***************************************

if __name__ == '__main__':
    """
    Main Entry Point
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--action',
                        dest='action',
                        type=str,
                        required=True,
                        choices=list(map(lambda a: a.value, ACTION)),
                        help='What action to run. This is the required main entry branching point.  Different commands result in different output types.')
    parser.add_argument('--ghtoken',
                        dest='ghtoken',
                        type=str,
                        required=True,
                        help='The GitHub Token (PAT) used to access the API.')
    orgUserGroup = parser.add_mutually_exclusive_group(required=True)
    orgUserGroup.add_argument('--org',
                              dest='org',
                              type=str,
                              required=False,
                              help='The Organization Name if dealign with org owned packages')
    orgUserGroup.add_argument('--user',
                              dest='user',
                              type=str,
                              required=False,
                              help='The User Name if dealign with User owned packages')
    parser.add_argument('--package_type',
                        dest='package_type',
                        type=str,
                        required=True,
                        choices=["npm", "maven", "rubygems", "docker", "nuget", "container"],
                        help='One of the list of known github package types. eg "container, npm, docker..."')
    parser.add_argument('--package_name',
                        dest='package_name',
                        type=str,
                        required=False,
                        help='The Package Name')
    parser.add_argument('--package_version_id',
                        dest='package_version_id',
                        type=str,
                        required=False,
                        help='The package version ID to operate on')
    parser.add_argument('--fetch_limit',
                        dest='fetch_limit',
                        required=False,
                        default=1000,
                        type=int,
                        help="Fetching from the GH API is limited to 1000 records at a time.  Increase this with caution.")
    parser.add_argument('--include',
                        dest='include',
                        required=False,
                        default=None,
                        nargs=2,
                        help="Include regex field matches")
    parser.add_argument('--exclude',
                        dest='exclude',
                        required=False,
                        default=None,
                        nargs=2,
                        help="Exclude regex field matches")
    parser.add_argument('--sort_by',
                        dest='sort_by',
                        required=False,
                        default=None,
                        help="Sort by a field")
    parser.add_argument('--reverse',
                        dest='reverse',
                        action='store_true',
                        required=False,
                        default=False,
                        help="Reverse the Sort by. Ignored with no --sort_by provided")
    parser.add_argument('--summary',
                        dest='summary',
                        action='store_true',
                        required=False,
                        default=False,
                        help="Don't output the raw json data, instead just summarize the actions")
    parser.add_argument('--dryrun',
                        dest='dryrun',
                        type=str,
                        required=False,
                        default=str(True).lower(),
                        choices=[str(True).lower(), str(False).lower()],
                        help='Delete operations can be dangerous. By default, we dryrun/pretend to do the actual operations.  Set this to False to run any Update/Delete operations.')
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        required=False,
                        default=False,
                        help="Add stderr debug output information")


    args = args = parser.parse_args()

    _debug = args.debug

    action: ACTION = ACTION(args.action)
    assert action is not None, "Unable to determine requested action from [{args.action}]"

    assert args.fetch_limit > 10 and args.fetch_limit < 999999, "--fetch_limit must be between 10 and 999999"

    summary = vars(args).copy()
    summary['ghtoken'] = "***"
    summary = {"args": summary }

    printSummary = args.summary
    printResult = not printSummary

    if action == ACTION.LIST_PACKAGES:
        result, summary = _listPackages(summary=summary,
                                        ghtoken=args.ghtoken,
                                        org=args.org,
                                        user=args.user,
                                        packageType=args.package_type,
                                        fetchLimit=args.fetch_limit,
                                        include=args.include,
                                        exclude=args.exclude,
                                        sortBy=args.sort_by,
                                        sortReverse=bool(args.reverse))

    if action in [ACTION.LIST_PACKAGE_VERSIONS, ACTION.DELETE_PACKAGE_VERSIONS]:
        assert args.package_name, f"--package_name is required with --action {args.package_name}"
        result, summary = _listPackageVersions(summary=summary,
                                               ghtoken=args.ghtoken,
                                               org=args.org,
                                               user=args.user,
                                               packageType=args.package_type,
                                               packageName=args.package_name,
                                               fetchLimit=args.fetch_limit,
                                               include=args.include,
                                               exclude=args.exclude,
                                               sortBy=args.sort_by,
                                               sortReverse=bool(args.reverse))

    if action == ACTION.DELETE_PACKAGE_VERSIONS:
        assert result is not None and type(result) is list
        printSummary = True
        printResult = False
        result, summary = _deletePackageVersions(summary=summary,
                                                 itemList=result,
                                                 ghtoken=args.ghtoken,
                                                 org=args.org,
                                                 user=args.user,
                                                 packageType=args.package_type,
                                                 packageName=args.package_name,
                                                 dryrun="true" in str(args.dryrun).lower())

    if printSummary:
        INFO_PRINT(json.dumps(summary, indent=4))

    if printResult:
        INFO_PRINT(json.dumps(result, indent=4))