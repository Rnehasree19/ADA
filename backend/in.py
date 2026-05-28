from ad_to_coord import Geocoder
from distance import DistanceCalculator
from tsp import TSP
from maps_redirect import GoogleMapsRedirect
import webbrowser


class WeddingRouteOptimizer:

    def __init__(self):

        self.geocoder = Geocoder()
        self.start_location = ""
        self.delivery_addresses = []

    def collect_inputs(self):

        self.start_location = input(
            "Enter Starting Location: "
        )

        while True:

            try:

                n = int(
                    input(
                        "Enter Number of Delivery Addresses: "
                    )
                )

                if n <= 0:

                    raise ValueError(
                        "Number must be greater than 0."
                    )

                break

            except ValueError as error:

                print(f"\n[ERROR] {error}")

        print("\nEnter Delivery Addresses:")

        for i in range(n):

            address = input(f"Address {i + 1}: ")

            self.delivery_addresses.append(address)

    def get_all_locations(self):

        all_locations = []

        start_coords = (
            self.geocoder.get_coordinates(
                self.start_location
            )
        )

        if start_coords:

            all_locations.append(
                (
                    self.start_location,
                    start_coords
                )
            )

        else:

            print(
                "\n[ERROR] Invalid starting location."
            )

            return []

        for address in self.delivery_addresses:

            coords = (
                self.geocoder.get_coordinates(
                    address
                )
            )

            if coords:

                all_locations.append(
                    (address, coords)
                )

            else:

                print(
                    f"\nSkipping invalid location:"
                    f" {address}"
                )

        return all_locations

    def display_coordinates(self, all_locations):

        print("\n===== LOCATIONS =====")

        for location, coords in all_locations:

            print(f"\nAddress: {location}")

            print(
                f"Coordinates: {coords}"
            )

    def display_distances(self, all_locations):

        print("\n===== DISTANCES =====")

        for i in range(len(all_locations)):

            for j in range(i + 1, len(all_locations)):

                loc1, coord1 = all_locations[i]
                loc2, coord2 = all_locations[j]

                distance = (
                    DistanceCalculator.calculate_distance(
                        coord1,
                        coord2
                    )
                )

                if distance:

                    print(
                        f"\n{loc1} -> {loc2}"
                    )

                    print(
                        f"Distance: {distance} km"
                    )

    def solve_tsp(self, all_locations):

        n = len(all_locations)

        if n < 2:

            print(
                "\n[ERROR] Not enough valid "
                "locations for TSP."
            )

            return

        cost_matrix = [
            [0 for _ in range(n)]
            for _ in range(n)
        ]

        for i in range(n):

            for j in range(n):

                if i != j:

                    distance = (
                        DistanceCalculator.calculate_distance(
                            all_locations[i][1],
                            all_locations[j][1]
                        )
                    )

                    if distance:

                        cost_matrix[i][j] = distance

        tsp_solver = TSP(cost_matrix)

        minimum_cost, best_path = tsp_solver.solve()

        print("\n===== OPTIMAL ROUTE =====\n")

        optimized_route = []

        for index in best_path:

            location_name = (
                all_locations[index][0]
            )

            optimized_route.append(
                location_name
            )

            print(location_name)

        print(
            f"\nMinimum Distance: "
            f"{minimum_cost} km"
        )

        maps_url = (
            GoogleMapsRedirect.generate_maps_url(
                optimized_route
            )
        )

        print("\n===== GOOGLE MAPS ROUTE =====\n")

        print(maps_url)

        webbrowser.open(maps_url)

    def run(self):

        try:

            self.collect_inputs()

            all_locations = (
                self.get_all_locations()
            )

            if not all_locations:

                return

            self.display_coordinates(
                all_locations
            )

            self.display_distances(
                all_locations
            )

            self.solve_tsp(
                all_locations
            )

        except KeyboardInterrupt:

            print(
                "\n\n[INFO] Program interrupted "
                "by user."
            )

        except Exception as error:

            print(
                f"\n[UNEXPECTED ERROR] {error}"
            )


if __name__ == "__main__":

    app = WeddingRouteOptimizer()

    app.run()