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
- Support `SWT` and `SWT Export` data import from a different graph only if source graph has the same `_t` tick value as the latest `-t` tick value of the target swt table. Works with "Загрузка данных из соседних вкладок" custom action only.
- Support data import from data lake node. Works with "Загрузка данных из озера данных" custom action only.

## Setup of the plugin
Go to dtcd_simple_math_core/dtcd_simple_math_core.conf and edit it:
- set logging `level` at the [logging] section.
- set parameters of [ot_simple_connector], usually `host` is `localhost`, all the rest parameters get from your administrator.
- set `swt_line_index` parameter to `PREVIOUS_MONTH` if you need to fill graph with fact swt table values, or `LATEST` if you need to fill graph with random latest row of swt table.
- set `time_offset` parameter to show the difference between timezone used to set wide swt table `_t` column values and utc timezone. For example if `_t` values were generated in `utc+3` timezone, the `time_offset` must be set to `3`.