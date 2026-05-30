import streamlit as st
import requests

# Replace this after deploying FastAPI on Render
API_URL = "https://ada-1-mywf.onrender.com/optimize-route"

st.set_page_config(
    page_title="Wedding Route Optimizer",
    layout="centered"
)

st.title("Wedding Route Optimizer")

st.markdown("""
### Features
- Geolocation
- Distance Calculation
- Traveling Salesman Problem (TSP)
- Google Maps Integration
""")

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
        key=f"address_{i}"
    )

    if address.strip():
        delivery_addresses.append(address)

if st.button("Optimize Route"):

    if not start_location.strip():
        st.error("Please enter starting location.")

    elif len(delivery_addresses) == 0:
        st.error("Please enter at least one delivery address.")

    else:

        payload = {
            "start_location": start_location,
            "delivery_addresses": delivery_addresses
        }

        try:

            with st.spinner("Optimizing Route..."):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=60
                )

                response.raise_for_status()

                data = response.json()

            if "error" in data:

                st.error(data["error"])

            else:

                st.success(
                    "Route Optimized Successfully!"
                )

                st.subheader("Optimized Route")

                for i, location in enumerate(data["route"]):
                    st.write(f"{i + 1}. {location}")

                st.subheader("Minimum Distance")

                st.info(f"{data['distance']} km")

                st.subheader("Google Maps Route")

                st.markdown(
                    f"[Open Route in Google Maps]({data['maps_url']})"
                )

        except requests.exceptions.Timeout:
            st.error(
                "Request timed out. Backend took too long to respond."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to backend. Check if FastAPI server is running."
            )

        except requests.exceptions.HTTPError as e:
            st.error(
                f"HTTP Error: {e}"
            )

        except Exception as e:
            st.error(
                f"Unexpected Error: {e}"
            )
