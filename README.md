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
- name: Delete all but the most recent packages for a tag.
    uses: shaneapowell/ghaction-package-admin@v0
    with:
      action: deletePackageVersions
      ghtoken: <token>
      org: <your org>
      page_type: container
      package_name: <name>
      include:
        - "metadata.contaienr.tags[*]"
        - "DEVELOP-.*"
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




# Building Docker Container
docker build . -f Dockerfile -t gh-package-admin
docker image prune

# Running at CLI
docker container run -it --rm gh-packages-admin:latest --help
docker container run -it --rm gh-packages-admin:latest --action listPackageVersions --ghtoken <token> --org <org> --package_type container --package_name <name> --include "metadata.container.tags[*]" "latest"  --summary






[
    {
        "id": 194943391,
        "name": "sha256:96199792ccf207fe7f16846d1172a05aa63daff2a428abfbbfa2301f53f20693",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194943391",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-24T01:36:20Z",
        "updated_at": "2024-03-24T01:36:20Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194943391",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-182",
                    "DEVELOP-latest"
                ]
            }
        }
    },
    {
        "id": 194780060,
        "name": "sha256:33ae6970315c39a9725ef2db8b44c15b28cb53a34967b82dc541732ede882796",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194780060",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-23T00:39:15Z",
        "updated_at": "2024-03-23T00:39:15Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194780060",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-181"
                ]
            }
        }
    },
    {
        "id": 194778760,
        "name": "sha256:563dcdb9dc465a2cd5e47e4c6184ff12572103417ea340f1337188762f8f8aeb",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194778760",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-23T00:34:55Z",
        "updated_at": "2024-03-23T00:34:55Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194778760",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-180"
                ]
            }
        }
    },
    {
        "id": 194772969,
        "name": "sha256:1dbb3fa1b0ba60e7152a8e1a7f62dea94713f633ecfdd8f055dfb013e286cf5b",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194772969",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-23T00:14:00Z",
        "updated_at": "2024-03-23T00:14:00Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194772969",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-179"
                ]
            }
        }
    },
    {
        "id": 194770975,
        "name": "sha256:9a2f2b2eb4dc46c54a48fa4700a825a371b0698b5b345fc7c841a981200f3da5",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194770975",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-23T00:06:04Z",
        "updated_at": "2024-03-23T00:06:04Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194770975",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-178"
                ]
            }
        }
    },
    {
        "id": 194769532,
        "name": "sha256:06a2ec73dfdec0b0bc8bc54141f34bf7c57a395b1b82341915a8beea2ed1d726",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194769532",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-22T23:58:33Z",
        "updated_at": "2024-03-22T23:58:33Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194769532",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-177"
                ]
            }
        }
    },
    {
        "id": 194764069,
        "name": "sha256:eb7f74b25df5ebb3a30ac4d5b4625df8d617b67ca1948c2d6ac765c2196d8a4c",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194764069",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-22T23:24:32Z",
        "updated_at": "2024-03-22T23:24:32Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194764069",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-176"
                ]
            }
        }
    },
    {
        "id": 194761504,
        "name": "sha256:8ba5fd3979e0b1a95452f2b788b9d100e321566540a32a072c3122d75650bfcf",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194761504",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-22T23:13:51Z",
        "updated_at": "2024-03-22T23:13:51Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194761504",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-175"
                ]
            }
        }
    },
    {
        "id": 194760271,
        "name": "sha256:8fd9144ccea9e4929d7052527f070112a37734c392650632b4a48e21a64723ed",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/194760271",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2024-03-22T23:08:02Z",
        "updated_at": "2024-03-22T23:08:02Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/194760271",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-174"
                ]
            }
        }
    },
    {
        "id": 107719851,
        "name": "sha256:7ea4681cf2932a0be236150888807d16c7e048182c6f79a300623c9826e6c386",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/107719851",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-07-07T13:17:01Z",
        "updated_at": "2023-07-07T13:17:01Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/107719851",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 107223200,
        "name": "sha256:c636e181a6264e2f755001c7027175c288a407b35dbc12c4cd19fbd128d5e28c",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/107223200",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-07-06T01:52:07Z",
        "updated_at": "2023-07-06T01:52:07Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/107223200",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 106198212,
        "name": "sha256:585950758dff3e92f07515ad43531f6a05878bb36431fd633ffaec5173217954",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/106198212",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-07-02T01:48:56Z",
        "updated_at": "2023-07-02T01:48:56Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/106198212",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 106058737,
        "name": "sha256:6a532c20df9c59b3e233df68380638c2608c4ad8ea62857faa65ebacd3691f73",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/106058737",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-30T21:49:05Z",
        "updated_at": "2023-06-30T21:49:05Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/106058737",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 106058169,
        "name": "sha256:a17ed57b9c6f88cfa312371b7cd802ee90726ef568a1f3219620b987a0fb1f6d",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/106058169",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-30T21:45:09Z",
        "updated_at": "2023-06-30T21:45:09Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/106058169",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 106024663,
        "name": "sha256:78213260474afe095c26d034623a9c95906c5095f9fde66202c9d72065acd862",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/106024663",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-30T18:18:53Z",
        "updated_at": "2023-06-30T18:18:53Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/106024663",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 105746756,
        "name": "sha256:bbdd9ddf179e953f45b8ca1c63e79bd5d336c9095e57e77405c99efb0287d41a",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/105746756",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-29T20:19:02Z",
        "updated_at": "2023-06-29T20:19:02Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/105746756",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 105714647,
        "name": "sha256:5b1edba2aae8a285d715fee6037ce8ffe0df73847ed50775866a1681b1b54279",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/105714647",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-29T17:02:21Z",
        "updated_at": "2023-06-29T17:02:21Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/105714647",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 105029988,
        "name": "sha256:c5eb7c8783a9b7102cfcbc687b223508a0af179d22931f6cf8319e2aca7e5016",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/105029988",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-27T17:15:28Z",
        "updated_at": "2023-06-27T17:15:28Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/105029988",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 105026421,
        "name": "sha256:b42e4811a5fe93b193c2a0eb7b6ca712dcce12c1bacf4f8d5469e257c2075688",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/105026421",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-27T16:57:03Z",
        "updated_at": "2023-06-27T16:57:03Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/105026421",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 104305506,
        "name": "sha256:874cf0aae811a8d4872759194aeae383de9ac9d477b92bc1da81c713ef22d219",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/104305506",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-25T01:49:31Z",
        "updated_at": "2023-06-25T01:49:31Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/104305506",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 102467822,
        "name": "sha256:b779c65a8a0155ac80879165ae11d3ab5899f08205227b164f74eba5499fa873",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/102467822",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-18T01:48:16Z",
        "updated_at": "2023-06-18T01:48:16Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/102467822",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 101620370,
        "name": "sha256:f3f6e566b968509c7cf4baad997808be61494b5c0dcb1f85756f90a9a35edd18",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/101620370",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-14T18:55:32Z",
        "updated_at": "2023-06-14T18:55:32Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/101620370",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 101249850,
        "name": "sha256:82011a5b541c803ecda5211e39d307d7bef29319ddbd36fcf603203fdcef95a3",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/101249850",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-13T19:29:58Z",
        "updated_at": "2023-06-13T19:29:58Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/101249850",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 101216825,
        "name": "sha256:fe21becaed1326efab2f727424646ebff50e508b200dee7afb8b82f809ee08dc",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/101216825",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-13T17:10:38Z",
        "updated_at": "2023-06-13T17:10:38Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/101216825",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 100894443,
        "name": "sha256:c295a96b68ef597bc2ccf745c4d072fe2892ab3de7e4a6f7016a2acb939efaed",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/100894443",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-12T19:53:00Z",
        "updated_at": "2023-06-12T19:53:00Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/100894443",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 100887159,
        "name": "sha256:a3a4f7d6c6b01b6e63e10ef5396bef510e73b0774ac8c536dc4c66f51e52f349",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/100887159",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-12T19:21:54Z",
        "updated_at": "2023-06-12T19:21:54Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/100887159",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 100475818,
        "name": "sha256:049c15ec2a50bcdeb2b0164c00b3b038f823a5801de5da53b305e1cab251a21e",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/100475818",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-11T01:48:24Z",
        "updated_at": "2023-06-11T01:48:24Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/100475818",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 98551199,
        "name": "sha256:2fb823b2eb181bbe57f210c3e0b27ba4cd892c46be1ac50914a6bb680475ff1c",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/98551199",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-06-04T01:50:15Z",
        "updated_at": "2023-06-04T01:50:15Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/98551199",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 96744990,
        "name": "sha256:c3a7d05f0355907508e97cbb5fcb7264036d32a6772aa5b3e6a9b68f24bd8e3d",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/96744990",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-05-28T01:48:21Z",
        "updated_at": "2023-05-28T01:48:21Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/96744990",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    },
    {
        "id": 96602148,
        "name": "sha256:791c534d1e1220daa0c011c79d0b09d5e342b569eafd2b91bd986cdc72a907be",
        "url": "https://api.github.com/orgs/AirStripTech/packages/container/pysim/versions/96602148",
        "package_html_url": "https://github.com/orgs/AirStripTech/packages/container/package/pysim",
        "created_at": "2023-05-26T20:10:03Z",
        "updated_at": "2023-05-26T20:10:03Z",
        "description": "AirStripTech-Simulator",
        "html_url": "https://github.com/orgs/AirStripTech/packages/container/pysim/96602148",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": []
            }
        }
    }
