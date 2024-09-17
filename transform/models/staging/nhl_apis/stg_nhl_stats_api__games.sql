with

    source as (select * from {{ source("nhl_stats_api", "games") }}),

    renamed as (
        select
            id,
            eastern_start_time,
            game_date,
            game_number,
            game_schedule_state_id,
            game_state_id,
            game_type,
            home_score,
            home_team_id,
            period,
            season,
            visiting_score,
            visiting_team_id,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id
        from source
    )

select *
from renamed
