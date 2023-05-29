# HR Sensor

## Usage
### General
If you do not know the address of your HR Monitor, put your device into broadcast mode and run the following command to list all BLE devices in range. 
```
python discover.py
```

Once you've found your address it should look something like `D2:82:35:C1:K5:34`. Run the following command replacing `{ADDR}` with the address copied in the previous step.
```
# Display only mode
python watch.py -d {ADDR}

# Write to file
python watch.py -d {ADDR} --file --file_path /tmp/hr.csv
```

### Development
You can list out all Characteristics/Descriptors/Services for the device with the following command.
```
python discover.py -d {ADDR}
```

## TODO: 
- [ ] Look into other datastore options (sqllite? Redis?)
- [ ] Networking, Webhooks? Public Datastore?
- [ ] Fix Reconnection, if broadcast is paused & resumed at all, it dies 
- [ ] Auto discovery of BLE HR devices?
- [ ] Starting the script can be a bit flakey at times? Whats causing this?
