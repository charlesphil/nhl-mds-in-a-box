with

    source as (select * from {{ source("nhl_api", "teams") }}),

    renamed as (
        select
            id,
            franchiseid::int as franchise_id,
            fullname as full_name,
            leagueid as league_id,
            rawtricode as raw_tricode,
            tricode as tricode
        from source
    )

select *
from renamed
