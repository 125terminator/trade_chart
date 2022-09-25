<template>
  <!-- <button @click="count++">You clicked me {{ count }} times.</button> -->
  <div class="checkbox">
  <input v-model="quantity" placeholder="Quantity" />
  <button @click="on_buy">Buy</button>
  <button @click="on_sell">Sell</button>
  <span class="checkbox">
  <input type="checkbox" id="checkbox" v-model="checked" />
    <label for="checkbox">{{ checked }}</label>
</span>
</div>
</template>


<script>

import * as Const from '../js/const.js'
import XHR from '../js/xhr.js'

const xhr = new XHR()


export default {
    props: {
        myDate: String,
        myPrice: Number,
    },
    methods: {
        on_buy() {
            console.log("buy", this.quantity)
            this.quantity = parseInt(this.quantity)
            xhr.post(Const.URL + 'buy', JSON.stringify({
                date: this.$parent.myDate, 
                price: this.$parent.myPrice, 
                qty: this.quantity, 
                intraday: this.checked
            }))
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
        quantity: 0,
    }
    }
}
</script>

<style>
    .timeframe {
        margin-right: 5px;
        user-select: none;
        cursor: pointer;
        font-weight: 200;
        max-width: 10px;
        color: #fdfdff;
        background-color: #fdfdff;
    }
    </style>