# Data

This directory will contain [DuckDB](https://duckdb.org/) databases.

## DuckDB Databases

Two types of DuckDB databases are expected in this directory once extractions and transformations are completed: source databases and dbt databases.

There is currently only one source database, `sources.duckdb`.

Of the dbt databases, two versions will exist for each one: a development version and a production version.

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

### dbt Databases

The structure of the `transform` dbt project will determine the set of databases seen in the `dev/` and `prod/` directories. For more information on the rationale behind the data warehouse scheme, see the [README](../transform/README.md) in the `transform` project.

The dbt databases are as follows (applies to both development and production versions):

- `staging`
  - Contains the tables that are derived from dbt models of source data with the data cleaned up for use in intermediate dbt models.
  - Each schema in this database refers to a source, with each table related to the data found at that source.
  - This database also contains the `reference` schema, which is a schema housing tables that only have static data.
  - All tables in this database are materialized from dbt models as views in order to pull in the freshest data possible whenever dbt is run.
- `intermediate`
  - Contains the tables from dbt models that are transformed from staging models beyond simple data cleaning. This will typically be expressed as aggregates, joins, etc.
  - Each schema in this database refers to the purpose the transformed tables will be used toward. In a business use case, this will most likely be the stakeholder requesting the data.
  - All tables in this database are materialized from dbt models as views to allow for any fresh data in the `staging` database to appear in these tables as well whenever dbt is run. Keeping a record of these intermediate tables allows us to troubleshoot any issues that may arise between a mart table and a staging table, which is also why these tables are not materialized as ephemeral tables (which is a valid alternative if data tracing is not a concern).
- `mart`
  - Contains the dbt models that will be exposed to end-users.
  - These tables should come from dbt models that are result of all other transformations done and loaded in the other two databases.
  - Each schema in this database also refers to the purpose the tables will be used toward. In a business use case, this will most likely be the stakeholder requesting the data.
  - All tables in this database will either be materialized from dbt models as tables or incremental tables. This will enable faster query times as tables contain the actual data that the SQL engine can query through. If these tables were instead materialized as views, this would require *all* parent transformations to be rerun. As tables, we can directly store the result of all upstream queries. The downside is that we will not obtain any fresh data in a mart table until all upstream models have been run.

#### Development

The development versions of the above dbt databases are intended to be run and written over during the development process. These databases are the default target for `dbt run`.

#### Production

The production versions of the above dbt databases should **not** be targeted unless necessary. These will be exposed to end-users and applications like business intelligence (BI) tools. This repo uses [Streamlit](../streamlit/README.md) as an interactive visualization tool. These databases will be written over on a regular cadence in order to pull in batches of fresh data.

## FAQ

### "Why is the data not committed to the repo?"

There are a number of reasons that the DuckDB databases aren't committed to the repo:

- While the DuckDB files may be small now, committing files that can grow to large sizes will cause issues with Github (and they *will* grow),
- I do not feel comfortable storing data I do not personally generate in a public repository owned by me,
- Running the extraction scripts and dbt models are trivial.

The **only** exception to the above reasons will be dbt `seed` models as they will be static CSV files that contain simple reference data.

### "Why create this directory at all?"

I wanted a central location for my data that was not buried within either the extract or transform projects so that I could access all of the data easily across all of the projects found in this repo. Technically, keeping each database in their respective projects makes for a good separation of concerns (for example, keeping `sources.duckdb` in the extract project would make it obvious that the database will not be written into by the dbt transform project). However, this adds a little bit of cognitive overhead and makes for an annoying time managing paths. This directory can also be thought of as a local representation of how data warehouses might present their databases.
