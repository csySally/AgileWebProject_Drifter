# CITS5505_AgileWebProject2

## Agile Marking:

Marks will be given for evidence of Agile development practices, i.e.

- appropriately sized commits with meaningful messages.
- planning of short-term goals via the Issues tab.
- reproducible bug reports via the Issues tab.
- use pull requests to merge in new features via the Pull Requests tab.
- exhibiting teamwork by contributing to discussions on the Issues
- exhibiting teamwork by adding code reviews to other people's Pull Requests.
- intermediate deliverables, pinpointed with Git tags.

### Issue Creating

1. On the GitHub repository page, click the "Issues" tab.
2. Click the "New issue" button to start creating a new issue.
3. Fill in the title and description for the issue. The title should summarise the issue or requirement, while the description should detail the problem, desired behaviour, steps to reproduce it, etc.

#### Managing Issues

- Use Labels: We can categorise issues by setting different labels for them (e.g. "bug", "feature request", "help wanted "), we can categorise issues for easy tracking and management.
- Assignees: We can assign one or more people to work on a particular issue, which helps to clarify the division of labour.
- Comments and Updates: Project team members should discuss under issues to provide progress updates, solutions or further questions.

#### Closing an Issue

An issue can be closed when it is resolved or a requirement is met by providing a short resolution statement in the issue discussion and clicking the "Close issue" button. If the issue reappears later, we can reopen the issue.

### Branch Creating

- Main branch is kept stable and all new development work is done on a separate branch.
- Each branch corresponds to an issue, making it easier to track work and review history.

#### How to Name A Branch?

Use a naming convention that includes the issue number and a short description, such as <b>issue-123-add-login-function</b>, so that we can learn directly from the branch name which issue it was created to resolve.

### Pull Request (PR) Guidelines

#### Creating a Pull Request

1. Branch Preparation: Ensure your feature branch is up-to-date with the latest changes from the main branch. This reduces the likelihood of merge conflicts.
2. Initiate the PR: From the GitHub repository page, navigate to the "Pull Requests" tab and click the "New pull request" button. Select your feature branch as the "compare" branch and main (or the appropriate target branch) as the "base" branch.
3. PR Description: Fill in a detailed description of the pull request. Include the purpose of the changes, which issue(s) the PR addresses, and a summary of the main changes. Linking the issue(s) by number (e.g., #123) will automatically associate the PR with those issues.
4. Review and Discussion: Before finalizing the PR, request reviews from team members. This promotes collaboration and code quality. Engage in discussions within the PR if there are comments or suggestions.

#### Reviewing a Pull Request

1. Code Review: Review the code changes for clarity, efficiency, and adherence to project standards. Look for any potential issues or improvements.
2. Feedback: Provide constructive feedback and suggestions for improvements. If changes are required, request changes; otherwise, approve the PR.

#### Merging a Pull Request

1. Close Linked Issues: If the PR description or commits didn’t automatically close the related issues, manually close them by mentioning the PR number (e.g., Closes #123 due to PR #456).
2. Post-Merge Cleanup: Delete the feature branch if it's no longer needed, to keep the repository tidy.
