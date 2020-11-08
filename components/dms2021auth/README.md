# DMS 2020-2021 Authentication Service

This service provides authentication functionalities to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
# Initialize the administrator user admin (password: admin)
dms2021auth-create-admin
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2021auth/config.yml`. This path is thus usually `${HOME}/.config/dms2021auth/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `host` (mandatory): The service host.
- `port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.

## Running the service

Just run `dms2021auth` as any other program.

## REST API specification

This service exposes a REST API so other services/applications can interact with it.

- `/` [`GET`]

  Status verification.
  - Returns:
    - `200 OK` if the service is running.
- `/sessions` [`POST`]

  Logs a user in.
  - Parameters:
    - `username` [form data] (`str`): The user name.
    - `password` [form data] (`str`): The user password.
  - Returns:
    - `200 OK` if the user was successfully logged-in. The response content (`application/json`) is a JSON dictionary containing the session id/token in the attribute `session_id`.
    - `401 Unauthorized` if the user credentials are not valid.
- `/sessions` [`DELETE`]

  Logs a user out.
  - Parameters:
    - `session_id` [form data] (`str`): The id of the session to close.
  - Returns:
    - `200 OK` if the user was successfully logged-out.
    - `401 Unauthorized` if the session does not exist or was already closed.
- `/users` [`POST`]

  Creates a new user.
  - Security:
    - The requestor must have the `AdminUsers` right.
  - Parameters:
    - `username` [form data] (`str`): The user name.
    - `password` [form data] (`str`): The user password.
    - `session_id` [form data] (`str`): The requestor session.
  - Returns:
    - `200 OK` if the user was created successfully.
    - `400 Bad Request` if the request is malformed (e.g., one of the parameters is not valid)
    - `401 Unauthorized` if the requestor does not meet the security requirements.
    - `409 Conflict` if a user with the given username already exists.
- `/users/<username>/rights/<right_name>` [`GET`]

  Gets whether a given user has a certain right or not.
  - Parameters:
    - `username` [path] (`str`): The user name.
    - `right_name` [path] (`str`): The right name.
  - Returns:
    - `200 OK` if the user has the specified right.
    - `404 Not Found` if the user does not have the right, the user does not exist, or the right does not exist.
- `/users/<username>/rights/<right_name>` [`POST`]

  Grants a certain right to a given user.
  - Security:
    - The requestor must have the `AdminRights` right.
  - Parameters:
    - `username` [path] (`str`): The user name.
    - `right_name` [path] (`str`): The right name.
    - `session_id` [form data] (`str`): The requestor session.
  - Returns:
    - `200 OK` if the user was granted the specified right successfully.
    - `401 Unauthorized` if the requestor does not meet the security requirements or no session was provided.
    - `404 Not Found` if the user does not exist, or the right does not exist.
- `/users/<username>/rights/<right_name>` [`DELETE`]

  Revokes a certain right from a given user.
  - Security:
    - The requestor must have the `AdminRights` right.
  - Parameters:
    - `username` [path] (`str`): The user name.
    - `right_name` [path] (`str`): The right name.
    - `session_id` [form data] (`str`): The requestor session.
  - Returns:
    - `200 OK` if the user was revoked the specified right successfully.
    - `401 Unauthorized` if the requestor does not meet the security requirements or no session was provided.
    - `404 Not Found` if the user does not exist, or the right does not exist.
