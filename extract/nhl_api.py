"""Extracts and loads data from NHL-owned APIs."""

import logging
import sys

import duckdb
import pandas as pd
import requests

logger = logging.getLogger("nhl_api")
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
    level=logging.INFO,
)


def main() -> None:
    """Extract and load data from the NHL APIs.

    This module is structured such that each function operates as their
    own sources.

    """
    # duckdb housekeeping
    con = duckdb.connect("../data/sources.duckdb")
    con.execute("create schema if not exists nhl_api")
    logger.info("Initialized duckdb connection.")

    session = requests.Session()
    logger.info("Initialized session.")

    # endpoints
    teams(session, con)

    con.close()

    logger.info("Extraction and loading completed!")


def teams(
    session: requests.Session,
    con: duckdb.DuckDBPyConnection,
) -> None:
    """Extract and load basic information on NHL teams.

    Includes all present and historical teams.
    Also cleans up the data for database loading.

    Args:
        session (requests.Session): A session object.
        con (duckdb.DuckDBPyConnection): A connection to the duckdb database.

    """
    logger.info("Retrieving teams data...")
    response = session.get("https://api.nhle.com/stats/rest/en/team")
    response.raise_for_status()

    try:
        raw = response.json()
    except requests.JSONDecodeError:
        logger.exception(
            "Response is not decodable as JSON! "
            "Check to make sure the endpoint hasn't changed.",
        )
        sys.exit(1)

    logger.info("Teams data retrieved. Loading into database...")

    df_to_load = (  # noqa: F841
        pd.DataFrame.from_dict(raw["data"])
        .fillna(0)  # normalize null values to 0
        .astype({"franchiseId": int})  # convert column back to original dtype
    )

    con.execute("create table if not exists teams as select * from df_to_load")
    con.execute("insert into teams select * from df_to_load")


if __name__ == "__main__":
    main()
