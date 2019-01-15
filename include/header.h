/* Generated with cbindgen:0.6.8 */

/* Warning, this file is autogenerated by cbindgen. Don't modify this manually. */

#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

/**
 * FFI struct for returned optimum Polygon label position
 */
typedef struct Position {
    double x_pos;
    double y_pos;
} Position;

/**
 * Wrapper for a void pointer to a sequence of 2-element arrays representing points, and the sequence length. Used for FFI.
 * Used for the outer Polygon shell. `data` is a `Vec<[c_double; 2]>`.
 */
typedef struct Array {
    const void *data;
    size_t len;
} Array;

/**
 * Wrapper for a void pointer to a sequence of [`Array`](struct.Array.html)s, and the sequence length. Used for FFI.
 * Each sequence entry represents an inner Polygon ring.
 */
typedef struct WrapperArray {
    const Array *data;
    size_t len;
} WrapperArray;

/**
 * FFI access to the [`polylabel`](fn.polylabel.html) function
 * Accepts three arguments:
 * - an exterior ring [`Array`](struct.Array.html)
 * - zero or more interior rings [`WrapperArray`](struct.WrapperArray.html)
 * - a tolerance `c_double`.
 */
Position polylabel_ffi(Array outer, WrapperArray inners, double tolerance);
