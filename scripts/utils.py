#!/usr/bin/env python3
import math


def clean(values):
    """Filter out invalid LiDAR values (0, inf, nan)."""
    return [r for r in values if r > 0.0 and not math.isinf(r) and not math.isnan(r)]
