# Configure beads with the ACF jira repo:


1. Generate a personal jira access token:

https://jira.acf.gov/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens

2. Run the following commands with your personal access token:

```bash
bd init --prefix bd && \
  bd migrate sync beads-sync && \
  bd config set jira.url "https://jira.acf.gov" && \
  bd config set jira.project "FE" && \
  bd config set allowed_prefixes "FE" && \
  bd config set  jira.api_token "<your jira personal access token>" && \
  mkdir -p ~/.local/bin/examples/jira-import && \
  cp ./.beads/*.py ~/.local/bin/examples/jira-import/
  # Important - don't set a jira.username value. The auth won't work
```

Now you should be able to pull jira issues:

```bash
bd jira sync --pull
```