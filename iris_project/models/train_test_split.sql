with iris_gold as (
    select *
    from {{ ref('iris_gold') }}
)
select
    *,
    case
        when random() < 0.8 then 'train'
        else 'test'
        end as split
from iris_gold