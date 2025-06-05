
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BRRR Deal Analyzer", layout="centered")
st.title("🏠 BRRR Property Deal Analyzer")

st.header("🔍 Property Inputs")
address = st.text_input("Property Address")
purchase_price = st.number_input("Purchase Price (£)", min_value=50000, step=1000)
deposit_percent = st.slider("Deposit (%)", min_value=10, max_value=50, value=25)
refurb_cost = st.number_input("Refurbishment Cost (£)", min_value=0, step=500)
rent_pcm = st.number_input("Expected Monthly Rent (£)", min_value=0, step=50)
post_refurb_value = st.number_input("Post-Refurbishment Value (£)", min_value=0, step=1000)

# Calculations
deposit = purchase_price * (deposit_percent / 100)
stamp_duty = 0
if purchase_price > 250000:
    stamp_duty = (0.05 * (purchase_price - 250000)) + (0.05 * 67500)
elif purchase_price > 125000:
    stamp_duty = 0.05 * (purchase_price - 125000)
else:
    stamp_duty = 0
stamp_duty += 0.03 * purchase_price  # Additional 3% for second homes

mortgage_fees = 1500
legal_fees = 1200
survey_fees = 600
total_fees = deposit + stamp_duty + refurb_cost + mortgage_fees + legal_fees + survey_fees

# Rental Yield and ROI
annual_rent = rent_pcm * 12
yield_percent = (annual_rent / purchase_price) * 100
re_mortgage = post_refurb_value * 0.75
cash_out = re_mortgage - (purchase_price + refurb_cost)
cash_left_in = total_fees - (re_mortgage - mortgage_fees)
roi = (annual_rent / cash_left_in) * 100 if cash_left_in > 0 else 0

st.header("📊 Financial Summary")
st.write(f"**Total Fees:** £{total_fees:,.2f}")
st.write(f"**Stamp Duty:** £{stamp_duty:,.2f}")
st.write(f"**Deposit:** £{deposit:,.2f}")
st.write(f"**Gross Yield:** {yield_percent:.2f}%")
st.write(f"**ROI:** {roi:.2f}%")
st.write(f"**Cash Left In After Refinance:** £{cash_left_in:,.2f}")

# Export Option
data = pd.DataFrame([{
    "Address": address,
    "Purchase Price": purchase_price,
    "Deposit": deposit,
    "Refurb Cost": refurb_cost,
    "Stamp Duty": stamp_duty,
    "Total Fees": total_fees,
    "Monthly Rent": rent_pcm,
    "Yield %": yield_percent,
    "ROI %": roi,
    "Cash Left In": cash_left_in
}])

st.download_button("📥 Download Deal as CSV", data.to_csv(index=False), "deal_analysis.csv")
