import streamlit as st
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable
import math  # Import math for rounding functions

# Function to check for non-negative input
def check_non_negative(value, field_name):
    if value < 0:
        st.error(f"{field_name} must be non-negative. Please enter a valid value.")
        return False
    return True

# Set the title of the app
st.title("AnalytIQ - Simplex Algorithm for Revenue Maximization")

# Create two tabs
products_tab, analyse_tab = st.tabs(["Products", "Analyse"])

# Products tab
with products_tab:
    st.header("Products")
    
    # Allow users to input product data through a table
    sample_data = {
        "Product": ["Computer A", "Computer B"],
        "Cost": [1000, 100],
        "Time": [4, 2],  # Time in hours to produce one unit
        "Revenue": [2000, 400]  # Revenue from one unit of product
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(sample_data)

    # Display the editable table where users can input their data
    edited_df = st.data_editor(df, use_container_width=True)
    
    st.write("### Data Preview")
    st.write(edited_df)

# Analyse tab
with analyse_tab:
    st.header("Analyse")

    # Extract data from the edited DataFrame
    if not edited_df.empty:
        # Extract relevant columns for the Simplex method
        products = edited_df['Product'].values
        costs = edited_df['Cost'].values
        times = edited_df['Time'].values
        revenues = edited_df['Revenue'].values

        # User-defined constraints
        st.write("### Constraints")

        # Input constraints for time and budget (these can be updated based on user needs)
        total_time_available = st.number_input("Total available time (hours)", min_value=0, value=10)
        if not check_non_negative(total_time_available, "Total available time"):
            st.stop()

        total_budget = st.number_input("Total available budget", min_value=0, value=1500)
        if not check_non_negative(total_budget, "Total available budget"):
            st.stop()

        # Input constraint for the total maximum number of computers that can be produced
        total_max_units = st.number_input("Maximum total units of all computers that can be produced", min_value=0, value=200)
        if not check_non_negative(total_max_units, "Maximum total units"):
            st.stop()

        # Create the linear programming problem
        prob = LpProblem("Maximize_Profit", LpMaximize)

        # Define decision variables for each product (number of products to produce)
        product_vars = {product: LpVariable(f"prod_{product}", lowBound=0, cat="Continuous") for product in products}

        # Objective function: Maximize total revenue (sum of product revenues)
        prob += sum(revenues[i] * product_vars[products[i]] for i in range(len(products)))

        # Add the constraints: total time, total budget, and total production limit
        prob += sum(times[i] * product_vars[products[i]] for i in range(len(products))) <= total_time_available, "Time_Constraint"
        prob += sum(costs[i] * product_vars[products[i]] for i in range(len(products))) <= total_budget, "Budget_Constraint"
        prob += sum(product_vars[products[i]] for i in range(len(products))) <= total_max_units, "Total_Production_Limit"

        # Display the "Evaluate" button
        evaluate_button = st.button("Evaluate")

        if evaluate_button:
            # Solve the linear programming problem
            prob.solve()

            # Check if the optimal solution is found
            if prob.status == 1:  # 1 means optimal solution found
                # Get the raw solution (before rounding)
                raw_results = {product: product_vars[product].varValue for product in products}

                # First, try rounding up the solution (using math.ceil)
                rounded_up_results = {product: math.ceil(raw_results[product]) for product in products}

                # Recalculate the total time and total cost with the rounded-up values
                total_time_used_up = sum(times[i] * rounded_up_results[products[i]] for i in range(len(products)))
                total_cost_used_up = sum(costs[i] * rounded_up_results[products[i]] for i in range(len(products)))

                # If the rounded-up values violate the constraints, round down instead
                if total_time_used_up <= total_time_available and total_cost_used_up <= total_budget and sum(rounded_up_results.values()) <= total_max_units:
                    # Use the rounded-up values if they satisfy the constraints
                    final_results = rounded_up_results
                else:
                    # Otherwise, round down using math.floor
                    final_results = {product: math.floor(raw_results[product]) for product in products}

                # Calculate the final revenue using the final rounded values
                final_revenue = sum(revenues[i] * final_results[products[i]] for i in range(len(products)))

                # Display the final rounded values and the maximum revenue
                st.write("### Final Solution:")
                st.write(f"Quantity of each product to produce:")
                for i, product in enumerate(products):
                    st.write(f"{product}: {final_results[product]} units")
                st.write(f"Maximum Revenue: ${final_revenue:.2f}")
            else:
                st.write("No optimal solution found.")
