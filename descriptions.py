import secrets

create_user = "Post route for creating user (Sign up). User atributes are: email, first_name, last_name and password." \
              " All those fields are required, email needs to be valid email type. Password is hashed after everything" \
              " gets verifyed. Parameter file is of UploadFile type and it is not required. If user doesn't provide it," \
              " image_path atribute in database is set to default image stored in static/images folder. If image is provided" \
              " it is also stored in static/images using random generated 10 characters long name so there is no images" \
              " with same names. Also user is automatically assigned RegularUser role (which has id of 3)."


get_all_users = "Get route that return all users from database. This route is restricted only for superadmins" \
                 "It returns "


get_user_by_id = "Get route that returns single user by his id which is provided as path parameter. It returns" \
                 "user with their role name and role id"


delete_user = "Delete route for deleting user from database. User's id is provided as path parameter and if user" \
              " with that id is found in database, he will be deleted. This route is restricted only for speradmins"


update_user_image =  "Put route to change user image. Id of user is provided as path parameter, user is than found " \
                     "by id, and new image_path (with new 10 char long name for image name) is saved in database " \
                     "and image is stored in static/images folder. File parameter (used for image) is UploadFile type."


update_user = "Put route to update user information (Except image). User atributes are sent in request and none of them" \
              " is required so user can update only his first_name for example. If user wants to change his password he" \
              " needs to provide his old password and new password. Password will be changed only if provided old password" \
              " matches password stored in database. If everything is good, new data is stored in database and new access" \
               "token and refresh token are sent as response (I didn't actually implement sending this new token in" \
               "header for athorization so old one is still working but if for example user changes his first_name" \
               "(which is one of the atributes sent in jwt payload) token will contain his old first_name so that needs " \
                "to be fixed."


get_all_services = "Get route that returns all services ordered by number of posts for each service. It is used on home" \
                   " page under 'popular services' section so that service that has most posts (when creating post, service " \
                   "needs to be chosen for that post) is first and so on. It is also used on admin services panel where admin" \
                   "can create, update and deleete services."


create_service = "Post route for creating service. This route is restricted only for admins and superadmins. To create service" \
                 " service name, description, short_description and image all must be provided. Image is saved in static/images" \
                 " folder using random generated 10 characters long name so there is no images with same names. File parameter" \
                 " (used for image) is UploadFile type and all others are strings."


get_service_by_id = "Get route that returns single service filtered by id that is provided as path parammeter. If service" \
                    " is not found in database, HTTP 404 error is returned."


delete_service = "Delete route that deletes service from database filtered by id that is provided as path parameter. This" \
                 " route is restricted only for admins and superadmins. If service is not found in database, HTTP 404 " \
                 "error is returned."


update_service = "Put route for changing service data. This route is restricted only for admins and superadmins. Service" \
                 " is found by id which is provided as path parameter. Updated_service is of ServiceUpdate type that has" \
                 " name, description and short_description atributes but none of them are required so only name can be " \
                 "changed for example. It is then checked which of atributes is provided one by one and service gets updated."


update_service_image = "Put route to change service image. This route is restricted only for admins and superadmins. Id " \
                       "of service is provided as path parameter, service is than found by id, and new image_path (with " \
                       "new 10 char long name for image name) is saved in database and image is stored in static/images " \
                       "folder. File parameter (used for image) is UploadFile type."


login_user = "User is found in db by email. If user is not found or his password/email doesn't match exception is returned" \
              " Than his role is retrived with his id and than based on that role his permissions are found and stored in array." \
             "New access and refresh tokens are than created and returned, access token contains user_id, name, role and permissions"


get_all_posts = "Get route to get all posts. This route is protected only for authorized users, db.query is first mapped " \
                 "as list of RowMapping objects since there is joined data from more tables. After that list is converted" \
                "to list of dictionaries so that review value could be set to 0 if there is not reviews for that post (by" \
                "default it is null)"


create_post = "Post route for creating post. This route is protected only for authorized users. To create post description" \
              " price, service_id and image all must be provided. Image is saved in static/images folder using random " \
              "generated 10 characters long name so there is no images with same names. File parameter (used for image) " \
              "is UploadFile type, description is string, price is float and service_id is integer.."


get_posts_by_service = "Get route that returns all posts of single service. Service_id is provided as path parameter. " \
                       "This route is protected only for authorized users. It can be used on home page for example" \
                       "when user selects one of those 'popular services' app takes him to service info page with" \
                       "posts for that service displayed."


