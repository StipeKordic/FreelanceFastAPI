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

#### 7. Add dummy data to database (Optional)
```bash
--Dummy data for services

INSERT INTO services ("name", "short_description", "image_path", "description") 
VALUES ('Service1','Choose Service 1', '/static/images/fus8n37fna1i0jq735ic.png', 'Description of the service 1'),
('Service2','Choose Service 2', '/static/images/fus8n37f12hhhjq735ic.png', 'Description of the service 2'),
('Service3','Choose Service 3', '/static/images/p0cdd37fna1i0jq735ic.png', 'Description of the service 3'),
('Service4','Choose Service 4', '/static/images/lmc44r4wqa1i0jq735ic.png', 'Description of the service 4'),
('Service5','Choose Service 5', '/static/images/fus8n37fna1i0jqzzyzy.png', 'Description of the service 5'),
('Service6','Choose Service 6', '/static/images/fus8n37fna1i123735ic.png', 'Description of the service 6'),
('Service7','Choose Service 7', '/static/images/fus8n37f8il50jq735ic.png', 'Description of the service 7');

--Dummy data for users 

INSERT INTO users ("email", "first_name", "last_name", "image_path", "password") 
VALUES ('user1@gmail.com','user1', '1resu', '/static/images/8jfh23gkwlfd07hnmpc4.png', '$2b$12$9D7AQF5ktJElqpqX468Cou/0WNpU/ZXwGz6JyWpbvmmReYCumx3EC'),
('user2@gmail.com','user2', '2resu', '/static/images/default.jpg', '$2b$12$SkmikCJ6sQu1RoKMBSmW7Ov7uBoHeYCqjKRWGTu9r9xvnqJUjFE7K'),
('user3@gmail.com','user3', '3resu', '/static/images/a9l3k2jfdgmp01vhbx5s.png', '$2b$12$1It5nX2RYiX4xPJbZvUWLOntmCUJdzd7TR1aaOQNDE5N4MEH/OU76'),
('user4@gmail.com','user4', '4resu', '/static/images/ytpvz4n12jxlh5m0qrc8.png', '$2b$12$cx08Ty/3fbAWEWVls2ttfu17VlncUQp9PvP0X9vu.DKjlYNS5PtFe'),
('user5@gmail.com','user5', '5resu', '/static/images/default.jpg', '$2b$12$LE8UeCI0K/oiBvsCM3fK7uAEDZZuVw05ZlMcluC6bR79Os4qB4Wi2'),
('user6@gmail.com','user6', '6resu', '/static/images/default.jpg', '$2b$12$lXIMbe14/G4OSGPkYIiKue6k5wkVgBn0aWMruo8vdUZjY.4T3PuFy'),
('user7@gmail.com','user7', '7resu', '/static/images/7gk1vzm8qol4fbp6dxjc.png', '$2b$12$OC9EVmSKzWR2JILX6M4OkuPQNkO5H0x0AtTnAJMurY/k8PIHwPuDa'),
('user8@gmail.com','user8', '8resu', '/static/images/2lrtpj1fbayivq4x9d3c.png', '$2b$12$0rhTI0PCLP05I1ScpSDum.CfY/tbCyaNv4sTwEI8qFThrwJuUCAj.'),
('user9@gmail.com','user9', '9resu', '/static/images/default.jpg', '$2b$12$jf8pWd8vrMjGkSAzf01BguPwjFaoR3eo32Apgp69eNGrCBSRM2g2q'),
('user10@gmail.com','user10', '10resu', '/static/images/k9n0x4yvlw8tm7qz3chb.png', '$2b$12$m8h6uCW6FD42/9Vdp5Vb6.F1frN4eCMEpCU9JvJErvDXrX0rR/xSC');

--Dummy data for user roles

INSERT INTO user_roles ("user_id", "role_id")
VALUES ('1', '1'), ('2', '2'), ('3', '3'), ('4', '3'), ('5', '3'), ('6', '3'), ('7', '3'), ('8', '3'), ('9', '3'), ('10', '3');

--Dummy data for posts

INSERT INTO posts ("user_id", "service_id", "description", "price", "image_path")
VALUES ('6','6','Objava 1 korisnika 6','198','/static/images/f5bd64a16e3f033b78b3.jpg'),
('2','3','Objava 1 korisnika 2','83','/static/images/2d32c3e19c2c03185d21.jpg'),
('10','3','Objava 1 korisnika 10','206','/static/images/c133aabdef54a9edadaf.jpg'),
('5','3','Objava 1 korisnika 5','272','/static/images/dc368e3c68d41ac6a55c.jpg'),
('3','2','Objava 1 korisnika 3','207','/static/images/eb6ce9454948a4773bf0.jpg'),
('4','5','Objava 1 korisnika 4','45','/static/images/005082e398f994d9067f.jpg'),
('9','1','Objava 1 korisnika 9','212','/static/images/75415093541a9c237679.jpg'),
('10','3','Objava 2 korisnika 10','244','/static/images/1279a595f12812642bf8.jpg'),
('8','6','Objava 1 korisnika 8','205','/static/images/534a2f8dc63227f5c533.jpg'),
('4','3','Objava 2 korisnika 4','202','/static/images/d054165b47cc6edae792.jpg'),
('7','4','Objava 1 korisnika 7','297','/static/images/21713495fa8866a38d9b.jpg'),
('6','2','Objava 2 korisnika 6','34','/static/images/1df562466e35e1f58b6f.jpg'),
('7','6','Objava 2 korisnika 7','32','/static/images/c58b9eb77670bcd1110c.jpg'),
('8','1','Objava 2 korisnika 8','296','/static/images/bb5d7938c4f6e7f12ee0.jpg'),
('6','7','Objava 3 korisnika 6','216','/static/images/3eac082c22c50b98e57d.jpg'),
('3','6','Objava 2 korisnika 3','224','/static/images/b33295747778618a1a28.jpg'),
('7','6','Objava 3 korisnika 7','113','/static/images/84e5beb3f119381bb0ba.jpg'),
('4','4','Objava 3 korisnika 4','72','/static/images/4da809ef560e15cf11b2.jpg'),
('5','7','Objava 2 korisnika 5','52','/static/images/88ba4d6b7ed2fedce618.jpg'),
('3','1','Objava 3 korisnika 3','282','/static/images/e269fc8fc1ae0abc836c.jpg'),
('3','4','Objava 4 korisnika 3','154','/static/images/fa233f83589ac4f1a688.jpg'),
('3','3','Objava 5 korisnika 3','149','/static/images/fe6a768b99cb3fa82d82.jpg'),
('4','2','Objava 4 korisnika 4','171','/static/images/b08ed74acea44bee3ccd.jpg'),
('6','4','Objava 4 korisnika 6','97','/static/images/ded2597b175d09827aa1.jpg'),
('2','1','Objava 2 korisnika 2','260','/static/images/f8e687b9626855c84172.jpg'),
('8','1','Objava 3 korisnika 8','86','/static/images/213dab6ecf4c120ddb12.jpg'),
('4','7','Objava 5 korisnika 4','141','/static/images/91020dec4cf9e38e4b1c.jpg'),
('7','7','Objava 4 korisnika 7','56','/static/images/7b0d75afa7e74a6c6d8f.jpg'),
('6','5','Objava 5 korisnika 6','218','/static/images/afa99e202c74160249ff.jpg'),
('5','2','Objava 3 korisnika 5','80','/static/images/1ccbdaaf6a0cab444758.jpg'),
('7','5','Objava 5 korisnika 7','266','/static/images/5509e29d0cb64b5f9fa1.jpg'),
('4','3','Objava 6 korisnika 4','159','/static/images/cf4101387c4d345f10f7.jpg'),
('5','1','Objava 4 korisnika 5','38','/static/images/f8f55aa1a4a968f1982b.jpg'),
('10','3','Objava 3 korisnika 10','48','/static/images/2d1d63fa1818d326440b.jpg'),
('1','6','Objava 1 korisnika 1','181','/static/images/09cb5fea1df6f844ed34.jpg'),
('10','5','Objava 4 korisnika 10','154','/static/images/5360e4195f1cb854a508.jpg'),
('10','5','Objava 5 korisnika 10','105','/static/images/c01ce07d54dd7f311e89.jpg'),
('8','5','Objava 4 korisnika 8','215','/static/images/b83bf264f0dac0660f53.jpg'),
('3','7','Objava 6 korisnika 3','201','/static/images/c91de66c8e08beec9b73.jpg'),
('7','6','Objava 6 korisnika 7','196','/static/images/4749b81dc4ae4d392dbd.jpg'),
('9','4','Objava 2 korisnika 9','78','/static/images/9c32c908b166677f1288.jpg'),
('9','4','Objava 3 korisnika 9','144','/static/images/9bf544854e51ef2aa015.jpg'),
('6','5','Objava 6 korisnika 6','93','/static/images/e7bd6ee1e9ce3540d5ed.jpg'),
('4','4','Objava 7 korisnika 4','255','/static/images/200d963aa23d4e15bfa0.jpg'),
('9','4','Objava 4 korisnika 9','191','/static/images/d423b89438f33ed47acc.jpg'),
('3','7','Objava 7 korisnika 3','214','/static/images/2a376c4d7cc62af43f79.jpg'),
('9','6','Objava 5 korisnika 9','70','/static/images/a33ee424896985df07cf.jpg'),
('1','1','Objava 2 korisnika 1','292','/static/images/40955052cdc77b7852da.jpg'),
('9','6','Objava 6 korisnika 9','156','/static/images/9ec9a8ab4f46416fdca5.jpg'),
('3','3','Objava 8 korisnika 3','106','/static/images/dd41a2b93b352ac21573.jpg');

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
