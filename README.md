# Projeto matrículas

## Descrição

A partir do arquivo `matriculas.csv`, criar uma aplicação web com conexão com banco de dados.

## Funcionalidades

- Total de alunos matriculados (no Brasil) por ano
- Total de alunos matriculados (no Brasil) por ano, com a possibilidade de escolher a modalidade (EaD ou Presencial)
- Ranking de cursos em 2022 (10 cursos com maior número de matrículas no Brasil)
- Ranking de cursos em 2022 (10 cursos com maior número de matrículas no Brasil), com a possibilidade de escolher a modalidade (EaD ou Presencial)
- Consulta para agregações semelhantes às anteriores com um filtro para Estados

## Requisitos não funcionais

- Usar MVC
- Não usar ORM do django
- Criar Model, Dao, Repository
- Usar o banco de dados postgres

## Como executar o projeto

1. **Clone o repositório**
   ```
   git clone git@github.com:High-Martin/matriculas.git
   cd matriculas
   ```

2. **Instale as dependências**
   ```
   pip install -r requirements.txt
   ```

3. **Coloque o arquivo CSV na pasta do projeto**
   - Faça o download do arquivo `Matriculados Brasil - Projeto.csv` no AVA
   - Renomear para `matriculas.csv`
   - Coloque-o na pasta raiz do projeto

4. **Configure o banco de dados PostgreSQL**
   
   Usando Docker:
   ```
   cd database
   docker-compose up -d
   cd ..
   ```

5. **Importe os dados do CSV para o banco de dados**
   ```
   python import_csv.py
   ```
   Este processo pode levar alguns minutos pois o arquivo é grande.

6. **Execute as migrações do Django**
   ```
   python manage.py migrate
   ```

7. **Crie um superusuário para acessar o admin**
   ```
   python manage.py createsuperuser
   ```

8. **Inicie o servidor de desenvolvimento**
   ```
   python manage.py runserver
   ```

