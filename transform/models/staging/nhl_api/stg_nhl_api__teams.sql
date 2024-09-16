with

source as (
    select * from {{ source('nhl_api', 'teams') }}
),

renamed as (
    select
        id,
        franchiseId::int as franchise_id,
        fullName as full_name,
        leagueId as league_id,
        rawTricode as raw_tricode,
        triCode as tricode
    from source
)

select * from renamed
