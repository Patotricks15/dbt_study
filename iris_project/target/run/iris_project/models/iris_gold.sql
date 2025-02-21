
  create view "iris"."public"."iris_gold__dbt_tmp"
    
    
  as (
    with silver as (
    select *
    from "iris"."public"."iris_silver"
)

select
    *,
    case species
        when 'setosa' then 1
        when 'versicolor' then 2
        when 'virginica' then 3
        else null
    end as species_id
from silver
  );