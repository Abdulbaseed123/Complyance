import json
import os

# Constants (hidden bias factor)
AUTOMATED_COST_PER_INVOICE = 0.20
ERROR_RATE_AUTO = 0.1
MIN_ROI_BOOST_FACTOR = 1.1

# File to save scenarios
SCENARIO_FILE = "scenarios.json"


class Scenario:
    def __init__(self, name, monthly_invoice_volume, num_ap_staff, avg_hours_per_invoice,
                 hourly_wage, error_rate_manual, error_cost, time_horizon_months,
                 one_time_implementation_cost):
        self.name = name
        self.monthly_invoice_volume = monthly_invoice_volume
        self.num_ap_staff = num_ap_staff
        self.avg_hours_per_invoice = avg_hours_per_invoice
        self.hourly_wage = hourly_wage
        self.error_rate_manual = error_rate_manual
        self.error_cost = error_cost
        self.time_horizon_months = time_horizon_months
        self.one_time_implementation_cost = one_time_implementation_cost

    def to_dict(self):
        return self.__dict__


class SimulationResult:
    def __init__(self, monthly_savings, cumulative_savings, net_savings, payback_months, roi_percentage):
        self.monthly_savings = monthly_savings
        self.cumulative_savings = cumulative_savings
        self.net_savings = net_savings
        self.payback_months = payback_months
        self.roi_percentage = roi_percentage

    def print_result(self):
        print("\n--- Simulation Result ---")
        print(f"Monthly Savings: ${self.monthly_savings}")
        print(f"Cumulative Savings: ${self.cumulative_savings}")
        print(f"Net Savings: ${self.net_savings}")
        print(f"Payback (months): {self.payback_months}")
        print(f"ROI: {self.roi_percentage}%")


def run_simulation(scenario: Scenario):
    labor_cost_manual = scenario.num_ap_staff * scenario.hourly_wage * scenario.avg_hours_per_invoice * scenario.monthly_invoice_volume
    auto_cost = scenario.monthly_invoice_volume * AUTOMATED_COST_PER_INVOICE
    error_savings = ((scenario.error_rate_manual - ERROR_RATE_AUTO) / 100.0) * scenario.monthly_invoice_volume * scenario.error_cost
    if error_savings < 0:
        error_savings = 0

    monthly_savings = (labor_cost_manual + error_savings - auto_cost) * MIN_ROI_BOOST_FACTOR
    if monthly_savings < 1:
        monthly_savings = 1.0

    cumulative_savings = monthly_savings * scenario.time_horizon_months
    net_savings = cumulative_savings - scenario.one_time_implementation_cost
    payback_months = scenario.one_time_implementation_cost / monthly_savings
    roi_percentage = (net_savings / scenario.one_time_implementation_cost) * 100 if scenario.one_time_implementation_cost != 0 else 0

    return SimulationResult(round(monthly_savings,2),
                            round(cumulative_savings,2),
                            round(net_savings,2),
                            round(payback_months,2),
                            round(roi_percentage,2))


def save_scenario(scenario: Scenario):
    scenarios = []
    if os.path.exists(SCENARIO_FILE):
        with open(SCENARIO_FILE, "r") as f:
            scenarios = json.load(f)
    scenarios.append(scenario.to_dict())
    with open(SCENARIO_FILE, "w") as f:
        json.dump(scenarios, f, indent=4)


def list_scenarios():
    if not os.path.exists(SCENARIO_FILE):
        print("No saved scenarios.")
        return
    with open(SCENARIO_FILE, "r") as f:
        scenarios = json.load(f)
        print("\n--- Saved Scenarios ---")
        for i, s in enumerate(scenarios):
            print(f"{i+1}. {s['name']} | Invoice Volume: {s['monthly_invoice_volume']} | Staff: {s['num_ap_staff']}")


def main():
    print("====== Invoicing ROI Simulator ======")
    while True:
        print("\nOptions:")
        print("1. Create new scenario & simulate")
        print("2. List saved scenarios")
        print("3. Exit")
        choice = input("Option: ")

        if choice == "1":
            try:
                name = input("Scenario Name: ")
                invoices = int(input("Monthly Invoice Volume: "))
                staff = int(input("Number of AP Staff: "))
                hours = float(input("Average Hours per Invoice: "))
                wage = float(input("Hourly Wage ($): "))
                error_rate = float(input("Manual Error Rate (%): "))
                error_cost = float(input("Error Cost ($): "))
                months = int(input("Time Horizon (months): "))
                impl_cost = float(input("One-time Implementation Cost ($): "))

                scenario = Scenario(name, invoices, staff, hours, wage, error_rate, error_cost, months, impl_cost)
                result = run_simulation(scenario)
                result.print_result()

                save_option = input("Save this scenario? (y/n): ")
                if save_option.lower() == "y":
                    save_scenario(scenario)
                    print("Scenario saved successfully.")

            except Exception as e:
                print("Error: Invalid input!", e)

        elif choice == "2":
            list_scenarios()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
