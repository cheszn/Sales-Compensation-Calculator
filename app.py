import streamlit as st

# Apply global styles for a polished look
st.markdown("""
    <style>
        .main .block-container {
            background-color: #112336;
            padding: 20px;
            border-radius: 8px;
            max-width: 800px;
            margin: auto;
        }

        .header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 20px;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .stNumberInput, .stTextInput {
            background-color: #261c1c;
            border: 1px solid #D1D5DB;
            border-radius: 6px;
            padding: 10px;
        }

        .stButton button {
            background-color: #1D4ED8;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px 20px;
            transition: background-color 0.3s;
            cursor: pointer;
            border: none;
        }

        .stButton button:hover {
            background-color: #2563EB;
        }

        .result-card {
            background-color: #EFF6FF;
            border: 1px solid #1D4ED8;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #0A2540;
            font-size: 1.3rem;
            font-weight: 500;
            text-align: center;
        }

        footer {
            font-size: 0.85rem;
            color: #9CA3AF;
            text-align: center;
            padding: 10px;
            margin-top: 30px;
            border-top: 1px solid #E5E7EB;
        }
    </style>
""", unsafe_allow_html=True)

# Header and navigation
st.markdown('<div class="header">Sales Compensation Calculator</div>',
            unsafe_allow_html=True)
tab = st.radio("Select Role", [
               "Sales Development Representative (SDR)", "Account Executive (AE)"])


def enforce_criteria(attainment_rate, commission):
    # Apply minimum threshold of 50% attainment and cap at 150%
    if attainment_rate < 0.5:
        return 0  # No commission if attainment is below 50%
    effective_attainment_rate = min(attainment_rate, 1.5)  # Cap at 150%
    return commission * effective_attainment_rate


if tab == "Sales Development Representative (SDR)":
    st.markdown('<div class="section-title">SDR Compensation Calculation</div>',
                unsafe_allow_html=True)

    # Base inputs
    base_salary = st.number_input(
        "Base Salary (per year)", min_value=0.0, value=50000.0, step=1000.0)
    sal_target_per_month = st.number_input(
        "SALs Target (per month)", min_value=1, value=20)
    sql_target_per_month = st.number_input(
        "SQLs Target (per month)", min_value=1, value=10)
    bonus_sals_target_attainment = st.number_input(
        "Bonus for SALs Target Attainment", min_value=0.0, value=1000.0)
    bonus_per_excess_sal = st.number_input(
        "Bonus per Excess SAL", min_value=0.0, value=50.0)
    bonus_sqls_target_attainment = st.number_input(
        "Bonus for SQLs Target Attainment", min_value=0.0, value=1000.0)
    bonus_per_excess_sql = st.number_input(
        "Bonus per Excess SQL", min_value=0.0, value=100.0)
    bonus_on_won_revenue = st.number_input(
        "Bonus on Won Revenue (%)", min_value=0.0, value=0.5) / 100

    # Monthly performance inputs
    total_sals_attained = st.number_input(
        "Total SALs Attained (Monthly)", min_value=0)
    total_sqls_attained = st.number_input(
        "Total SQLs Attained (Monthly)", min_value=0)
    total_revenue_assist = st.number_input(
        "Total Won Revenue Assisted (€)", min_value=0.0)

    # Calculation Logic
    sal_attainment_rate = total_sals_attained / sal_target_per_month
    sql_attainment_rate = total_sqls_attained / sql_target_per_month
    monthly_base_salary = base_salary / 12

    # Apply cap to target attainment bonuses
    base_sal_bonus = enforce_criteria(
        sal_attainment_rate, bonus_sals_target_attainment)
    base_sql_bonus = enforce_criteria(
        sql_attainment_rate, bonus_sqls_target_attainment)

    # Apply cap to excess bonuses
    excess_sals_count = max(0, min(total_sals_attained - sal_target_per_month,
                            sal_target_per_month * 1.5 - sal_target_per_month))
    excess_sqls_count = max(0, min(total_sqls_attained - sql_target_per_month,
                            sql_target_per_month * 1.5 - sql_target_per_month))
    excess_sal_bonus = excess_sals_count * bonus_per_excess_sal
    excess_sql_bonus = excess_sqls_count * bonus_per_excess_sql

    # Calculate revenue bonus
    revenue_bonus = total_revenue_assist * bonus_on_won_revenue

    # Total earnings calculation
    total_target_attainment_earnings = base_sal_bonus + base_sql_bonus
    total_above_earnings = excess_sal_bonus + excess_sql_bonus + revenue_bonus
    grand_total = total_target_attainment_earnings + \
        total_above_earnings + monthly_base_salary

    # Display results
    st.markdown('<div class="result-card">Total SDR Earnings: €<b>{:,.2f}</b></div>'.format(
        grand_total), unsafe_allow_html=True)

