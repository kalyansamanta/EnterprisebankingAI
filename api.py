from fastapi import FastAPI

app = FastAPI(title="Enterprise Banking API")

@app.get("/")
def home():
    return {"message": "Enterprise Banking API Running"}

@app.get("/balance")
def balance():

    return {
        "customer": "Kalyan Samanta",
        "account": "XXXX1234",
        "balance": "₹2,56,740",
        "status": "Active"
    }


@app.get("/ifsc")
def ifsc():

    return {
        "bank": "State Bank of India",
        "ifsc": "SBIN0001234"
    }


@app.get("/branch")
def branch():

    return {
        "branch": "Kolkata Main Branch",
        "timing": "09:30 AM - 04:30 PM"
    }


@app.get("/loan")
def loan():

    return {

        "loan_type": "Home Loan",

        "interest_rate": "8.50%",

        "max_amount": "₹50,00,000"

    }