<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, TimeScale, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import 'chartjs-adapter-moment';

ChartJS.register(TimeScale, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default {
  name: 'Device Graph',
  components: { Line },
  props: {
    'devices': Object
  },
  data() {
    return {
      deviceColors: {},
      colors: [
        "#25CCF7","#FD7272","#54a0ff","#00d2d3",
        "#1abc9c","#2ecc71","#3498db","#9b59b6","#34495e",
        "#16a085","#27ae60","#2980b9","#8e44ad","#2c3e50",
        "#f1c40f","#e67e22","#e74c3c","#ecf0f1","#95a5a6",
        "#f39c12","#d35400","#c0392b","#bdc3c7","#7f8c8d",
        "#55efc4","#81ecec","#74b9ff","#a29bfe","#dfe6e9",
        "#00b894","#00cec9","#0984e3","#6c5ce7","#ffeaa7",
        "#fab1a0","#ff7675","#fd79a8","#fdcb6e","#e17055",
        "#d63031","#feca57","#5f27cd","#54a0ff","#01a3a4"
      ]
    }
  },
  methods: {
    getRandomColor() {
      const idx = Math.floor(Math.random() * this.colors.length);
      return this.colors.splice(idx, 1)[0];
    },
    getDeviceColor(device) {
      if(!this.deviceColors.hasOwnProperty(device)) {
        this.deviceColors[device] = this.getRandomColor();
      }
      return this.deviceColors[device];
    },
    getChartDatasets() {
      return Object.entries(this.devices).map(device => {
        const [id, data] = device;
        const clr = this.getDeviceColor(id);
        return {
          label: data.name,
          backgroundColor: clr,
          borderColor: clr,
          data: data.hr.slice(Math.max(0, data.hr.length - 120))
        };
      });
    }
  },
  computed: {
    chartData: function() {
      return {
        datasets: this.getChartDatasets()
      }
    },
    chartOptions: function() {
      return {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                labels: {
                  color: "white",
                  font: {
                    weight: 'bold'
                  }
                }
            }
        },
        scales: {
          y: {
            // suggestedMin: Math.min(...this.device_data.hr.map(d => d.y)) - 10,
            // suggestedMax: Math.max(...this.device_data.hr.map(d => d.y)) + 10,
            grid: {
              color: 'rgba(255,255,255,0.2)'
            },
            ticks: {
              color: "white",
              font: {
                weight: 'bold'
              }
            }
          },
          x: {
            type: 'time',
            time: {
              round: 'second',
              unit: 'second',
              minUnit: 'second'
            },
            grid: {
              color: 'rgba(255,255,255,0.2)'
            },
            ticks: {
              color: "white",
              font: {
                weight: 'bold'
              },
              autoSkip: false,
              maxRotation: 90,
              minRotation: 90,

              callback: (value, index, ticks) => {
                const diff = Math.floor(((new Date()).getTime() - (new Date(value)).getTime()) / 1000);
                return `${diff}s ago`
              }
            }
          }
        }
      }
    }
  }
}
</script>

<template>
    <div class="device_graph">
        <Line
            id="my-chart-id"
            :options="chartOptions"
            :data="chartData"
        />
    </div>
</template>

<style scoped>
  .device_graph {
      position: relative;
  }
  canvas {
      height: 46vh;
  }
</style>
