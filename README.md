# HR Sensor

- run `python discover_devices.py` to list all the BLE devices.
- Find your device, and copy the Address for it.
- Run `python watch.py -d {ADDRESS}` to monitor the HR
- Run `python watch.py -h` for a list of arguments

---
- Run `python discover.py {ADDRESS}` to list the Chars/Disc/Svcs for the address