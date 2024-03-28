# WorkInProgress. NOT READY YET. Check back soon.
![warning](https://cdn-icons-png.freepik.com/256/9668/9668941.png)
--

# The GitHub Action
Each command line parameter is provided by the action.   There is a direct 1:1 mapping of each.


## Order of Operations
1. fetch all records in default order from GitHub.
2. stop fetch once the optional `--fetch_limit` is reached.
3. apply the `--include` filter.
4. apply the `--exclude` filter.
5. apply the `--sort` and `--reverse` operation.
6. excute the operation on the final list

# Common Tasks

## Report on packages with a given tag format
Use a `--include` filter matching your tag.  Include the `--summary` flag to create a simple json output.  For example, if you want to report on all package versions with `-latest` at the end of any tags. Such as tags with `develop-latest` and `v1-latest`.
### CLI
```sh
pipenv run ghpkadmin --action listPackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".*-latest" --summary
```
### Action
```yaml
- name: Delete Packages without Tags
    uses: shaneapowell/ghaction-package-admin@v0
    with:
      action: listPackageVersions
      ghtoken: <token>
      org: <your org>
      page_type: container
      package_name: <name>
      include:
        - "metadata.contaienr.tags[*]"
        - ".*-latest"
      summary: true
```
### Docker
```sh
pipenv run ghpkadmin --action listPackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".*-latest" --summary
```

## Delete all container packages without a tag
Use a `--exclude` filter matching any that include any value in the tags.
- `"metadata.container.tags[*]"` -> Finds the values of all tags
- '".*"' -> Matches to any content within any tag.

### CLI
```sh
pipenv run ghpkadmin --action deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".*"
```
### Action
```yaml
- name: Delete Packages without Tags
    uses: shaneapowell/ghaction-package-admin@v0
    with:
      action: deletePackageVersions
      ghtoken: <token>
      org: <your org>
      page_type: container
      package_name: <name>
      exclude:
        - "metadata.contaienr.tags[*]"
        - ".*"
```

### Docker
```sh
docker container run -it --rm gh-packages-admin  --action deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --exclude "metadata.container.tags[*]" ".*"
```

## Keep only the most recent 5 containers with specific format tag.
- Use the `--include` filter to find only the containes you are interested in.
- Lets also `--exclude` any tags we find with `-latest` in the text.
- Sort the result by either `created_at` or `updated_at` timestamps in reverse order **youngest at the top**.
- Slice the result to skip the first 5 to the end
### CLI
```sh
pipenv run ghpkadmin --action deletePackageVersions --ghtoken <token> --org <your org> --package_type container --package_name <name> --include "metadata.container.tags[*]" "DEVELOP-.*" --sort "updated_at" --reverse --slice 5 none
```
### Action
```yaml
- name: Delete all but the most recent packages for a tag (case insensitive).
    uses: shaneapowell/ghaction-package-admin@v0
    with:
      action: deletePackageVersions
      ghtoken: <token>
      org: <your org>
      page_type: container
      package_name: <name>
      include:
        - "metadata.contaienr.tags[*]"
        - "(?i)DEVELOP-.*"
      exclude:
        - "metadata.contaienr.tags[*]"
        - ".*-latest"
      sort: "upated_at"
      reverse: true
      slice:
        - 5
        - none
```


# FAQ

## None of my delete operations actually delete anything?
By default the `--dryrun` flag is set to `True`.  You MUST explicitly turn it off with
```--dryrun false```

## I get a 404 error when I try to delete any package versions?
99% of the time, this is a permissions issue. Ensure teh user account tied to your github token, has `admin` rights on the package in question.


# Notes

A work in progress.
A single action with various admin functions for the github packages.

- List Packages
    - filters
        - regex
- List Versions of a Package
    - filters
        - regex
        - container tags
- Delete Versions of a Package
    - filters
        - regex
        - cotnainer tags
    - sort
        - date
        - tags
        - labels
    - delete by (only filter matching)
        - keep top (by sort) n items
        - oder than date
        - all matching



# Developer Notes
## Building Docker Container for local testing of action
```
> docker build --no-cache . -f Dockerfile -t ghcr.io/shaneapowell/ghaction-package-admin:develop
> docker image prune
```

## Running Docker at CLI
```
> docker container run -it --rm gh-packages-admin:latest --help
> docker container run -it --rm gh-packages-admin:latest --action listPackageVersions --ghtoken <token> --org <org> --package_type container --package_name <name> --include "metadata.container.tags[*]" "latest"  --summary
```

## Testing a GH Action Container Run
```
 /usr/bin/docker run --name ghcrioshaneapowellghactionpackageadmindevelop_dab656 --label 3a8d4e --workdir /github/workspace --rm -e "INPUT_OPERATON" -e "INPUT_OPERATION" -e "HOME" -e "GITHUB_JOB" -e "GITHUB_REF" -e "GITHUB_SHA" -e "GITHUB_REPOSITORY" -e "GITHUB_REPOSITORY_OWNER" -e "GITHUB_REPOSITORY_OWNER_ID" -e "GITHUB_RUN_ID" -e "GITHUB_RUN_NUMBER" -e "GITHUB_RETENTION_DAYS" -e "GITHUB_RUN_ATTEMPT" -e "GITHUB_REPOSITORY_ID" -e "GITHUB_ACTOR_ID" -e "GITHUB_ACTOR" -e "GITHUB_TRIGGERING_ACTOR" -e "GITHUB_WORKFLOW" -e "GITHUB_HEAD_REF" -e "GITHUB_BASE_REF" -e "GITHUB_EVENT_NAME" -e "GITHUB_SERVER_URL" -e "GITHUB_API_URL" -e "GITHUB_GRAPHQL_URL" -e "GITHUB_REF_NAME" -e "GITHUB_REF_PROTECTED" -e "GITHUB_REF_TYPE" -e "GITHUB_WORKFLOW_REF" -e "GITHUB_WORKFLOW_SHA" -e "GITHUB_WORKSPACE" -e "GITHUB_ACTION" -e "GITHUB_EVENT_PATH" -e "GITHUB_ACTION_REPOSITORY" -e "GITHUB_ACTION_REF" -e "GITHUB_PATH" -e "GITHUB_ENV" -e "GITHUB_STEP_SUMMARY" -e "GITHUB_STATE" -e "GITHUB_OUTPUT" -e "RUNNER_OS" -e "RUNNER_ARCH" -e "RUNNER_NAME" -e "RUNNER_ENVIRONMENT" -e "RUNNER_TOOL_CACHE" -e "RUNNER_TEMP" -e "RUNNER_WORKSPACE" -e "ACTIONS_RUNTIME_URL" -e "ACTIONS_RUNTIME_TOKEN" -e "ACTIONS_CACHE_URL" -e "ACTIONS_RESULTS_URL" -e GITHUB_ACTIONS=true -e CI=true -v "/var/run/docker.sock":"/var/run/docker.sock" -v "/home/runner/work/_temp/_github_home":"/github/home" -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" -v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands" -v "/home/runner/work/ghaction-package-admin/ghaction-package-admin":"/github/workspace" ghcr.io/shaneapowell/ghaction-package-admin:develop  "--operation" "" "--debug"
```

## using 'act' to test contaienr
- build a local copy of the docker image (see above)
- run the local-image in act
```
ct --pull=false -W ./github/workflows/local_test.yml
```