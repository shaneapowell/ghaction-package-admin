
![DEVELOP](https://github.com/shaneapowell/ghaction-package-admin/actions/workflows/DEVELOP.yml/badge.svg)
![RELEASE](https://github.com/shaneapowell/ghaction-package-admin/actions/workflows/RELEASE.yml/badge.svg)
![Example](https://github.com/shaneapowell/ghaction-package-admin/actions/workflows/cleanup_packages.yml/badge.svg)

### This action provides flexible administration to your GitHub packages.

# Features
- Query/List/summarize all packages
- Query/List/summarize all package versions
- filter package and version lists by any value in the result json.
- Both `include` and `exclude` filtering
- Sort by any value in the result json.
- full regex matching capabilities
- result-set slicing [python list slicing](https://www.geeksforgeeks.org/python-list-slicing/)
- **Delete Package Versions**

# Future/Planned Options
- return the summary json back to the `output` option of the Action.
- extract a specific value from the json response into the `output` option of the Action.
- Better Feedback of processing during a long running operation.

# The GitHub Action
See the **`Common Tasks`** section below for a few useful examples.
```yml
- name: Org owned packages
      uses: shaneapowell/ghaction-package-admin@v0
      with:
        ghtoken: ${{ github.token }}
        operation: deletePackageVersions
        org: ${{ github.repository_owner }}
        package_type: container
        package_name: <your package name>
        include: metadata.container.tags[*]   .*-latest
        exclude: metadata.container.tags[*]   .*-develop
        sort_by: updated_at
        revese: false
        summary: true
        debug: false
        slice: 5 __NONE__
        dryrun: ${{ inputs.dryrun }}

- name: User owned packages
      uses: shaneapowell/ghaction-package-admin@v0
      with:
        ghtoken: ${{ github.token }}
        operation: deletePackageVersions
        user: ${{ github.repository_owner }}
        package_type: container
        package_name: <your package name>
        include: metadata.container.tags[*]   .*-latest
        exclude: metadata.container.tags[*]   .*-develop
        sort_by: updated_at
        revese: false
        summary: true
        debug: false
        slice: 5 __NONE__
        dryrun: ${{ inputs.dryrun }}
```

# Options
`__NONE__` is a special string that is used to pass in a blank/null as a parameter value. From the command line, you can simply leave off the option, and it will be ignored. This special string provides a means for the yml based action to be able to pass through all expected parameters, and still allow for a parameter to specifically ignored.  In other cases, it might be needed to pass a `null/None` value to an option.  This is especially true in the use of the `--slice` option.

## `--operation [string]` *required
Takes a single value.  The operation to perform. Must be one of the following strings. More options To be added in future releases.
- `listPackages` - Lists the packages owned by the given user/org.
- `listPackageVersions` - Lists the package versions owned by the given user/org.
    - must also provide `--package_name` option.
- `deletePackageVersions` - Given the result of the filters and sort, delete the found items.
    - must also provide `--package_name` option.

## `--ghtoken [string]` *required
The `PAT` GitHub token.  The permissions of that token must be sufficient to perform the actions in question.  see the FAQ for examples of errors and possible solutions.

## `--org [string]` *required or --user
If this is an Organization owned package. Provide this `--org` and do NOT provide the `--user` option.

## `--user [string]` *required or --org
If this is an User owned package. Provide the `--user` and do NOT provide the `--org` option.

## `--package_type [string]` *required
One of the GitHub package type codes.  If you are using ghcr.io, you'll want to use the `container` type.

See [list packages for an organization](https://docs.github.com/en/rest/packages/packages?apiVersion=2022-11-28#list-packages-for-an-organization) for all github types

- `npm`
- `maven`
- `rubygems`
- `docker`
- `nuget`
- `container`

## `--package_name [string]` *required
The name of your package.

## `--include [json-path] [regex]`
The filter to include records in the result list.  see **`Include/Exclude Filters`** section below.
This filter will find matches in the result set and keep them in the list. Removing those that don't match.

An include filter is made up of 2 string values.  a `json-path` and a `regex` separated by white space.
```
--include metadata.container.tag[*]  develop-.*
```
```
--include created_at  2024-03-.*
```

## `--exclude [json-path] [regex]`
Same as the `--include` filters, except this filter excludes it's matches.  You can combine `--include` and `--exclude` in a single run.
```
--exclude metadata.container.tag[*]   latest
```
```
--exclude metadata.container.tag[*]   .+-latest
```
```
--exclude metadata.container.tag[*]  v1.*
```

## `--sort_by [json-path]`
Sort the result set by the given `json-path` identified field.  The default is a natural string sort of the values in this field.  Sorting is done after filtering is complete.

```
--sort_by updated_at
```

```
--sort_by metadata.package_type
```

```
--sort_by id
```

## `--reverse [boolean]` *default=false
Reverse the `sort_by` result. `true` or `false`
```
--reverse true
```

## `--slice [int] [int]`
Perform a python list [`slice`](https://www.geeksforgeeks.org/python-list-slicing/) operation on the result set after the above `--include`, `--exclude` and `--sort_by` operations are done.  The 2 int values are applied on either side of the normal python slice syntax `[int:int]`.  These 2 values are expected to be integer values, but also can be the special string `__NONE__` to specify a blank option in the slice.

### Examples:
These parameter examples show how they are used to generate the python Slice operation.
- Strip off the 1st 3 items in the list == `[3:]`
```
--slice 3 __NONE__
```
- Strip off the tail 4 items in the list == `[:-4]`
```
--slice __NONE__ -4
```
- Keep only the last 2 items in the list == `[-2:]`
```
--slice -2 __NONE__
```
- Skip the first 5 and take the next 10 only == `[5:15]`
```
--slice 5 15
```
- Strip off the first and last items == `[1:-1]`
```
--slice 1 -1
```

## `--summary [boolean]`  *default is operation specific
When the operation selected is one of the `list` operations, set this option to true to generate a summary json output instead of the list of results output.  This option is defaulted to `true` when any of the `delete` operations are selected.
- listPackages `default=false`
- listPackageVersions `default=false`
- deletePackageVersions `default=true`
```
--summary true
```

## `--debug  [boolean]` *default=false
Set to `true` to generate a considerable amount of additional debugging log outputs.  Helps when there are unknown reasons for unexpected results
```
--debug true
```

## `--dryrun [boolean]`  *default=true
This option only affects any of the destructive operations.  `true` by default, this allows you to test any of the `delete` operations expected results.   Set this to `false` to actually execute the `delete` operation.  Be careful when enabling this option.
```
--dryrun false
```

## `--fetch_limit [int]`  *default=1000
Limit the **before-filtering** initial fetching total from the github api to this maximum total amount. The GitHub api uses a paging mechanism to fetch all data. The github imposed limit is 100 records at a time per page.  To prevent an accidental over-load of fetching, this utility has a default total initial fetch limit of `1000` records.  You can artificially limit this to a shorter amount for batching or testing purposes.  Or, you can increase it, at your own risk.

Important not here, this limit is imposed BEFORE any filtering or sorting is done.  This simply limits the data loaded that is then to be processed by the filters and sorting of this utility.
```
--fetch_limit 10
```

```
--fetch_limit 50
```

# Order of Operations
When this action runs, the various options run in a particular order.  Allowing for predictable results.
1. fetch all records in default order from GitHub. Up to the default maximum 1000 `--fetch_limit`
2. stop fetch once the optional `--fetch_limit` is reached.
3. apply the `--include` filter.
4. apply the `--exclude` filter.
5. apply the `--sort` and `--reverse` operation.
6. excute the operation on the final list

# Option Value Types

## `string`
A standard `string` value to be passed in.  No need to wrap in `""` quotes.

## `int`
A standard `int` value.

## `boolean`
A string value, one of `true` or `false`.

## `json-path`
This is a string that represents the [`json-path`](https://github.com/h2non/jsonpath-ng/) to a value in the data results.  This action uses the [`jsonpath-ng`](https://github.com/h2non/jsonpath-ng/) library to reference a value in the json api results.

## `regex`
a standard python `regex` string.  [Online regex testers](https://regex101.com/) help a great deal in designing a good `regex` for your needs.  This action uses the standard python [`re` package](https://docs.python.org/3/howto/regex.html)

## `__NONE__`
A special values that signifies a blank/empty/null/None value

# Include/Exclude Filters
The power of this action is in it's ability to filter by any value within the api response that suites your needs.  You are also not limited to `--include`, but can also use `--exclude` at the same time.

Both the `--include` and `--exclude` options take 2 parameters.  With the 1st being a `json-path` to a data field in the response list.  The second parameter is a `regex` string used to match with the content at the `json-path` provided.

Rather than have this action define a set of filter criteria for you to chose from, instead I went with allowing you to define the filter to fit your needs.  With this great power, comes great responsibility!

First you will need to understand the response format of the json returned by the `--operation`.  This `json` response is needed to build a [`json-path`](https://github.com/h2non/jsonpath-ng/) to fit your filter needs.  See [sample json responses](docs/sample_json.md), or run one of the list `--operations` with `--fetch_limit 10` to see what fields are in the response json.

Once you know the field you wish to filter by, you must now define a `regex` string to match the field value to suite your filter needs.

Finally, you must decide if the result you want will `--include` or `--exclude` objects that match the filter parameters.  Or, a combination of both together.

## json-path options
 The response json from the api come in one of 2 forms. Either a single object, or a list of objects.   The `listPacakges` and `listPackageVersions` operations both return lists of objects.  The json path to this list automaticaly includes the leading `[*]` of the `json-path`

 The `json-path` format generally takes the form of a dot-notation between model objects within the json.
 ```json
 { "id": 1, "name": "foo", "sub": { "subid": "A", "name": "bar" } }
 ```
 To reference the `"bar"` value at the sub models `"name"` field, you need simply `sub.name`

## regex options
Explaining Regex matching here is beyond the scope of this readme.  You must test various regex strings to be sure you get teh response you expect, without making false positive matches for things you mean to avoid.

# Common `json-path` values
## container tags from `listPackageVersions`
Container tags are kept within a sub-model of each versions json model.  The container tags are contained within an array/list of strings.   You must include the trailing `[*]` to have the filters match all tags.  if you leave the trailing `[*]` off, the regex will attempt to match against the resulting list, which will not work as expected.
- `metadata.container.tags[*]` == All tags (this is the normal scenario)
- `metadata.container.tags[0]` == Only the 1st tag (I would not use this, no guarantee of the order the tags are stored in the list)

## created timestamp
Both package and package version models include a root model level `created_at` timestamp in an ISO8601 format.
- `created_at`

## updated timestamp
Like the created timestamp, both package and version models include a root model level `updated_at` timestamp in ISO8601 format.
- `updated_at`

## package or version id
Both packages and package versions have a unique ID at the root model.
- `id`

# Common Tasks
Provided here is a set of somewhat common package administration tasks. Each task listed provides a command line (CLI) version, the Action version, and a local Docker run version.

You can also reference this [task in action here in this repo](https://github.com/shaneapowell/ghaction-package-admin/blob/develop/.github/workflows/cleanup_packages.yml).

## Report on package versions where the tag contains a value
Use a `--include` filter matching your tag.  Include the `--summary` flag to create a simple json output.  For example, if you want to report on all package versions with `-latest` at the end of any tags. Such as tags with `develop-latest` and `v1-latest`.
### CLI
```sh
pipenv run ghpkadmin --operation listPackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --include "metadata.container.tags[*]" ".+-latest" --summary
```
### Action
```yaml
- name: List Packages with tag
    uses: shaneapowell/ghaction-package-admin@v1
    with:
      operation: listPackageVersions
      ghtoken: ${{ github.token }}
      org: ${{ github.repository_owner }}
      page_type: container
      package_name: <name>
      include: metadata.container.tags[*]"  .+-latest
      summary: true
```
### Docker
```sh
docker run --name ghpkgadmin --rm ghcr.io/shaneapowell/ghaction-package-admin:v1 --operation listPackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --include "metadata.container.tags[*]" ".*-latest" --summary
```

## Delete all container packages without a tag
Use the `--exclude` filter matching any that include any value in the tags. In other words, only return versions that do NOT have a value in the tags list.
- `"metadata.container.tags[*]"` -> Finds the values of all tags
- `".+"` -> Matches to any content within any tag. You could also use `".*"` since the tags are held within a list of strings.

### CLI
```sh
pipenv run ghpkadmin --operation deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".+"
```
### Action
```yaml
- name: Delete Packages without Tags
    uses: shaneapowell/ghaction-package-admin@v1
    with:
      operation: deletePackageVersions
      ghtoken: ${{ github.token }}
      org: ${{ github.repository_owner }}
      page_type: container
      package_name: <name>
      exclude: metadata.contaienr.tags[*]   .+
```

### Docker
```sh
docker container run --name ghpkgadmin --rm ghcr.io/shaneapowell/ghaction-package-admin:v1  --operation deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".*"
```

## Keep only the most recent 5 containers with specific format tag.
Lets include only versions with `DEVELOP-`.  And lets also make sure to avoid any versions with `-latest` anywhere in the tag.
- Use the `--include` filter to find only the versions that have `develop-`
- Lets use the regex `(?i)` to make the filter case-insensitive.  Matching `develop` and `Develop` and `DEVELOP`
- Use the `--exclude` filter to avoid tags we find with `-latest` in the text.
- Sort the result by either `created_at` or `updated_at` timestamps in reverse order **youngest at the top**.
- Slice the result to skip the first 5.
### CLI
```sh
pipenv run ghpkadmin --operation deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --include "metadata.container.tags[*]" "(?i)DEVELOP-.*" --exclude "metadata.container.tags[*]  .*-latest --sort updated_at --reverse --slice 5 __NONE__
```
### Action
```yaml
- name: Delete all but the most recent packages for a tag (case insensitive).
    uses: shaneapowell/ghaction-package-admin@v1
    with:
      operation: deletePackageVersions
      ghtoken: ${{ github.token }}
      user: ${{ github.repository_owner }}
      page_type: container
      package_name: <name>
      include: metadata.container.tags[*]"  (?i)DEVELOP-.*
      exclude: metadata.contaienr.tags[*]"  .*-latest
      sort: "updated_at"
      reverse: true
      slice: 5  __NONE__
```


# FAQ

# How can I try/test the operation locally?
The above common tasks examples include the `action` syntax, a `cli` syntax, and a `docker run` syntax.  You can reference the [developer](docs/developer.md) doc for some more help in how to try the `cli` or `docker` examples on your local machine.

# Why does it take so long for the delete operation to run?
The delete operation is done 1 record at a time.  Each operation itself takes a few seconds to complete. If you are trying to clean out hundreds of records at once, this WILL take quite some time to complete.  You might want to run in batches by specifying the `--slice 20 __NONE__` option to only delete 20 at a time.  Or the `--fetch_limit` option.  You might need to run your delete operation locally in batches to widdle down your list.

## How do I know what fields are available to use in the `json-path` for my filter?
See the list of [sample json responses](docs/sample_json.md) for reference.
Or, run one of the `--operation` commands to list the contents, using the `--fetch_limit 10` to simply return the first 10 records and stop.

## None of my delete operations actually delete anything?
By default the `--dryrun` flag is set to `True`.  You MUST explicitly turn it off with
```--dryrun false```

## I get a `401` Client Error
Typically caused by your `PAT` token not having the necessary authorization permissions to perform the operation.

## I get a `404` error when I try to delete any package versions?
99% of the time, this is a permissions issue. Ensure the user account tied to your github token, has `admin` rights on the package in question.

## I get a `422 Client Error`
This could very well be a bug in this action.  If you receive one of these errors, please submit an `issue` with debugging output enabled to assist with resolving the problem.
