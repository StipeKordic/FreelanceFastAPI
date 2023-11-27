from fastapi import FastAPI
from routes import auth_router, post_routes, review_routes, service_routes, user_routes, role_routes, permission_routes

app = FastAPI()

app.include_router(user_routes.user_router)
app.include_router(service_routes.service_router)
app.include_router(auth_router.auth_router)
app.include_router(post_routes.post_router)
app.include_router(review_routes.review_router)
app.include_router(role_routes.role_router)
app.include_router(permission_routes.permission_router)

# models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"Hello": "world!"}
