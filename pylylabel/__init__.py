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

def polylabel(ext, interiors=[], tolerance=1.0):
    """
    Calculate the optimum label position within a Polygon
    You may pass either a Shapely Polygon and a tolerance, or
    an exterior ring (list), a list of interior rings (list), and a tolerance

    Accepts Polygon instances as well as lists and lists of lists
    This is a terrible interface, but y'know, dynamic languages

    """
    if isinstance(ext, Polygon):
        _ext = ext.exterior.coords
        _interiors = [ring.coords for ring in ext.interiors]
        return polylabel_ffi(_ext, _interiors, tolerance)
    else:
        return polylabel_ffi(ext, interiors, tolerance)
