# Extract

This project contains the Python scripts used to extract data from various NHL sources and load them into [DuckDB](https://duckdb.org/) databases to power the `transform` and `streamlit` projects.

I [migrated to dlt](https://dlthub.com/) to power the extraction once the folks at dltHub released version 1.0.0. Since I exclusively used (semi) public REST APIs from the NHL, `dlt` seemed like a good drop-in replacement to my previous extraction scripts as it appears to be extremely robust in pulling data from REST APIs. For details on how I ran the extraction prior to migrating to `dlt`, [see the Legacy section below](#legacy).

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

## Legacy
