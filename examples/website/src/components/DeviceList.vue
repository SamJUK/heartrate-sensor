<script setup>
import Device from './DeviceList/Device.vue'
</script>

<script>
export default {
    name: 'Device List',
    props: {
        'devices': Object, 
        'active_devices': Object,
        'is_loading': Boolean
    }
}
</script>

<template>
    <div class="device_selector">
        <div class="no-devices" v-show="Object.keys(devices).length < 1"><p>No Devices</p></div>
        
        <Device :id="id" :name="name" :selected="active_devices.hasOwnProperty(id)" 
            @selected="this.$emit('select-device', id)"
            v-for="[id, name] in Object.entries(devices)" />

        <p class="scanning" @click="!is_loading ? this.$emit('scan') : 0">{{ is_loading ? 'Scanning...' : 'Start Scan' }}</p>
    </div>
</template>

<style scoped>
    .device_selector {
        border: 1px solid white;
        border-radius: 7px;
        min-width: 200px;
        max-width: 400px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
    }
    .no-devices {
        text-align: center;
        font-weight: bold;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .no-devices button {
        width: 70px;
    }
    .scanning {
        cursor: pointer;
        text-align: center;
        font-weight: bold;
        position: absolute;
        width: 100%;
        bottom: 0;
        margin: 0;
        padding: 10px 0;
        background: rgba(0,0,0,.3);
    }
</style>
