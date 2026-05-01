# API Barbearia

API para gerenciamento de barbearia com cadastro de clientes, barbeiros, serviços, agendamentos, pagamentos e custos.

Este projeto usa:

- Python
- SQLAlchemy
- PostgreSQL via Docker Compose
- `requirements.txt`
- `docker-compose.yml` ou `docker-compose.yaml`

---

## 1. Pré-requisitos

Antes de iniciar, tenha instalado:

- Python 3.11 ou superior
- Docker
- Docker Compose
- Git

---

## 2. Clonar o projeto

```bash
git clone https://github.com/wallace0003/api-barbearia.git
cd api-barbearia
```

---

## 3. Criar e ativar o ambiente virtual

### Linux, macOS ou WSL

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 4. Instalar as dependências

O projeto já possui o arquivo `requirements.txt`.

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

---

## 5. Configuração do banco com Docker Compose

Este projeto usa PostgreSQL via Docker Compose.

---

## 6. Criar o script SQL de criação das tabelas

O PostgreSQL executa automaticamente os arquivos `.sql` que estiverem dentro de:

```bash
/docker-entrypoint-initdb.d/
```

No nosso projeto, vamos criar o script local em:

```bash
db/init/01_create_tables.sql
```

Crie a pasta:

```bash
mkdir -p db/init
```

Agora crie o arquivo:

```bash
touch db/init/01_create_tables.sql
```

Cole o conteúdo abaixo dentro de `db/init/01_create_tables.sql`.

---

## 7. Subir o banco de dados

Execute:

```bash
docker compose up -d
```

Para acompanhar os logs do PostgreSQL:

```bash
docker compose logs -f postgres
```

---

## 8. Criando as tabelas pelo VS Code usando a extensão Database Client

Você pode criar as tabelas diretamente pelo VS Code usando a extensão **Database Client**.

Essa forma é mais simples porque não precisa depender do arquivo `db/init/01_create_tables.sql` ser executado automaticamente pelo Docker.  
Basta subir o banco com Docker, conectar nele pelo VS Code e executar o script SQL manualmente.

> Importante: este projeto não usa `.env`. As credenciais do banco estão diretamente no `docker-compose.yml`.

---



## 8.1. Subir o banco PostgreSQL com Docker

Antes de conectar pelo VS Code, suba o banco:

```bash
docker compose up -d
```

Confira se o container está rodando:

```bash
docker compose ps
```

Também é possível verificar os logs do PostgreSQL:

```bash
docker compose logs -f postgres
```

---

##8.2. Dados de conexão do banco

Considerando o `docker-compose.yml` do projeto, os dados de conexão são:

```text
Tipo do banco: PostgreSQL
Host: localhost
Porta: 5432
Database: barbearia
Usuário: postgres
Senha: postgres
```

A URL de conexão equivalente é:

```text
postgresql://postgres:postgres@localhost:5432/barbearia
```

---

## 8.3. Instalar a extensão Database Client no VS Code

No VS Code:

1. Abra a aba **Extensions**.
2. Pesquise por:

```text
Database Client
```

3. Instale a extensão.
4. Depois de instalar, aparecerá uma opção de banco de dados na lateral do VS Code.

---

## 8.4. Criar a conexão com o PostgreSQL

Na aba da extensão **Database Client**:

1. Clique para criar uma nova conexão.
2. Escolha o banco **PostgreSQL**.
3. Preencha os dados:

```text
Name: Barbearia(pode ser qulquer nome, fica a sua preferência)
Host: localhost
Port: 5432
Username: barber
Password: barber123
Database: barber_db
```

4. Clique em **Test Connection**.
5. Se a conexão estiver correta, clique em **Save** ou **Connect**.

Depois disso, o banco `barbearia` ficará disponível dentro do VS Code.

---

## 8.5. Criar um arquivo SQL dentro da conexão

Após conectar no banco:

1. Abra a conexão `Barbearia PostgreSQL`.
2. Selecione o banco `barbearia`.
3. Crie uma nova query ou um novo arquivo SQL pela própria extensão.
4. Cole o script SQL completo.
5. Execute o script.

Normalmente a extensão permite executar o arquivo inteiro.  
Caso algum erro aconteça, execute o script por partes, começando pelos `ENUMs`.

---

## 8.6. Atenção aos ENUMs

As tabelas `schedulings` e `payments` usam campos do tipo `ENUM`.

Por isso, antes de criar essas tabelas, é obrigatório criar os tipos:

