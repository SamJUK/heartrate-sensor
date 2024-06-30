<script>
export default {
    name: 'Device Log',
    props: {
        'logs': Array
    }
}
</script>

<template>
    <div class="device_log">
        <p class="device_log_line" v-for="line in logs" :class="{
            error: line.type == 'error',
            info: line.type == 'info',
            debug: line.type == 'debug',
            }">[{{ line.date }}] {{ line.msg }}</p>
    </div>
</template>

<style scoped>
    .device_log {
        border: 1px solid white;
        border-radius: 7px;
        padding: 15px;
        background: rgba(0,0,0,.2);
        height: 100%;
        overflow: scroll;
    }
    .device_log_line {
        margin: 0;
        padding: 5px 0;
    }
    .error {
        color: #ff7171;
        font-weight: bold;
    }
    .debug {
        opacity: .5;
    }
    .device_log_line:nth-child(even) {
        background: rgba(255,255,255,.03)
    }
</style>
