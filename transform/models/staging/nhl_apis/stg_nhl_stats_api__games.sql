with

    source as (select * from {{ source("nhl_stats_api", "games") }}),

    renamed as (
        select
            id,
            eastern_start_time,
            game_date,
            game_number,
            game_schedule_state_id,
            case
                when game_schedule_state_id = 1 then 'required'
                when game_schedule_state_id = 2 then 'if needed'
                when game_schedule_state_id = 3 then 'postponed'
                when game_schedule_state_id = 5 then 'cancelled'
            end as game_schedule_state,
            game_state_id,
            case
                when game_state_id = 1 then 'unplayed'
                when game_state_id = 3 then 'in progress'
                when game_state_id = 4 then 'tied'
                when game_state_id = 6 or game_state_id = 7 then 'played'
            end as game_state,
            game_type as game_type_id,
            case
                when game_type_id = 1 then 'preseason'
                when game_type_id = 2 then 'regular season'
                when game_type_id = 3 then 'stanley cup'
                when game_type_id = 4 then 'all-star'
                when game_type_id = 6 then 'world cup of hockey group stage'
                when game_type_id = 7 then 'world cup of hockey knockout stage'
                when game_type_id = 8 then 'world cup of hockey pre-tournament'
                when game_type_id = 9 then 'winter olympics'
                when game_type_id = 10 then 'young stars'
                when game_type_id = 12 then 'women all-star'
                when game_type_id = 13 then '2004-05 nhl season'
                when game_type_id = 14 then 'canada cup'
                when game_type_id = 18 then 'off-season exhibition tour'
                when game_type_id = 19 then '2025 nhl 4 nations face-off'
            end as game_type,
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
