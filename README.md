# shellypy2
not to be confused with [pyShelly](https://github.com/StyraHem/pyShelly)  
Python 3 Wrapper around the Shelly HTTP api forked from the 
original [ShellyPy](https://pypi.org/project/ShellyPy/) project 
that seems to be dead or at least sleeping at the moment.


## why
other packages like [pyShelly](https://github.com/StyraHem/pyShelly) 
only support CoAP or MSQT, neither I am comfortable using in personal projects


## examples
#### relay
a simple working example for the Shelly 1 that turns a relay on

```python
import shelly

device = shelly.Shelly("192.168.0.5")

device.relay(0, turn=True)
```
[examples/toggle_relay.py](examples/toggle_relay.py)

#### monitor
a simple working example for the Shelly 1 that request monitor information

```python
import shelly

device = shelly.Shelly("192.168.68.121")

deviceMeter = device.meter(0)  # request meter information
print(deviceMeter['power'])  # print power information
print(deviceMeter['total'])  # print total information
```
other examples are available as well [examples/meter.py](examples/meter.py)

## devices
#### supported
- Shelly1
- Shelly1PM
- Shelly2
- Shelly2PM
- Shelly2.5
- Shelly4Pro (untested)
- Shelly Plug (untested)
- Shelly PlugS
- Shelly Bulb (untested)
- Shelly H&T (Gen 1 and Gen 3)
- Shelly Smoke (untested)
- Shelly EM (untested)
- Shelly flood (untested)

#### unsupported
- Shelly Sense (documentation is inaccurate, incomplete)
- Shelly RGBW (documentation is incomplete)

## applicability
this wrapper is best used in closed networks where other solutions are either 
not an option or not desired give your shelly devices static IP adresses for 
best results


## license
this project is licensed under the [MIT License](LICENSE)  
feel free to do whatever you want with it
