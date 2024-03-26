"""
A simple python script that can run a set of GitHub Package Admin functions.
- list packages
- list package versions
- delete package versions
"""
import sys
import argparse
from typing import Optional
from enum import Enum
import requests
import json
import jsonpath_ng
import re

KEY_ORG = "org"
KEY_USER = "user"

API_ROOT = "https://api.github.com"

LIST_PACKAGES_FOR_ORG = API_ROOT + "/orgs/{org}/packages?package_type={package_type}"
LIST_PACKAGES_FOR_USER = API_ROOT + "/users/{username}/packages?package_type={package_type}"

DELETE_PACKAGE_FOR_ORG = API_ROOT + "/orgs/{org}/packages/{package_type}/{package_name}"
DELETE_PACKAGE_FOR_USER = API_ROOT + "/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

LIST_PACKAGE_VERSIONS_FOR_ORG = API_ROOT + "/orgs/{org}/packages/{package_type}/{package_name}/versions"
LIST_PACKAGE_VERSIONS_FOR_USER = API_ROOT + "/users/{username}/packages/{package_type}/{package_name}/versions"

DELETE_PACKAGE_VERSION_FOR_ORG = API_ROOT + "/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}"
DELETE_PACKAGE_VERSION_FOR_USER = API_ROOT + "/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

DEBUG_PRINT = lambda msg: print("DEBUG: "+msg, file=sys.stderr)
INFO_PRINT = lambda msg: print(msg)


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


def _includeFilter(itemList: list[str],
                   include: Optional[tuple[str, str]],
                   summary: dict) -> tuple[list[str], dict]:
    """
    Returns a NEW list of filtered items.
    And the origianl summary dict altered
    """
    assert len(include) == 2, "Include Filter must have 2 values.  (path, regex)"
    includePath = include[0]
    includeRegex = include[1]

    summary["include_filter"] = f"'{includePath}', '{includeRegex}'"

    # Item Path Matcher, and it's matching regex value matcher
    fieldPathExpr = jsonpath_ng.parse(includePath)
    fieldValueExpr = re.compile(includeRegex)

    newItemList = []

    # for each element in the root result model list. Look for a item path/value match
    for item in itemList:

        DEBUG_PRINT("-")
        DEBUG_PRINT(f"Searching: {item}")

        # Find all/any path matches into this item
        fieldPathList = fieldPathExpr.find(item)
        DEBUG_PRINT(f"Found {len(fieldPathList)} values at path'{fieldPathExpr}'")
        for fieldPath in fieldPathList:
            # Grab the value at this path. We go to strings on all, since we're going to regex anyway
            fieldValue = str(fieldPath.value)

            # If we get a value match, add to the new root list, and break this loop
            if fieldValueExpr.match(fieldValue) is not None:
                DEBUG_PRINT(f"Regex '{includeRegex} matches Value '{fieldValue}'. Adding to result list and moving to next item")
                newItemList.append(item)
                DEBUG_PRINT(f'Filter Result List Size [{len(newItemList)}]')
                break

    DEBUG_PRINT(f"Include Filter Result {len(newItemList)}")
    summary["include_filter_result"] = len(newItemList)
    return newItemList, summary


def _excludeFilter(itemList: list[str],
                   exclude: Optional[tuple[str, str]],
                   summary: dict) -> tuple[list[str], dict]:
    """
    Run the exclude filter on the item list
    """
    assert len(exclude) == 2, "Exclude Filter must have 2 values.  (path, regex)"
    excludePath = exclude[0]
    excludeRegex = exclude[1]

    summary["exclude_filter"] = f"'{excludePath}', '{excludeRegex}'"

    # Item Path Matcher, and it's matching regex value matcher
    fieldPathExpr = jsonpath_ng.parse(excludePath)
    fieldValueExpr = re.compile(excludeRegex)

    newItemList = []

    # for each element in the root result model list. Look for a item path/value match
    for item in itemList:

        DEBUG_PRINT("-")
        DEBUG_PRINT(f"Searching: {item}")

        # Find all/any path matches into this item
        fieldPathList = fieldPathExpr.find(item)
        DEBUG_PRINT(f"Found {len(fieldPathList)} values at path'{fieldPathExpr}'")
        if len(fieldPathList) == 0:
            newItemList.append(item)
        else:
            for fieldPath in fieldPathList:
                # Grab the value at this path. We go to strings on all, since we're going to regex anyway
                fieldValue = str(fieldPath.value)

                # If we DON'T get a value match, add to the new root list, and break this loop
                if fieldValueExpr.match(fieldValue) is None:
                    DEBUG_PRINT(f"Regex '{excludeRegex} does NOT matche Value '{fieldValue}'. Adding to result list and moving to next item")
                    newItemList.append(item)
                    DEBUG_PRINT(f'Filter Result List Size [{len(newItemList)}]')
                    break

    DEBUG_PRINT(f"Exclude Filter Result {len(newItemList)}")
    summary["exclude_filter_result"] = len(newItemList)
    return newItemList, summary


