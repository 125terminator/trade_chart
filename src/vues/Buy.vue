<template>
  <!-- <button @click="count++">You clicked me {{ count }} times.</button> -->
  <div>
  <input v-model="quantity" placeholder="Quantity" />
  <button @click="on_buy">Buy</button>
  <button @click="on_sell">Sell</button>
</div>
</template>


<script>

import * as Const from '../js/const.js'
import XHR from '../js/xhr.js'

const xhr = new XHR()


export default {
    methods: {
        on_buy() {
            console.log("buy", this.quantity)
            xhr.post(Const.URL + 'buy', this.quantity)
        },
        on_sell() {
            console.log("sell", this.quantity)
            xhr.post(Const.URL + 'sell', this.quantity)
        }
    },
    data() {
    return {
        count: 0,
        checked: false,
        quantity: "",
    }
    }
}
</script>