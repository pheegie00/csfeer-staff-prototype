

## Local Setup


For open id redirection to work correctly, you'll need to add the following entry
to your `/etc/hosts` file:

  ```
  127.0.0.1       oauth.csfeer
  ```

After that, with the default settings, you should be able to run the app:

  ```
  docker-compose build
  docker-compose up
  ```
