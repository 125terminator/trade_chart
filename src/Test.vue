<template>
    <!-- Real time data example -->
    <span>
        <trading-vue :data="chart" :width="this.width" :height="this.height"
                :chart-config="{MIN_ZOOM:1}"
                ref="tvjs"
                :toolbar="true"
                :index-based="index_based"
                :color-back="colors.colorBack"
                :color-grid="colors.colorGrid"
                :color-text="colors.colorText">
        </trading-vue>
        <span class="gc-mode">
            <input type="checkbox" v-model="index_based">
            <label>Index Based</label>
        </span>
        <!-- <tf-selector :charts="charts" v-on:selected="on_selected">
        </tf-selector> -->
    </span>
    </template>

<script>
import TradingVue from 'trading-vue-js'
import TfSelector from 'trading-vue-js'
import { Utils } from 'trading-vue-js'
import { HOUR4 } from 'trading-vue-js'
import { DataCube } from 'trading-vue-js'
import Stream from './Stream.js'
import { ScriptOverlay } from 'trading-vue-js'
import { BSB } from 'trading-vue-js'
import moment from 'moment'

import Data from '../data/data.json'

const WSS = `ws://localhost:13254`
// Gettin' data through webpeck proxy
const PORT = location.port
// const URL = `http://localhost:${PORT}/api/v1/klines?symbol=`
// const WSS = `ws://localhost:${PORT}/ws/btcusdt@aggTrade`
const URL = `http://localhost:8008/api/`
// var a = new WebSocket(WSS)
// a.close()

export default {
    name: 'app',
    components: { TradingVue, TfSelector },

    mounted() {
    window.addEventListener('resize', this.onResize)
    this.onResize()

    // Load the last data chunk & init DataCube:
    let now = Utils.now()
    this.load_chunk([now - HOUR4, now]).then(data => {
            this.chart = new DataCube({
                ohlcv: data['chart.data'],
                type: "Spline",
                // onchart: [{
                //     type: 'EMAx6',
                //     name: 'Multiple EMA',
                //     data: []
                // }],
                // offchart: [{
                //     type: 'BuySellBalance',
                //     name: 'Buy/Sell Balance, $lookback',
                //     data: [],
                //     settings: {}
                // }],
                datasets: [{
                    type: 'Trades',
                    id: 'binance-btcusdt',
                    data: []
                }]
            }, { aggregation: 100 })
            // this.chart.interval_ms = 1e6
            // Register onrange callback & And a stream of trades
            this.chart.onrange(this.load_chunk)
            this.$refs.tvjs.resetChart()
            console.log(this.$refs.tvjs)
            console.log(this.$props)
            // this.stream = new Stream(WSS)
            // this.stream.ontrades = this.on_trades
            window.dc = this.chart      // Debug
            window.tv = this.$refs.tvjs // Debug
            // this.$refs.tvjs.interval_ms = parseFloat(1e6)
        })
    },
    methods: {
        on_selected(tf) {
            // this.chart.set('chart.data', this.charts[tf.name])
            this.$refs.tradingVue.resetChart()
            this.log_scale = false
        },
        onResize(event) {
            this.width = window.innerWidth
            this.height = window.innerHeight - 50
        },
        // New data handler. Should return Promise, or
        // use callback: load_chunk(range, tf, callback)
        async load_chunk(range) {
            let [t1, t2] = range
            let x = 'BTCUSDT'
            let q = `${x}&interval=1m&startTime=${t1}&endTime=${t2}`
            // let r = await fetch(URL + q).then(r => r.json())
            // return this.format(this.parse_binance(r))
            let r = await fetch(URL + q).then(r => r.json())
            return this.format(this.parse_data(r))
        },
        // Parse a specific exchange format
        parse_binance(data) {
            console.log(data.chart)
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
            var t = e, a = [], b=[];
            if (!t || !t.data || !t.data.candles)
                return a;
            for (var o = 0; o < t.data.candles.length; o++) {
                a[o] = {}
                b[o] = {}
                if ("day" === chartInterval && -330 !== (new Date).getTimezoneOffset()) {
                    var n = t.data.candles[o][0];
                    a[o].DT = moment(n.substr(0, n.indexOf("+"))).toDate()
                } else 
                    a[o].DT = moment(t.data.candles[o][0]).toDate();
                a[o].Open = parseFloat(trimString(t.data.candles[o][1])),
                a[o].High = parseFloat(trimString(t.data.candles[o][2])),
                a[o].Low = parseFloat(trimString(t.data.candles[o][3])),
                a[o].Close = parseFloat(trimString(t.data.candles[o][4])),
                a[o].Volume = parseFloat(trimString(t.data.candles[o][5])),
                a[o].OI = parseFloat(trimString(t.data.candles[o][6]))
                b[o] = [parseFloat(moment(a[o].DT).format('X')), a[o].Open, a[o].High, a[o].Low, a[o].Close, a[o].Volume]
                }
            // return a.sort((function(e, t) {
            //     return e.DT.getTime() - t.DT.getTime()
            // }
            // )), a
            return b
    },
        format(data) {
            // Each query sets data to a corresponding overlay
            return {
                'chart.data': data
                // other onchart/offchart overlays can be added here,
                // but we are using Script Engine to calculate some:
                // see EMAx6 & BuySellBalance
            }
        },
        on_trades(trade) {
            this.chart.update({
                t: trade[0],     // Exchange time (optional)
                price: parseFloat(trade[1]),   // Trade price
                volume: parseFloat(5),  // Trade amount
                // 'datasets.binance-btcusdt': [ // Update dataset
                //     trade.T,
                //     trade.m ? 0 : 1,          // Sell or Buy
                //     parseFloat(trade.q),
                //     parseFloat(trade.p)
                // ],
                // ... other onchart/offchart updates
            })
        }
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    },
    data() {
        return {
            chart: {
                type: "Spline"
            },
            chart: new DataCube({}),
            width: window.innerWidth,
            height: window.innerHeight,
            colors: {
                colorBack: '#fff',
                colorGrid: '#eee',
                colorText: '#333',
            },
            index_based: false,
            overlays: [ScriptOverlay, BSB],
            type: "Spline"
        }
    }
}

function trimString(e) {
    return String(e).replace(/^\s+|\s+$/g, "")
}
</script>


<!-- https://github.com/tvjsx/trading-vue-js/blob/e881bdb5c3ec3b890d21e3059cb6b3ef85a47432/docs/guide/OVERLAYS.md -->