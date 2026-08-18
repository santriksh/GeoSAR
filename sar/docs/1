# Radiometry Module

## Overview

The Radiometry module contains algorithms that operate on the
radiometric values of SAR images.

Radiometric operations modify or compare the backscatter values while
preserving the spatial geometry of the image.

Current functions

- difference()
- db_to_linear()
- linear_to_db()
- ratio()

Future functions

- radiometric normalization
- incidence angle correction
- terrain correction utilities

---

# What is SAR Backscatter?

Synthetic Aperture Radar measures the amount of microwave energy
returned from the Earth's surface.

This returned energy is called **backscatter**.

Backscatter depends on

- surface roughness
- dielectric properties
- moisture content
- vegetation structure
- sensor geometry

Higher backscatter generally indicates stronger reflection toward the
sensor.

---

# Why are Sentinel-1 images stored in dB?

Although radar measures power in Linear units, Sentinel-1 GRD products
are commonly represented in **decibels (dB)**.

The conversion is

σ°(dB) = 10 log10(σ°Linear)

Reasons

- compresses the large dynamic range
- easier visualization
- easier interpretation
- standard representation in SAR literature

Typical values

Open Water        -25 dB to -15 dB

Agriculture       -15 dB to -8 dB

Forest            -10 dB to -5 dB

Urban              -5 dB to +5 dB

---

# Linear Representation

Many SAR algorithms require Linear power.

Conversion

Linear = 10^(dB / 10)

Linear values are always positive.

This representation preserves the physical relationship between
backscatter values.

Algorithms such as

- ratio()
- coefficient_of_variation()
- Lee filter

must operate on Linear data.

---

# Difference Image

Function

difference()

Formula

ΔVV = VVpost − VVpre

Input

- dB image
- dB image

Output

- dB image

Interpretation

Negative values

↓

Decrease in backscatter

Positive values

↓

Increase in backscatter

Difference images are useful for

- change detection
- flood mapping
- event monitoring

---

# Ratio Image

Function

ratio()

Formula

Ratio = Linearpost / Linearpre

Input

- dB image
- dB image

Internal processing

dB

↓

Linear

↓

Ratio

↓

Linear Output

Output

Linear

Ratio values

≈1

↓

No change

>1

↓

Increase

<1

↓

Decrease

---

# Why not compute ratio directly in dB?

Subtracting dB values is mathematically equivalent to

10 log10(post / pre)

This is called the **log-ratio**.

GeoSAR provides

difference()

for log-ratio

and

ratio()

for the true Linear ratio.

The two products serve different scientific purposes.

---

# dB ↔ Linear Conversion

GeoSAR provides

db_to_linear()

Purpose

Convert SAR backscatter from dB to Linear.

Typical use

- ratio()
- coefficient_of_variation()
- Lee filter

---

linear_to_db()

Purpose

Convert Linear backscatter back to dB.

Typical use

Visualization

Export

Comparison with Sentinel-1 products

---

# Choosing the Correct Representation

Operation                     Required Scale

difference()                  dB

local_mean()                  dB or Linear

local_variance()              dB or Linear

local_std()                   dB or Linear

ratio()                       Linear Output

coefficient_of_variation()    Linear

Lee Filter                    Linear

GLCM                          Usually Linear

---

# Scientific Validation

GeoSAR performs scientific validation in addition to software
validation.

Example

coefficient_of_variation()

accepts only Linear images.

Attempting to compute CV on dB images raises a ValueError because the
coefficient of variation is mathematically meaningful only for
positive-valued data.

This prevents scientifically invalid analyses.

---

# Typical Workflow

pre = load_sar(...)

post = load_sar(...)

post = align_to_reference(pre, post)

delta = difference(pre, post)

ratio = ratio(pre, post)

linear = db_to_linear(pre)

cv = coefficient_of_variation(linear)

---

# Summary

Difference

↓

Log-ratio

↓

dB Output

Ratio

↓

True ratio

↓

Linear Output

The choice depends on the scientific objective.

Difference is preferred for visual interpretation and many change
detection tasks.

Ratio is preferred for quantitative radiometric analysis and algorithms
that require Linear backscatter.



# Common Pitfalls

### 1. Confusing Difference with Ratio

Difference()

computes

VVpost(dB) − VVpre(dB)

Ratio()

computes

Linearpost / Linearpre

These products are related but not identical.

---

### 2. Computing CV on dB Images

Incorrect

cv = coefficient_of_variation(pre)

Correct

linear = db_to_linear(pre)

cv = coefficient_of_variation(linear)

---

### 3. Extremely Large Ratio Values

Very large ratio values often occur when the pre-event backscatter is
close to zero.

This is expected behaviour and reflects the mathematics of the ratio
rather than an implementation error.
