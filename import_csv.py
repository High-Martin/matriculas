import os
import csv
import psycopg2
from django.conf import settings
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matriculados.settings')
django.setup()

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname=settings.DATABASES['default']['NAME'],
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['PASSWORD'],
    host=settings.DATABASES['default']['HOST'],
    port=settings.DATABASES['default']['PORT']
)
cursor = conn.cursor()

# Criar a tabela para os dados
cursor.execute("""
CREATE TABLE IF NOT EXISTS matriculas (
    id SERIAL PRIMARY KEY,
    estado VARCHAR(100),
    cidade VARCHAR(100),
    ies VARCHAR(255),
    sigla VARCHAR(50),
    organizacao VARCHAR(100),
    categoria_administrativa VARCHAR(100),
    nome_curso VARCHAR(255),
    nome_detalhado_curso VARCHAR(255),
    modalidade VARCHAR(50),
    grau VARCHAR(100),
    matriculas_2014 INTEGER,
    matriculas_2015 INTEGER,
    matriculas_2016 INTEGER,
    matriculas_2017 INTEGER,
    matriculas_2018 INTEGER,
    matriculas_2019 INTEGER,
    matriculas_2020 INTEGER,
    matriculas_2021 INTEGER,
    matriculas_2022 INTEGER
);
""")
conn.commit()

# Importar dados do CSV
csv_file = 'matriculas.csv'
batch_size = 1000
total_rows = 0

print(f"Iniciando importação do arquivo {csv_file}...")

try:
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Pular cabeçalho

        batch = []
        for row in reader:
            # Validar que a linha tem o número correto de colunas
            if len(row) < 19:
                print(f"Linha ignorada (dados insuficientes): {row}")
                continue

            # Converter valores de matrícula para inteiros, tratando valores vazios
            matriculas = []
            for i in range(10, 19):
                try:
                    if i < len(row) and row[i] and row[i].strip():
                        matriculas.append(int(row[i]))
                    else:
                        matriculas.append(0)
                except ValueError:
                    print(f"Erro ao converter valor '{row[i]}' para inteiro. Usando 0.")
                    matriculas.append(0)

            # Preparar dados para inserção
            data = (
                row[0] if len(row) > 0 else '',  # estado
                row[1] if len(row) > 1 else '',  # cidade
                row[2] if len(row) > 2 else '',  # ies
                row[3] if len(row) > 3 else '',  # sigla
                row[4] if len(row) > 4 else '',  # organizacao
                row[5] if len(row) > 5 else '',  # categoria_administrativa
                row[6] if len(row) > 6 else '',  # nome_curso
                row[7] if len(row) > 7 else '',  # nome_detalhado_curso
                row[8] if len(row) > 8 else '',  # modalidade
                row[9] if len(row) > 9 else '',  # grau
                *matriculas  # anos 2014-2022
            )
            batch.append(data)
            
            # Inserir em lotes para melhor performance
            if len(batch) >= batch_size:
                args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in batch)
                cursor.execute(f"INSERT INTO matriculas (estado, cidade, ies, sigla, organizacao, categoria_administrativa, nome_curso, nome_detalhado_curso, modalidade, grau, matriculas_2014, matriculas_2015, matriculas_2016, matriculas_2017, matriculas_2018, matriculas_2019, matriculas_2020, matriculas_2021, matriculas_2022) VALUES {args_str}")
                conn.commit()
                total_rows += len(batch)
                print(f"Importados {total_rows} registros...")
                batch = []

        # Inserir o lote final se houver dados restantes
        if batch:
            args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in batch)
            cursor.execute(f"INSERT INTO matriculas (estado, cidade, ies, sigla, organizacao, categoria_administrativa, nome_curso, nome_detalhado_curso, modalidade, grau, matriculas_2014, matriculas_2015, matriculas_2016, matriculas_2017, matriculas_2018, matriculas_2019, matriculas_2020, matriculas_2021, matriculas_2022) VALUES {args_str}")
            conn.commit()
            total_rows += len(batch)

    print(f"Importação concluída! Total de {total_rows} registros importados.")

except Exception as e:
    print(f"Erro durante a importação: {e}")
    conn.rollback()

finally:
    # Fechar conexões
    cursor.close()
    conn.close() 