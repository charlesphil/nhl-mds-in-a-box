with

    source as (select * from {{ source("nhl_stats_api", "skaters") }}),

    renamed as (
        select
            assists,
            ev_goals,
            ev_points,
            faceoff_win_pct,
            game_winning_goals,
            games_played,
            goals,
            last_name,
            ot_goals,
            penalty_minutes,
            player_id,
            plus_minus,
            points,
            points_per_game,
            position_code,
            pp_goals,
            pp_points,
            season_id,
            sh_goals,
            sh_points,
            shooting_pct,
            shoots_catches,
            shots,
            skater_full_name as full_name,
            team_abbrevs,
            time_on_ice_per_game,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id
        from source
    )

select *
from renamed
