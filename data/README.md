# Data

This directory will contain [DuckDB](https://duckdb.org/) databases and this README contains entity relationship diagrams (ERDs) for schemas in those databases where possible.

## DuckDB Databases

Three DuckDB databases are expected in this directory once extractions and transformations are completed: `sources.duckdb`, `dev.duckdb` `prod.duckdb`.

### sources.duckdb

Contains all raw data obtained from various sources. Each source is represented by a schema within this database.

#### `nhl_api`

This schema contains data pulled from endpoints at two NHL-owned APIs. See [this README by Zmalski](https://github.com/Zmalski/NHL-API-Reference/blob/main/README.md) for an unofficial documentation of these APIs.

Tables:

- `teams`

### dev.duckdb

Development version of the production database where business logic can be developed into the appropriate tables and views. This repo uses the [transform](../transform/README.md) dbt project to create models for these tables and views.

### prod.duckdb

Production database of tables and views intended to be exposed to end-users and applications like business intelligence (BI) tools. This repo uses [Streamlit](../streamlit/README.md) as an interactive visualization tool.

## FAQ

### "Why is the data not committed to the repo?"

There are a number of reasons that the duckdb databases aren't committed to the repo:

- While the duckdb files may be small now, committing files that can grow to large sizes will cause issues with Github (and they *will* grow),
- I do not feel comfortable storing third-party data in a public repository,
- Running the extraction scripts and transformation models are trivial.

The only exceptions to the above reasons will be dbt `seed` models

### "Why create this directory at all?"

Because this repo is structured as a monorepo, I wanted a central location for my data that was not buried within either the `extract` or `transform` projects so that I could access all of the data easily across all of the projects found in this repo.
