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
  Type:
  ```bash
  alembic upgrade head
```
in terminal to create tables in your database

#### 6. Add basic data in database
```bash
INSERT INTO roles ("role_name") VALUES ('SuperAdmin'), ('Admin'), ('RegularUser');
```
```bash
INSERT INTO permissions ("permission_name") VALUES ('get_all_users'), ('create_service'), ('delete_service'), ('update_service'), ('update_service_image'), ('update_role_of_user'), ('delete_user');
```

In update_role_of_permission endpoint you should do 3 requests. new_role_id needs to be 1 in all 3 requests and permission_id should be 1, 6 and 7.
When you register first user you should make him superadmin by configuring his role_id in user_roles table from 3 to 1.
