#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ffi.py

Created by Stephan Hügel on 2016-08-25

This file is part of polylabel-rs.

The MIT License (MIT)

Copyright (c) 2016 Stephan Hügel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from shapely.geometry import Polygon
from .pylylabel import polylabel_ffi

def polylabel(geometry, tolerance=1.0):
    """
    Calculate the optimum label position within a Polygon
    geometry is either a Shapely Polygon, or a geojson-like
    polygon geometry (a list of rings where the first one is the
    exterior ring, followed by interior rings, where a ring is a list
    of [x, y] coordinates)
    """
    if isinstance(geometry, Polygon):
        exterior = geometry.exterior.coords
        interiors = [ring.coords for ring in geometry.interiors]
    else:
        exterior = geometry[0]
        interiors = geometry[1:]
    return polylabel_ffi(exterior, interiors, tolerance)
