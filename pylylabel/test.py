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

from . import polylabel
from shapely.geometry import Polygon

if __name__ == "__main__":
    # test that everything's working

    exterior = [[4.0, 1.0], [5.0, 2.0], [5.0, 3.0], [4.0, 4.0], [3.0, 4.0], [2.0, 3.0], [2.0, 2.0], [3.0, 1.0], [4.0, 1.0]]
    res = polylabel([exterior], tolerance=0.1)
    if res != (3.5, 2.5, 1.4142135623730951): 
        raise ValueError(f"Polylabel returned an incorrect value: {res}")

    interiors = [
                    [[3.5, 3.5], [4.4, 2.0], [2.6, 2.0], [3.5, 3.5]],
                    [[4.0, 3.0], [4.0, 3.2], [4.5, 3.2], [4.0, 3.0]],
                ]

    res = polylabel([exterior, *interiors], tolerance=0.1)
    if res != (3.125, 2.875, 0.8838834764831844):
        raise ValueError(f"Polylabel returned an incorrect value: {res}")

    # A Shapely polygon
    res = polylabel(Polygon(exterior, interiors), tolerance=0.1)
    if res != (3.125, 2.875, 0.8838834764831844):
        raise ValueError(f"Polylabel returned an incorrect value: {res}")
