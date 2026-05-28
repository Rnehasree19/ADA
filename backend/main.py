from fastapi import FastAPI
from fastapi import Request

from fastapi.middleware.cors import CORSMiddleware

from ad_to_coord import Geocoder
from distance import DistanceCalculator
from tsp import TSP
from maps_redirect import GoogleMapsRedirect


app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:8501"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Backend running"
    }


@app.post("/optimize-route")
async def optimize_route(request: Request):

    data = await request.json()

    geocoder = Geocoder()

    all_locations = []

    start_coords = geocoder.get_coordinates(
        data["start_location"]
    )

    if not start_coords:

        return {
            "error": "Invalid start location"
        }

    all_locations.append(
        (
            data["start_location"],
            start_coords
        )
    )

    for address in data["delivery_addresses"]:

        coords = geocoder.get_coordinates(
            address
        )

        if coords:

            all_locations.append(
                (
                    address,
                    coords
                )
            )

    n = len(all_locations)

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

                cost_matrix[i][j] = distance

    tsp_solver = TSP(cost_matrix)

    minimum_cost, best_path = tsp_solver.solve()

    optimized_route = []

    for index in best_path:

        optimized_route.append(
            all_locations[index][0]
        )

    maps_url = (
        GoogleMapsRedirect.generate_maps_url(
            optimized_route
        )
    )

    return {

        "route": optimized_route,

        "distance": minimum_cost,

        "maps_url": maps_url
    }