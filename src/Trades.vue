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
                        <td v-for="col in columns" v-bind:style="row['p&l'] < 0 ? {color: '#f00'} : {color: '#008000'}">
                            {{row[col]}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

import * as Const from './js/const.js'

export default {
    name: "Trade",
    mounted() {
        this.refresh()
    },
    methods: {
        refresh() {
            fetch(Const.URL + 'trades')
                .then(
                    response => response.text() // .json(), .blob(), etc.
                ).then(
                    text => {console.log(text)
                         this.rows = text}
                );
        }
    },
    data() {
        return {
            columns: ['buy_price', 'sell_price', 'qty', 'type', 'p&l', 'brokerage'],
            rows: [],
        }
    }
}
</script>
