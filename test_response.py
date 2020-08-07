"""
Run the same tests as in the older version.
"""

from variable_decay import trending_score

class Claim:
    """
    Represent a claim and a pattern of support
    """

    def __init__(self, name, support_interval, support_lbc):
        self.name = name
        self.support_interval = support_interval
        self.support_lbc = support_lbc

    def generate_data(self, start_height, end_height, chunk_blocks=10):
        """
        Make Lex's data list and then trending scores
        """
        data = []

        supports = []
        for height in range(start_height, end_height + 1):
            if height % chunk_blocks == 0:
                if height > 0:
                     # height, max, min, sum, count, unique
                    row = [height,
                           max(supports), min(supports), sum(supports),
                           len(supports), 1]
                    data.append(row)
            # Add supports
            if height % self.support_interval == 0:
                supports.append(int(1E8*self.support_lbc))

        return data

    def plot_trending(self, start_height, end_height):
        data = self.generate_data(0, 1000)
        heights = [h for h in range(start_height, end_height+1001)]
        trending_scores = [trending_score(h, data) for h in heights]
        import matplotlib.pyplot as plt
        plt.plot(heights, trending_scores)
        plt.show()

if __name__ == "__main__":
    minnow = Claim("minnow", 1, 1)
    minnow.plot_trending(0, 1000)

