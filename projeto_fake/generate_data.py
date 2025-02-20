import csv
from faker import Faker
import random

fake = Faker('pt_BR')
num_registros = 50

estados = ['SP', 'RJ', 'MG', 'RS', 'PR']

nome_arquivo = 'fake_clientes.csv'

with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(['id', 'nome', 'idade', 'estado'])
    
    for i in range(1, num_registros + 1):
        nome = fake.first_name()
        idade = random.randint(18, 70) 
        estado = random.choice(estados)
        escritor.writerow([i, nome, idade, estado])

print(f'Dados fake gerados e salvos em {nome_arquivo}')
