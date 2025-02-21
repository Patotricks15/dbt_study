with train_test_split as (
    select *
    from "iris"."public"."train_test_split"
)
select
    sepal_length,
    sepal_width,
    petal_length,
    petal_width,
    sepal_ratio,
    petal_ratio,
    species,
    species_id
from train_test_split
where split = 'train'