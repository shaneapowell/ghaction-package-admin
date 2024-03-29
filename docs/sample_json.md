# Sample Json
Some referece examples of the json response models from the GitHub API.  These examples are here to help in finding the `json-path` to a specific value to be filtered or sorted.

## listPackages
```json
[
    {
        "id": 5314228,
        "name": "docker-zenphoto",
        "package_type": "container",
        "owner": {
            "login": "shaneapowell",
            "id": 12113620,
            "node_id": "MDQ6VXNlcjEyMTEzNjIw",
            "avatar_url": "https://avatars.githubusercontent.com/u/12113620?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/shaneapowell",
            "html_url": "https://github.com/shaneapowell",
            "followers_url": "https://api.github.com/users/shaneapowell/followers",
            "following_url": "https://api.github.com/users/shaneapowell/following{/other_user}",
            "gists_url": "https://api.github.com/users/shaneapowell/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/shaneapowell/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/shaneapowell/subscriptions",
            "organizations_url": "https://api.github.com/users/shaneapowell/orgs",
            "repos_url": "https://api.github.com/users/shaneapowell/repos",
            "events_url": "https://api.github.com/users/shaneapowell/events{/privacy}",
            "received_events_url": "https://api.github.com/users/shaneapowell/received_events",
            "type": "User",
            "site_admin": false
        },
        "visibility": "public",
        "url": "https://api.github.com/users/shaneapowell/packages/container/docker-zenphoto",
        "created_at": "2023-07-02T19:56:06Z",
        "updated_at": "2023-07-03T14:37:19Z",
        "repository": {
            "id": 661310082,
            "node_id": "R_kgDOJ2rKgg",
            "name": "docker-zenphoto",
            "full_name": "shaneapowell/docker-zenphoto",
            "private": false,
            "owner": {
                "login": "shaneapowell",
                "id": 12113620,
                "node_id": "MDQ6VXNlcjEyMTEzNjIw",
                "avatar_url": "https://avatars.githubusercontent.com/u/12113620?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/shaneapowell",
                "html_url": "https://github.com/shaneapowell",
                "followers_url": "https://api.github.com/users/shaneapowell/followers",
                "following_url": "https://api.github.com/users/shaneapowell/following{/other_user}",
                "gists_url": "https://api.github.com/users/shaneapowell/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/shaneapowell/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/shaneapowell/subscriptions",
                "organizations_url": "https://api.github.com/users/shaneapowell/orgs",
                "repos_url": "https://api.github.com/users/shaneapowell/repos",
                "events_url": "https://api.github.com/users/shaneapowell/events{/privacy}",
                "received_events_url": "https://api.github.com/users/shaneapowell/received_events",
                "type": "User",
                "site_admin": false
            },
            "html_url": "https://github.com/shaneapowell/docker-zenphoto",
            "description": "A docker image of the popular ZenPhoto CMS",
            "fork": false,
            "url": "https://api.github.com/repos/shaneapowell/docker-zenphoto",
            "forks_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/forks",
            "keys_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/keys{/key_id}",
            "collaborators_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/collaborators{/collaborator}",
            "teams_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/teams",
            "hooks_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/hooks",
            "issue_events_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/issues/events{/number}",
            "events_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/events",
            "assignees_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/assignees{/user}",
            "branches_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/branches{/branch}",
            "tags_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/tags",
            "blobs_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/git/blobs{/sha}",
            "git_tags_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/git/tags{/sha}",
            "git_refs_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/git/refs{/sha}",
            "trees_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/git/trees{/sha}",
            "statuses_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/statuses/{sha}",
            "languages_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/languages",
            "stargazers_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/stargazers",
            "contributors_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/contributors",
            "subscribers_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/subscribers",
            "subscription_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/subscription",
            "commits_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/commits{/sha}",
            "git_commits_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/git/commits{/sha}",
            "comments_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/comments{/number}",
            "issue_comment_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/issues/comments{/number}",
            "contents_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/contents/{+path}",
            "compare_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/compare/{base}...{head}",
            "merges_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/merges",
            "archive_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/{archive_format}{/ref}",
            "downloads_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/downloads",
            "issues_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/issues{/number}",
            "pulls_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/pulls{/number}",
            "milestones_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/notifications{?since,all,participating}",
            "labels_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/labels{/name}",
            "releases_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/releases{/id}",
            "deployments_url": "https://api.github.com/repos/shaneapowell/docker-zenphoto/deployments"
        },
        "html_url": "https://github.com/users/shaneapowell/packages/container/package/docker-zenphoto"
    },
    {
        "id": 6353161,
        "name": "ghaction-package-admin",
        "package_type": "container",
        "owner": {
            "login": "shaneapowell",
            "id": 12113620,
            "node_id": "MDQ6VXNlcjEyMTEzNjIw",
            "avatar_url": "https://avatars.githubusercontent.com/u/12113620?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/shaneapowell",
            "html_url": "https://github.com/shaneapowell",
            "followers_url": "https://api.github.com/users/shaneapowell/followers",
            "following_url": "https://api.github.com/users/shaneapowell/following{/other_user}",
            "gists_url": "https://api.github.com/users/shaneapowell/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/shaneapowell/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/shaneapowell/subscriptions",
            "organizations_url": "https://api.github.com/users/shaneapowell/orgs",
            "repos_url": "https://api.github.com/users/shaneapowell/repos",
            "events_url": "https://api.github.com/users/shaneapowell/events{/privacy}",
            "received_events_url": "https://api.github.com/users/shaneapowell/received_events",
            "type": "User",
            "site_admin": false
        },
        "visibility": "public",
        "url": "https://api.github.com/users/shaneapowell/packages/container/ghaction-package-admin",
        "created_at": "2024-03-28T01:59:08Z",
        "updated_at": "2024-03-28T18:07:30Z",
        "repository": {
            "id": 777280213,
            "node_id": "R_kgDOLlRa1Q",
            "name": "ghaction-package-admin",
            "full_name": "shaneapowell/ghaction-package-admin",
            "private": false,
            "owner": {
                "login": "shaneapowell",
                "id": 12113620,
                "node_id": "MDQ6VXNlcjEyMTEzNjIw",
                "avatar_url": "https://avatars.githubusercontent.com/u/12113620?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/shaneapowell",
                "html_url": "https://github.com/shaneapowell",
                "followers_url": "https://api.github.com/users/shaneapowell/followers",
                "following_url": "https://api.github.com/users/shaneapowell/following{/other_user}",
                "gists_url": "https://api.github.com/users/shaneapowell/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/shaneapowell/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/shaneapowell/subscriptions",
                "organizations_url": "https://api.github.com/users/shaneapowell/orgs",
                "repos_url": "https://api.github.com/users/shaneapowell/repos",
                "events_url": "https://api.github.com/users/shaneapowell/events{/privacy}",
                "received_events_url": "https://api.github.com/users/shaneapowell/received_events",
                "type": "User",
                "site_admin": false
            },
            "html_url": "https://github.com/shaneapowell/ghaction-package-admin",
            "description": "My various GitHub Actions",
            "fork": false,
            "url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin",
            "forks_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/forks",
            "keys_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/keys{/key_id}",
            "collaborators_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/collaborators{/collaborator}",
            "teams_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/teams",
            "hooks_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/hooks",
            "issue_events_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/issues/events{/number}",
            "events_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/events",
            "assignees_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/assignees{/user}",
            "branches_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/branches{/branch}",
            "tags_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/tags",
            "blobs_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/git/blobs{/sha}",
            "git_tags_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/git/tags{/sha}",
            "git_refs_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/git/refs{/sha}",
            "trees_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/git/trees{/sha}",
            "statuses_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/statuses/{sha}",
            "languages_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/languages",
            "stargazers_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/stargazers",
            "contributors_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/contributors",
            "subscribers_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/subscribers",
            "subscription_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/subscription",
            "commits_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/commits{/sha}",
            "git_commits_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/git/commits{/sha}",
            "comments_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/comments{/number}",
            "issue_comment_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/issues/comments{/number}",
            "contents_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/contents/{+path}",
            "compare_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/compare/{base}...{head}",
            "merges_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/merges",
            "archive_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/{archive_format}{/ref}",
            "downloads_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/downloads",
            "issues_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/issues{/number}",
            "pulls_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/pulls{/number}",
            "milestones_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/notifications{?since,all,participating}",
            "labels_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/labels{/name}",
            "releases_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/releases{/id}",
            "deployments_url": "https://api.github.com/repos/shaneapowell/ghaction-package-admin/deployments"
        },
        "html_url": "https://github.com/users/shaneapowell/packages/container/package/ghaction-package-admin"
    }
]


```

