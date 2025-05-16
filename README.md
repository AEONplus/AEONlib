# AEONlib

A suite of modules to enable TDA/MMA observations

[code](https://github.com/AEONplus/AEONlib)

[issues](https://github.com/AEONplus/AEONlib/issues)

# Configuration
Many of the facilities and services accessed by AEONlib require specific configuration such
as api keys, urls, etc. All configuration can be supplied by either supplying a .env file or
setting environmental variables in the execution environment.

Example .env file:

```
AEON_LCO_API_ROOT="https://observe.lco.global/api"
AEON_LCO_TOKEN="my-api-token"
```

Or set environmental variables via the shell:

```bash
export AEON_LCO_API_ROOT="https://observe.lco.global/api"
export AEON_LCO_TOKEN="my-api-token"
```

All configuration keys are prefixed with AEON_ to prevent conflicts. See the documentation for
each service to see which configuration keys are available, or check
[conf.py](src/aeonlib/conf.py)

Environmental variables take precedence over .env files. See the
[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) documentation
for more details.


# Testing
This project uses [pytest](https://docs.pytest.org/) to run tests:

```bash
pytest
```

Some tests are marked as `online`. These tests make real http requests in order
to test interfaces with various services. To run them:

```bash
pytest -m online
```

A subset of `online` tests are marked as `side_effect`. These are tests that change data on remote
systems. For example, a test might be testing creating new observation requests, or updating the
status of one. You might want to disable these:

```bash
pytest -m "not side_effect"
```

CI does not run tests marked as online.

## Viewing logs during tests
Aeonlib turns on the Pytest
[Live Logging](https://docs.pytest.org/en/stable/how-to/logging.html#live-logs) feature.
By default any logging calls with a level above `WARNING` will be displayed to the console
during the test run. It may be helpful to display debug logging, especially if debugging remote
facilities or services:

```bash
pytest -m online --log-cli-level=debug
```

# Linting
All code is formatted via [ruff](https://astral.sh/ruff).

# Code Generation
Las Cumbres Observatory [instrument classes](src/aeonlib/ocs/lco/instruments.py)
are generated via the [generator.py](codegen/lco/generator.py) script. This script
takes as input the [OCS instruments api](https://observe.lco.global/api/instruments/)
in order to produce definitions of all instruments currently available on the network.

To update the definitions, first make sure you have installed the `codegen` dependency
group:

```bash
uv sync --group codegen  # or poetry install --with codegen
```

This ensures regular users of the library do not need to install these dependencies.

The `generate.py` script takes as input JSON as produced by the instruments endpoint:

```bash
codegen/lco/generator.py instruments.json
```

Or directly from stdin using a pipe:

```bash
curl https://observe.lco.global/api/instruments/ | codegen/lco/generator.py
```

If the output looks satisfactory, you can redirect the output to overwrite the
LCO instruments definition file:

```bash
curl https://observe.lco.global/api/instruments/ | codegen/lco/generator.py > src/aeonlib/ocs/lco/instruments.py
```
# Supported Facilities

This list is a work in progress.

## Las Cumbres Observatory (LCO)

### Dependency group
Las Cumbres Observatory requires no additional dependency groups to be installed.

### Configuration Values
See [configuration](#configuration) for instructions on setting these values.

```python
lco_token: str = ""
lco_api_root: str = "https://observe.lco.global/api/"
```
### Helpful links

* [LCO Observation Portal](https://observe.lco.global/)
* [LCO Developer Documentation](https://developers.lco.global/)
* [OCS API Documentation](https://observatorycontrolsystem.github.io/api/observation_portal/)

## SOAR

SOAR is functionally the same as LCO, but has it's own set of instruments and be configured seperately.

### Dependency group
SOAR requires no additional dependency groups to be installed.

### Configuration Values
See [configuration](#configuration) for instructions on setting these values.

```python
soar_token: str = ""
soar_api_root: str = "https://observe.lco.global/api/"
```
Note: the soar API token will default to the same value as lco_token, if it is set.

## ESO (European Southern Observatory)

Full documentation: TODO

### Dependency Group
To use the ESO facility, you must install the `eso` group:
```bash
pip install aeonlib[eso]
uv sync --group eso
poetry install --with eso
```

### Configuration Values
See [configuration](#configuration) for instructions on setting these values.

```python
eso_environment: str = "demo"
eso_username: str = ""
eso_password: str = ""
```

### Helpul links

* [ESO Phase 2 API](https://www.eso.org/sci/observing/phase2/p2intro/Phase2API.html)
* [ESO Phase 2 Demo Application](https://www.eso.org/p2demo/home)