```text
scheduling_status
payment_method
payment_status
```

Se esses tipos não forem criados antes, o PostgreSQL retornará erro parecido com:

```text
type "scheduling_status" does not exist
```

Por isso, o script abaixo já está completo e pronto para executar.

---

## 8.7. Script pronto para criação das tabelas

Copie todo o script abaixo e execute dentro da conexão do banco `barbearia` usando a extensão **Database Client** do VS Code.

```sql
-- =========================================================
-- SCRIPT DE CRIAÇÃO DAS TABELAS DA API BARBEARIA
-- Banco: PostgreSQL
-- =========================================================

-- =========================================================
-- TABELA: clients
-- =========================================================

CREATE TABLE IF NOT EXISTS clients (
    id_client INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    client_name VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL,
    number VARCHAR(11) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_clients_email
    ON clients (email);

CREATE INDEX IF NOT EXISTS ix_clients_number
    ON clients (number);

-- =========================================================
-- TABELA: barbers
-- =========================================================

CREATE TABLE IF NOT EXISTS barbers (
    id_barber INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    barber_name VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL,
    number VARCHAR(11) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_barbers_email
    ON barbers (email);

CREATE INDEX IF NOT EXISTS ix_barbers_number
    ON barbers (number);

-- =========================================================
-- TABELA: services
-- =========================================================

CREATE TABLE IF NOT EXISTS services (
    id_service INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    service_name VARCHAR(60) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    duration INTEGER NOT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_services_service_name
    ON services (service_name);

-- =========================================================
-- TABELA: costs
-- =========================================================

CREATE TABLE IF NOT EXISTS costs (
    id_costs INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_costs_category
    ON costs (category);

-- =========================================================
-- TABELA: schedulings
-- =========================================================

CREATE TABLE IF NOT EXISTS schedulings (
    id_scheduling INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

    id_client INTEGER NOT NULL,
    id_barber INTEGER NOT NULL,
    id_service INTEGER NOT NULL,

    status scheduling_status NOT NULL DEFAULT 'PENDING',

    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_schedulings_client
        FOREIGN KEY (id_client)
        REFERENCES clients (id_client)
        ON DELETE CASCADE,

    CONSTRAINT fk_schedulings_barber
        FOREIGN KEY (id_barber)
        REFERENCES barbers (id_barber)
        ON DELETE RESTRICT,

    CONSTRAINT fk_schedulings_service
        FOREIGN KEY (id_service)
        REFERENCES services (id_service)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS ix_schedulings_start_at
    ON schedulings (start_at);

CREATE INDEX IF NOT EXISTS ix_schedulings_barber_start_at
    ON schedulings (id_barber, start_at);

-- =========================================================
-- TABELA: payments
-- =========================================================

CREATE TABLE IF NOT EXISTS payments (
    id_payment INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

    id_scheduling INTEGER NOT NULL,

    payment_method payment_method NOT NULL,

    status payment_status NOT NULL DEFAULT 'PENDING',

    CONSTRAINT uq_payments_id_scheduling
        UNIQUE (id_scheduling),

    CONSTRAINT fk_payments_scheduling
        FOREIGN KEY (id_scheduling)
        REFERENCES schedulings (id_scheduling)
        ON DELETE CASCADE
);
```

---

## 8.8. Verificar se as tabelas foram criadas

Depois de executar o script, rode esta query no **Database Client**:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

O resultado esperado é:

```text
barbers
clients
costs
payments
schedulings
services
```

Também é possível verificar os tipos `ENUM` criados:

```sql
SELECT typname
FROM pg_type
WHERE typname IN (
    'scheduling_status',
    'payment_method',
    'payment_status'
)
ORDER BY typname;
```

O resultado esperado é:

```text
payment_method
payment_status
scheduling_status
```

---

## 8.9. Conferir a estrutura de uma tabela

Para conferir as colunas criadas em uma tabela, execute:

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'schedulings'
ORDER BY ordinal_position;
```
```

---

## 7.10. Possíveis erros e soluções

### Erro: `type "scheduling_status" does not exist`

Esse erro acontece quando a tabela `schedulings` é criada antes do `ENUM`.

Solução: execute primeiro a parte do script chamada:

```text
ENUMS
```

Depois execute novamente o restante do script.

---

### Erro: `connection refused`

Esse erro acontece quando o PostgreSQL não está rodando.

Solução:

```bash
docker compose up -d
```

Depois confira:

```bash
docker compose ps
```

