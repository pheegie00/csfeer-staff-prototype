# Configure beads with the ACF jira repo:

1. Install beads from source:

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

6. Sync with jira:

    ```
    bd jira sync
    ```
