import os
import sys
module_path = os.path.abspath(os.path.expanduser("~/notebooks/geospatial/"))
# print(f"Module path is {module_path}")
# print(f"Sys path is {sys.path}")
if module_path not in sys.path:
    print("$$$$$$$$")
    sys.path.append(module_path)

from pathlib import Path

import logging

#from sar.io import read_geotiff
from sar.sar_io import load_sar

from sar.pipeline.flood import detect_flood

# from sar.visualization import (
#     display,
#     display_overlay,compare,
# )
from sar.visualization import compare

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

DATA = Path("/home/ubuntu/notebooks/geospatial/")

PRE_IMAGE = (
    DATA /
    "sample_image_preflood1.tif"
)

POST_IMAGE = (
    DATA /
    "sample_image_postflood1.tif"
)

pre = load_sar(
    PRE_IMAGE,
)

post = load_sar(
    POST_IMAGE,
)

result = detect_flood(
    before=pre,
    after=post,

    threshold=-2.5,

    apply_refined_lee=True,

    min_object_size=50,
)

# display(
#     result.log_ratio,
#     title="Log Ratio",
# )

# display(
#     result.flood_mask,
#     title="Detected Flood",
# )

# display_overlay(
#     image=post,
#     mask=result.flood_mask,
#     title="Detected Flood",
# 

compare(
    before=result.before,
    after=result.after,
    log_ratio=result.log_ratio,
    flood_mask=result.flood_mask,
)

stats = result.statistics

print()

print("=" * 60)
print("FLOOD STATISTICS")
print("=" * 60)

print(
    f"Flooded Pixels      : "
    f"{stats.flooded_pixels:,}"
)

print(
    f"Flooded Area (m²)   : "
    f"{stats.flooded_area_m2:,.0f}"
)

print(
    f"Flooded Area (ha)   : "
    f"{stats.flooded_area_hectares:,.2f}"
)

print(
    f"Flood Percentage    : "
    f"{stats.flooded_percentage:.2f}%"
)


