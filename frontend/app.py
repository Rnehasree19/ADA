import streamlit as st
import requests
import sys
import os

sys.path.append(
    os.path.abspath("C:/Users/nagme/OneDrive/Desktop/ADA/backend")
)

API_URL = "http://127.0.0.1:8000/optimize-route"

st.set_page_config(

    page_title="Wedding Route Optimizer",

    layout="centered"
)

st.title("Wedding Route Optimizer")

st.markdown(
    """
    Optimize wedding delivery routes using:
    - Geolocation
    - Distance Calculation
    - TSP Algorithm
    - Google Maps Integration
    """
)

start_location = st.text_input(
    "Enter Starting Location"
)

num_addresses = st.number_input(

    "Number of Delivery Addresses",

    min_value=1,

    step=1
)

delivery_addresses = []

st.subheader("Delivery Addresses")

for i in range(num_addresses):

    address = st.text_input(
        f"Address {i + 1}",
        key=i
    )

    if address:

        delivery_addresses.append(address)

if st.button("Optimize Route"):

    if not start_location:

        st.error(
            "Please enter starting location."
        )

    elif len(delivery_addresses) == 0:

        st.error(
            "Please enter delivery addresses."
        )

    else:

        payload = {

            "start_location": start_location,

            "delivery_addresses":
                delivery_addresses
        }

        try:

            with st.spinner(
                "Optimizing Route..."
            ):

                response = requests.post(
                    API_URL,
                    json=payload
                )

            data = response.json()

            if "error" in data:

                st.error(data["error"])

            else:

                st.success(
                    "Route Optimized Successfully!"
                )

                st.subheader(
                    "Optimized Route"
                )

                for i, location in enumerate(
                    data["route"]
                ):

                    st.write(
                        f"{i+1}. {location}"
                    )

                st.subheader(
                    "Minimum Distance"
                )

                st.info(
                    f"{data['distance']} km"
                )

                st.subheader(
                    "Google Maps Route"
                )

                st.markdown(

                    f"""
                    [Open Route in Google Maps]
                    ({data['maps_url']})
                    """
                )

        except Exception as error:

            st.error(
                f"Backend connection failed:\n{error}"
            )