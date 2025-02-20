-- Seleciona os clientes com idade maior ou igual a 40
select
    id,
    nome,
    idade,
    estado
from {{ ref('fake_clientes') }}
where idade >= 40
