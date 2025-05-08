# Projeto matrículas

## Descrição

A partir do arquivo `matriculas.csv`, criar uma aplicação web com conexão com banco de dados.

## Funcionalidades

- Lista de alunos matriculados (no Brasil) por ano
  - Filtro de modalidade (EaD ou Presencial)
  - Filtro de estado
- Ranking de cursos em 2022 (10 cursos com maior número de matrículas no Brasil)
  - Filtro de modalidade (EaD ou Presencial)
  - Filtro de estado

## Requisitos não funcionais

- Usar MVC
- Não usar ORM do django
- Criar Model, Dao, Repository
- Usar o banco de dados postgres

## Como executar o projeto

1. **Clone o repositório**

   ```bash
   git clone git@github.com:High-Martin/matriculas.git
   cd matriculas
   ```

2. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

3. **Coloque o arquivo CSV na pasta do projeto**
   - Faça o download do arquivo `Matriculados Brasil - Projeto.csv` no AVA
   - Renomear para `matriculas.csv`
   - Coloque-o na pasta raiz do projeto

4. **Configure o banco de dados PostgreSQL**
   Usando Docker:

   ```bash
   cd database
   docker-compose up -d
   cd ..
   ```

5. **Importe os dados do CSV para o banco de dados**

   ```bash
   python import_csv.py
   ```

   Este processo pode levar alguns minutos pois o arquivo é grande.

6. **Execute as migrações do Django**

   ```bash
   python manage.py migrate
   ```

7. **Crie um superusuário para acessar o admin**

   ```bash
   python manage.py createsuperuser
   ```

8. **Inicie o servidor de desenvolvimento**

   ```bash
   python manage.py runserver
   ```
