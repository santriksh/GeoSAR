"""
Assam Flood Detection Example

Session 1
---------

1. Read Sentinel-1 images
2. Inspect metadata
3. Apply Refined Lee
4. Inspect filtered images
"""
import os
import sys
module_path = os.path.abspath(os.path.expanduser("~/notebooks/geospatial/"))
# print(f"Module path is {module_path}")
# print(f"Sys path is {sys.path}")
if module_path not in sys.path:
    print("$$$$$$$$")
    sys.path.append(module_path)
from pathlib import Path
from sar.sar_geometry import align_to_reference
import numpy as np
from sar.sar_radiometry import (db_to_linear,linear_to_db)
from sar.threshold import *
from sar.filters.refined_lee_geosar import (
    refined_lee,
)
from sar.sar_io import load_sar
from sar.sar_change import *


DATA_DIR = Path("/home/ubuntu/notebooks/geospatial")

PRE_IMAGE = (
    DATA_DIR /
    "sample_image_preflood1.tif"
)

POST_IMAGE = (
    DATA_DIR /
    "sample_image_postflood1.tif"
)


print("=" * 70)
print("READING IMAGES")
print("=" * 70)

pre = load_sar(
    PRE_IMAGE,
)

post = load_sar(
    POST_IMAGE,
)

if pre.value_scale.lower() == "db":
    print("Converting pre image to linear...")
    pre = db_to_linear(pre)

if post.value_scale.lower() == "db":
    print("Converting post image to linear...")
    post = db_to_linear(post)

print("Done.\n")


def summarize_image(
    image,
    name,
):
    """
    Print a concise summary of a SAR image.
    """

    print("=" * 70)
    print(name)
    print("=" * 70)

    print(
        f"Shape        : {image.shape}"
    )

    print(
        f"CRS          : {image.crs}"
    )

    print(
        f"Value Scale  : {image.value_scale}"
    )

    print(
        f"Resolution   : {image.metadata.spatial.resolution}"
    )

    valid = image.data[
        image.mask
    ]
    valid = valid[
    np.isfinite(valid)
    ]

    print(
        f"Valid Pixels : {valid.size}"
    )

    print(
        f"Minimum      : {valid.min():.6f}"
    )

    print(
        f"Maximum      : {valid.max():.6f}"
    )

    print(
        f"Mean         : {valid.mean():.6f}"
    )

    print(
        f"Std Dev      : {valid.std():.6f}"
    )

    print()


summarize_image(
    pre,
    "PRE-FLOOD IMAGE",
)

summarize_image(
    post,
    "POST-FLOOD IMAGE",
)



print("=" * 70)
print("VALIDATION")
print("=" * 70)


if pre.shape != post.shape:

    print(
        "Aligning post image..."
    )

    post = align_to_reference(
        reference=pre,
        moving=post,
    )

assert (
    pre.crs
    ==
    post.crs
)

assert (
    pre.value_scale
    ==
    post.value_scale
)

print("✓ Images are compatible.\n")

print("=" * 70)
print("PRE IMAGE BEFORE REFINED LEE")
print("=" * 70)

print(
    "NaNs:",
    np.isnan(pre.data).sum(),
)

print(
    "Mask True:",
    pre.mask.sum(),
)

print(
    "NaNs inside valid:",
    np.isnan(
        pre.data[
            pre.mask
        ]
    ).sum(),
)

print("=" * 70)
print("APPLYING REFINED LEE")
print("=" * 70)

pre_filtered = refined_lee(
    pre,
)

# print("=" * 70)
# print("REFINED LEE DIAGNOSTICS")
# print("=" * 70)

# print(
#     "Total pixels:",
#     pre_filtered.data.size,
# )

# print(
#     "NaN pixels:",
#     np.isnan(pre_filtered.data).sum(),
# )

# print(
#     "Finite pixels:",
#     np.isfinite(pre_filtered.data).sum(),
# )

# print(
#     "Mask True:",
#     pre_filtered.mask.sum(),
# )