get_posts_by_filter = "Get route that returns all posts that satisfy certain conditions. Min and max price, review and" \
                      "service_id are sent as query parameters. This route is protected only for authorized users." \
                      "Posts are than queried by those parameters. Prices and review have default values." \
                      " (0 review as it is lowest, 0 for min_price as it is lowest and 999 for max_price as some big number)." \
                      " In case of service_id default value is 0 for cases when user doesn't want to filter by services." \
                      " There is a basic_query that suits all cases. 4 cases are combination of whether review and service_id" \
                      " are sent. If service_id is not sent (default value is than used which is 0) than in WHERE statement (.filter)" \
                      " it is not checked if service_id equals Post.service_id. if service_id has value other than 0 that case" \
                      " is checked. If review is not sent (default value is 0) HAVING statement is not included and otherwise" \
                      " HAVING statement is included. That is because avg of reviews returns null if there is no reviews and" \
                      " null >= 0 if False so in that cases this condition is not checked at all. Also pagination is included" \
                      " with 10 results per page. Offset and limit" \
                      " functions are not in basic_query because there is additional conditions like having statement and" \
                      " where statement in some cases. At the end elements are converted to dictionaries so end result doesn't" \
                      " show null for review but number 0." \


get_posts_of_logged_user = "Get route that returns all post of user that is logged in. This route is protected only for " \
                           "authorized users. User_id used to query posts is pulled out of JWT Token."


get_post_by_id = "Get route that returns single post filtered by id. This route is protected only for authorized users. If" \
                 " post is not found HTTP 404 error is returned."


update_post = "Put route for changing post data. This route is protected only for authorized users. Post is found by id" \
              " which is provided as path parameter. Updated_post is of PostUpdate type that has price and description " \
              "atributes but none of them are required so only price can be changed for example. It is then checked which" \
              " of atributes is provided one by one and post gets updated."


delete_post = "Delete route that deletes post from database filtered by id that is provided as path parameter. This route" \
              " is protected only for authorized users. If post is not found in database, HTTP 404 error is returned."


update_post_image = "Put route to change post image. This route is protected only for authorized users. Id of post " \
                    "is provided as path parameter, post is than found by id, and new image_path (with new 10 char " \
                    "long name for image name) is saved in database and image is stored in static/images folder. File " \
                    "parameter (used for image) is UploadFile type."


review_post = "Post route to store review of post by specific user. Review is is sent as Review type that contains " \
              " post_id and review (number from 1 to 5). It is then first checked if that specific user already voted" \
              " for that specific post and if he did his old review is updated and if he didn't new review is saved. " \
              "User_id used to query reviews is pulled out of JWT Token. This route is protected only for authorized users."


get_review_of_post = "Get route that returns final review of post and number of reviews for that post. This route is " \
                     "protected only for authorized users. Id of post is sent as path parameter."


get_all_roles = "Get route that returns all roles defined in database."


create_role = "Post route for creating new role. Only role_name is required."


update_role_of_user = "Put route for updating role of user. User_id and new_role_id are sent as path parameters. User is" \
                      " queried from UserRole table and when user (from user_roles table) is found his role_id gets " \
                      "updated. This route is restricted only for superadmins."


update_role = "Put route for updating name of certain role."


get_all_permissions = "Get route that returns all permissions defined in database."


create_permission = "Post route for creating new permission. Only permission_name is required. After creating permission" \
                    " in permissions table new PermissionRole is added in permission_roles table. it has permission_id" \
                    " of that new created permission and role_id of admin since there are only admin and superadmin " \
                    "roles and routes not stored in permissions table are available for all users. If permission is " \
                    "meant to be only for superadmins role_id of that PermissionRole can be changed to superadmins role."


update_role_of_permission = "Put route for updating which role can access certain permission. If role_id is 1 than "  \
                            "it means only SuperAdmin will be able to use that permission, if it is set to 2 than it means" \
                            "both Admin and SuperAdmin can use it. By default role_id for every permission is set on 2" \
                            "in permission_roles table (create_permission endpoint)."


update_permission = "Put route for updating name of certain permission."


create_new_access_token = "Refresh token is sent as query parameter and user id is extracted from that refresh token." \
                           " User is then queried by that id and his info is saved in data dictionary just like" \
                           " login route. New access token is then created. This route is supposed to be called every "\
                            "few minutes before original tokens expire so user doesn't need to login constantly. Refresh "\
                            "token also has expiration time so when it is done user will then need to log in again"

'''
lista = [('6','6','Objava 1 korisnika 6','198','/static/images/f5bd64a16e3f033b78b3.jpg'),
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
('3','3','Objava 8 korisnika 3','106','/static/images/dd41a2b93b352ac21573.jpg')]

putanje = [
    "/static/images/e6188aadba0dfbb9849e.jpg",
    "/static/images/98d09f7f6c52ac395a11.jpg",
    "/static/images/eff7b21ef27b4235a287.jpg",
    "/static/images/0239886d2fcd6b3e8f5b.jpg",
    "/static/images/fbb0d805c87dcfbc7a5d.jpg",
    "/static/images/9bdc6511db8d9f295012.jpg"

]
import random
for element in lista:
    description = "Post "+ element[2][7]+ " from user "+ element[2][19::]
    slika = random.choice(putanje)
    dijelovi = list(element)
    print("('"+dijelovi[0]+"','"+ dijelovi[1]+"','"+ description+"','"+ dijelovi[3]+"','"+ slika+"'),")'''