<script>
    import { Doughnut } from 'vue-chartjs'

    export default {
        name: 'chartDonut',
        extends: Doughnut,
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
                legend: {
                    position: "right",
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
        height: 200px;
        padding: 1rem;
    }
</style>