---

### Erro: `password authentication failed`

Esse erro acontece quando usuário, senha ou banco estão diferentes do `docker-compose.yml`.

Confira se os dados estão assim:

```text
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: barbearia
```

E conecte no Database Client com:

```text
Host: localhost
Port: 5432
Database: barbearia
Username: postgres
Password: postgres
```

---

### As tabelas não aparecem depois de executar o script

Atualize a conexão no Database Client.

Normalmente existe uma opção como:

```text
Refresh
```

Depois expanda novamente:

```text
barbearia > public > tables
```

---

## 8.11. Observação sobre o Docker e o script SQL

Existem duas formas de criar as tabelas:

### Opção 1: Pelo Docker automaticamente

Usando um volume no `docker-compose.yml`:

```yaml
volumes:
  - ./db/init/01_create_tables.sql:/docker-entrypoint-initdb.d/01_create_tables.sql:ro
```

Nesse caso, o PostgreSQL executa o arquivo automaticamente apenas na primeira criação do volume.

Se o banco já foi criado antes, o script não roda novamente.

Para recriar do zero:

```bash
docker compose down -v
docker compose up -d
```

Atenção: esse comando apaga os dados do banco.

---

### Opção 2: Pelo Database Client no VS Code

Essa é a forma mais prática durante o desenvolvimento.

Basta:

1. Subir o banco com Docker.
2. Conectar no PostgreSQL pelo Database Client.
3. Criar uma nova query SQL.
4. Colar o script.
5. Executar.
6. Atualizar a conexão.
7. Conferir as tabelas em `public > tables`.

Essa opção não depende do script estar dentro da pasta `db/init`.

---

## 9. Rodar a API

Com o banco rodando e as dependências instaladas, execute:

```bash
python -m src.main
```
ou
```bash
python3 -m src.main
```
ou 
```bash
py -m src.main
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação Swagger ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

A documentação ReDoc ficará disponível em:

```text
http://127.0.0.1:8000/redoc
```

---

## 10. Comandos úteis

Subir o banco:

```bash
docker compose up -d
```

Parar os containers:

```bash
docker compose down
```

Parar os containers e apagar o volume do banco:

```bash
docker compose down -v
```

Ver logs do PostgreSQL:

```bash
docker compose logs -f postgres
```

Entrar no PostgreSQL pelo terminal:

```bash
docker compose exec postgres psql -U postgres -d barbearia
```

Listar tabelas:

```sql
\dt
```

Sair do terminal do PostgreSQL:

```sql
\q
```

---

## 11. Estrutura das tabelas criadas

O script cria as seguintes tabelas:

### `clients`

Tabela de clientes.

Campos principais:

- `id_client`
- `client_name`
- `email`
- `number`
- `created_at`

---

### `barbers`

Tabela de barbeiros.

Campos principais:

- `id_barber`
- `barber_name`
- `email`
- `number`
- `created_at`
- `status`

---

### `services`

Tabela de serviços oferecidos pela barbearia.

Campos principais:

- `id_service`
- `service_name`
- `price`
- `duration`
- `status`

---

### `costs`

Tabela de custos da barbearia.

Campos principais:

- `id_costs`
- `description`
- `price`
- `category`

---

### `schedulings`

Tabela de agendamentos.

Campos principais:

- `id_scheduling`
- `id_client`
- `id_barber`
- `id_service`
- `status`
- `start_at`
- `end_at`

Relacionamentos:

- Um agendamento pertence a um cliente.
- Um agendamento pertence a um barbeiro.
- Um agendamento pertence a um serviço.

---

### `payments`

Tabela de pagamentos.

Campos principais:

- `id_payment`
- `id_scheduling`
- `payment_method`
- `status`

Relacionamento:

- Um pagamento pertence a um agendamento.
- Cada agendamento pode ter apenas um pagamento.

---

## 12. Observações importantes

A tabela `services` deve ser criada apenas uma vez, mesmo que a classe `Service` apareça repetida em algum trecho de código.

O arquivo `.env` não é necessário neste projeto.

O arquivo `docker-compose.yml` é responsável por subir o PostgreSQL e executar o script SQL inicial.

O arquivo `db/init/01_create_tables.sql` é responsável por criar os ENUMs, tabelas, índices e relacionamentos no banco.

Sempre que alterar o script SQL e quiser recriar o banco do zero em ambiente de desenvolvimento, execute:

```bash
docker compose down -v
docker compose up -d
```