## listPackageVersions
```json
[
     {
        "id": 197157002,
        "name": "sha256:26c2273e4af28bd25e1ed407da33e2b2713ba9fc68d1100b532aef82632e00d7",
        "url": "https://api.github.com/users/shaneapowell/packages/container/ghaction-package-admin/versions/197157002",
        "package_html_url": "https://github.com/users/shaneapowell/packages/container/package/ghaction-package-admin",
        "created_at": "2024-03-28T17:52:59Z",
        "updated_at": "2024-03-28T17:52:59Z",
        "html_url": "https://github.com/users/shaneapowell/packages/container/ghaction-package-admin/197157002",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "latest",
                    "develop",
                    "develop-40"
                ]
            }
        }
    },
    {
        "id": 197146033,
        "name": "sha256:01087717097c3222823bc0e93b526b0fe001b7bb0098a46a2dd0f6ab5f132ba0",
        "url": "https://api.github.com/users/shaneapowell/packages/container/ghaction-package-admin/versions/197146033",
        "package_html_url": "https://github.com/users/shaneapowell/packages/container/package/ghaction-package-admin",
        "created_at": "2024-03-28T17:22:11Z",
        "updated_at": "2024-03-28T17:22:11Z",
        "html_url": "https://github.com/users/shaneapowell/packages/container/ghaction-package-admin/197146033",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-39"
                ]
            }
        }
    },
    {
        "id": 197138788,
        "name": "sha256:ebb271e11ba83b4e1cdc981b764b0fc568e70c36d5930fb887682e000581fa18",
        "url": "https://api.github.com/users/shaneapowell/packages/container/ghaction-package-admin/versions/197138788",
        "package_html_url": "https://github.com/users/shaneapowell/packages/container/package/ghaction-package-admin",
        "created_at": "2024-03-28T17:03:50Z",
        "updated_at": "2024-03-28T17:03:50Z",
        "html_url": "https://github.com/users/shaneapowell/packages/container/ghaction-package-admin/197138788",
        "metadata": {
            "package_type": "container",
            "container": {
                "tags": [
                    "DEVELOP-38"
                ]
            }
        }
    }

]
```
