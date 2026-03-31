"""
main.py — FastAPI hotspot portal (template wiring reference)
Replace the stub data with your real MikroTik / MTN / Airtel logic.
"""
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid

app = FastAPI()
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



@app.get("/", response_class=HTMLResponse)
async def index(request: Request, mac: str = ""):
    return templates.TemplateResponse(request=request, name="home.html", context={
        "request": request,
        "plans": PLANS,
        "mac_address": mac,
        "location_name": "Main Branch",  # from MikroTik login query
    })


@app.get("/pay/{plan_id}", response_class=HTMLResponse)
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


@app.post("/pay/initiate", response_class=HTMLResponse)
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


@app.get("/success", response_class=HTMLResponse)
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


@app.get("/payment/failed", response_class=HTMLResponse)
async def failed_page(request: Request, ref: str = "", plan_id: str = "24hr"):
    return templates.TemplateResponse(request=request, name="failed.html", context={
        "request": request,
        "transaction_ref": ref,
        "plan_id": plan_id,
        "error_reason": "The payment request was declined or timed out.",
    })
