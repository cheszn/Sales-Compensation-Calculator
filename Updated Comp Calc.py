import streamlit as st
import matplotlib.pyplot as plt

# Apply global styles for a polished look
st.set_page_config(
    page_title="Sales Compensation Calculator", layout="centered")
st.markdown("""
    <style>
        .main .block-container {
            background-color: #112336;
            padding: 20px;
            border-radius: 8px;
            max-width: 1000px;
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

        .stNumberInput > label, .stTextInput > label {
            color: #fcfcfc;
            font-weight: 500;
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

        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #1D4ED8;
            color: #9CA3AF;
            text-align: left;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)

# Header and navigation
st.markdown('<div class="header">Sales Compensation Calculator</div>',
            unsafe_allow_html=True)
tab = st.radio("Select Role", [
               "Sales Development Representative (SDR)", "Account Executive (AE)"])


def calculate_pro_rata_bonus(attainment_rate, bonus_amount):
    if attainment_rate < 0.5:
        return 0  # No bonus if attainment is below 50%
    elif attainment_rate >= 1.0:
        return bonus_amount  # Full bonus at 100% attainment or above
    else:
        return bonus_amount * attainment_rate  # Pro-rata bonus


if tab == "Sales Development Representative (SDR)":
    st.markdown('<div class="section-title">SDR Compensation Calculation</div>',
                unsafe_allow_html=True)

    st.write("Please enter your compensation details and performance metrics.")

    # Base inputs with tooltips
    base_salary = st.number_input("Base Salary (per year)", min_value=0.0, value=50000.0, step=1000.0,
                                  help="Your annual base salary before any bonuses.")
    sal_target_per_month = st.number_input("SALs Target (per month)", min_value=1, value=20,
                                           help="Monthly target for Sales Accepted Leads (SALs).")
    sql_target_per_month = st.number_input("SQLs Target (per month)", min_value=1, value=10,
                                           help="Monthly target for Sales Qualified Leads (SQLs).")
    bonus_sals_target_attainment = st.number_input("Bonus for SALs Target Attainment (€)", min_value=0.0, value=1000.0,
                                                   help="Bonus received upon achieving 100% of SALs target.")
    bonus_per_excess_sal = st.number_input("Bonus per Excess SAL (€)", min_value=0.0, value=50.0,
                                           help="Bonus for each SAL beyond the monthly target.")
    bonus_sqls_target_attainment = st.number_input("Bonus for SQLs Target Attainment (€)", min_value=0.0, value=1000.0,
                                                   help="Bonus received upon achieving 100% of SQLs target.")
    bonus_per_excess_sql = st.number_input("Bonus per Excess SQL (€)", min_value=0.0, value=100.0,
                                           help="Bonus for each SQL beyond the monthly target.")
    bonus_on_won_revenue = st.number_input("Bonus on Won Revenue (%)", min_value=0.0, value=0.5,
                                           help="Percentage bonus on revenue from deals you assisted.") / 100

    # New input for Quality Metrics
    lead_conversion_rate = st.number_input("Lead Conversion Rate (%)", min_value=0.0, max_value=100.0, value=50.0,
                                           help="Your lead conversion rate for the month.") / 100

    st.markdown("---")
    st.write("Please enter your performance metrics for the month.")

    # Monthly performance inputs
    total_sals_attained = st.number_input("Total SALs Attained (Monthly)", min_value=0,
                                          help="Total number of SALs you achieved this month.")
    total_sqls_attained = st.number_input("Total SQLs Attained (Monthly)", min_value=0,
                                          help="Total number of SQLs you achieved this month.")
    total_revenue_assist = st.number_input("Total Won Revenue Assisted (€)", min_value=0.0,
                                           help="Total revenue from deals you assisted in closing.")

    # Calculation Logic
    sal_attainment_rate = total_sals_attained / \
        sal_target_per_month if sal_target_per_month > 0 else 0
    sql_attainment_rate = total_sqls_attained / \
        sql_target_per_month if sql_target_per_month > 0 else 0
    monthly_base_salary = base_salary / 12

    # Determine target attainment bonuses (with pro-rata)
    base_sal_bonus = calculate_pro_rata_bonus(
        sal_attainment_rate, bonus_sals_target_attainment)
    base_sql_bonus = calculate_pro_rata_bonus(
        sql_attainment_rate, bonus_sqls_target_attainment)

    # Adjust bonuses based on Lead Conversion Rate
    base_sal_bonus *= lead_conversion_rate
    base_sql_bonus *= lead_conversion_rate

    # Caps on excess bonuses (100% over target)
    max_excess_sals = sal_target_per_month * 1.0  # Cap at 100% over target
    max_excess_sqls = sql_target_per_month * 1.0  # Cap at 100% over target

    # Calculate excess bonuses with caps
    excess_sals_count = max(
        0, min(total_sals_attained - sal_target_per_month, max_excess_sals))
    excess_sqls_count = max(
        0, min(total_sqls_attained - sql_target_per_month, max_excess_sqls))
    excess_sal_bonus = excess_sals_count * \
        bonus_per_excess_sal * lead_conversion_rate
    excess_sql_bonus = excess_sqls_count * \
        bonus_per_excess_sql * lead_conversion_rate

    # Calculate revenue bonus
    revenue_bonus = total_revenue_assist * bonus_on_won_revenue

    # Total earnings calculation
    total_target_attainment_earnings = base_sal_bonus + base_sql_bonus
    total_excess_earnings = excess_sal_bonus + excess_sql_bonus + revenue_bonus
    grand_total = total_target_attainment_earnings + \
        total_excess_earnings + monthly_base_salary

    # Display results
    st.markdown('<div class="result-card">Total SDR Earnings: €<b>{:,.2f}</b></div>'.format(
        grand_total), unsafe_allow_html=True)

    # Calculation Summary
    st.write("### Calculation Summary")
    st.write("""
    Your earnings are based on the following components:

    1. **Base Salary**: Fixed monthly amount as part of your annual base salary.
    2. **Target Attainment Bonuses**: Calculated based on your achievement against monthly targets, with pro-rata bonuses for attainment between 50% and 100%, adjusted by your Lead Conversion Rate.
    3. **Excess Bonuses**: Additional bonuses for each SAL and SQL achieved beyond your target, capped at 100% over your target and adjusted by your Lead Conversion Rate.
    4. **Revenue Bonus**: A percentage of the total won revenue you assisted in closing.
    5. **Quality Metrics**: Your Lead Conversion Rate impacts your bonuses, emphasizing lead quality.
    """)

    # Expandable Detailed Breakdown
    with st.expander("See Detailed Calculation Breakdown"):
        if sal_attainment_rate < 0.5 and sql_attainment_rate < 0.5:
            st.write(
                "**No Bonus Earned**: Attainment rates below 50% do not qualify for bonuses.")
        else:
            st.write(f"""
            **Base Salary**: €{monthly_base_salary:,.2f}

            **SAL Target Attainment Bonus**:
            - Attainment Rate: {sal_attainment_rate * 100:.2f}%
            - Bonus Earned Before Conversion Rate: €{calculate_pro_rata_bonus(sal_attainment_rate, bonus_sals_target_attainment):,.2f}
            - Lead Conversion Rate: {lead_conversion_rate * 100:.2f}%
            - Adjusted Bonus Earned: €{base_sal_bonus:,.2f}

            **SQL Target Attainment Bonus**:
            - Attainment Rate: {sql_attainment_rate * 100:.2f}%
            - Bonus Earned Before Conversion Rate: €{calculate_pro_rata_bonus(sql_attainment_rate, bonus_sqls_target_attainment):,.2f}
            - Lead Conversion Rate: {lead_conversion_rate * 100:.2f}%
            - Adjusted Bonus Earned: €{base_sql_bonus:,.2f}

            **Excess SAL Bonus**:
            - Excess SALs: {excess_sals_count} (Capped at {max_excess_sals})
            - Bonus Earned Before Conversion Rate: €{excess_sals_count * bonus_per_excess_sal:,.2f}
            - Lead Conversion Rate: {lead_conversion_rate * 100:.2f}%
            - Adjusted Bonus Earned: €{excess_sal_bonus:,.2f}

            **Excess SQL Bonus**:
            - Excess SQLs: {excess_sqls_count} (Capped at {max_excess_sqls})
            - Bonus Earned Before Conversion Rate: €{excess_sqls_count * bonus_per_excess_sql:,.2f}
            - Lead Conversion Rate: {lead_conversion_rate * 100:.2f}%
            - Adjusted Bonus Earned: €{excess_sql_bonus:,.2f}

            **Revenue Bonus**:
            - Total Assisted Revenue: €{total_revenue_assist:,.2f}
            - Bonus Earned: €{revenue_bonus:,.2f}

            **Total Earnings**: €{grand_total:,.2f}
            """)

    # Visualization of Attainment Rates
    st.write("### Performance Visualization")
    st.write("**SAL Attainment Rate:**")
    st.progress(min(sal_attainment_rate, 1.0))
    st.write("**SQL Attainment Rate:**")
    st.progress(min(sql_attainment_rate, 1.0))
    st.write("**Lead Conversion Rate:**")
    st.progress(lead_conversion_rate)

elif tab == "Account Executive (AE)":
    st.markdown('<div class="section-title">AE Compensation Calculation</div>',
                unsafe_allow_html=True)

    st.write("Please enter your compensation details and performance metrics.")

    # Base inputs for AE role with tooltips
    base_salary = st.number_input("Base Salary (per year)", min_value=0.0, value=70000.0, step=1000.0,
                                  help="Your annual base salary before any commissions.")
    commission_rate = st.number_input("Standard Commission Rate (%)", min_value=0.0, value=5.0,
                                      help="Commission rate applied to sales up to 100% of target.") / 100
    overachievement_rate = st.number_input("Overachievement Commission Rate (%)", min_value=0.0, value=7.5,
                                           help="Commission rate applied to sales between 100% and 150% of target.") / 100
    exceptional_rate = st.number_input("Exceptional Commission Rate (%)", min_value=0.0, value=10.0,
                                       help="Commission rate applied to sales above 150% of target.") / 100
    monthly_target = st.number_input("Monthly Sales Target (€)", min_value=0.0, value=50000.0,
                                     help="Your monthly sales target.")

    st.markdown("---")
    st.write("Please enter your performance metrics for the month.")

    total_sales = st.number_input("Total Sales Closed (€)", min_value=0.0,
                                  help="Total sales value you closed this month.")

    # AE Calculation Logic
    attainment_rate = total_sales / monthly_target if monthly_target > 0 else 0
    monthly_base_salary = base_salary / 12

    if attainment_rate >= 0.5:
        # Calculate commissions based on attainment rate
        commission = 0
        if attainment_rate <= 1.0:
            # Attainment between 50% and 100%: Pro-rata commission
            commission = total_sales * commission_rate * attainment_rate
        else:
            # Attainment above 100%
            # Commission for sales up to 100% of target
            sales_up_to_target = monthly_target
            commission += sales_up_to_target * commission_rate

            # Sales between 100% and 150% of target
            if attainment_rate <= 1.5:
                sales_between_100_150 = total_sales - sales_up_to_target
                commission += sales_between_100_150 * overachievement_rate
            else:
                sales_between_100_150 = monthly_target * 0.5
                commission += sales_between_100_150 * overachievement_rate

                # Sales above 150% of target
                sales_above_150 = total_sales - (monthly_target * 1.5)
                commission += sales_above_150 * exceptional_rate

    else:
        commission = 0  # No commission if attainment is below 50%

    total_earnings = commission + monthly_base_salary

    # Display results
    st.markdown('<div class="result-card">Total AE Earnings: €<b>{:,.2f}</b></div>'.format(
        total_earnings), unsafe_allow_html=True)

    # Calculation Summary
    st.write("### Calculation Summary")
    st.write("""
    Your earnings are based on the following components:

    1. **Base Salary**: Fixed monthly amount as part of your annual base salary.
    2. **Commission**: Calculated based on your total sales and attainment rate, with pro-rata commissions between 50% and 100% attainment.
    3. **Overachievement Commission**: Higher commission rates applied to sales exceeding 100% of target, structured in tiers.
    """)

    # Expandable Detailed Breakdown
    with st.expander("See Detailed Calculation Breakdown"):
        if attainment_rate < 0.5:
            st.write(
                "**No Commission Earned**: Attainment rate below 50% does not qualify for commissions.")
        else:
            st.write(f"""
            **Base Salary**: €{monthly_base_salary:,.2f}

            **Total Sales**: €{total_sales:,.2f} \n 
            **Attainment Rate**: {attainment_rate * 100:.2f}%

            **Commission Breakdown**:
            """)
            commission_details = ""

            if attainment_rate <= 1.0:
                # Pro-rata commission
                commission_amount = total_sales * commission_rate * attainment_rate
                commission_details += f"""
                - Pro-Rata Commission Rate: {commission_rate * 100:.2f}%
                - Commission Earned: €{commission_amount:,.2f}
                """
            else:
                # Sales up to 100% of target
                sales_up_to_target = monthly_target
                commission_up_to_target = sales_up_to_target * commission_rate
                commission_details += f"""
                - Sales up to 100% of Target (€{monthly_target:,.2f}):
                    - Commission Rate: {commission_rate * 100:.2f}%
                    - Commission Earned: €{commission_up_to_target:,.2f}
                """

                # Sales between 100% and 150% of target
                if attainment_rate <= 1.5:
                    sales_between_100_150 = total_sales - sales_up_to_target
                    commission_between_100_150 = sales_between_100_150 * overachievement_rate
                    commission_details += f"""
                    - Sales between 100% and 150% of Target (€{sales_between_100_150:,.2f}):
                        - Commission Rate: {overachievement_rate * 100:.2f}%
                        - Commission Earned: €{commission_between_100_150:,.2f}
                    """
                else:
                    sales_between_100_150 = monthly_target * 0.5
                    commission_between_100_150 = sales_between_100_150 * overachievement_rate
                    commission_details += f"""
                    - Sales between 100% and 150% of Target (€{sales_between_100_150:,.2f}):
                        - Commission Rate: {overachievement_rate * 100:.2f}%
                        - Commission Earned: €{commission_between_100_150:,.2f}
                    """

                    # Sales above 150% of target
                    sales_above_150 = total_sales - (monthly_target * 1.5)
                    commission_above_150 = sales_above_150 * exceptional_rate
                    commission_details += f"""
                    - Sales above 150% of Target (€{sales_above_150:,.2f}):
                        - Commission Rate: {exceptional_rate * 100:.2f}%
                        - Commission Earned: €{commission_above_150:,.2f}
                    """

                total_commission_earned = commission
                commission_details += f"""
                **Total Commission Earned**: €{total_commission_earned:,.2f}
                """

            st.write(commission_details)
            st.write(f"**Total Earnings**: €{total_earnings:,.2f}")

    # Visualization of Attainment Rate
    st.write("### Performance Visualization")
    st.write("**Sales Attainment Rate:**")
    # Assuming maximum of 200% for visualization
    st.progress(min(attainment_rate / 2.0, 1.0))

# Footer
st.markdown("""
<footer>
    © 2024 - All Rights Reserved
    <br>
    **Disclaimer:** The calculations provided are estimates and subject to company policies and approvals.
</footer>
""", unsafe_allow_html=True)
