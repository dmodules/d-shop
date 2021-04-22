<template>
    <div>
        <l-map :center="[44.74839, 0]" :zoom="1" style="height: 307px" :options="mapOptions" ref="dmMap" @mousemove="showTooltip">
            <l-choropleth-layer
                :data="geoData"
                titleKey="name"
                idKey="name"
                geojsonIdKey="name_sort"
                :value="value"
                :geojson="geojson"
                :colorScale="colorScale"
                :strokeWidth="1"
                :currentStrokeWidth="1"
            >
                <template slot-scope="props">
                    <div id="dm-choropleth-tooltip" v-if="props.currentItem.name">{{props.currentItem.name}}: {{props.currentItem.value}}</div>
                </template>
            </l-choropleth-layer>
        </l-map>
    </div>
</template>

<script>
    import { LMap } from 'vue2-leaflet';
    import { ChoroplethLayer } from 'vue-choropleth'
    import geojson from '@/data/geo.json'

    export default {
        name: 'ProjectChoropleth',
        components: { 
            LMap,
            'l-choropleth-layer': ChoroplethLayer
        },
        props: {
            geoData: Array
        },
        data: () => ({
            geojson,
            colorScale: ["1e2221", "1e2221", "066bf9"],
            value: {
                key: "amount",
                metric: ""
            },
            mapOptions: {
                attributionControl: false,
                scrollWheelZoom: false
            },
            currentStrokeColor: '3d3213'
        }),
        methods: {
            showTooltip ($event) {
                let tooltip = document.getElementById('dm-choropleth-tooltip')
                if (tooltip) {
                    tooltip.style.top = ""+($event.containerPoint.y + 10)+"px"
                    tooltip.style.left = ""+($event.containerPoint.x + 10)+"px"
                }
            }
        }
    }
</script>

<style scoped>
    @import "~leaflet/dist/leaflet.css";

    #dm-choropleth-tooltip:not(:empty){
        background-color:rgba(0,0,0,.9);
        border-radius:0.75rem;
        box-shadow:0 1px 15px rgba(0,0,0,.04), 0 1px 6px rgba(0,0,0,.04);
        color:#fff;
        display:inline-block;
        position:absolute;
        z-index:888;
        padding:4px 16px;
    }
</style>

<style>
    #app .leaflet-pane,
    #app .leaflet-overlay-pane,
    #app .leaflet-map-pane svg{
        z-index:198;
    }
    #app .leaflet-top, #app .leaflet-bottom{
        z-index:198;
    }
</style>
