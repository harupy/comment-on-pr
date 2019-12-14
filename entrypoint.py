import json
import os
import re
from pprint import pprint

from github import Github


def read_json(filepath):
    """
    Read a json file as a dictionary.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    data : dict

    """
    with open(filepath, 'r') as f:
        return json.load(f)


def get_actions_input(input_name):
    """
    Get a Github actions input by name.

    Parameters
    ----------
    input_name : str

    Returns
    -------
    action_input : str

    Notes
    -----
    GitHub Actions creates an environment variable for the input with the name:

    INPUT_<CAPITALIZED_VARIABLE_NAME> (e.g. "INPUT_FOO" for "foo")

    References
    ----------
    .. [1] https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#example

    """
    return os.getenv('INPUT_{}'.format(input_name).upper())


def main():
    # search a pull request that triggered this action
    gh = Github(os.getenv('GITHUB_TOKEN'))
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    branch_label = event['pull_request']['head']['label']  # author:branch_name
    branch_name = branch_label.split(':')[-1]
    repo = gh.get_repo(event['repository']['full_name'])
    prs = repo.get_pulls(state='open', sort='created', head=branch_label)
    pr = prs[0]

    template_path = os.path.join('.github/workflows', get_actions_input('filename'))

    with open(template_path, 'r') as f:
        template = f.read()

    pprint(event)
    print(template)

    pr_info = {
        'pull_id': pr.number,
        'branch_name': branch_name
    }
    comment = template.format(**pr_info)
    pr.create_issue_comment(comment)


if __name__ == '__main__':
    main()
