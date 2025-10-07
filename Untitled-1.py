<!DOCTYPE html>
<html>
<head>
    <title>Invoicing ROI Simulator</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 5px; margin: 5px; width: 200px; }
        label { display: inline-block; width: 220px; }
    </style>
</head>
<body>
    <h1>Invoicing ROI Simulator</h1>
    <form method="POST">
        <label>Scenario Name:</label><input type="text" name="name" required><br>
        <label>Monthly Invoice Volume:</label><input type="number" name="monthly_invoice_volume" required><br>
        <label>AP Staff:</label><input type="number" name="num_ap_staff" required><br>
        <label>Avg Hours per Invoice:</label><input type="number" step="0.01" name="avg_hours_per_invoice" required><br>
        <label>Hourly Wage ($):</label><input type="number" step="0.01" name="hourly_wage" required><br>
        <label>Manual Error Rate (%):</label><input type="number" step="0.01" name="error_rate_manual" required><br>
        <label>Error Cost ($):</label><input type="number" step="0.01" name="error_cost" required><br>
        <label>Time Horizon (months):</label><input type="number" name="time_horizon_months" required><br>
        <label>Implementation Cost ($):</label><input type="number" step="0.01" name="one_time_implementation_cost" required><br>
        <button type="submit">Simulate</button>
    </form>

    {% if result %}
        {% if result.error %}
            <p style="color:red">{{ result.error }}</p>
        {% else %}
            <h2>Results</h2>
            <p>Monthly Savings: ${{ result.monthly_savings }}</p>
            <p>Cumulative Savings: ${{ result.cumulative_savings }}</p>
            <p>Net Savings: ${{ result.net_savings }}</p>
            <p>Payback (months): {{ result.payback_months }}</p>
            <p>ROI (%): {{ result.roi_percentage }}</p>
        {% endif %}
    {% endif %}
</body>
</html>
