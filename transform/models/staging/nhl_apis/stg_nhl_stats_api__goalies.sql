with

    source as (select * from {{ source("nhl_stats_api", "goalies") }}),

    renamed as (
        select
            assists,
            games_played,
            games_started,
            goalie_full_name as full_name,
            goals,
            goals_against,
            goals_against_average,
            last_name,
            losses,
            ot_losses,
            penalty_minutes,
            player_id,
            points,
            save_pct,
            saves,
            shoots_catches,
            shots_against,
            shutouts,
            ties,
            time_on_ice,
            wins,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id
        from source
    )

select *
from renamed
