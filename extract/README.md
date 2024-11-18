# Extract

This project contains the Python scripts used to extract data from various NHL sources and load them into [DuckDB](https://duckdb.org/) databases to power the `transform` and `streamlit` projects.

I [migrated to dlt](https://dlthub.com/) to power the extraction once the folks at dltHub released version 1.0.0. Since I exclusively used (semi) public REST APIs from the NHL, `dlt` seemed like a good drop-in replacement to my previous extraction scripts as it appears to be extremely robust in pulling data from REST APIs. For details on how I ran the extraction prior to migrating to `dlt`, [see the Legacy section below](#legacy).

See [this README by Zmalski](https://github.com/Zmalski/NHL-API-Reference?tab=readme-ov-file#nhl-stats-api-documentation) for an unofficial documentation of the NHL Stats API.

## How This Project Interacts With the Rest of the Repository

The script can be manually run via `poetry run python nhl_apis.py`, and should be run this way if this project is not being interfaced with Airflow. However, the preferred way to run the data extraction is through scheduled Airflow tasks.

## dlt Pipeline

I modeled the script after the [example found in the dlt docs for REST APIs](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic). There are two main parts to each REST API source: the definition and the pipeline.

### Defining Sources

Sources are defined by configuring the `RESTAPIConfig` object. There are three main parts to the object: the client, any resource defaults, and the resources.

- `client`
  - This part will hold the details necessary to connect to all endpoints of an API.
  - Common elements are the base URL, any required headers, authentication if necessary, and how to paginate through results if needed.
- `resource_defaults`
  - This optional part will configure default values for each and every resource in the source.
  - Elements include shared primary keys, how to write load data to the destination, and parameters used across all resources.
- `resources`
  - These can be thought of as the "endpoints."
  - Each resource should be listed and any resource-specific configuration should be defined here.

### Creating the Pipeline

`dlt` makes this part incredibly easy to implement by providing one simple function, `dlt.pipeline()`.

There is one caveat which is specific to this project.

When defining the load destination for the extracted data, we must provide two parameters: `destination` and `dataset_name`.
We can think of `destination` as the database and `dataset_name` as the schema in which to land our extracted data into.
Because we are dealing with DuckDB databases, the *default* value for DuckDB will only create the database in the same directory as the script.
Since we are trying to point to a custom path (`../data/`), this requires importing the dlt duckdb module. Only then can the path be customized.

## Configuring `dlt`

`dlt` reads from `config.toml` which can be found in the `.dlt/` directory. This configuration file is intended to be used by pipelines to access common, non-sensitive settings such as paths, hosts, URLs, and so on. The only two settings in this file so far are `dlthub_telemetry` and `log_level`.

`dlthub_telemetry` [phones home to dltHub](https://dlthub.com/docs/reference/telemetry#what-we-send-when) and provides various runtime metrics and system information. This setting is unfortunately **opt-out** instead of opt-in, so it is set to false here.

`log_level` sets the level in which to output logging information to the console. This has been set to "INFO" to track all pipeline actions.

In the event that credentials or other sensitive information is required when running a pipeline, create a `secrets.toml` file in the `.dlt/` directory. This file should *not* be committed to the repo and is already included in the root level gitignore. [See the documentation](https://dlthub.com/docs/general-usage/credentials/setup#secretstoml-and-configtoml) for more information on configuring secrets.

## Legacy

The `do_not_use_nhl_api.py` script used to pull teams data from the same APIs as the ones found in the `dlt` script.
The way this was achieved was by sending requests to the endpoints and storing the results in dataframes.

DuckDB provides a Python API and is used in the script to initialize and form a connection to an in-memory database that writes to disk. This script was also my attempt at implementing a custom logger and to handle various edge-case failures.

Since `dlt` handles all of the same work in a robust and well-tested package, there was no need to continue on reinventing the wheel and spending effort on something the open-source community has already provided.

The script remains in the repo as an example of a minimalist version of what `dlt` does behind the scenes. Feel free to run the script manually to look at the DuckDB database (which will be created in the same directory as the script), but this script will never be run by the data orchestration tool and will remain as a proof of concept for REST API data ingestion.
