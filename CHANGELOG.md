## [0.1.6] - 2023-08-10

### Fixed

- GET swt request now returns an array of on exact line of the swt table with index of `tick`, given in request.
- if swt table happen to be sparse, smc now increases the density of it according to its schema.

### Changed

- if `tick` sent not as `digit`, plugin returns an error message.
- if `tick` is not sent at all, default value of `-1` is used.

## [0.1.5] - 2023-08-04

### Fixed
- too many values to unpack error

## [0.1.4] - 2023-08-03

### Fixed
- added support of string enclosed with singular quotes used in `select` values. Example: regular string `"text"`, string from `select` entry: `"'text''"`. Never use singular quotes to give `string` values, always double. Singular quotes used in OTL to define columns only.

### Changed
- replaced import of data from external swt tables with simple swt calc

## [0.1.3] - 2023-07-27

### Changed

- update of the `ot_simple_connector` version to 0.1.12
- added `property_globals` section to dtcd_simple_math_core.conf.example. Please update your *.conf file.

### Fixed

- parsing inPort values when not surrounded by whitespaces. Example: `(inPort1 + inPort2 + inPort3) / 100` evaluated to `(inPort1 + 'DataNode_1.value' + inPort3) / 100`.
- parsing float values as float values, not strings. Example: `eval 'DataNode_1.value' = '0.6'` did not evaluate.

## [0.1.2] - 2023-07-20

### Changed

- `ot_simple_connector` version updated up to 0.1.11

### Fixed

- 400 error on a first calc of a graph with DataLakeNode in it

## [0.1.1] - 2023-07-18

### Changed

- `ot_simple_connector` version updated up to 0.1.10

## [0.1.0] - 2023-07-10

### Added

- Creation of the swt table on a first graph calculation if it does not exist.
- Parametrized `otl_create_fresh_swt` template and regexp strings at the config file.
- Documentation.
- Tests.
- Import data through `SWT` and `SWT Export` property request type without any custom actions or buttons, from
  properties of the nodes from a different graph if source graph has the same `_t` tick value as the latest tick of
  target graph.
- Import data through ports of the nodes.

### Fixed

- Cyrillic symbols usage problem.
- Parsing of the `email` string in the `expression` of the property of the noe fixed.

### Changed

- Graph calculation is only through the `POST` method to `/dtcd_simple_math_core/v1/graph/` url with `swt_name`
  and `graph` parameters required.
- SWT may be read only through the `GET` method to `/dtcd_simple_math_core/v1/swt/` url with `swt_name` parameter
  required.