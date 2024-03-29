I develop on Linux, so I apologize if these are Linux slanted commands. I hope translating them to mac or windows equivalent is not too challenging.

# How to clone and run from the command line
- clone this repo.
- install python 3.11 on your system.
- install the pipenv utility
    - `> pip install pipenv`
- use pipenv to setup the dependencies
    - `> pipenv sync`
- Run the pipenv command with the options you wish to test
    - `> pipenv run ghpkgadmin --help`
    - `> pipenv run ghpkgadmin --operation listPackageVersions --ghtoken **** --packageType ...`

# How to run the docker image from the command line
If you have docker running on your machine, you can have it pull the action image and run the command from a command prompt.  You need only change how the package is executed, and provide all the same command line options as the above
- Ensure Docker is setup and running on your machine.
- Simply run the example docker command at the command prompt changing out:
    -`pipenv run ghpkgadmin`
    - for `docker run --name ghpkgadmin --label ghpkgadmin  --rm ghcr.io/shaneapowell/ghaction-package-admin:v1 ...`

```sh
docker run --name ghpkgadmin --rm ghcr.io/shaneapowell/ghaction-package-admin:v1 --operation listPackageVersions --ghtoken <token> --user <your user> --package_type container --package_name <name> --summary
```

# How can I test out the action locally?
I use the [`act` utility](https://aur.archlinux.org/packages/act) to test out actions locally.  This command has worked well for me.
```sh
> act -W ./github/workflows/local_test.yml
```

I have also been able to test locally generated images by specifying `--pull=false`.

```sh
> act --pull=false -W ./github/workflows/local_test.yml
```

# An example of the full docker command the github agent executes

## Testing a GH Action Container Run
```
 /usr/bin/docker run --name ghcrioshaneapowellghactionpackageadmindevelop_dab656 --label 3a8d4e --workdir /github/workspace --rm -e "INPUT_OPERATON" -e "INPUT_OPERATION" -e "HOME" -e "GITHUB_JOB" -e "GITHUB_REF" -e "GITHUB_SHA" -e "GITHUB_REPOSITORY" -e "GITHUB_REPOSITORY_OWNER" -e "GITHUB_REPOSITORY_OWNER_ID" -e "GITHUB_RUN_ID" -e "GITHUB_RUN_NUMBER" -e "GITHUB_RETENTION_DAYS" -e "GITHUB_RUN_ATTEMPT" -e "GITHUB_REPOSITORY_ID" -e "GITHUB_ACTOR_ID" -e "GITHUB_ACTOR" -e "GITHUB_TRIGGERING_ACTOR" -e "GITHUB_WORKFLOW" -e "GITHUB_HEAD_REF" -e "GITHUB_BASE_REF" -e "GITHUB_EVENT_NAME" -e "GITHUB_SERVER_URL" -e "GITHUB_API_URL" -e "GITHUB_GRAPHQL_URL" -e "GITHUB_REF_NAME" -e "GITHUB_REF_PROTECTED" -e "GITHUB_REF_TYPE" -e "GITHUB_WORKFLOW_REF" -e "GITHUB_WORKFLOW_SHA" -e "GITHUB_WORKSPACE" -e "GITHUB_ACTION" -e "GITHUB_EVENT_PATH" -e "GITHUB_ACTION_REPOSITORY" -e "GITHUB_ACTION_REF" -e "GITHUB_PATH" -e "GITHUB_ENV" -e "GITHUB_STEP_SUMMARY" -e "GITHUB_STATE" -e "GITHUB_OUTPUT" -e "RUNNER_OS" -e "RUNNER_ARCH" -e "RUNNER_NAME" -e "RUNNER_ENVIRONMENT" -e "RUNNER_TOOL_CACHE" -e "RUNNER_TEMP" -e "RUNNER_WORKSPACE" -e "ACTIONS_RUNTIME_URL" -e "ACTIONS_RUNTIME_TOKEN" -e "ACTIONS_CACHE_URL" -e "ACTIONS_RESULTS_URL" -e GITHUB_ACTIONS=true -e CI=true -v "/var/run/docker.sock":"/var/run/docker.sock" -v "/home/runner/work/_temp/_github_home":"/github/home" -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" -v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands" -v "/home/runner/work/ghaction-package-admin/ghaction-package-admin":"/github/workspace" ghcr.io/shaneapowell/ghaction-package-admin:develop  "--operation" "" "--debug"
```

## Building a Docker Image for local testing of action
```
> docker build --no-cache . -f Dockerfile -t ghcr.io/shaneapowell/ghaction-package-admin:develop
```
```
> docker image prune
```