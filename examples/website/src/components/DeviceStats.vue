<script>
export default {
    name: 'Device List',
    props: {
        'device': String,
        'data': Object
    },
    computed: {
        heartRate() {
            return this.data
                ? this.data.hr.map(d => d.y).filter(hr => !isNaN(hr))
                : [];
        }
    }
}
</script>

<template>
    <div class="device_stats">
        <h2>{{ data.name || '&nbsp' }}</h2>
        <p><b>Current: {{ data.hr.slice(-1)[0]?.y }} bpm</b></p>
        <p>Minimum: {{ Math.min(...heartRate) }} bpm</p>
        <p>Maximum: {{ Math.max(...heartRate) }} bpm</p>
        <p>Average: {{ Math.floor(heartRate.reduce((i,c) => i+c, 0) / heartRate.length) }} bpm</p>
        <button @click="this.$emit('disconnect', device)" v-show="device">Disconnect</button>
    </div>
</template>

<style scoped>
    .device_stats {
        border: 1px solid white;
        border-radius: 7px;
        padding: 10px 20px;
    }
</style>
