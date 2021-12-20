from numpy.core.fromnumeric import ndim
from skimage.measure import label,regionprops
from skimage.filters import threshold_triangle
from skimage import filters
from scipy import ndimage
import os, re, numpy as np, math
import matplotlib.pyplot as plt

tear = os.listdir()
pencils = 0

def get_ratio(reg):
    y0, x0 = reg.local_centroid
    orientation = reg.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * reg.minor_axis_length
    y1 = y0 - math.sin(orientation) * 0.5 * reg.minor_axis_length
    x2 = x0 - math.sin(orientation) * 0.5 * reg.major_axis_length
    y2 = y0 - math.cos(orientation) * 0.5 * reg.major_axis_length
    return  math.sqrt((x1-x0)**2+(y1-y0)**2),math.sqrt((x2-x0)**2+(y2-y0)**2)

def sort_key(e):
    return e.area

for i in tear:
    if re.match(r".+.jpg", i):
        count = 0
        image = plt.imread(i)
        image = np.mean(image, 2).astype("uint8")
        sobel = filters.sobel(image)
        th = filters.threshold_li(sobel)
        sobel[sobel < th] = 0
        sobel[sobel > 0] = 1
        sb = ndimage.binary_fill_holes(sobel)
        for j in range(5):
            sb = ndimage.binary_erosion(sb)
        labeled = label(sb)
        regions = regionprops(labeled)
        regions = sorted(regions, key = sort_key, reverse = True)
        for region in regions:
            if region.area < 10000:
                continue
            a,b = get_ratio(region)
            count = count + 1 if a / b > 10 or b / a > 10 else count
        print("На изображении", i, "количество карандашей =", count, sep=" ")
        pencils += count

print("Общее количество карандашей =", pencils, sep=" ")