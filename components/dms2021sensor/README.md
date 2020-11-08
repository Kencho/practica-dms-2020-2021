# DMS 2020-2021 Sensor Service

This service provides sensing functionalities to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2021sensor/config.yml`. This path is thus usually `${HOME}/.config/dms2021sensor/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `host` (mandatory): The service host.
- `port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.

## Running the service

Just run `dms2021sensor` as any other program.

## REST API specification

This service exposes a REST API so other services/applications can interact with it.

_(TO DO)_
