# Comment on PR

A GitHub action to add a comment on pull requests.

## Usage Example

[`.github/workflows/example.yml`](.github/workflows/example.yml)

```yml
name: Add checkout commands
on: pull_request
jobs:
  comment:
    name: Add checkout commands
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
      - uses: wamburu/comment-on-pr@1.0.1-beta
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          filename: template.md
```

[`.github/workflows/template.md`](.github/workflows/template.md)

````markdown
commands to checkout to this branch

```
git fetch upstream pull/{pull_id}/head:{branch_name}
git checkout {branch_name}
```
````

The template above creates:

![comment_example](./assets/comment_example.png)
