from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.database import engine
from app.auth.router import router as auth_router
from app.applications.router import router as applications_router
from app.conclusion.router import router as conclusion_router
from app.signature.router import router as signature_router
from app.notification.router import router as notification_router
from app.admin.views import (
    ApplicationsAdmin,
    UsersAdmin,
    ConclusionAdmin,
    SignatureAdmin,
    NotificationAdmin,
)

from app.config import broker_router
from app.applications.consumer import process_order

app = FastAPI()
admin = Admin(app, engine)

app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(conclusion_router)
app.include_router(signature_router)
app.include_router(notification_router)

app.include_router(broker_router)

admin.add_view(UsersAdmin)
admin.add_view(ApplicationsAdmin)
admin.add_view(ConclusionAdmin)
admin.add_view(SignatureAdmin)
admin.add_view(NotificationAdmin)

origins = ["http://localhost:5500", "http://127.0.0.1:5500", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
