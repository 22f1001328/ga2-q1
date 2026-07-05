from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid

app = FastAPI()

# EXACT values assigned in the question
ALLOWED_ORIGIN = "https://dash-d8ygdp.example.com"
EMAIL = "22f1001328@ds.study.iitm.ac.in"

# Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware for required headers
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"

    return response


@app.get("/stats")
async def stats(values: str):
    try:
        numbers = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain only integers"},
        )

    if not numbers:
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