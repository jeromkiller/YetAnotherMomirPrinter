import numpy as np
from scipy.ndimage import gaussian_filter
from matplotlib import pyplot as plt

# generate some blue noise using the void and cluster algoritm
# mostly adapted from the fantastic blogpost https://github.com/laszlokorte/blue-noise

def generateNoise(width: int, height: int, sigma=2.0, initial_percentage=0.1, path: str ="noise.png"):
    shape = (width, height)

    # start with some white noise for a random seed
    white_noise = np.random.rand(width, height)
    placed_points = (white_noise <= initial_percentage).astype(float)

    gaussian = None
    swapped = None
    swaps = 0
    while True:
        # now move these initial points around to spread out the energy evenly
        gaussian = gaussian_filter(placed_points, sigma, mode='wrap')
        highest = (gaussian * placed_points).argmax()   # multiplying masks the non initial points, so we don't try to remove a point that isn't a pixel
        lowest = (gaussian + placed_points).argmin()   # adding makes sure we don't add to a point that's already a pixel
        highest_cord = np.unravel_index(highest, shape)
        lowest_cord = np.unravel_index(lowest, shape)

        if highest == lowest:
            break
        
        if swapped == (lowest_cord, highest_cord):
            break

        placed_points[highest_cord] = 0.0
        placed_points[lowest_cord] = 1.0
        swapped = (highest_cord, lowest_cord)
        swaps += 1

    # use the initial points to set our first values
    ranks = np.zeros((width, height))
    initial_rank = np.sum(placed_points)
    rank = initial_rank
    remove_points = placed_points.copy()
    while rank:
        gaussian = gaussian_filter(remove_points, sigma, mode='wrap')
        highest = (gaussian * remove_points).argmax()
        highest_cord = np.unravel_index(highest, (width, height))
        ranks[highest_cord] = rank
        remove_points[highest_cord] = 0.0
        rank -= 1

    # find the lowest energy point and place a new value there
    rank = initial_rank + 1
    total = width * height
    while rank <= total:
        gaussian = gaussian_filter(placed_points, sigma, mode='wrap')
        lowest = (gaussian + placed_points).argmin()
        lowest_cord = np.unravel_index(lowest, (width, height))
        placed_points[lowest_cord] = 1.0
        ranks[lowest_cord] = rank
        rank += 1


    plt.imsave(path, ranks, cmap='gray')
    return path


if __name__ == "__main__":
    generateNoise(128, 128)
    
