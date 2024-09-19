with

    source as (select * from {{ source('nhl_search_api', 'players') }}),

    renamed as (
        select
            player_id::integer as player_id,
            name as full_name,
            position_code,
            case
                when position_code = 'C' then 'center'
                when position_code = 'D' then 'defense'
                when position_code = 'R' then 'right wing'
                when position_code = 'L' then 'left wing'
                when position_code = 'G' then 'goalie'
            end as position,
            active,
            height,
            height_in_inches,
            height_in_centimeters,
            weight_in_pounds,
            weight_in_kilograms,
            birth_city,
            birth_state_province,
            birth_country,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id,
            last_season_id,
            sweater_number,
            last_team_id,
            last_team_abbrev,
            team_id,
            team_abbrev
        from source
    )

select *
from renamed
