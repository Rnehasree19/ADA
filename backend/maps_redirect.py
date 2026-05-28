class GoogleMapsRedirect:

    @staticmethod
    def generate_maps_url(route_locations):

        base_url = (
            "https://www.google.com/maps/dir/"
        )

        formatted_locations = []

        for location in route_locations:

            formatted_location = (
                location.replace(" ", "+")
            )

            formatted_locations.append(
                formatted_location
            )

        final_url = (
            base_url +
            "/".join(formatted_locations)
        )

        return final_url