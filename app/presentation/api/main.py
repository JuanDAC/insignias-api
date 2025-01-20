from fastapi import FastAPI
from app.presentation.api.v1.insignias.insignia_route import router as insignia_route
from app.presentation.api.v1.users.user_route import router as user_route

app = FastAPI(title="insignia_app", description="API to handler insignia and users")

app.include_router(insignia_route)
app.include_router(user_route)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)