elif tab == "Account Executive (AE)":
    st.markdown('<div class="section-title">AE Compensation Calculation</div>',
                unsafe_allow_html=True)

    # Base inputs for AE role
    base_salary = st.number_input(
        "Base Salary (per year)", min_value=0.0, value=70000.0, step=1000.0)
    commission_rate = st.number_input(
        "Commission Rate (%)", min_value=0.0, value=5.0) / 100
    accelerator_threshold = st.number_input(
        "Accelerator Threshold (%)", min_value=100, value=150) / 100
    accelerator_rate = st.number_input(
        "Accelerated Commission Rate (%)", min_value=0.0, value=10.0) / 100
    monthly_target = st.number_input(
        "Monthly Sales Target (€)", min_value=0.0, value=50000.0)

    total_sales = st.number_input("Total Sales Closed (€)", min_value=0.0)

    # AE Calculation Logic with 1:1 payout and capping
    attainment_rate = total_sales / monthly_target
    commission = 0

    # Calculate standard commission only if attainment meets or exceeds 50%
    if attainment_rate >= 0.5:
        # Cap at 150% for the standard commission
        capped_attainment_rate = min(attainment_rate, 1.5)
        commission = (monthly_target * commission_rate) * \
            capped_attainment_rate

        # Add accelerated commission for sales above the accelerator threshold
        if attainment_rate > accelerator_threshold:
            accelerated_sales = total_sales - \
                (monthly_target * accelerator_threshold)
            commission += accelerated_sales * accelerator_rate

    monthly_base_salary = base_salary / 12
    total_earnings = commission + monthly_base_salary

    st.markdown('<div class="result-card">Total AE Earnings: €<b>{:,.2f}</b></div>'.format(
        total_earnings), unsafe_allow_html=True)

# Summary of Calculation
st.write("**Calculation Summary**")
st.write("""
Your earnings are based on the following:
1. **Base Salary**: This is your fixed monthly salary.
2. **Target Attainment Bonuses**: Calculated based on your achievement against monthly targets. You must meet at least 50% of your target to qualify for any commission.
3. **Excess Bonuses**: Additional bonuses for each SAL and SQL achieved beyond your target.
4. **Revenue Bonus**: A percentage of the total won revenue assisted.
5. **Attainment Cap**: Your total commission is capped at 150% of target attainment.
""")

# Expandable Detailed Breakdown
with st.expander("See Detailed Calculation Breakdown"):
    if tab == "Sales Development Representative (SDR)":
        # Conditional Explanation for SDR Attainment
        if sal_attainment_rate < 0.5 and sql_attainment_rate < 0.5:
            st.write("""
                **No Commission Earned**: Since both SAL and SQL attainment rates are below the 50% threshold, no commission is awarded.
                """)
        else:
            st.write(f"""
                **Base Salary**: €{monthly_base_salary:,.2f}
                - Fixed monthly amount as part of your annual base salary.
                
                **SAL Target Attainment Bonus**: €{base_sal_bonus:,.2f}
                - You achieved {sal_attainment_rate * 100:.0f}% of your SAL target.
                - The bonus is capped at 150% attainment for the target bonus.

                **SQL Target Attainment Bonus**: €{base_sql_bonus:,.2f}
                - You achieved {sql_attainment_rate * 100:.0f}% of your SQL target.
                - The bonus is capped at 150% attainment for the target bonus.

                **Excess SAL Bonus**: €{excess_sal_bonus:,.2f}
                - This bonus is for each SAL beyond the capped target (up to 150% of target SALs).
                
                **Excess SQL Bonus**: €{excess_sql_bonus:,.2f}
                - This bonus is for each SQL beyond the capped target (up to 150% of target SQLs).
                
                **Revenue Bonus**: €{revenue_bonus:,.2f}
                - Calculated as a percentage of the assisted won revenue (€{total_revenue_assist:,.2f}).

                **Grand Total (Capped at 150% Attainment)**: €{grand_total:,.2f}
                - This total includes the base salary, attainment bonuses, excess bonuses, and revenue bonus, all within the 150% cap.
                """)
    elif tab == "Account Executive (AE)":
        # Conditional Explanation for AE Attainment
        if attainment_rate < 0.5:
            st.write("""
                    **No Commission Earned**: Since your attainment rate is below the 50% threshold, no commission is awarded.
                    """)
        else:
            st.write(f"""
                    **Base Salary**: €{monthly_base_salary:,.2f}
                    - Fixed monthly amount as part of your annual base salary.
                    
                    **Standard Commission (Capped at 150% Attainment)**: €{(monthly_target * commission_rate) * min(attainment_rate, 1.5):,.2f}
                    - You achieved {attainment_rate * 100:.0f}% of your sales target.
                    - The standard commission is capped at 150% attainment, allowing for a maximum of 150% of the target commission.

                    **Accelerated Commission**: €{(total_sales - (monthly_target * accelerator_threshold)) * accelerator_rate if attainment_rate > accelerator_threshold else 0:,.2f}
                    - Since your attainment exceeded the accelerator threshold ({accelerator_threshold * 100:.0f}%), an additional commission rate is applied to sales above this threshold.

                    **Grand Total Earnings (Capped at 150% Attainment)**: €{total_earnings:,.2f}
                    - This total includes the base salary, standard commission, and any accelerated commission based on your attainment rate, all within the 150% cap.
                    """)

# Footer
st.markdown('<footer>© 2024 - All Rights Reserved</footer>',
            unsafe_allow_html=True)
