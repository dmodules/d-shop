<script>
    import { Line } from 'vue-chartjs'

    export default {
        name: 'chartLine',
        extends: Line,
        props: {
            data: {}
        },
        watch: {
            $props: {
                deep: true,
                    handler () {
                    this.setData()
                }
            }
        },
        data: () => ({
            chartdata: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        display: true,
                        stacked: true,
                        gridLines: {
                            display: false
                        },
                    }],
                    yAxes: [{
                        display: true,
                        stacked: true,
                        gridLines: {
                            display: true
                        },
                    }]
                }
            },
        }),
        mounted () {
            this.setData()
        },
        methods: {
            setData () {
                this.$set(this.chartdata, "datasets", this.data.datasets)
                this.$set(this.chartdata, "labels", this.data.labels)
                this.renderChart(this.chartdata, this.options)
            },
        }
    }
</script>

<style scoped>
    canvas {
        height: 307px;
        padding: 1rem;
    }
</style>