# Data

This directory will contain [DuckDB](https://duckdb.org/) databases and this README contains entity relationship diagrams (ERDs) for schemas in those databases where possible.

## DuckDB Databases

Three DuckDB databases are expected in this directory once extractions and transformations are completed: `sources.duckdb`, `dev.duckdb` `prod.duckdb`.

### sources.duckdb

Contains all raw data obtained from various sources. Each source is represented by a schema within this database.

#### `nhl_stats_api`

This schema contains data pulled from the NHL Stats API. See [this README by Zmalski](https://github.com/Zmalski/NHL-API-Reference?tab=readme-ov-file#nhl-stats-api-documentation) for an unofficial documentation of this API.

Tables:

- `games`
- `goalies`
- `skaters`
- `teams`
- `team_season_stats`

#### `nhl_search_api`

This schema contains data pulled from an API the NHL uses to power search results on their website. Only seems to be used on the [Players](https://www.nhl.com/player) page at the moment.

Tables:

- `players`

### dev.duckdb

Development version of the production database where business logic can be developed into the appropriate tables and views. This repo uses the [transform](../transform/README.md) dbt project to create models for these tables and views. This database is the default target for `dbt run`.

### prod.duckdb

Production database of tables and views intended to be exposed to end-users and applications like business intelligence (BI) tools through specific schemas. This repo uses [Streamlit](../streamlit/README.md) as an interactive visualization tool. This database must be explicitly targeted by dbt in order for changes to occur.

## FAQ

### "Why is the data not committed to the repo?"

There are a number of reasons that the DuckDB databases aren't committed to the repo:

- While the DuckDB files may be small now, committing files that can grow to large sizes will cause issues with Github (and they *will* grow),
- I do not feel comfortable storing third-party data in a public repository,
- Running the extraction scripts and dbt models are trivial.

The only exceptions to the above reasons will be dbt `seed` models as they will be static CSV files that contain simple reference data.

### "Why create this directory at all?"

I wanted a central location for my data that was not buried within either the extract or transform projects so that I could access all of the data easily across all of the projects found in this repo. Technically, keeping each database in their respective projects makes for a good separation of concerns (for example, keeping `sources.duckdb` in the extract project would make it obvious that the database will not be written into by the dbt transform project). However, this adds a little bit of cognitive overhead and makes for an annoying time managing paths. This directory can also be thought of as a local representation of how data warehouses might present their databases.
