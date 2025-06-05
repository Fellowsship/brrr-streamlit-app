
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="BRRR Deal Analyzer", layout="wide")
st.title("🏠 BRRR Property Deal Analyzer")

st.sidebar.header("📂 Upload CSV (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload a CSV of property deals", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded successfully!")
else:
    st.info("Or manually enter a new property deal below.")
    address = st.text_input("Property Address")
    latitude = st.number_input("Latitude (for map)", value=51.5)
    longitude = st.number_input("Longitude (for map)", value=-0.12)
    purchase_price = st.number_input("Purchase Price (£)", min_value=50000, step=1000)
    deposit_percent = st.slider("Deposit (%)", min_value=10, max_value=50, value=25)
    refurb_cost = st.number_input("Refurbishment Cost (£)", min_value=0, step=500)
    rent_pcm = st.number_input("Expected Monthly Rent (£)", min_value=0, step=50)
    post_refurb_value = st.number_input("Post-Refurbishment Value (£)", min_value=0, step=1000)

    # Calculate
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

    annual_rent = rent_pcm * 12
    yield_percent = (annual_rent / purchase_price) * 100
    re_mortgage = post_refurb_value * 0.75
    cash_out = re_mortgage - (purchase_price + refurb_cost)
    cash_left_in = total_fees - (re_mortgage - mortgage_fees)
    roi = (annual_rent / cash_left_in) * 100 if cash_left_in > 0 else 0

    df = pd.DataFrame([{
        "Address": address,
        "Lat": latitude,
        "Lon": longitude,
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

st.header("📊 Filter by Investment Goals")
min_roi = st.slider("Minimum ROI (%)", 0, 50, 10)
min_yield = st.slider("Minimum Yield (%)", 0, 20, 5)
max_cash_left = st.slider("Max Cash Left In (£)", 0, 100000, 25000)

filtered_df = df[
    (df["ROI %"] >= min_roi) &
    (df["Yield %"] >= min_yield) &
    (df["Cash Left In"] <= max_cash_left)
]

st.dataframe(filtered_df)

st.download_button("📥 Download Filtered Deals", filtered_df.to_csv(index=False), "filtered_deals.csv")

st.header("🗺️ Map of Properties (UK)")
if "Lat" in filtered_df.columns and "Lon" in filtered_df.columns:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=54.0,
            longitude=-2.0,
            zoom=5,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered_df,
                get_position='[Lon, Lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=3000,
            ),
        ],
    ))