# print(
#     "Mask False:",
#     (~pre_filtered.mask).sum(),
# )
# ###############################
# print("=" * 70)
# print("NaN Debug")
# print("=" * 70)
# print("NaN pixels:", np.isnan(pre_filtered.data).sum())
# print("Finite pixels:", np.isfinite(pre_filtered.data).sum())
# print("Mask True:", pre_filtered.mask.sum())
# print("NaNs inside valid:", np.isnan(pre_filtered.data[pre_filtered.mask]).sum())
# #######################

post_filtered = refined_lee(
    post,
)

print("Done.\n")


summarize_image(
    pre_filtered,
    "PRE-FLOOD (FILTERED)",
)

summarize_image(
    post_filtered,
    "POST-FLOOD (FILTERED)",
)

print("=" * 70)
print("SESSION 1 COMPLETE")
print("=" * 70)

print(
    "Images successfully read and filtered."
)


print("=" * 70)
print("CHANGE DETECTION")
print("=" * 70)

difference = difference_change(
    pre_filtered,
    post_filtered,
)

ratio = ratio_change(
    pre_filtered,
    post_filtered,
)

log_ratio = log_ratio_change(
    pre_filtered,
    post_filtered,
)

print("Done.\n")


import matplotlib.pyplot as plt
import numpy as np


def show_change_image(
    image,
    title,
    cmap,
    percentile=2,
):
    """
    Display a change image using robust
    percentile stretching.
    """

    valid = image.data[image.mask]

    vmin = np.percentile(
        valid,
        percentile,
    )

    vmax = np.percentile(
        valid,
        100 - percentile,
    )

    plt.figure(figsize=(10, 8))

    plt.imshow(
        image.data,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    plt.colorbar()

    plt.title(title)

    plt.tight_layout()

    plt.show()


show_change_image(
    difference,
    "Difference Change",
    cmap="RdBu",
)

show_change_image(
    ratio,
    "Ratio Change",
    cmap="viridis",
)

show_change_image(
    log_ratio,
    "Log Ratio Change (dB)",
    cmap="RdBu",
)


def print_statistics(
    image,
    name,
):
    valid = image.data[image.mask]

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Minimum : {valid.min():.4f}")
    print(f"Maximum : {valid.max():.4f}")
    print(f"Mean    : {valid.mean():.4f}")
    print(f"Median  : {np.median(valid):.4f}")
    print(f"Std Dev : {valid.std():.4f}")

print_statistics(
    difference,
    "Difference",
)

print_statistics(
    ratio,
    "Ratio",
)

print_statistics(
    log_ratio,
    "Log Ratio",
)


def show_histogram(
    image,
    title,
    bins=200,
):
    valid = image.data[image.mask]

    plt.figure(figsize=(8, 5))

    low = np.percentile(valid, 1)
    high = np.percentile(valid, 99)

    plt.hist(
    valid[
        (valid >= low)
        &
        (valid <= high)
    ],
    bins=200,
)

    # plt.hist(
    #     valid,
    #     bins=bins,
    # )

    plt.title(title)

    plt.xlabel("Value")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.show()



show_histogram(
    difference,
    "Difference",
)

show_histogram(
    ratio,
    "Ratio",
)

show_histogram(
    log_ratio,
    "Log Ratio",
)


thresholds = [-1,-2,-3,-4,-5,-6,]

for t in thresholds:

    binary = threshold_less_than(
        log_ratio,
        t,
    )

    show_binary(
        binary,
        f"Threshold = {t} dB",
    )


for t in thresholds:

    binary = threshold_less_than(
        log_ratio,
        t,
    )

    flooded = binary.data.sum()

    percentage = (
        100
        * flooded
        / log_ratio.mask.sum()
    )

    print(
        f"{t:5.1f} dB : "
        f"{flooded:10d} pixels "
        f"({percentage:.2f}%)"
    )

    
areas = []

for t in thresholds:

    binary = threshold_less_than(
        log_ratio,
        t,
    )

    areas.append(
        binary.data.sum()
    )


plt.figure(figsize=(7,5))

plt.plot(
    thresholds,
    areas,
    marker="o",
)

plt.grid(True)

plt.xlabel("Threshold (dB)")

plt.ylabel("Flooded Pixels")

plt.title("Threshold Sensitivity")

plt.show()