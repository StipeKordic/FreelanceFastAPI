# FreelanceFastAPI

#### 1. Clone repo on your machine
  ```bash
  git clone https://github.com/StipeKordic/FreelanceFastAPI
```

#### 2. Open folder in your editor and configure virtual enviroment
   Use this command in powershell terminal:
   ```bash
  python -m venv .venv
```
   and than select that enviroment as your python interpreter

#### 3. Install requirements  
   ```bash
  pip install -r requirements.txt
```
#### 4. Create and configure .env file

  | Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `SECRET_KEY` | `string` | **Required**. Your secret key |
| `ALGORITHM` | `string` | **Required**. hashing algorithm. I was using HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `integer` | **Required**. Time for access token to expire in minutes |
| `REFRESH_TOKEN_EXPIRE_HOURS` | `integer` | **Required**. Time for refresh token to expire in hours |
| `SQLALCHEMY_DATABASE_URL` | `string` | **Required**. Link to your database |

#### 5. Configure alembic
  In alembic.ini file in main folder change sqlalchemy.url variable to your SQLALCHEMY_DATABASE_URL
  Then you can do 
  ```bash
  alembic upgrade head
```
in terminal to create tables in your database
