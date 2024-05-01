# DRIFTER

## About the Application

In this fast-paced world, everyone's heart harbours unspoken mysteries and late-night musings. Do those unspoken secrets in casual conversations or written silently on the pages of your diary sometimes make you feel lonely and helpless? Have you ever wanted to find an outlet for those questions?

Welcome to "Drifter" - a unique platform for your questions to fly freely in an anonymous world. Here, everyone can be a listener and a sharer. Whether it's late-night blues, dawn doubts, or those flashes of inspiration and things you haven't told others, they can all find their home here.

"Drifter" makes the power of anonymity gentle and powerful. There are no preconceived prejudices, only stories waiting to be discovered and mysteries to be solved. Send a secret note and it will randomly fly to a corner of the world; reply to a stranger's query and your words may become a beacon for them. In the process, different people will gather around a secret or question, sharing their perspectives so that everyone's experience is resonated and understood.

Please speak up at Drifter!

### MVP

1. User registration and login

Allow users to create accounts and log in to secure user information.

2. Send a text note

Users can send notes anonymously, the content can be anything.

3. Receive Notes

Users randomly receive secret notes from anonymous users. Plus Users can also search for notes containing specific keywords, such as "love".

4. Anonymous Reply

Users can reply anonymously to the received note. If the user can't answer or doesn't want to answer the current note, he/she can choose to read the next one.

5. View Reply

Users can view the replies received to the notes they send.

### Future Improvements

1. Users can insert pictures in the note.
2. Allow users to like or dislike the replies they receive.
3. Users can save their favourite replies to a "favourites" list for later viewing.

## Group Members

| UWA ID   | Name        | Github Username |
| -------- | ----------- | --------------- |
| 23687599 | Sally Chen  | csySally        |
| 23212326 | Lili Liu    | LiliLiu09       |
| 24117922 | Zhengxu Jin | joshjin11       |
| 23495103 | David Pan   | xxxxx           |

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

#### How to Create A New Branch from Main?

1. Switch to the main branch and pull the latest changes from the remote repository.

```
git checkout main
git pull origin main

```

2. Create a new branch from main to develop your new feature.

```
git checkout -b issue-123-add-login-function

```

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

```
git checkout main
git merge issue-123-add-login-function
git push origin main

```
