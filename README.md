# fastapi users

uma api assincrona de usuario com fast api, validacao de email e senha com regex,
token com pyjwt, hash de senha com pwdlib utilizando o algoritmo argon2, versionamento de banco de dados com alembic,
banco de dados assincrono com sqlalchemy utilizando o plugin asyncpg para a api e psycopg2 para versionamento de banco de dados

### bibliotecas utilizadas "producao"

* fastapi = "^0.115.0"
* uvicorn = "^0.31.0"
* sqlalchemy = "^2.0.35"
* alembic = "^1.13.3"
* pwdlib = {extras = ["argon2"], version = "^0.2.1"}
* pydantic-settings = "^2.5.2"
* asyncpg = "^0.29.0"
* psycopg2-binary = "^2.9.9"
* pyjwt = "^2.9.0"
* python-multipart = "^0.0.12"

  ### bibliotecas utilizadas "desinvolvimento"

* pytest = "^8.3.3"
* black = "^24.10.0"
* pytest-asyncio = "^0.24.0"
* factory-boy = "^3.3.1"
* freezegun = "^1.5.1"
* httpx = "^0.27.2"
* aiosqlite = "^0.20.0"

### dependencias

* docker
* docker-compose

### para rodar 
git clone 
cd fastapi_users

"docker-compose"

``` docker-compose build ```

``` docker-compose up ```

"docker-compose plugin"

``` docker compose build ```

``` docker compose up ```
