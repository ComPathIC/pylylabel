use std::slice;

extern crate libc;
use self::libc::{c_void, c_double, size_t};

use super::geo::{Point, Polygon, LineString};

use super::polylabel;
use super::num::Float;

/// Wrapper for a void pointer to a sequence of [`Array`](struct.Array.html)s, and the sequence length
///
/// Used for inner Polygon rings
#[repr(C)]
pub struct WrapperArray {
    pub data: *const Array,
    pub len: size_t,
}

/// Wrapper for a void pointer to a sequence of 2-element arrays representing points, and the sequence length
///
/// Used for outer Polygon rings. `data` is a `Vec<[c_double; 2]>`
#[repr(C)]
pub struct Array {
    pub data: *const c_void,
    pub len: size_t,
}

/// FFI struct for returned optimum Polygon label position
#[repr(C)]
pub struct Position {
    pub x_pos: c_double,
    pub y_pos: c_double,
}

// convert a Polylabel result Point into values that can be sent across the FFI boundary
impl<T> From<Point<T>> for Position
    where T: Float
{
    fn from(point: Point<T>) -> Position {
        Position {
            x_pos: point.x().to_f64().unwrap() as c_double,
            y_pos: point.y().to_f64().unwrap() as c_double,
        }
    }
}

fn reconstitute(arr: &Array) -> Vec<[f64; 2]> {
    unsafe { slice::from_raw_parts(arr.data as *mut [f64; 2], arr.len).to_vec() }
}

fn reconstitute2(arr: WrapperArray) -> Vec<Vec<[f64; 2]>> {
    let arrays = unsafe { slice::from_raw_parts(arr.data as *mut Array, arr.len) };
    arrays.into_iter().map(|x| reconstitute(x)).collect()
}

/// FFI access to the [`polylabel`](fn.polylabel.html) function
///
/// Accepts three arguments: an exterior ring [`Array`](struct.Array.html), an interior rings [`WrapperArray`](struct.WrapperArray.html), and a tolerance `c_float`.
#[no_mangle]
pub extern "C" fn polylabel_ffi(outer: Array,
                                inners: WrapperArray,
                                tolerance: c_double)
                                -> Position {
    let exterior: Vec<[f64; 2]> =
        unsafe { slice::from_raw_parts(outer.data as *mut [c_double; 2], outer.len).to_vec() };
    let interior: Vec<Vec<[f64; 2]>> = reconstitute2(inners);
    let ls_ext = LineString(exterior.iter().map(|e| Point::new(e[0], e[1])).collect());
    let ls_int: Vec<LineString<c_double>> = interior.iter()
        .map(|vec| LineString(vec.iter().map(|e| Point::new(e[0], e[1])).collect()))
        .collect();

    let poly = Polygon(ls_ext, ls_int);
    polylabel(&poly, &tolerance).into()
}

#[cfg(test)]
mod tests {
    use super::{Array, WrapperArray, reconstitute2};
    use super::libc::{c_void, size_t};
    use std::mem;

    // Only used for testing
    fn gen_array(v: Vec<[f64; 2]>) -> Array {
        let array = Array {
            data: v.as_ptr() as *const c_void,
            len: v.len() as size_t,
        };
        mem::forget(v);
        array
    }
    // only used for testing
    fn gen_wrapperarray(v: Vec<Vec<[f64; 2]>>) -> WrapperArray {
        let converted: Vec<Array> = v.into_iter().map(|x| gen_array(x)).collect();
        let array2 = WrapperArray {
            data: converted.as_ptr() as *const Array,
            len: converted.len() as size_t,
        };
        mem::forget(converted);
        array2
    }
    #[test]
    fn test_array() {
        let i_a = vec![[0.5, 0.5], [1.0, 1.0], [1.5, 0.5]];
        let i_b = vec![[0.55, 0.55], [0.8, 0.8], [1.2, 0.55]];
        let inners = vec![i_a, i_b];
        let array = gen_wrapperarray(inners);
        let rec_inners = reconstitute2(array);
        assert_eq!(rec_inners[0][2], [1.5, 0.5])
    }

}