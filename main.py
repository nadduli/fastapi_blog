"""
main.py — FastAPI hotspot portal (template wiring reference)
Replace the stub data with your real MikroTik / MTN / Airtel logic.
"""
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def add_template_globals(request: Request, call_next):
    request.state.current_year = datetime.now().year
    return await call_next(request)



PLANS = [
    {
        "id": "1hr",
        "name": "1 Hour",
        "duration_label": "60 Minutes",
        "price": 500,
        "icon": "⚡",
        "popular": False,
        "speed": "Up to 5 Mbps",
        "features": ["60 minutes access", "Shared bandwidth", "Basic browsing & WhatsApp"],
        "duration_seconds": 3600,
    },
    {
        "id": "24hr",
        "name": "24 Hours",
        "duration_label": "1 Full Day",
        "price": 1000,
        "icon": "🌞",
        "popular": True,
        "speed": "Up to 10 Mbps",
        "features": ["24 hours access", "Streaming ready", "WhatsApp, TikTok & more", "No throttling"],
        "duration_seconds": 86400,
    },
    {
        "id": "7day",
        "name": "7 Days",
        "duration_label": "Weekly Pass",
        "price": 6000,
        "icon": "📅",
        "popular": False,
        "speed": "Up to 10 Mbps",
        "features": ["7 days access", "Unlimited sessions", "Priority bandwidth", "All platforms"],
        "duration_seconds": 604800,
    },
    {
        "id": "30day",
        "name": "30 Days",
        "duration_label": "Monthly Pass",
        "price": 25000,
        "icon": "💎",
        "popular": False,
        "speed": "Up to 20 Mbps",
        "features": ["30 days access", "Fastest speeds", "Unlimited data", "Priority support"],
        "duration_seconds": 2592000,
    },
]


def get_plan(plan_id: str):
    return next((p for p in PLANS if p["id"] == plan_id), None)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, mac: str = ""):
    return templates.TemplateResponse(request=request, name="home.html", context={
        "request": request,
        "plans": PLANS,
        "mac_address": mac,
        "location_name": "Kamwokya Site",  # from MikroTik login query
    })


@app.get("/pay/{plan_id}", response_class=HTMLResponse, include_in_schema=False)
async def payment_page(request: Request, plan_id: str, mac: str = "", redirect: str = ""):
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return templates.TemplateResponse(request=request, name="payment.html", context={
        "request": request,
        "plan": plan,
        "mac_address": mac,
        "redirect_url": redirect,
    })


@app.post("/pay/initiate", response_class=HTMLResponse, include_in_schema=False)
async def initiate_payment(
    request: Request,
    plan_id: str = Form(...),
    gateway: str = Form(...),
    phone: str = Form(...),
    name: str = Form(""),
    mac_address: str = Form(""),
    redirect_url: str = Form(""),
):
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404)

 

    tx_ref = f"NC-{uuid.uuid4().hex[:10].upper()}"  # stub

    return templates.TemplateResponse(request=request, name="pending.html", context={
        "request": request,
        "transaction_ref": tx_ref,
        "gateway": gateway,
        "phone": phone,
        "amount": plan["price"],
        "plan_name": plan["name"],
        "plan_id": plan_id,
        "mac_address": mac_address,
    })


@app.get("/api/payment/status/{tx_ref}")
async def payment_status(tx_ref: str):
    """
    Poll endpoint called by pending.html every 5 seconds.
    Replace with real DB lookup + gateway status check.
    Returns: {"status": "pending" | "success" | "failed"}
    """
    # TODO: check your DB / gateway webhook result for tx_ref
    return {"status": "pending"}  # stub


@app.get("/success", response_class=HTMLResponse, include_in_schema=False)
async def success_page(request: Request, ref: str = ""):
    # TODO: Load real session data from DB by ref
    now = datetime.now()
    expires = now + timedelta(hours=24)

    return templates.TemplateResponse(request=request, name="success.html", context={
        "request": request,
        "plan_name": "24 Hours",
        "amount": 1000,
        "transaction_ref": ref,
        "activated_at": now.strftime("%d %b %Y, %H:%M"),
        "expires_at": expires.strftime("%d %b %Y, %H:%M"),
        "expires_at_iso": expires.isoformat(),
    })


@app.get("/payment/failed", response_class=HTMLResponse, include_in_schema=False)
async def failed_page(request: Request, ref: str = "", plan_id: str = "24hr"):
    return templates.TemplateResponse(request=request, name="failed.html", context={
        "request": request,
        "transaction_ref": ref,
        "plan_id": plan_id,
        "error_reason": "The payment request was declined or timed out.",
    })

@app.get("/admin", response_class=RedirectResponse, include_in_schema=False)
async def admin_redirect():
    return RedirectResponse(url="/admin/dashboard")

@app.get("/admin/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def admin_dashboard(request: Request):
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    metrics = {
        "today_revenue": 4000,
        "weekly_revenue": 28000,
        "monthly_revenue": 120000,
        "active_users": 45,
        "available_amount": 150000,
        "router_health": "98%", # Mock health percentage
        "chart_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "chart_data": [5000, 4200, 6000, 4000, 7500, 8000, 4000]
    }

    return templates.TemplateResponse(request=request, name="admin_dashboard.html", context={
        "request": request,
        "metrics": metrics,
        "greeting": greeting,
        "admin_name": "Daniel",
        "page_title": "Admin Dashboard",
        "active_page": "dashboard"
    })

@app.get("/admin/router", response_class=HTMLResponse, include_in_schema=False)
async def admin_router_page(request: Request, message: str = ""):
    # Mock router configuration from database
    router_config = {
        "ip_address": "192.168.88.1",
        "api_port": 8728,
        "username": "admin",
        "password": ""
    }
    return templates.TemplateResponse(request=request, name="admin_router.html", context={
        "request": request,
        "active_page": "router",
        "router_status": "offline",  # 'connected' or 'offline'
        "router_config": router_config,
        "message": message
    })

@app.post("/admin/router/save", response_class=RedirectResponse, include_in_schema=False)
async def admin_router_save(
    request: Request,
    ip_address: str = Form(...),
    api_port: int = Form(...),
    username: str = Form(...),
    password: str = Form(""),
):
    # Mock saving to DB
    from urllib.parse import urlencode
    return RedirectResponse(
        url=f"/admin/router?{urlencode({'message': 'MikroTik credentials updated successfully.'})}",
        status_code=303
    )

# --- Auth Routes ---
@app.get("/auth/login", response_class=HTMLResponse, include_in_schema=False)
async def auth_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth_login.html", context={"request": request})

@app.post("/auth/login", response_class=RedirectResponse, include_in_schema=False)
async def auth_login_post():
    # Mock login success, redirect to dashboard
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@app.get("/auth/register", response_class=HTMLResponse, include_in_schema=False)
async def auth_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth_register.html", context={"request": request})

@app.post("/auth/register", response_class=RedirectResponse, include_in_schema=False)
async def auth_register_post():
    # Mock registration success
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@app.get("/auth/forgot-password", response_class=HTMLResponse, include_in_schema=False)
async def auth_forgot_password_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth_forgot_password.html", context={"request": request})

@app.post("/auth/forgot-password", response_class=RedirectResponse, include_in_schema=False)
async def auth_forgot_password_post():
    # Mock forgot password success
    return RedirectResponse(url="/auth/login", status_code=303)
