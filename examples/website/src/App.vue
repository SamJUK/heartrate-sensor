<script setup>
import DeviceList from './components/DeviceList.vue'
import DeviceStats from './components/DeviceStats.vue'
import DeviceGraph from './components/DeviceGraph.vue'
import DeviceLog from './components/DeviceLog.vue'
</script>
<script>

const WEBSOCKET_HOST = '127.0.0.1';
const WEBSOCKET_PORT = 8765;

export default {
  name: 'App',
  data() {
    return {
      'websocket': null,
      'scanning_devices': false,
      'devices': {},
      'active_devices': {},
      'logs': [],
    }
  },
  methods: {
    send(msg) {
      this.log('Sending Websocket Message: ' + msg, 'debug');
      this.websocket.send(msg);
    },
    onSelectDevice(device) {
      if (this.active_devices.hasOwnProperty(device)) {
        return console.error('Already Connected to device', device);
      }
      this.log('Connecting to device: ' + device);
      this.active_devices[device] = {
        name: this.devices[device],
        hr: []
      };
      this.websocket.send(`connect:${device}`);
    },
    onScan() {
      this.scanning_devices = true;
      this.log('Scanning for devices');
      this.websocket.send('scan');
    },
    onDisconnect(device) {
      this.log('Disconnected from device', device);
      this.websocket.send(`disconnect:${device}`);
      delete this.active_devices[device];
    },
    log(msg, type) {
      this.logs = [{
        date: (new Date()).toISOString(),
        type: type ? type : 'info',
        msg: msg
      }, ...this.logs]
    },
    reconnectDevices() {
      Object.keys(this.active_devices).forEach(device => {
        console.log('Reconnecting', device);
        this.websocket.send(`connect:${device}`);
      });
    },
    startWebsocket(cb) {
      this.websocket = new WebSocket(`ws://${WEBSOCKET_HOST}:${WEBSOCKET_PORT}`);
      this.websocket.onopen = _ => {
        this.log('Websocket connected');
        this.onScan();
        if (cb) {
          cb();
        }
      };
      this.websocket.onerror = event => {
        this.log('Websocket Error', 'error');
        console.error('Websocket Error', event);
      };
      this.websocket.onclose = event => {
        this.log('Websocket Closed; Restarting in 3s', 'error');
        console.error('Websocket Closed; Restarting in 3s', event);
        const self = this;
        setTimeout(_ => {
          self.startWebsocket(self.reconnectDevices)
        }, 3000);
      };
      this.websocket.onmessage = event => {
        // console.log('Received WS Msg', event);
        let data = JSON.parse(event.data);
        if (data?.action === 'devices') {
          this.log(`Found Devices: ${JSON.stringify(data.devices)}`)
          console.log('Devices', data.devices);
          this.devices = data.devices;
          this.scanning_devices = false;
        } else if (data?.action === 'hr') {
          this.log(`[${this.devices[data.device_id]}] Received HR: ${data.hr}`, 'debug')
          this.active_devices[data.device_id].hr.push({
            x: new Date(data.date),
            y: Number(data.hr)
          });
        } else {
          this.log(`Received Unknown WS Message: ${event.data}`, 'error');
          console.log('Unknown WS Message', data)
        }
      };
    }
  },
  mounted() {
    this.startWebsocket();
  }
}
</script>

<template>
  <div class="toolbar">
    <DeviceList :devices="devices" :active_devices="active_devices" :is_loading="scanning_devices"
      @select-device="onSelectDevice" @scan="onScan" />

    <DeviceStats :device="device" :data="deviceData" @disconnect="onDisconnect"
      v-for="[device, deviceData] in Object.entries(active_devices)" />
  </div>
  <div class="body">
    <DeviceGraph :devices="this.active_devices" />
  </div>
  <div class="footer">
    <DeviceLog :logs="logs" />
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  gap: 25px;
  height: 30vh;
}

.body {
  width: 100%;
  height: 46vh;
}

.footer {
  height: 20vh;
}
</style>
