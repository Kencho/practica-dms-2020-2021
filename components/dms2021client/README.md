# DMS 2020-2021 Client application

This applicationserves as the control console for the different services of the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2021client/config.yml`. This path is thus usually `${HOME}/.config/dms2021client/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `debug`: If set to true, the service will run in debug mode.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.
- `sensors`: A dictionary with the configuration needed to connect to the different sensor services. Each key identifies a sensor, and their values are themselves dictionaries with the connection information:
  - `host` and `port`: Host and port used to connect to the service.

## Running the service

Just run `dms2021client` as any other program.
