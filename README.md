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
   and than select that enviroment as your python interpreter. You can also do it in settings if you are using PyCharm.

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
in terminal to create tables in your database. (First you need to make a database and make a connection to it which you can do using last step.)

#### 6. Add basic data in database
```bash
INSERT INTO roles ("role_name") VALUES ('SuperAdmin'), ('Admin'), ('RegularUser');
```
```bash
INSERT INTO permissions ("permission_name") VALUES ('get_all_users'), ('create_service'), ('delete_service'), ('update_service'), ('update_service_image'), ('update_role_of_user'), ('delete_user');
```
```bash
INSERT INTO permission_roles ("permission_id", "role_id") VALUES (1,1),(2,2),(3,2),(4,2),(5,2),(6,1),(7,1);
```

When you register first user you should make him superadmin by configuring his role_id in user_roles table from 3 to 1.
(If you are doing step 7 don't worry about this as user1 is set to be SuperAdmin.)

#### 7. Add dummy data to database (Optional)
```bash
--Dummy data for services

INSERT INTO services ("name", "short_description", "image_path", "description") 
VALUES ('Service1','Choose Service 1', '/static/images/6c56d34fab87f9f659a1.jpg', 'Description of the service 1'),
('Service2','Choose Service 2', '/static/images/bf8d6600707909f58ca8.jpg', 'Description of the service 2'),
('Service3','Choose Service 3', '/static/images/605821d645adb8be85ca.jpg', 'Description of the service 3'),
('Service4','Choose Service 4', '/static/images/bf8d6600707909f58ca8.jpg', 'Description of the service 4'),
('Service5','Choose Service 5', '/static/images/6c56d34fab87f9f659a1.jpg', 'Description of the service 5'),
('Service6','Choose Service 6', '/static/images/676082136b6a3e31a9a2.jpg', 'Description of the service 6'),
('Service7','Choose Service 7', '/static/images/eff7b21ef27b4235a287.jpg', 'Description of the service 7');

--Dummy data for users 

INSERT INTO users ("email", "first_name", "last_name", "image_path", "password") 
VALUES ('user1@gmail.com','user1', '1resu', '/static/images/0e55b61b7051e464735e.jpg', '$2b$12$9D7AQF5ktJElqpqX468Cou/0WNpU/ZXwGz6JyWpbvmmReYCumx3EC'),
('user2@gmail.com','user2', '2resu', '/static/images/default.jpg', '$2b$12$SkmikCJ6sQu1RoKMBSmW7Ov7uBoHeYCqjKRWGTu9r9xvnqJUjFE7K'),
('user3@gmail.com','user3', '3resu', '/static/images/bf8d6600707909f58ca8.jpg', '$2b$12$1It5nX2RYiX4xPJbZvUWLOntmCUJdzd7TR1aaOQNDE5N4MEH/OU76'),
('user4@gmail.com','user4', '4resu', '/static/images/605821d645adb8be85ca.jpg', '$2b$12$cx08Ty/3fbAWEWVls2ttfu17VlncUQp9PvP0X9vu.DKjlYNS5PtFe'),
('user5@gmail.com','user5', '5resu', '/static/images/default.jpg', '$2b$12$LE8UeCI0K/oiBvsCM3fK7uAEDZZuVw05ZlMcluC6bR79Os4qB4Wi2'),
('user6@gmail.com','user6', '6resu', '/static/images/default.jpg', '$2b$12$lXIMbe14/G4OSGPkYIiKue6k5wkVgBn0aWMruo8vdUZjY.4T3PuFy'),
('user7@gmail.com','user7', '7resu', '/static/images/9bdc6511db8d9f295012.jpg', '$2b$12$OC9EVmSKzWR2JILX6M4OkuPQNkO5H0x0AtTnAJMurY/k8PIHwPuDa'),
('user8@gmail.com','user8', '8resu', '/static/images/9bdc6511db8d9f295012.jpg', '$2b$12$0rhTI0PCLP05I1ScpSDum.CfY/tbCyaNv4sTwEI8qFThrwJuUCAj.'),
('user9@gmail.com','user9', '9resu', '/static/images/default.jpg', '$2b$12$jf8pWd8vrMjGkSAzf01BguPwjFaoR3eo32Apgp69eNGrCBSRM2g2q'),
('user10@gmail.com','user10', '10resu', '/static/images/676082136b6a3e31a9a2.jpg', '$2b$12$m8h6uCW6FD42/9Vdp5Vb6.F1frN4eCMEpCU9JvJErvDXrX0rR/xSC');

--Dummy data for user roles

INSERT INTO user_roles ("user_id", "role_id")
VALUES ('1', '1'), ('2', '2'), ('3', '3'), ('4', '3'), ('5', '3'), ('6', '3'), ('7', '3'), ('8', '3'), ('9', '3'), ('10', '3');

--Dummy data for posts

INSERT INTO posts ("user_id", "service_id", "description", "price", "image_path")
VALUES('6','6','Post 1 from user 6','198','/static/images/9bdc6511db8d9f295012.jpg'),
('2','3','Post 1 from user 2','83','/static/images/98d09f7f6c52ac395a11.jpg'),
('10','3','Post 1 from user 10','206','/static/images/9bdc6511db8d9f295012.jpg'),
('5','3','Post 1 from user 5','272','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('3','2','Post 1 from user 3','207','/static/images/98d09f7f6c52ac395a11.jpg'),
('4','5','Post 1 from user 4','45','/static/images/98d09f7f6c52ac395a11.jpg'),
('9','1','Post 1 from user 9','212','/static/images/eff7b21ef27b4235a287.jpg'),
('10','3','Post 2 from user 10','244','/static/images/9bdc6511db8d9f295012.jpg'),
('8','6','Post 1 from user 8','205','/static/images/e6188aadba0dfbb9849e.jpg'),
('4','3','Post 2 from user 4','202','/static/images/9bdc6511db8d9f295012.jpg'),
('7','4','Post 1 from user 7','297','/static/images/9bdc6511db8d9f295012.jpg'),
('6','2','Post 2 from user 6','34','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('7','6','Post 2 from user 7','32','/static/images/e6188aadba0dfbb9849e.jpg'),
('8','1','Post 2 from user 8','296','/static/images/9bdc6511db8d9f295012.jpg'),
('6','7','Post 3 from user 6','216','/static/images/9bdc6511db8d9f295012.jpg'),
('3','6','Post 2 from user 3','224','/static/images/fbb0d805c87dcfbc7a5d.jpg'),
('7','6','Post 3 from user 7','113','/static/images/e6188aadba0dfbb9849e.jpg'),
('4','4','Post 3 from user 4','72','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('5','7','Post 2 from user 5','52','/static/images/98d09f7f6c52ac395a11.jpg'),
('3','1','Post 3 from user 3','282','/static/images/fbb0d805c87dcfbc7a5d.jpg'),
('3','4','Post 4 from user 3','154','/static/images/e6188aadba0dfbb9849e.jpg'),
('3','3','Post 5 from user 3','149','/static/images/9bdc6511db8d9f295012.jpg'),
('4','2','Post 4 from user 4','171','/static/images/fbb0d805c87dcfbc7a5d.jpg'),
('6','4','Post 4 from user 6','97','/static/images/9bdc6511db8d9f295012.jpg'),
('2','1','Post 2 from user 2','260','/static/images/fbb0d805c87dcfbc7a5d.jpg'),
('8','1','Post 3 from user 8','86','/static/images/e6188aadba0dfbb9849e.jpg'),
('4','7','Post 5 from user 4','141','/static/images/e6188aadba0dfbb9849e.jpg'),
('7','7','Post 4 from user 7','56','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('6','5','Post 5 from user 6','218','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('5','2','Post 3 from user 5','80','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('7','5','Post 5 from user 7','266','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('4','3','Post 6 from user 4','159','/static/images/98d09f7f6c52ac395a11.jpg'),
('5','1','Post 4 from user 5','38','/static/images/98d09f7f6c52ac395a11.jpg'),
('10','3','Post 3 from user 10','48','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('1','6','Post 1 from user 1','181','/static/images/9bdc6511db8d9f295012.jpg'),
('10','5','Post 4 from user 10','154','/static/images/e6188aadba0dfbb9849e.jpg'),
('10','5','Post 5 from user 10','105','/static/images/eff7b21ef27b4235a287.jpg'),
('8','5','Post 4 from user 8','215','/static/images/9bdc6511db8d9f295012.jpg'),
('3','7','Post 6 from user 3','201','/static/images/98d09f7f6c52ac395a11.jpg'),
('7','6','Post 6 from user 7','196','/static/images/eff7b21ef27b4235a287.jpg'),
('9','4','Post 2 from user 9','78','/static/images/98d09f7f6c52ac395a11.jpg'),
('9','4','Post 3 from user 9','144','/static/images/e6188aadba0dfbb9849e.jpg'),
('6','5','Post 6 from user 6','93','/static/images/eff7b21ef27b4235a287.jpg'),
('4','4','Post 7 from user 4','255','/static/images/eff7b21ef27b4235a287.jpg'),
('9','4','Post 4 from user 9','191','/static/images/98d09f7f6c52ac395a11.jpg'),
('3','7','Post 7 from user 3','214','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('9','6','Post 5 from user 9','70','/static/images/e6188aadba0dfbb9849e.jpg'),
('1','1','Post 2 from user 1','292','/static/images/0239886d2fcd6b3e8f5b.jpg'),
('9','6','Post 6 from user 9','156','/static/images/9bdc6511db8d9f295012.jpg'),
('3','3','Post 8 from user 3','106','/static/images/eff7b21ef27b4235a287.jpg');

--Dummy data for reviews

INSERT INTO reviews ("user_id", "post_id", "review")
VALUES ('1','45','3'),
('10','50','1'),
('3','8','1'),
('4','20','4'),
('6','45','4'),
('5','42','5'),
('4','37','1'),
('10','12','3'),
('7','14','4'),
('7','21','5'),
('1','50','2'),
('7','10','3'),
('3','41','5'),
('1','42','4'),
('10','26','4'),
('3','36','2'),
('5','8','5'),
('7','36','5'),
('4','28','3'),
('6','30','4'),
('2','15','4'),
('10','47','2'),
('8','7','4'),
('9','50','3'),
('7','24','2'),
('6','10','4'),
('2','40','4'),
('9','39','3'),
('8','6','3'),
('9','12','3'),
('1','18','2'),
('2','5','2'),
('5','48','4'),
('3','31','2'),
('3','37','4'),
('8','28','1'),
('8','8','2'),
('5','16','3'),
('2','1','5'),
('1','14','2'),
('9','29','1'),
('4','36','3'),
('10','49','2'),
('1','38','2'),
('7','48','2'),
('3','17','1'),
('10','35','2'),
('9','32','2'),
('2','19','3'),
('6','23','2'),
('10','18','4'),
('2','41','3'),
('7','7','4'),
('5','21','2'),
('6','32','1'),
('5','40','3'),
('7','50','2'),
('4','12','4'),
('5','12','4'),
('3','23','1'),
('8','10','2'),
('4','22','5'),
('6','22','5'),
('2','21','1'),
('2','43','2'),
('10','41','4'),
('2','50','2'),
('4','40','4'),
('2','16','5'),
('9','46','1'),
('1','49','3'),
('2','7','2'),
('3','32','5'),
('3','7','3'),
('5','1','3'),
('8','21','3'),
('8','31','2'),
('6','49','4'),
('6','38','4'),
('3','15','2'),
('1','1','3'),
('6','2','3'),
('5','39','3'),
('10','23','5'),
('2','11','1'),
('7','25','1'),
('10','1','2'),
('5','37','4'),
('3','10','1'),
('4','21','5'),
('10','27','4'),
('5','31','3'),
('5','5','5'),
('8','27','1'),
('10','16','1'),
('10','46','2'),
('4','14','2'),
('9','13','1'),
('6','26','3'),
('1','15','4'),
('6','35','3'),
('1','21','4'),
('10','32','2'),
('5','13','1'),
('10','31','4'),
('4','26','5'),
('6','11','5'),
('8','42','3'),
('3','4','2'),
('7','46','5'),
('9','4','4'),
('7','8','3'),
('5','41','4'),
('7','32','1'),
('3','30','3'),
('2','34','5'),
('5','27','1'),
('3','28','1'),
('10','25','1'),
('9','38','3'),
('4','11','2'),
('5','28','2'),
('8','2','4'),
('9','37','1'),
('7','4','2'),
('9','22','1'),
('2','47','3'),
('2','36','3'),
('6','9','4'),
('2','14','2'),
('1','37','5'),
('10','42','4'),
('3','11','3'),
('9','8','5'),
('1','27','2'),
('7','23','3'),
('8','24','1'),
('10','24','4'),
('2','28','4'),
('10','10','4'),
('1','36','3'),
('7','38','2'),
('4','25','4'),
('9','24','3'),
('9','40','4'),
('7','9','5'),
('6','47','4'),
('5','2','1'),
('5','17','5'),
('4','19','5'),
('6','6','5'),
('2','38','3'),
('2','48','3'),
('5','43','1'),
('7','5','2'),
('8','37','2'),
('9','2','2'),
('8','43','4'),
('2','4','5'),
('5','9','4'),
('10','17','4'),
('2','12','5'),
('4','17','3'),
('8','48','3'),
('1','32','2'),
('5','45','3'),
('1','46','4'),
('8','4','5'),
('1','9','4'),
('2','17','2'),
('1','39','5'),
('2','22','1'),
('3','14','2'),
('6','19','2'),
('10','4','2'),
('9','35','4'),
('9','27','5'),
('3','13','4'),
('3','9','3'),
('8','1','1'),
('8','50','1'),
('6','34','2'),
('8','47','4'),
('1','40','4'),
('10','40','2'),
('10','30','5'),
('6','48','2'),
('6','20','3'),
('4','45','4'),
('1','8','5'),
('5','32','2'),
('4','15','5'),
('5','25','3'),
('10','45','2'),
('8','22','3'),
('10','38','4'),
('3','48','5');
```
