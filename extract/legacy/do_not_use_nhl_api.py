"""Extracts and loads data from NHL-owned APIs.

Please note that this script was created before I used dlt in this project.

dlt has since released their first stable version (1.0.0), making this script
unnecessary.

"""

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
    con = duckdb.connect("sources.duckdb")
    con.execute("create schema if not exists nhl_api")
    con.execute("use nhl_api")
    logger.info("Initialized DuckDB connection.")

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
        con (duckdb.DuckDBPyConnection): A connection to the DuckDB database.

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

    df_to_load = pd.DataFrame.from_dict(raw["data"])  # noqa: F841

    con.execute("create table if not exists teams as select * from df_to_load")

    logger.info("Teams data successfully loaded.")


if __name__ == "__main__":
    main()
