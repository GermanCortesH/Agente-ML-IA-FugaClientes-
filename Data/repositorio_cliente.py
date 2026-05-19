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
    """Simula nuevos datos en tiempo real"""

    today = datetime.today()

    signup_date = today - timedelta(days=random.randint(100, 2000))
    last_login = today - timedelta(days=random.randint(1, 400))

    return {
        "customer_id": random.randint(1000, 9999),
        "signup_date": signup_date.strftime("%Y-%m-%d"),
        "last_login_date": last_login.strftime("%Y-%m-%d"),
        "plan": random.choice(["basic", "pro", "enterprise"]),
        "monthly_fee": round(random.uniform(5, 50), 2),
        "support_tickets": random.randint(0, 20),
        "usage_minutes": random.randint(10, 2000),
        "country": random.choice(["ES", "US", "MX", "AR", "FR"]),
        "is_active": random.choice([0, 1])
    }