import math


class DistanceCalculator:

    EARTH_RADIUS_KM = 6371

    @staticmethod
    def calculate_distance(coord1, coord2):

        try:

            if coord1 is None or coord2 is None:

                raise ValueError(
                    "Invalid coordinates provided."
                )

            lat1, lon1 = coord1
            lat2, lon2 = coord2

            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)

            lat2 = math.radians(lat2)
            lon2 = math.radians(lon2)

            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = (
                math.sin(dlat / 2) ** 2
                +
                math.cos(lat1)
                * math.cos(lat2)
                * math.sin(dlon / 2) ** 2
            )

            c = 2 * math.atan2(
                math.sqrt(a),
                math.sqrt(1 - a)
            )

            distance = (
                DistanceCalculator.EARTH_RADIUS_KM * c
            )

            return round(distance, 2)

        except ValueError as error:

            print(f"\n[ERROR] {error}")

        except Exception as error:

            print(
                f"\n[UNEXPECTED ERROR] {error}"
            )

        return None