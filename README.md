# DataCAD_simple_math_core

Plugin for [complex rest](https://github.com/ISGNeuroTeam/complex_rest/tree/develop)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Deploy [complex rest](https://github.com/ISGNeuroTeam/complex_rest/tree/develop)

### Installing

* Make symlink for ./DataCAD_simple_math_core/DataCAD_simple_math_core in plugins directory
* Run complex rest server

## Running the tests
Run all tests:
```bash
python ./complex_rest/manage.py test ./plugin_dev/dtcd_simple_math_core/tests --settings=core.settings.test
```

## Deployment

* Make plugin archive:
```bash
make pack
```
* Unpack archive into complex_rest plugins directory

## Built With

* [Django](https://docs.djangoproject.com/en/3.2/) - The web framework used


## Contributing

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors
Starchenkov Andrey
Serditov Nikita

## License

[OT.PLATFORM. License agreement.](LICENSE.md)

## Features
- Creates swt table when graph is calculated first time and has no swt table.
- Supports importing data through inPort/outPort in terms of one graph. As it works with data from swt table, not graph, then sometimes it requires two consequent graph calculations to calc all imported data.

## Setup of the plugin
Go to dtcd_simple_math_core/dtcd_simple_math_core.conf and edit it:
- set logging `level` at the [logging] section
- set parameters of [ot_simple_connector], usually `host` is `localhost`, all the rest parameters get from your administrator
- if you are using `smc` at FGK production server, you must change the `otl_create_fresh_swt` of the [graph_globals] section to `| readFile format=json path=wide | fields _sn, _t | writeFile format=json path=SWT/` 