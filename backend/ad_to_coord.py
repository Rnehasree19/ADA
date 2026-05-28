import requests


class Geocoder:

    BASE_URL = (
        "https://nominatim.openstreetmap.org/search"
    )

    def get_coordinates(self, address):

        try:

            if not address.strip():

                raise ValueError(
                    "Address cannot be empty."
                )

            params = {
                "q": address,
                "format": "json",
                "limit": 1
            }

            headers = {
                "User-Agent":
                    "wedding-route-optimizer"
            }

            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if not data:

                raise ValueError(
                    f"Location not found: {address}"
                )

            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])

            return latitude, longitude

        except requests.exceptions.Timeout:

            print(
                "\n[ERROR] Request timed out."
            )

        except requests.exceptions.ConnectionError:

            print(
                "\n[ERROR] No internet connection."
            )

        except requests.exceptions.HTTPError:

            print(
                "\n[ERROR] API request failed."
            )

        except ValueError as error:

            print(f"\n[ERROR] {error}")

        except Exception as error:

            print(
                f"\n[UNEXPECTED ERROR] {error}"
            )

        return None