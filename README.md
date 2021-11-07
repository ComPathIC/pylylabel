# Pylylabel
A Rust implementation of the [Polylabel](https://github.com/mapbox/polylabel) algorithm.

This is a fork of [polylabel-rs](https://github.com/urschrei/polylabel-rs). Pylylabel's `polylabel` function also
returns the distance from the label position to the polygon. Python binding is provided using PyO3.

The orange dot is the polygon centroid. The teal dot is the ideal label position. Red boxes show the search space.
[![GIF](output.gif)]()

## How to Use
```rust
extern crate pylylabel;
use pylylabel::polylabel;

extern crate geo;
use geo::{Point, Polygon};

let coords = vec![
    (0.0, 0.0),
    (4.0, 0.0),
    (4.0, 1.0),
    (1.0, 1.0),
    (1.0, 4.0),
    (0.0, 4.0),
    (0.0, 0.0)
];
let poly = Polygon::new(coords.into(), vec![]);
let label_pos, distance = polylabel(&poly, &0.10);
// Point(0.5625, 0.5625), 0.5625
```

## Documentation
https://docs.rs/polylabel

## Performance vs Accuracy
Using a 4-core 2.3 GHz Intel Core i5, finding a label position on a ~9k-vertex polygon (representing the Norwegian mainland) using a tolerance of `1.0` takes around 9 ms. Depending upon the dimensions of your polygon(s), you may require a higher tolerance (i.e. a smaller number). See [here](https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude/8674#8674) for some guidance on the accuracy provided by each decimal place.

## Build
Requirements:
- Python 3.5+
- Rust stable
- [maturin](https://github.com/PyO3/maturin)

`maturin build --release`

## License
[MIT](license.txt)
