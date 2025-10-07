# Mocked Oauth

Keycloak is a compliant OIDC provider that CSFEER makes use of in environments where Okta (DOS preferred authentication provider) is not available.  It provides all the same functionality that we expect consume in production.

## Configuration

The default admin password is admin/admin

[realm.json](./realm.json) is an exported realm that is automatically loaded when the container starts up.

### Updating the configuration

Occasionally, the configuration will need updates such as:

- adding new scopes
- adjust the Oauth client settings

In those scenarios, the `realm.json` needs to be kept up to date.  This can be accomplished by visiting the [realm settings](http://localhost:8081/admin/master/console/#/CSFEER/realm-settings) and usings the export action.  After exporting, the realm.json should be overwritten entirely and committed.
