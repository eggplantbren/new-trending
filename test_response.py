"""
Run the same tests as in the older version.
"""
import matplotlib.pyplot as plt
from variable_decay import trending_score

class Claim:
    """
    Represent a claim and a pattern of support
    """
    all_claims = []

    def __init__(self, name, supports):
        self.name = name
        self.supports = supports
        Claim.all_claims.append(self)

    def generate_data(self, start_height, end_height, chunk_blocks=10):
        """
        Make Lex's data list and then trending scores
        """
        data = []

        for height in range(start_height, end_height + 1):

            # Supports due this block
            supports = [1E8*s[1] for s in self.supports if s[0] == height]

            if height % chunk_blocks == 0:
                if len(supports) > 0:
                     # height, max, min, sum, count, unique
                    row = [height,
                           max(supports), min(supports), sum(supports),
                           len(supports), 1]
                    data.append(row)

        return data

    def plot_trending(self, start_height, end_height):
        data = self.generate_data(0, 1000)
        heights = [h for h in range(start_height, end_height+1001)]
        trending_scores = [trending_score(h, data) for h in heights]
        plt.plot(heights, trending_scores, label=self.name)

if __name__ == "__main__":

    # Time interval to plot
    start_height, end_height = 0, 1000

    Claim("Popular Minnow", [(h, 1.0) for h in range(400)])
    Claim("Dolphin", [(0, 1.0E4)])
    Claim("Blue Whale", [(0, 5.0E5)])
    for claim in Claim.all_claims:
        claim.plot_trending(start_height, end_height)
    plt.legend()
    plt.xlim(left=0.0)
    plt.ylim(bottom=0.0)
    plt.show()

