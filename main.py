from fastapi import FastAPI, status
from routes import auth_router, post_routes, review_routes, service_routes, user_routes, role_routes, permission_routes
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.user_router)
app.include_router(service_routes.service_router)
app.include_router(auth_router.auth_router)
app.include_router(post_routes.post_router)
app.include_router(review_routes.review_router)
app.include_router(role_routes.role_router)
app.include_router(permission_routes.permission_router)

# models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
