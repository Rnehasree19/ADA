class TSP:

    def __init__(self, cost_matrix):

        self.cost = cost_matrix

        self.n = len(cost_matrix)

        self.minimum_cost = float('inf')

        self.best_path = []

    def dfs(
        self,
        vis,
        last,
        cnt,
        current_cost,
        path
    ):

        if cnt == self.n:

            current_cost += self.cost[last][0]

            complete_path = path + [0]

            if current_cost < self.minimum_cost:

                self.minimum_cost = current_cost

                self.best_path = complete_path

            return

        for city in range(1, self.n):

            if not vis[city]:

                vis[city] = True

                self.dfs(

                    vis,

                    city,

                    cnt + 1,

                    current_cost + self.cost[last][city],

                    path + [city]
                )

                vis[city] = False

    def solve(self):

        vis = [False] * self.n

        vis[0] = True

        self.dfs(

            vis,

            0,

            1,

            0,

            [0]
        )

        return (
            round(self.minimum_cost, 2),
            self.best_path
        )