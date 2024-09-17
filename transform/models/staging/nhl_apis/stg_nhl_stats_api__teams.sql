with

    source as (select * from {{ source("nhl_stats_api", "teams") }}),

    renamed as (
        select
            id,
            franchise_id
            full_name,
            league_id,
            raw_tricode,
            tri_code as tricode,
            to_timestamp(_dlt_load_id::double) as _dlt_load_time,
            _dlt_id
        from source
    )

select *
from renamed
