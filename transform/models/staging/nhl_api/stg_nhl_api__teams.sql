with

source as (
    select * from {{ source('nhl_api', 'teams') }}
)

select * from source
