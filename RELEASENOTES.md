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