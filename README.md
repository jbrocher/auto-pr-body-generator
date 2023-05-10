# AI Powered Automatic PR Body Generator

This github action automatically generates the body of a pull request by summarizing the changes made in the code diff. The action requires an OpenAI account to work and the input variable `OPENAI_API_KEY` must be set with [an openai API key](https://platform.openai.com/account/api-keys).

## Usage

Here's an example workflow that uses this action. Detailed explanation are given in the following sections 

```yaml
name: Auto-PR-Body Generator

on:
  pull_request:

permissions:
  contents: read
  repository-projects: write
  pull-requests: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Auto-PR-Body Generator
        uses: jbrocher/automatic-pr-body-generator@v1.0
        with:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Trigger

The action will look for a PR opened for the git ref that triggered the action. We recommend triggering the action once the PR is opened and on each subsequent push so the body is kept up to date. This can be achieved wit the `pull_request` trigger : 

```yaml
on:
  pull_request:
```


### Permissions

In order to edit the PR body, at the minimum you workflow must set the following permissions: 

```yaml
permissions:
  contents: read
  repository-projects: write
```

### Openapi API key

This action relies on Openai to generate the body, and as such needs an active open aiaccount to work. Once you've generated an API key, pass it as input to the action using the `with` directive: 

```yaml
  - name: Auto-PR-Body Generator
    uses: jbrocher/auto-pr-body-generator@v1.0
    with:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```


## Behavior  with existing PR body
The action indicates the start of the automatically generated body with the following delimiter  `### === auto-pr-body ===`
Please note that the action will replace everything after the delimiter in the PR body each time it runs. If you want to keep some content in the PR body, make sure to add it before the delimiter.
