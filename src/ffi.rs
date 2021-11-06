use crate::polylabel;
use geo::{LineString, Point, Polygon};
use pyo3::{prelude::*};
use std::f64;

/// FFI access to the [`polylabel`](fn.polylabel.html) function
///
/// Accepts three arguments:
///
/// - an exterior ring [`Array`](struct.Array.html)
/// - zero or more interior rings [`WrapperArray`](struct.WrapperArray.html)
/// - a tolerance `c_double`.
/// If an error occurs while attempting to calculate the label position, the resulting point coordinates
/// will be NaN, NaN.
#[pyfunction]
pub fn polylabel_ffi(
    outer: Vec<[f64; 2]>,
    interior: Vec<Vec<[f64; 2]>>,
    tolerance: f64,
) -> (f64, f64) {
    let exterior: LineString<_> = outer.into();
    let ls_int: Vec<LineString<f64>> = interior.into_iter().map(|vec| vec.into()).collect();
    let poly = Polygon::new(exterior, ls_int);
    polylabel(&poly, &tolerance).unwrap_or_else(|_| Point::new(f64::NAN, f64::NAN)).x_y()
}

#[pymodule]
fn pylylabel(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(polylabel_ffi, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::ffi::polylabel_ffi;

    #[test]
    fn test_ffi() {
        let outer = vec![
            [4.0, 1.0],
            [5.0, 2.0],
            [5.0, 3.0],
            [4.0, 4.0],
            [3.0, 4.0],
            [2.0, 3.0],
            [2.0, 2.0],
            [3.0, 1.0],
            [4.0, 1.0],
        ];
        let inners = vec![
            vec![[3.5, 3.5], [4.4, 2.0], [2.6, 2.0], [3.5, 3.5]],
            vec![[4.0, 3.0], [4.0, 3.2], [4.5, 3.2], [4.0, 3.0]],
        ];

        let res = polylabel_ffi(outer, inners, 0.1);
        assert_eq!(res, (3.125, 2.875));
    }
}
