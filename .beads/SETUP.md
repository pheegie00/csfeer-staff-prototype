# Configure beads with the ACF jira repo:

1. Install beads and jira-beads-sync from source:

    ```
    make install-beads
    ```

2. Install dolt:

    ```
    brew install dolt
    ```

3. Configure beads to work with our project:

    ```
    make configure-beads
    ```

4. Generate a [jira API token](https://jira.acf.gov/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens)

5. Set that token in your bd config:

    ```
    bd config set  jira.api_token "<your jira personal access token>"
    ```

6. Pull tickets from jira

    ```
    bd jira sync --pull
    ```
7. Use `jira-beads-sync` to work with individual issues:

```
$ jira-beads-sync quickstart FE-501
jira-beads-sync quickstart
========================

Using issue key: FE-501

Fetching FE-501 and its dependencies...
Fetching FE-501...

✓ Fetched 1 issue(s)

Converting to beads format...

✓ Conversion complete!
  1 issue(s) written to /Users/ryanbagwell/projects/csfeer/.beads/issues.jsonl


```


