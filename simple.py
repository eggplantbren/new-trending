import math

DECAY_TIMESCALE = 300.0

def trending(heights, lbc):
    """
    Compute trending trajectory
    """
    ys = [0.0]
    for i in range(1, len(heights)):
        gap  = heights[i] - heights[i-1]
        mag  = abs(lbc[i]**0.25 - lbc[i-1]**0.25)
        sign = 1.0 if lbc[i] > lbc[i-1] else -1.0
        rate = 1.0/DECAY_TIMESCALE
        if lbc[i] >= 100.0:
            rate *= 1.0 + math.log10(lbc[i]/100.0)
        ys.append(math.exp(-rate)*ys[-1] + mag*sign)
    return ys

if __name__ == "__main__":

    # Create some data
    # Initial publication bid
    heights = [0]
    lbc = [0.1]

    # 10 LBC more every 10th block
    for i in range(1, 1001):
        if i % 10 == 0:
            heights.append(i)
            lbc.append(lbc[-1] + 10.0)

    import matplotlib.pyplot as plt
    plt.plot(heights, lbc, "o-")
    plt.plot(heights, trending(heights, lbc), "o-")
    plt.show()