def _sortBy(itemList: list[str],
             sortBy: str,
             sortReverse: bool,
             summary: dict) -> tuple[list[str], dict]:
    """
    Run the sort by on the provided list
    """
    summary["sort_by"] = f"'{sortBy}', reverse='{sortReverse}'"

    fieldPathExpr = jsonpath_ng.parse(sortBy)

    newItemList = []  # A list of tuples. [0] is the sorting value. [1] is the item

    # Build a list of tuples, with the desired field value in the [0] of the tuple
    for item in itemList:

        fieldValues = [item.value for item in fieldPathExpr.find(item)]
        fieldValues.sort(reverse=sortReverse)
        fieldValue = (fieldValues or [None])[0]
        newItemList.append( (fieldValue, item) )

    # Sort pushing Nones to the end
    newItemList.sort(key=lambda x: (x[0] is None, x[0]), reverse=sortReverse)

    newItemList = list(map(lambda x: x[1], newItemList))
    return newItemList, summary


def _filterAndSortListResponseJson(jsonData: str,
                                   include: Optional[tuple[str, str]],  # path, regex
                                   exclude: Optional[tuple[str, str]],  # path, regex
                                   sortBy: Optional[str],
                                   sortReverse: Optional[bool],
                                   summary: dict) -> tuple[list[str], dict]:
    """
    Take the raw string json response. This response should contain a root list of items.
    Run the include and exclude filters on it.
    Apply the sorting rule.
    return the result as a json string
    """
    DEBUG_PRINT(f"include filter: {include}")
    DEBUG_PRINT(f"exclude filter: {exclude}")
    DEBUG_PRINT(f"sort by: {sortBy}")

    # Main List Matcher. Find each item from the root list point.
    rootListPathExpr = jsonpath_ng.parse("[*]")
    rootItemList = [item.value for item in rootListPathExpr.find(jsonData)]  # Flatten from a DatumInContext into a simple list
    DEBUG_PRINT(f"Contains {len(rootItemList)} total items")
    summary["initial_items_found"] = len(rootItemList)

    if include:
        rootItemList, summary = _includeFilter(itemList=rootItemList, include=include, summary=summary)

    if exclude:
        rootItemList, summary = _excludeFilter(itemList=rootItemList, exclude=exclude, summary=summary)

    if sortBy:
        rootItemList, summary = _sortBy(itemList=rootItemList, sortBy=sortBy, sortReverse=sortReverse, summary=summary)

    summary["final_items_found"] = len(rootItemList)
    return rootItemList, summary



def _listPackages(ghtoken: str,
                  org: Optional[str],
                  user: Optional[str],
                  packageType: str,
                  include: Optional[tuple[str, str]],
                  exclude: Optional[tuple[str, str]],
                  sortBy: Optional[str],
                  sortReverse: Optional[bool],
                  summarize: bool) -> dict:
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

    DEBUG_PRINT(f"URL -> {url}\n")

    response = requests.get(url, headers=_generateRerquestHeaders(ghtoken))
    response.raise_for_status()
    jsonData = response.json()

    summary = {
        "org": org,
        "user": user,
        "packageType": packageType,
    }
    packageList, summary = _filterAndSortListResponseJson(jsonData=jsonData, include=include, exclude=exclude, sortBy=sortBy, sortReverse=sortReverse, summary=summary)

    if summarize:
        INFO_PRINT(json.dumps(summary, indent=4))
    else:
        INFO_PRINT(json.dumps(packageList, indent=4))


def _listPackageVersions(ghtoken: str,
                         org: Optional[str],
                         user: Optional[str],
                         packageType: str,
                         packageName: str,
                         include: Optional[tuple[str, str]],
                         exclude: Optional[tuple[str, str]],
                         sortBy: Optional[str],
                         sortReverse: Optional[bool],
                         summarize: bool) -> dict:
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

    DEBUG_PRINT(f"URL -> {url}\n")

    response = requests.get(url, headers=_generateRerquestHeaders(ghtoken))
    response.raise_for_status()
    jsonData = response.json()

    summary = {
        "org": org,
        "user": user,
        "packageType": packageType,
        "packageName": packageName
    }

    versionList, summary = _filterAndSortListResponseJson(jsonData=jsonData, include=include, exclude=exclude, sortBy=sortBy, sortReverse=sortReverse, summary=summary)

    if summarize:
        INFO_PRINT(json.dumps(summary, indent=4))
    else:
        INFO_PRINT(json.dumps(versionList, indent=4))


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
                        help='One of the list of known github package types. eg "container"')
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
                        action='store_true',
                        required=False,
                        default=True,
                        help='Delete operations can be dangerous. By default, we dryrun/pretend to do the actual operations.  Set this to False to run any Update/Delete operations.')
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        required=False,
                        default=False,
                        help="Add stderr debug output information")


    args = args = parser.parse_args()

    if not args.debug:
        DEBUG_PRINT = lambda msg: True

    action: ACTION = ACTION(args.action)
    assert action is not None, "Unable to determine requested action from [{args.action}]"


    if action == ACTION.LIST_PACKAGES:
        _listPackages(ghtoken=args.ghtoken,
                      org=args.org,
                      user=args.user,
                      packageType=args.package_type,
                      include=args.include,
                      exclude=args.exclude,
                      sortBy=args.sort_by,
                      sortReverse=bool(args.reverse),
                      summarize=args.summary)

    elif action == ACTION.LIST_PACKAGE_VERSIONS:
        assert args.package_name, f"--package_name is required with --action {ACTION.LIST_PACKAGE_VERSIONS}"
        _listPackageVersions(ghtoken=args.ghtoken,
                             org=args.org,
                             user=args.user,
                             packageType=args.package_type,
                             packageName=args.package_name,
                             include=args.include,
                             exclude=args.exclude,
                             sortBy=args.sort_by,
                             sortReverse=bool(args.reverse),
                             summarize=args.summary)




