# school-drf

#### A Stack utilizada
* Python 3.10
* Framework: Django: 4.0 
* Django-rest-framework 3.13
* Postgresql
* Docker
* Docker-compose

#### GitHub - clone do projeto 

```bash
git clone https://github.com/Rodrigovvo/school-drf.git
```


#### Configure o arquivo .env

O arquivo .env contém dados do enviroment do sistema.

```bash
cp .env_sample .env
```

#### Executando a aplicação pela primeira vez

É necessário criar o banco de dados antes da aplicação, o banco de dados padrão é denominado **school**.

Inicie o projeto, executando o build:
```bash
sudo docker-compose build
```

Após, em um terminal suba o baco de dados:

```bash
sudo docker-compose up bd 
```

Em um outro terminal rode a migração do Django:

```bash
sudo docker-compose run --rm backend python manage.py migrate
```

Depois de rodar a migração pode derrubar o service da database:

```bash
sudo docker-compose down
```

E agora pode subir o projeto normalmente:

```bash
sudo docker-compose up
```

Os endereços e portas das aplicações são:

Backend - Django:

```bash
http://localhost:8000
```
#### Documentação da API Interna

#### Create Student

```http
  POST /api/v1/students/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `nickname`      | `string` | **Required**. Nickname of the student. |
| `address`|`string`|**Required**. Address of the student. |
| `age`|`string`|**Required**. Age of the student.  | 
| `doc`|`string`|**Required**. Student's CPF number |
| `email`|`email`|**Required**. Student's email |
| `first_name`|`string`| First name of the student.| 
| `last_name`|`string`| Last name of the student.| 
| `course`|`string`|**Required**. Course name of the student.| 

#### List students

```http
  GET /api/v1/students/
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `count`      | `integer` | Numbers os items. |
| `next`      | `uri` |  URI for next page |
| `previous`|`uri`| URI for previous page |
| `number_of_pages`|`integer`| Max number of pages  | 
| `current_page`|`integer`| Current page  | 
| `results`|`array`| Students |

* results items:

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `enrollment_number`      | `integer` | Enrollment number of the student. |
| `nickname`      | `string` |  Nickname of the student. |
| `address`|`string`|Address of the student. |
| `age`|`string`| Age of the student.  | 
| `doc`|`string`| Student's CPF number. |
| `email`|`email`| Student's email. |
| `first_name`|`string`| First name of the student.| 
| `last_name`|`string`| Last name of the student.| 
| `course`|`string`| Course name of the student.| 
| `is_active`|`bool`| If is a active student.| 

* Response sample:
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "number_of_pages": 13,
  "current_page": 1,
  "results": [
      {
      "enrollment_number": 0,
      "nickname": "string",
      "address": "string",
      "age": "string",
      "doc": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "course": "string",
      "is_active": true
      }
    ]
}
```
#### Get student

```http
  GET /api/v1/students/{enrollment_number}
```
* ###### PATH PARAMETERS:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `enrollment_number`      | `integer` | **Required**. Id of item to fetch |

#### Update recipe

```http
  PUT /api/v1/students/{enrollment_number}
```
* ###### PATH PARAMETERS:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `enrollment_number`      | `integer` | **Required**. Id of item to fetch |

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `nickname`      | `string` | **Required**. Nickname of the student. |
| `address`|`string`|**Required**. Address of the student. |
| `age`|`string`|**Required**. Age of the student.  | 
| `doc`|`string`|**Required**. Student's CPF number |
| `email`|`email`|**Required**. Student's email |
| `first_name`|`string`| First name of the student.| 
| `last_name`|`string`| Last name of the student.| 
| `course`|`string`|**Required**. Course name of the student.| 
| `is_active`|`bool`| If is a active student.| 

#### Delete student

```http
  DELETE /recipes/chef/recipe/{enrollment_number}
```
* ###### PATH PARAMETERS:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `enrollment_number`      | `integer` | **Required**. Id of item to fetch |



#### Executando comandos do framework Django:

Para executar qualquer comando do Django (startapp, createsuperuser, makemigrations, migrate etc) deve considerar se os services estão *no ar* ou não.

Se o service **backend** estiver *no ar* e *rodando* corretamente, basta utilizar o próprio service para executar o comando desejado.
Exemplos:

```bash
sudo docker-compose exec backend python manage.py startapp novo_app
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```

#### Testes
Para executar os testes execute o comando:
```bash
sudo docker-compose run --rm backend python manage.py test api.v1.tests.test_student
```