
  create view "iris"."public"."train_test_split__dbt_tmp"
    
    
  as (
    with iris_gold as (
    select *
    from "iris"."public"."iris_gold"
)
select
    *,
    case
        when random() < 0.8 then 'train'
        else 'test'
        end as split
from iris_gold
  );