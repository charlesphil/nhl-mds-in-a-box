import dlt
import httpx
import requests
from rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_source,
    rest_api_resources,
)


# The API doesn't have an endpoint with a full list of player ids.
# We'll get around this by looking through the roster of each team.
TEAMS = []
response = requests.get('https://api.nhle.com/stats/rest/en/team')
for team in response.json()['data']:
        TEAMS.append(team['teamAbbrev']['default'])

print(TEAMS)


@dlt.transformer
async def rosters(team):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api-web.nhle.com/v1/roster/{team}/current")
        return response.json()


# def load_players() -> None:
    # pipeline = dlt.pipeline(
    #     pipeline_name="nhl_api"
    #     destination=dlt.destinations.duckdb("../data/sources.duckdb")
    #     dataset_name="nhl_api"
    # )


if __name__ == "__main__":
    # load_players()
    print(list(TEAMS | rosters()))
