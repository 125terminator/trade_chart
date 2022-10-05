<template>
    <div class="flex">
        <div>
            <span v-bind:style="nse_change < 0 ? {color: '#f00'} : {color: '#008000'}">NSE: {{ nse_change }}%</span>
            <!-- <input @keyup.enter="on_symbol_change" v-model="symbol_model" placeholder="Enter Symbol" /> -->
            <select v-model="symbol_model">
                <option value="ashokley">Asholkley</option>
                <option value="reliance">Reliance</option>
                <option value="nse">NSE</option>
            </select>
            <button @click="on_symbol_change">GET</button>
        </div>
        <div class="container container-chart">
            <div class="trading-vue">
                <trading-vue :data="chart" :width="1400" :height="500" :chart-config="{MIN_ZOOM:1}" ref="tvjs"
                    :toolbar="false" :overlays="overlays" :index-based="index_based" :color-back="colors.colorBack"
                    :color-grid="colors.colorGrid" :color-text="colors.colorText">
                </trading-vue>
                <Buy />
                <tf-selector :charts="tfs" v-on:selected="on_selected" :timeframe="tf">
                </tf-selector>
            </div>
        </div>
        <div>
            <span>Stream sleep time</span> | 
            <input v-model="stream_sleep_sec" type="range" min="1" max="20"/>
            <span>{{ stream_sleep_sec/10 }} seconds</span>
        </div>
        <div>
        <button @click="on_pause_resume"> {{pause === false ? "PAUSE": "RESUME"}}</button>
    </div>
        <div class="container container-holdings">
            <table id="thirdTable">
                <thead>
                    <tr>
                        <th v-for="col in columns" v-on:click="sortTable(col)">{{col}}</th>
                    </tr>
                </thead>  
                <tbody>
                    <tr v-for="row in rows">
                        <td v-for="col in columns"
                            v-bind:style="row['Net chg.'] < 0 ? {color: '#f00'} : {color: '#008000'}">
                            {{row[col]}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

import TradingVue from 'trading-vue-js'
import TfSelector from './vues/TFSelector.vue'
import { DataCube } from 'trading-vue-js'
import Volume from './vues/Volume.vue'
import moment from 'moment'
import Buy from './vues/Buy.vue'


import * as Const from './js/const.js'
import * as Utils from './js/utils.js'
import Stream from './js/Stream.js'
import Data from '../data/data.json'


export default {
    name: 'app',
    components: { TradingVue, TfSelector, Buy },
    mounted() {
        window.addEventListener('keyup', (event) => {
            if (event.key === ' ') {
                this.on_pause_resume()
            }
        })
        window.addEventListener('resize', this.onResize)
        this.onResize()
        // Load the last data chunk & init DataCube:

    },
    watch: {
        symbol_model(o, n) {
            this.on_symbol_change()
        },
        stream_sleep_sec(o, n) {
            this.stream.send({'stream_sleep_sec': this.stream_sleep_sec/10})
        }
    },
    methods: {
        on_symbol_change() {
            this.symbol = this.symbol_model
            this.on_selected()
        },
        on_pause_resume() {
            if (this.pause === false) {
                this.pause = true
            } else {
                this.pause = false
            }
            this.stream.send({ 'pause': this.pause, 'subscription': 'all' })
        },
        on_selected(tf) {
            if (tf === undefined) {
                tf = 60000
            }
            this.getState().then(state => {
                let now_ms = parseFloat(moment(state.now).format('X')) * 1000
                this.load_chunk([now_ms, now_ms], tf).then(data => {
                    this.chart = new DataCube({
                        chart: {
                            type: this.chart_types[this.symbol],
                            data: data['chart.data'],
                            tf: tf,
                            indexBased: true,
                            settings: {
                                showVolume: false,
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
                        ],
                    }, { auto_scroll: false }
                    )
                    // Register onrange callback & And a stream of trades
                    this.chart.onrange(this.load_chunk)
                    this.$refs.tvjs.resetChart()
                    this.stream.ontrades = this.on_trades
                    window.dc = this.chart      // Debug
                    window.tv = this.$refs.tvjs // Debug
                })
            })
        },
        async getState() {
            let q = `state`
            let r = await fetch(Const.URL + q).then(r => r.json())
            return r
        },
        onResize() {
            this.width = window.innerWidth
            this.height = window.innerHeight - 50
        },
        // New data handler. Should return Promise, or
        // use callback: load_chunk(range, tf, callback)
        async load_chunk(range, tf) {
            // console.log(tf)
            let [t1, t2] = range
            let q = `stock/?stock=${this.symbol}&interval=${tf}&startTime=${t1}&endTime=${t2}`
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
                return x.slice(0, 6)
            })
        },
        parse_data(e) {

            var chartInterval = "10minute"
            var t = e.data, b = [];
            // if (!t || !t.data || !t)
            //     return a;
            for (var o = 0, p = 0; o < t.length; o++, p += 60000) {
                var dt
                b[o] = {}
                if ("day" === chartInterval && -330 !== (new Date).getTimezoneOffset()) {
                    var n = t[o].index;
                    dt = moment(n.substr(0, n.indexOf("+"))).toDate()
                } else
                    dt = moment(t[o].index).toDate();

                let oo = parseFloat(moment(dt).format('X')) * 1000
                var vol = t[o].Volume / 1000
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
        on_trades(data) {
            this.nse_change = data.nse_change
            var trade = data.live[this.symbol]
            this.myDate = trade[0]
            this.myPrice = trade[1]
            // console.log(this.$refs.tvjs.getRange())
            trade[0] = parseFloat(moment(trade[0]).format('X')) * 1000 + 19800000
            trade[5] = trade[5] / 1000
            this.chart.update({
                candle: trade,
            })
            this.chart.update({
                t: trade[0] + 60 * 1000,     // Exchange time (optional)
                price: trade[1],   // Trade price
                volume: 0,  // Trade amount
            })
            let d = window.tv.getRange()[1] - trade[0]
            // console.log(d)
            // console.log(trade[0])
            if (d > -600000) {
                window.tv.goto(trade[0] + 60 * 10000)
            }


            var holdings = data.holdings
            //   columns: ['Instrument', 'Qty.', 'Avg.', 'Cur. val', 'P&L', 'Net chg.'],
            for (var i = 0; i < holdings.length; i++) {
                holdings[i][this.columns[3]] = trade[1]
                var pAndL = holdings[i][this.columns[3]] - holdings[i][this.columns[2]]
                var neg_qty = holdings[i]['Qty.'] < 0 ? -1 : 1
                holdings[i][this.columns[4]] = (pAndL * holdings[i][this.columns[1]]).toFixed(2)
                holdings[i][this.columns[5]] = neg_qty * ((pAndL / holdings[i][this.columns[2]]) * 100).toFixed(2)
                //   console.log(holdings)

                let bp = holdings[i][this.columns[2]]
                let sp = holdings[i][this.columns[3]]
                let qty = holdings[i][this.columns[1]]
                if (qty < 0) {
                    // intraday
                    [bp, sp] = [sp, bp]
                    qty = -qty
                }
                
                let brokerage = Utils.cal_intra(bp, sp, qty)
                holdings[i][this.columns[4]] = brokerage[0]
                holdings[i][this.columns[6]] = brokerage[1]
            }
            this.rows = holdings
        },
        // "sortTable": function sortTable(col) {
        // this.rows.sort(function(a, b) {
        //   if (a[col] > b[col]) {
        //     return 1;
        //   } else if (a[col] < b[col]) {
        //     return  -1;
        //   }
        //   return 0;
        // })
        // }
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
        window.removeEventListener('keyup', this.handler);
    },
    data() {
        return {
            pause: true,
            symbol: "ashokley",
            symbol_model: "ashokley",
            chart_types: { 'nse': 'Candles', 'reliance': 'Candles' },
            nse_change: 0,
            chart1: Data,
            chart: {},
            tf: '1m',
            tfs: { '1m': {}, '5m': {}, '10m': {}, '15m': {}, '30m': {}, '1H': {}, '2H': {}, '3H': {}, '1D': {} },
            width: window.innerWidth,
            height: window.innerHeight,
            colors: {
                colorBack: '#fff',
                colorGrid: '#eee',
                colorText: '#333',
            },
            index_based: false,
            overlays: [Volume],
            timezone: 0,
            stream: new Stream(Const.WSS),
            myPrice: 0,
            myDate: "",
            rows: [
            ],
            columns: ['Instrument', 'Qty.', 'Avg.', 'Cur. val', 'P&L', 'Net chg.', 'Brokerage'],
            stream_sleep_sec: 1,
        }
    },
}

</script>
<style>
.flex {
    display: flex;
    background-color: bisque;
    flex-direction: column;
}

.flex .container {
    width: 200px;
    margin: 10px;
    border: 3px solid #000;
    background-color: #fff;
}

.flex .container-holdings {
    min-height: 100px;
    width: 1400px;
}

.flex .container-chart {
    flex-shrink: 0;
    flex-grow: 1;
    min-width: 1400px;
    min-height: 500px;
}

.container-holdings .holdings {
    display: flex;

}

table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    table-layout: fixed
}

td,
th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
    color: #008000;
}

/* table {
  font-family: 'Open Sans', sans-serif;
  width: 750px;
  border-collapse: collapse;
  border: 3px solid #44475C;
  margin: 10px 10px 0 10px;
}

table th {
  text-transform: uppercase;
  text-align: left;
  background: #44475C;
  color: #FFF;
  cursor: pointer;
  padding: 8px;
  min-width: 30px;
}
table th:hover {
        background: #717699;
      }
table td {
  text-align: left;
  padding: 8px;
  border-right: 2px solid #7D82A8;
}
table td:last-child {
  border-right: none;
}
table tbody tr:nth-child(2n) td {
  background: #D4D8F9;
} */
</style>

<!-- https://github.com/tvjsx/'trading-vue-js'/blob/e881bdb5c3ec3b890d21e3059cb6b3ef85a47432/docs/guide/OVERLAYS.md -->