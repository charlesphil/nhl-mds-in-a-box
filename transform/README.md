# Transform - dbt Project

This is the [dbt core](https://docs.getdbt.com/docs/introduction) project used to transform source data into data models based on required business logic.

## Getting Started

Once the Poetry environment has been set up, create a file in your `~/.dbt/` directory named `profiles.yml`.

Copy the contents of `profiles_template.yml` into `profiles.yml`. Here it is again for convenience:

```yml
nhl_mds_in_a_box_transform:
  outputs:
    dev:
      type: duckdb
      path: ../data/dev.duckdb
      attach:
        - path: ../data/sources.duckdb
      threads: 1

    prod:
      type: duckdb
      path: ../data/prod.duckdb
      attach:
        - path: ../data/sources.duckdb
      threads: 4

  target: dev
```

Then, with the working directory set to this current directory, run:

```console
poetry run dbt deps
```

ss
