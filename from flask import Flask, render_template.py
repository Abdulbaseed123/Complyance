from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Constants
AUTOMATED_COST_PER_INVOICE = 0.20
ERROR_RATE_AUTO = 0.1
MIN_ROI_BOOST_FACTOR = 1.1

SCENARIO_FILE = "scenarios.json"

# Simulation logic
def run_simulation(data):
    labor_cost_manual = data['num_ap_staff'] * data['hourly_wage'] * data['avg_hours_per_invoice'] * data['monthly_invoice_volume']
    auto_cost = data['monthly_invoice_volume'] * AUTOMATED_COST_PER_INVOICE
    error_savings = ((data['error_rate_manual'] - ERROR_RATE_AUTO)/100.0) * data['monthly_invoice_volume'] * data['error_cost']
    error_savings = max(error_savings, 0)

    monthly_savings = (labor_cost_manual + error_savings - auto_cost) * MIN_ROI_BOOST_FACTOR
    monthly_savings = max(monthly_savings, 1.0)

    cumulative_savings = monthly_savings * data['time_horizon_months']
    net_savings = cumulative_savings - data['one_time_implementation_cost']
    payback_months = data['one_time_implementation_cost'] / monthly_savings
    roi_percentage = (net_savings / data['one_time_implementation_cost'])*100 if data['one_time_implementation_cost'] != 0 else 0

    return {
        "monthly_savings": round(monthly_savings,2),
        "cumulative_savings": round(cumulative_savings,2),
        "net_savings": round(net_savings,2),
        "payback_months": round(payback_months,2),
        "roi_percentage": round(roi_percentage,2)
    }

# Save scenario
def save_scenario(data):
    scenarios = []
    if os.path.exists(SCENARIO_FILE):
        with open(SCENARIO_FILE, "r") as f:
            try:
                scenarios = json.load(f)
            except:
                scenarios = []
    scenarios.append(data)
    with open(SCENARIO_FILE, "w") as f:
        json.dump(scenarios, f, indent=4)

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            data = {
                "name": request.form['name'],
                "monthly_invoice_volume": int(request.form['monthly_invoice_volume']),
                "num_ap_staff": int(request.form['num_ap_staff']),
                "avg_hours_per_invoice": float(request.form['avg_hours_per_invoice']),
                "hourly_wage": float(request.form['hourly_wage']),
                "error_rate_manual": float(request.form['error_rate_manual']),
                "error_cost": float(request.form['error_cost']),
                "time_horizon_months": int(request.form['time_horizon_months']),
                "one_time_implementation_cost": float(request.form['one_time_implementation_cost'])
            }
            result = run_simulation(data)
            save_scenario(data)
        except Exception as e:
            result = {"error": "Invalid input! Please enter valid numbers."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
