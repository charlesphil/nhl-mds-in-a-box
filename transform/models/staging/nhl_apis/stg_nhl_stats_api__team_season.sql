with

    source as (select * from {{ source('nhl_stats_api', 'team_season') }}),

    renamed as (
        select
            games_played,
            goals_against,
            goals_against_per_game,
            goals_for,
            goals_for_per_game,
            losses,
            penalty_kill_net_pct,
            penalty_kill_pct,
            point_pct,
            points,
            power_play_net_pct,
            power_play_pct,
            regulation_and_ot_wins,
            season_id,
            shots_against_per_game,
            shots_for_per_game,
            team_full_name,
            team_id,
            ties,
            wins,
            wins_in_regulation,
            wins_in_shootout,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id,
            faceoff_win_pct,
            ot_losses
        from source
    )

select *
from renamed
