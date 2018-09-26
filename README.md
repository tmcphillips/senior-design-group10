# senior-design-group10
Document sharing between team members, sponsors, faculty advisors, and DAB members for the Senior Design Software Project

### Code Review

When merging, be sure to select the `Squash and Merge` option on Github.

#### Requester

Before pushing your feature branch to remote, be sure to use `pull --rebase` with master to avoid merge conflicts on the pull request and squash merge commits like `merged with <branch_name>`.

#### Reviewer

When someone requests you review their work, make sure you get a copy of that person's pull request and test their code locally. To get the pull request as a new branch, follow [these steps](https://help.github.com/articles/checking-out-pull-requests-locally/#modifying-an-inactive-pull-request-locally)

Summary:

Use `git fetch origin pull/<Merge Number>/head:<Name of new Branch>`, then checkout the newly created branch

