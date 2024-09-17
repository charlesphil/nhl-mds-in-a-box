"""Extracts and loads data from NHL-owned APIs."""

import logging
from typing import Generator

import dlt
from dlt.sources.helpers import requests
from dlt.sources.rest_api import (
    RESTAPIConfig,  # type: ignore[reportPrivateImportUsage]
    rest_api_resources,
)

logger = logging.getLogger("dlt")


def main() -> None:
    """."""
    logger.info("Starting nhl_api pipeline.")
    load_nhl_stats_api()
    logger.info("Pipeline completed.")


@dlt.source
def nhl_stats_api() -> Generator:
    """."""

    config: RESTAPIConfig = {
        "client": {"base_url": "https://api.nhle.com/stats/rest/en/"},
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
        },
        "resources": [
            {"name": "teams", "endpoint": {"path": "team"}},
            {"name": "games", "endpoint": {"path": "game"}},
            {
                "name": "skaters",
                "primary_key": "playerId",
                "endpoint": {
                    "path": "skater/summary",
                    "params": {
                        "cayenneExp": "",
                        "limit": "-1",
                        "isAggregate": "true",
                        "isGame": "true",
                    },
                },
            },
            {
                "name": "goalies",
                "primary_key": "playerId",
                "endpoint": {
                    "path": "goalie/summary",
                    "params": {
                        "cayenneExp": "",
                        "limit": "-1",
                        "isAggregate": "true",
                        "isGame": "true",
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_nhl_stats_api() -> None:
    """."""
    pipeline = dlt.pipeline(
        pipeline_name="nhl_apis",
        destination=dlt.destinations.duckdb("../data/sources.duckdb"),
        dataset_name="nhl_stats_api",
    )

    load_info = pipeline.run(nhl_stats_api())
    logger.info(load_info)


@dlt.source
def nhl_web_api() -> Generator:
    """."""

    config: RESTAPIConfig = {
        "client": {"base_url": "https://api-web.nhle.com/v1/"},
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
        },
        "resources": [
            {"name": "teams", "endpoint": {"path": "team"}},
            {"name": "games", "endpoint": {"path": "game"}},
            {
                "name": "skaters",
                "primary_key": "playerId",
                "endpoint": {
                    "path": "skater/summary",
                    "params": {
                        "cayenneExp": "seasonId=20232024",
                        "limit": "-1",
                        "isAggregate": "true",
                        "isGame": "true",
                    },
                },
            },
            {
                "name": "goalies",
                "primary_key": "playerId",
                "endpoint": {
                    "path": "goalie/summary",
                    "params": {
                        "cayenneExp": "seasonId=20232024",
                        "limit": "-1",
                        "isAggregate": "true",
                        "isGame": "true",
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_nhl_web_api() -> None:
    """."""
    pipeline = dlt.pipeline(
        pipeline_name="nhl_apis",
        destination=dlt.destinations.duckdb("../data/sources.duckdb"),
        dataset_name="nhl_web_api",
    )

    load_info = pipeline.run(nhl_stats_api())
    logger.info(load_info)


if __name__ == "__main__":
    main()
