## [0.1.0] - 2023-07-10

### Added
- Creation of the swt table on a first graph calculation if it does not exist.
- Parametrized `otl_create_fresh_swt` template and regexp strings at the config file.
- Documentation.
- Tests.

### Fixed
- Cyrillic symbols usage problem.

### Changed
- Graph calculation is only through the `POST` method to `/dtcd_simple_math_core/v1/graph/` url with `swt_name` and `graph` parameters required.
- SWT may be read only through the `GET` method to `/dtcd_simple_math_core/v1/swt/` url with `swt_name` parameter required.