# solar_park_data

> For access to our data please email sekretariat@ipv.uni-stuttgart.de.

Read data from the ipv's rooftop solar park.

## Installation

```console
pip install git+https://github.com/uni-stuttgart-ipv/solar_park_data.git
```

## Data

### Modules

+ Voltage
+ Current
+ Power
+ Temperature

### Environmental

+ Solar spectrum
+ Relative humidity
+ Ambient temperature

## Testing

> Use `pytest` for testing.

You must setup environment variables with API tokens before testing.
+ **INFLUXDB_TOKEN**
+ **AWS_TOKEN**

## License

`solar-park-data` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
