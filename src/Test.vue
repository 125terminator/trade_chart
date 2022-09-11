<template>
    <!-- <Buy /> -->
    <div class="trading-vue">
        <trading-vue :data="chart" :width="this.width" :height="this.height"
                :chart-config="{MIN_ZOOM:1}"
                ref="tvjs"
                :toolbar="true"
                :overlays="overlays"
                :index-based="index_based"
                :color-back="colors.colorBack"
                :color-grid="colors.colorGrid"
                :color-text="colors.colorText">
        </trading-vue>
        <Buy />
        <tf-selector :charts="tfs" v-on:selected="on_selected">
        </tf-selector>
        
  
    </div>
    </template>

<script>
// :timezone="5.5"
import TradingVue from '../../trading-vue-js'
import TfSelector from './vues/TFSelector.vue'
import { Utils } from '../../trading-vue-js'
// import { HOUR4 } from 'trading-vue-js'
import { DataCube }  from '../../trading-vue-js'
import Stream from './Stream.js'
import Volume from './vues/Volume.vue'
import moment from 'moment'
import Overlays from 'tvjs-overlays'
import LineTool from './vues/LineTool.vue'
import Buy from './vues/Buy.vue'


import * as Const from './js/const.js'

// import rel from '../data/reliance.csv'
// var csv = require('jquery-csv')
// console.log(csv.toArrays(rel))



import Data from '../data/data.json'


// var a = new WebSocket(WSS)
// a.close()

export default {
    name: 'app',
    components: { TradingVue, TfSelector, LineTool, Buy },
    mounted() {
    window.addEventListener('resize', this.onResize)
    this.onResize()
    // Load the last data chunk & init DataCube:
    
    },
    methods: {
        on_selected(tf) { 
    // let tf=60000
        this.getState().then(state => {
            let now_ms = parseFloat(moment(state.now).format('X'))*1000
        this.load_chunk([now_ms, now_ms], tf).then(data => {
                this.chart = new DataCube({
                    chart: {
                        type: "Candles",
                        data: data['chart.data'],
                        tf: tf,
                        indexBased: true,
                        settings: {
                            showVolume: false,
                            // colorCandleUp: "#4CAF50",
                            // colorCandleDw: "#DF514C"
                        },
                    },
                    offchart: [{
                        name: "Volume",
                        type: "Volume",
                        data: data['chart.data'],
                        settings: {}
                    },
                    // {
                    //     type: 'BuySellBalance',
                    //     name: 'Buy/Sell Balance, $lookback',
                    //     data: [],
                    //     settings: {}
                    // }
                ]  ,
                    // datasets: [{
                    //     type: 'Trades',
                    //     id: 'binance-btcusdt',
                    //     data: []
                    // }]
                }, { auto_scroll: false }
                )
                // Register onrange callback & And a stream of trades
                this.chart.onrange(this.load_chunk)
                this.$refs.tvjs.resetChart()
                this.stream = new Stream(Const.WSS)
                this.stream.ontrades = this.on_trades
                window.dc = this.chart      // Debug
                window.tv = this.$refs.tvjs // Debug

                console.log(this.$refs.tvjs)
                // if (this.$refs.tvjs.cursor.locked) return
                // let last = this.chart.last_candle
                
                // if (!last) return
                // let tl = last[0]
                // let d = this.$regs.tvjs.getRange()[1] - tl
                // if (d > 0) {
                //     console.log("gone")
                //     this.tv.goto(t + d)
                // }
            })
        })
        },
        async getState() {
            let q = `state`
            let r = await fetch(Const.URL + q).then(r => r.json())
            return r
        },
        onResize(event) {
            this.width = window.innerWidth
            this.height = window.innerHeight - 50
        },
        // New data handler. Should return Promise, or
        // use callback: load_chunk(range, tf, callback)
        async load_chunk(range, tf) {
            // console.log(tf)
            let [t1, t2] = range
            let x = 'BTCUSDT'
            let q = `?stock=${x}&interval=${tf}&startTime=${t1}&endTime=${t2}`
            // let r = await fetch(URL + q).then(r => r.json())
            // return this.format(this.parse_binance(r))
            let r = await fetch(Const.URL + q).then(r => r.json())
            return this.format(this.parse_data(r))
        },
        // Parse a specific exchange format
        parse_binance(data) {
            data = data.chart.data
            if (!Array.isArray(data)) return []
            return data.map(x => {
                for (var i = 0; i < x.length; i++) {
                    x[i] = parseFloat(x[i])
                }
                return x.slice(0,6)
            })
        },
        parse_data(e) {

            var chartInterval = "10minute"
            var t = e.data, a = [], b=[];
            // if (!t || !t.data || !t)
            //     return a;
            for (var o = 0, p=0; o < t.length; o++, p+=60000) {
                var dt
                b[o] = {}
                if ("day" === chartInterval && -330 !== (new Date).getTimezoneOffset()) {
                    var n = t[o].index;
                    dt = moment(n.substr(0, n.indexOf("+"))).toDate()
                } else 
                    dt = moment(t[o].index).toDate();

                let oo = parseFloat(moment(dt).format('X'))*1000
                var vol = t[o].Volume/1000
                b[o] = [oo, t[o].Open, t[o].High, t[o].Low, t[o].Close, vol]
                }
            return b
    },
        format(data) {
            // console.log(data)
            // Each query sets data to a corresponding overlay
            return {
                'chart.data': data,
                'offchart.Volume0.data': data,
                // other onchart/offchart overlays can be added here,
                // but we are using Script Engine to calculate some:
                // see EMAx6 & BuySellBalance
            }
        },
        on_trades(trade) {
            this.myDate = trade[0]
            this.myPrice = trade[1]
            // console.log(this.$refs.tvjs.getRange())
            trade[0] = parseFloat(moment(trade[0]).format('X'))*1000 + 19800000
            trade[5] = trade[5]/1000
            this.chart.update({
                candle: trade,
            })
            let d = window.tv.getRange()[1] - trade[0]
            // console.log(d)
            if (d > -600000) {
            window.tv.goto(trade[0])
            }
            
        },
        getJson() {
        },
        
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    },
    data() {
        return {
            chart1: Data,
            chart: {},
            tfs: {'1m': {}, '2m': {}, '5m': {}, '10m': {}, '15m': {}, '30m': {}, '1H': {}},
            width: window.innerWidth,
            height: window.innerHeight,
            colors: {
                colorBack: '#fff',
                colorGrid: '#eee',
                colorText: '#333',
            },
            index_based: false,
            overlays: [Volume, LineTool],
            timezone: 0,
            stream: undefined,
            myPrice: 0,
            myDate: "",
        }
    }
}

</script>
<style>
</style>

<!-- https://github.com/tvjsx/'trading-vue-js'/blob/e881bdb5c3ec3b890d21e3059cb6b3ef85a47432/docs/guide/OVERLAYS.md -->