from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import uuid
import time

app = FastAPI()

# Your assigned allowed origin
ALLOWED_ORIGIN = "https://dash-d8ygdp.example.com"

# Replace this with YOUR IITM login email EXACTLY
EMAIL = "22f1001328@ds.study.iitm.ac.in"

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# Middleware to add required headers
class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response


app.add_middleware(HeaderMiddleware)


@app.get("/stats")
async def stats(values: str):
    try:
        numbers = [int(x.strip()) for x in values.split(",") if x.strip() != ""]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain only integers"},
        )

    if len(numbers) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "No values supplied"},
        )

    total = sum(numbers)

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }
