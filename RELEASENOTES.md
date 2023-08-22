## [0.1.9] - 2023-08-22

### Added 
- `time_offset` parameter to establish the difference between timezone where `_t` column values of the `wide` swt table were generated and `utc` timezone.

### Changed
- now `PREVIOUS_MONTH` leads to fill the graph with values of the row of swt table which `_t` value is previous to current time **considering timezone**. So if today is 2nd of August 2023, then values from row with `1688158800` (30th of June 2023 21:00:00) at `_t` column will be used.

## [0.1.8] - 2023-08-15

### Changed

- graph is filled with values of the different row of the swt table now, depending on `swt_line_index` config parameter.
  - `PREVIOUS_MONTH` leads to fill the graph with values of the row of swt table which `_t` value is previous to current time. So if today is 2nd of August 2023, then values from row with `1690837200` (31st of July 2023) at `_t` column will be used 
  - `LAST` leads to fill graph with values of the last row of current swt table. Which may be **not the latest**.     

## [0.1.7] - 2023-08-10

### Fixed

- GET swt request now returns **an array** of an exact line of the swt table with index of `tick`, given in request.

### Changed

- if `tick` sent not as `digit`, plugin returns an error message.
- if `tick` is not sent at all, default value of `-1` is used.

## [0.1.6] - 2023-08-09

### Fixed

- GET swt request now returns exact line of the swt table with index of `tick`, given in request
- if swt table happen to be sparse, smc now increases the density of it according to its schema

## [0.1.5] - 2023-08-04

### Fixed

- too many values to unpack error

## [0.1.4] - 2023-08-03

### Changed
- replaced import of data from external swt tables with simple swt calc

## [0.1.3] - 2023-07-27

### Changed
- update of the `ot_simple_connector` version to 0.1.12

### Fixed
- parsing inPort values when not surrounded by whitespaces. Example: `(inPort1 + inPort2 + inPort3) / 100` evaluated to `(inPort1 + 'DataNode_1.value' + inPort3) / 100`.
- parsing float values as float values, not strings. Example: `eval 'DataNode_1.value' = '0.6'` did not evaluate.


## [0.1.2] - 2023-07-20

### Changed
- update of the `ot_simple_connector` version to 0.1.11

### Fixed
- 400 error on a first calc of a graph with DataLakeNode in it

## [0.1.1] - 2023-07-18

### Changed
- update of the `ot_simple_connector` version to 0.1.10

## [0.1.0] - 2023-07-10

### New
- Creation of the swt table on a first graph calculation if it does not exist.
- Parametrized `otl_create_fresh_swt` template and regexp strings at the config file.
- Documentation.
- Tests.
- Graph calculation is only through the `POST` method to `/dtcd_simple_math_core/v1/graph/` url with `swt_name` and `graph` parameters required.
- SWT may be read only through the `GET` method to `/dtcd_simple_math_core/v1/swt/` url with `swt_name` parameter required.
- Import data through `SWT` and `SWT Export` property request type without any custom actions or buttons, from properties of the nodes from a different graph if source graph has the same `_t` tick value as the latest tick of target graph.
- Import data through ports of the nodes.
- Parsing of the `email` string in the `expression` of the property of the noe fixed.