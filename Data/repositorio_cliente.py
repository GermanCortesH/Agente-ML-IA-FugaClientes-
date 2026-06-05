from datetime import datetime, timedelta
import random

# -----------------------------
# MOCK DATABASE
# -----------------------------

CUSTOMERS_DB = [
    {
        "customer_id": 1,
        "signup_date": "2023-01-10",
        "last_login_date": "2026-04-01",
        "plan": "basic",
        "monthly_fee": 9.99,
        "support_tickets": 5,
        "usage_minutes": 120,
        "country": "ES",
        "is_active": 1
    },
    {
        "customer_id": 2,
        "signup_date": "2022-06-15",
        "last_login_date": "2025-12-10",
        "plan": "pro",
        "monthly_fee": 29.99,
        "support_tickets": 0,
        "usage_minutes": 900,
        "country": "US",
        "is_active": 1
    },
    {
        "customer_id": 3,
        "signup_date": "2021-03-20",
        "last_login_date": "2025-01-01",
        "plan": "basic",
        "monthly_fee": 9.99,
        "support_tickets": 12,
        "usage_minutes": 30,
        "country": "MX",
        "is_active": 0
    },
]

# -----------------------------
# REPOSITORY FUNCTIONS
# -----------------------------

def get_customer_by_id(customer_id: int):
    """Simula una API externa"""
    for customer in CUSTOMERS_DB:
        if customer["customer_id"] == customer_id:
            return customer
    return None


def get_all_customers():
    """Para testing / entrenamiento"""
    return CUSTOMERS_DB



def generate_random_customer():

    today = datetime.today()

    signup_date = today - timedelta(
        days=random.randint(100, 2000)
    )

    last_login = today - timedelta(
        days=random.randint(1, 400)
    )

    usage_minutes = random.randint(10, 2000)

    support_tickets = random.randint(0, 20)

    monthly_fee = round(random.uniform(5, 50), 2)

    plan = random.choice([
        "basic",
        "pro",
        "enterprise"
    ])

    country = random.choice([
        "ES",
        "US",
        "MX",
        "AR",
        "FR"
    ])

    # =====================================
    # LOGICA CHURN
    # =====================================

    churn_risk = 0

    # poco uso
    if usage_minutes < 200:
        churn_risk += 35

    # muchos tickets
    if support_tickets > 10:
        churn_risk += 30

    # mucho tiempo sin login
    inactive_days = (today - last_login).days

    if inactive_days > 90:
        churn_risk += 40

    # planes baratos tienen mas churn
    if plan == "basic":
        churn_risk += 10

    # clientes antiguos tienden a quedarse
    customer_age = (today - signup_date).days

    if customer_age > 1000:
        churn_risk -= 20

    # ruido aleatorio
    churn_risk += random.randint(-10, 10)

    # =====================================
    # TARGET FINAL
    # =====================================

    is_active = 0 if churn_risk >= 50 else 1

    return {

        "customer_id": random.randint(1000, 9999),

        "signup_date": signup_date.strftime("%Y-%m-%d"),

        "last_login_date": last_login.strftime("%Y-%m-%d"),

        "plan": plan,

        "monthly_fee": monthly_fee,

        "support_tickets": support_tickets,

        "usage_minutes": usage_minutes,

        "country": country,

        "is_active": is_active
    }