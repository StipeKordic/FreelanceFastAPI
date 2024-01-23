create_user = "Post route for creating user (Sign up). User atributes are: email, first_name, last_name and password." \
              " All those fields are required, email needs to be valid email type. Password is hashed after everything" \
              " gets verifyed. Parameter file is of UploadFile type and it is not required. If user doesn't provide it," \
              " image_path atribute in database is set to default image stored in static/images folder. If image is provided" \
              " it is also stored in static/images using random generated 10 characters long name so there is no images" \
              " with same names. Also user is automatically assigned RegularUser role (which has id of 3)."


get_all_users = "Get route that return all users except currently loggedIn user from database. This route is " \
                 "restricted only for superadmins"


get_user_by_id = "Get route that returns single user by his id which is provided as path parameter."


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


login_user = ""


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


get_posts_by_filter = "Get route that returns all posts that satisfy certain conditions. Min and max price and review are" \
                      " sent as query parameters and service_id is sent as path parameter. This route is protected only for" \
                      " authorized users. Posts are than queried by those parameters. prices and review have default values" \
                      " (0 review as it is lowest, 0 for min_price as it is lowest and 999 for max_price as some big number)." \
                      " There are two different queries because if review is 0 it should return all posts that satisfy other " \
                      "parameters but avg is returning null for posts that don't have reviews so avg>=0 doesn't return them. " \
                      "So one of the queries doesn't check at all for review if sent review is 0 (meaning review parameter was not sent at all)."


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


update_role_of_permission = "Put route for updating role that can access that specific permission."


update_permission = "Put route for updating name of certain permission."


create_new_access_token = "Refresh token is sent as query parameter and user id is extracted from that refresh token." \
                           " User is then queried by that id and his info is saved in data dictionary just like" \
                           " login route. New access token is then created. This route is supposed to be called every "\
                            "few minutes before original tokens expire so user doesn't need to login constantly. Refresh "\
                            "token also has expiration time so when it is done user will then need to log in again"\


#POPRAVI OPIS FUNKCIJA ZA USERA I UPDATE_ROLE_OF_PERMISSION POPRAVI I PROVJERI ACCESS