<template>
    <div class="flex">
        <div>
            <button @click="refresh">Refresh</button>
        </div>
        <div>
            <select v-model="symbol_model">
                <option value="ashokley">Asholkley</option>
                <option value="reliance">Reliance</option>
                <option value="nse">NSE</option>
            </select>
        </div>
        <div>
            <tf-selector :charts="tfs" v-on:selected="on_selected" :timeframe="tf">
            </tf-selector>
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
                        <td v-for="col in columns" v-bind:style="col === 'index' ? {color: '#000'} : row[col] < 0 ? {color: '#f00'} : {color: '#008000'}">
                            {{row[col]}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import moment from 'moment'

import * as Const from './js/const.js'
import TfSelector from './vues/TFSelector.vue'

export default {
    name: "StockAnalysis",
    components: { TfSelector },
    mounted() {
        // this.$props.timeframe = "10m"
    },
    watch: {
        symbol_model(o, n) {
            this.on_selected(this.tf_to_ms(this.tf))
        }
    },
    methods: {
        refresh() {
        },
        on_selected(tf) {
            this.getState().then(state => {
                let now_ms = parseFloat(moment(state.now).format('X')) * 1000
                this.load_history(now_ms, tf).then(data => {
                    this.rows = data.data
                })
            })
        },
        async load_history(t2, tf) {
            let q = `analysis/?stock=${this.symbol_model}&interval=${tf}&endTime=${t2}`
            let r = await fetch(Const.URL + q).then(r => r.json())
            return r
        },
        async getState() {
            let q = `state`
            let r = await fetch(Const.URL + q).then(r => r.json())
            return r
        },
        tf_to_ms() {
            let multiply_factor = 1
            if (this.tf.includes('m')) {
                multiply_factor = 6000
            }
            else if (this.tf.includes('H')) {
                multiply_factor = 6000*60
            }
            else if(this.tf.includes('D')) {
                multiply_factor = 6000*60*24
            }
            return parseInt(this.tf)*multiply_factor
        }
    },
    data() {
        return {
            tf: "1D",
            columns: ['index', 'close_open', 'high_low', 'high_open', 'low_open', 'volume'],
            rows: [],
            symbol_model: 'ashokley',
            tfs: { '1m': {}, '5m': {}, '10m': {}, '15m': {}, '30m': {}, '1H': {}, '2H': {}, '3H': {}, '1D': {} },
        }
    }
}
</script>
