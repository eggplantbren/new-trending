"""
A simple AR-type example that only looks at `sum`.
"""
import math

# Decay timescale in blocks
DECAY_TIMESCALE = 250

def soften(y):
    """
    Soften LBC changes
    """
    return y**0.25

def delay(y):
    """
    Time delay of big supports
    """
    d = y**0.3333333
    return d

def decay_speedup_factor(y):
    """
    Speedup decay
    """
    if y < 1000.0:
        return 1.0
    return 1.0 + math.log10(y/1000.0)

def trending_score(height, data, chunk_blocks=10):
    """
    Output: Trending score
    """

    # Imagine some times in the midpoints of the chunks
    ts = [row[0] - 0.5*chunk_blocks for row in data[::-1]]

    # Get totals of supports, converted to LBC
    ys = [row[3]/1E8 for row in data[::-1]]

    # Sum all the exponential kernels
    trending = 0.0
    for t, y in zip(ts, ys):

        # Kernel amplitude, start time and decay rate
        amp = soften(y)
        t0  = t + delay(y)
        ell = DECAY_TIMESCALE/decay_speedup_factor(y)

        if height >= t0:
            trending += amp*math.exp(-(height - t0)/ell)

    return trending


if __name__ == "__main__":

    # Example data for a claim
    data = [
        # height, max, min, sum, count, unique
        (800000,  10E8,   5E8,  20E8,     3,      3),  # 10, 5, 5
        (799990,  10E8,   5E8,  15E8,     2,      2),  # 10, 5
        (799980,  6E12,   5E8,  6E12,     1,      1),  # 60000
        (799970,   2E8,   1E8,   7E8,     5,      3),  # 2, 2, 1, 1, 1
    ]

#    trending_score(800300, data)

    import matplotlib.pyplot as plt
    heights = range(799950, 801000)
    trends = []
    for height in heights:
        trends.append(trending_score(height, data))
    plt.plot(heights, trends, "-")
    plt.xlabel("Height")
    plt.ylabel("Trending Score")
    plt.show()


