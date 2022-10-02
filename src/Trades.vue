<template>
    <div class="flex">
        <button @click="refresh">Refresh</button>
        <div class="container container-holdings">
            <table id="thirdTable">
                <thead>
                    <tr>
                        <th v-for="col in columns" v-on:click="sortTable(col)">{{col}}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in rows">
                        <td v-for="col in row" v-bind:style="row[4] < 0 ? {color: '#f00'} : {color: '#008000'}">
                            {{col}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

import * as Const from './js/const.js'
import Stream from './js/Stream.js'

export default {
    name: "Trade",
    mounted() {
        this.refresh()
        setTimeout(this.start_stream, 500);
    },
    methods: {
        refresh() {
            fetch(Const.URL + 'trades')
                .then(
                    response => response.text() // .json(), .blob(), etc.
                ).then(
                    text => {
                         this.rows = JSON.parse(text)}
                );
        },
        start_stream() {
            this.stream.ontrades = this.on_trades
            this.stream.send({'pause': false, 'subscription': 'trades'})
        },
        on_trades(data) {
            this.rows = data
        }
    },
    beforeDestroy() {
        this.stream.off()
    },
    data() {
        return {
            columns: ['buy_price', 'sell_price', 'qty', 'type', 'p&l', 'brokerage'],
            rows: [],
            stream: new Stream(Const.WSS),
        }
    }
}
</script>
