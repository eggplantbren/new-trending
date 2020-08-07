"""
A simple AR-type example that only looks at `sum`.
"""
import math

# Decay timescale in blocks
DECAY_TIMESCALE = 250

def trending_score(height, data, chunk_blocks=10):
    """
    Output: Trending score
    """

    # A simple softening function
    def soften(change):
        return change**0.25

    # Imagine some times in the midpoints of the chunks
    ts = [row[0] - 0.5*chunk_blocks for row in data[::-1]]
    ys = [soften(row[3]) for row in data[::-1]]

    # Sum exponential kernels
    trending = 0.0
    for t, y in zip(ts, ys):
        if t <= height:
            gap = height - t
            trending += y*math.exp(-gap/DECAY_TIMESCALE)

    return trending


if __name__ == "__main__":

    # Example data for a claim
    data = [
        # height, max, min, sum, count, unique
        (800000,  10,   5,  20,     3,      3),  # 10, 5, 5
        (799990,  10,   5,  15,     2,      2),  # 10, 5
        (799980,   6,   5,  16,     3,      3),  # 6, 5, 5
        (799970,   2,   1,   7,     5,      3),  # 2, 2, 1, 1, 1
    ]


    import matplotlib.pyplot as plt
    heights = range(799950, 801000)
    trends = []
    for height in heights:
        trends.append(trending_score(height, data))
    plt.plot(heights, trends, "o-")
    plt.show()


