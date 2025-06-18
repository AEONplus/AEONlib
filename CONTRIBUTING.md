# Contribution Guide
All contributions are subject to the code of conduct.

## Adding a Facility
Before implementing a new facility it may be worth studying the current facility implementations for common practices and examples.

### Declaring dependencies
AEONlib uses [dependency groups](https://peps.python.org/pep-0735/) to separate the dependencies of each facility module. This is because it is unlikely that one will utilize all facilities offered by AEONlib. Because some facilities have completely unique transitive dependencies, this ends up saving a lot of unnecessary package installations.

A facility might not need any additional dependencies - the base group includes [httpx](https://www.python-httpx.org/) for http requests and [Pydantic/](https://pydantic.dev/) for data de/serialization.

If the facility does need additional dependencies, add a group to `pyproject.toml` and list them there. Afterward make a note in the facility's README section with the name of the group library consumers will need to install.

### Configuration values
Most facilities will require some kind of runtime configuration, such as authentication keys. AEONlib leverages [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for settings management. Any facility that requires runtime configuration must place the keys in `src/aenlib/conf.py`. Reading from files or environmental variables directly inside a facility will not be accepted.

Using to `conf.py` ensures that consumers have a consistent and facility agnostic means of providing configuration to AEONlib powered applications, whether it be via .env files, environmental variables, or direct instantiation. 

### Define data models
Facilities should attempt to avoid making excessive use of plain Python dictionaries or JSON to model data. Wherever possible leverage [Pydantic/](https://pydantic.dev/) to define types that consumers can pass to your facility functions. The more well defined your models, the better experience the facility users will have. Well defined models eliminate malformed data structures, prevent typos and provide code completion in developer tools. They can also provide rich validation rules, sometimes negating the need for online validation altogether.

AEONlib also provides several [data types](https://github.com/AEONplus/AEONlib/blob/main/src/aeonlib/types.py) that improve Pydantic models:
1. `aeonlib.types.Time` using this type in a Pydantic model allows consumers to pass in `astropy.time.Time` objects as well as `datetime` objects. The facility can then decide how the time is serialized to match whatever specific format is required.
2. `aeonlib.types.Angle` similarly to the `Time` type, this allows consumers to pass in `astropy.coordinates.Angle` types as well as floats, the facility can then decide how to serialize the type.

These types eliminate the need for the facility user to need to remember which exact format a facility requires (time in hms? Or ISO UTC?) and simply pass in higher level objects instead.

Aeonlib also defines a few high level models: `aeonlib.models.Window` and several target types. If a facility can translate these models or even use them directly it should. This means a consumer of Aeonlib can define these high level models once, for example from a data alert stream, and use them with every facility for which they want to perform observations.

### Write the facility module
The facility class should contain all of the business logic of consuming data models and interacting with the facility itself.

This is the most loosely defined set of functionality as every facility is different. Here are a few guidelines:

1. Embrace the [Principle of Least Surprise](https://en.wikipedia.org/wiki/Principle_of_least_astonishment). Does the facility already provide a client library or well known API? In most cases, it's preferable that it work similarly in AEONlib - thus creating less cognitive overhead for consumers of the facility API. This is more art than science, then again sometimes science is more art than science...
2. Expose the full power of the facility. Facilities should not hide the details behind obtuse abstractions. Remember, the person using AEONlib to interact with a facility is a being of considerable intelligence. Provide convenient abstractions where possible but also allow access to the underlying details. This is a library, not an application.  

### Add online tests
It's important to include tests that prove that the facility is functional. Additionally, writing the tests is a good way to write the facility as it's being developed and it is good documentation of how it's meant to be used.

See the other facility's `test_online` modules for examples. Tests that use `pytest.mark.online` will not be run during normal test runs or CI, so you do not need to worry about them hitting your facility unnecessarily. There is an additional mark: `pytest.mark.side_effect` which can be used to mark tests that modify remote data which you can use to filter those tests if you'd like.

Online facility tests most likely require authentication credentials. It is _not_ necessary to include these credentials in any pull requests. However project maintainers may request them in order to verify such tests pass.

### Open a PR!
We look forward to your contribution!
 