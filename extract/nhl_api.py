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
    session = requests.Session()
    logger.info("Initialized session.")
    teams_df = extract_teams(session)
    load_teams(teams_df)


def extract_teams(session: requests.sessions.Session) -> pd.DataFrame:
    """Retrieve basic information on NHL teams.

    Includes all present and historical teams.
    This function also cleans up the data for database loading.

    Args:
        session (requests.session.Session): A session object.

    Returns:
        pd.DataFrame: A DataFrame containing the normalized returned response
            data.

    """
    logger.info("Retrieving team data...")
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

    return (
        pd.DataFrame.from_dict(raw["data"])
        .fillna(0)  # normalize data here, some have nulls
        .astype({"franchiseId": int})  # convert column back to original dtype
    )


def load_teams(df: pd.DataFrame) -> None:
    """Load the normalized team DataFrame into the database.

    Args:
        df (pd.DataFrame): DataFrame containing normalized data from source.

    """
    logger.info("Loading DataFrame into database...")

    with duckdb.connect("../data/sources.duckdb") as conn:
        conn.execute("create schema if not exists nhl_api")
        conn.execute("use nhl_api")
        conn.execute("create table if not exists teams as select * from df")
        conn.execute("insert into teams select * from df")


if __name__ == "__main__":
    main()
