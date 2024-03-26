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
    LIST_PACKAGE_VERSION = "listPackageVersions"


def _generateRerquestHeaders(ghtoken: str) -> dict:
    """
    Generate a common basic auth object for all GH interactions
    """
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {ghtoken}",
        "X-GitHub-Api-Version": "2022-11-28"
    }


def _filterAndSortListResponseJson(jsonData: str,
                                   include: Optional[tuple[str, str]],
                                   exclude: Optional[tuple[str, str]],
                                   summary: dict) -> str:
    """
    Take the raw string json response. This response should contain a root list of items.
    Run the include and exclude filters on it.
    Apply the sorting rule.
    return the result
    """
    DEBUG_PRINT(f"include filter: {include}")
    DEBUG_PRINT(f"exclude filter: {exclude}")

    # Main List Matcher. Find each item from the root list point.
    rootListPathExpr = jsonpath_ng.parse("[*]")
    rootItemList = [item.value for item in rootListPathExpr.find(jsonData)]  # Flatten from a DatumInContext into a simple list
    DEBUG_PRINT(f"Contains {len(rootItemList)} total items")
    summary["items_found"] = len(rootItemList)

    # Inclusion Regex Matching on a give ()
    if include:
        assert len(include) == 2, "Include Filter must have 2 values.  (path, regex)"
        includePath = include[0]
        includeRegex = include[1]

        summary["include_filter"] = f"'{includePath}', '{includeRegex}'"

        # Item Path Matcher, and it's matching regex value matcher
        itemPathExpr = jsonpath_ng.parse(includePath)
        itemValueExpr = re.compile(includeRegex)

        newRootItemList = []

        # for each element in the root result model list. Look for a item path/value match
        for rootItem in rootItemList:
            rootItemValue = rootItem
            DEBUG_PRINT("-")
            DEBUG_PRINT(f"Searching: {rootItemValue}")

            # Find all/any path matches into this item
            itemPathList = itemPathExpr.find(rootItemValue)
            DEBUG_PRINT(f"Found {len(itemPathList)} values at path'{itemPathExpr}'")
            for itemPath in itemPathList:
                # Grab the value at this path. We go to strings on all, since we're going to regex anyway
                itemPathValue = str(itemPath.value)

                # If we get a value match, add to the new root list, and break this loop
                if itemValueExpr.match(itemPathValue) is not None:
                    DEBUG_PRINT(f"Regex '{includeRegex} matches Value '{itemPathValue}'. Adding to result list and moving to next item")
                    newRootItemList.append(rootItemValue)
                    DEBUG_PRINT(f'Filter Result List Size [{len(newRootItemList)}]')
                    break

        DEBUG_PRINT(f"Include Filter Result {len(newRootItemList)}")
        summary["include_filter_result"] = len(newRootItemList)
        rootItemList = newRootItemList


    # Inclusion Regex Matching on a give ()
    if exclude:
        assert len(exclude) == 2, "Exclude Filter must have 2 values.  (path, regex)"
        excludePath = exclude[0]
        excludeRegex = exclude[1]

        summary["exclude_filter"] = f"'{excludePath}', '{excludeRegex}'"

        # Item Path Matcher, and it's matching regex value matcher
        itemPathExpr = jsonpath_ng.parse(excludePath)
        itemValueExpr = re.compile(excludeRegex)

        newRootItemList = []

        # for each element in the root result model list. Look for a item path/value match
        for rootItem in rootItemList:
            rootItemValue = rootItem
            DEBUG_PRINT("-")
            DEBUG_PRINT(f"Searching: {rootItemValue}")

            # Find all/any path matches into this item
            itemPathList = itemPathExpr.find(rootItemValue)
            DEBUG_PRINT(f"Found {len(itemPathList)} values at path'{itemPathExpr}'")
            if len(itemPathList) == 0:
                newRootItemList.append(rootItemValue)
            else:
                for itemPath in itemPathList:
                    # Grab the value at this path. We go to strings on all, since we're going to regex anyway
                    itemPathValue = str(itemPath.value)

                    # If we DON'T get a value match, add to the new root list, and break this loop
                    if itemValueExpr.match(itemPathValue) is None:
                        DEBUG_PRINT(f"Regex '{excludeRegex} does NOT matche Value '{itemPathValue}'. Adding to result list and moving to next item")
                        newRootItemList.append(rootItemValue)
                        DEBUG_PRINT(f'Filter Result List Size [{len(newRootItemList)}]')
                        break

        DEBUG_PRINT(f"Exclude Filter Result {len(newRootItemList)}")
        summary["exclude_filter_result"] = len(newRootItemList)
        rootItemList = newRootItemList

    return jsonData



def _listPackages(ghtoken: str,
                  org: Optional[str],
                  user: Optional[str],
                  packageType: str,
                  include: Optional[tuple[str, str]],
                  exclude: Optional[tuple[str, str]],
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
    jsonData = _filterAndSortListResponseJson(jsonData=jsonData, include=include, exclude=exclude, summary=summary)

    if summarize:
        INFO_PRINT(json.dumps(summary, indent=4))
    else:
        INFO_PRINT(json.dumps(jsonData, indent=4))


def _listPackageVersions(ghtoken: str,
                         org: Optional[str],
                         user: Optional[str],
                         packageType: str,
                         packageName: str,
                         include: Optional[tuple[str, str]],
                         exclude: Optional[tuple[str, str]],
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

    jsonData = _filterAndSortListResponseJson(jsonData=jsonData, include=include, exclude=exclude, summary=summary)

    if summarize:
        INFO_PRINT(json.dumps(summary, indent=4))
    else:
        INFO_PRINT(json.dumps(jsonData, indent=4))


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
                      summarize=args.summary)

    elif action == ACTION.LIST_PACKAGE_VERSION:
        assert args.package_name, f"--package_name is required with --action {ACTION.LIST_PACKAGE_VERSION}"
        _listPackageVersions(ghtoken=args.ghtoken,
                             org=args.org,
                             user=args.user,
                             packageType=args.package_type,
                             packageName=args.package_name,
                             include=args.include,
                             exclude=args.exclude,
                             summarize=args.summary)




