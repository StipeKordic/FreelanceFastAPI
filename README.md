# FreelanceFastAPI

####1. Clone repo on your machine
  ```bash
  git clone https://github.com/StipeKordic/FreelanceFastAPI
```

####2. Open folder in your editor and configure virtual enviroment
   Use this command in powershell terminal: ```bash
  python -m venv .venv
```
   and than select that enviroment as interpreter

####3. Install requirements  
   ```bash
  pip install -r requirements.txt
```
####4. Create and configure -env file
   SECRET_KEY = {Secret key that can be any string}
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = {Time for access token to expire in minutes}
  REFRESH_TOKEN_EXPIRE_HOURS = {Time for refresh token to expire in hours}
  SQLALCHEMY_DATABASE_URL = {Link to your database}
