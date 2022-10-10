<template>
    <!-- Timeframe Selector -->
    <div class="tf-selector">
        <span class="timeframe" :key="i" v-for="(tf, i) in this.timeframes" v-on:click="on_click(tf, i)"
            v-bind:style="selected === i ? {color: '#f00'} : {color: '#000'}">
            {{tf}}
        </span>
        <!-- <select v-model="selected">
        <option v-for="(tf) in this.timeframes">{{tf}}</option>
    </select> -->
    </div>
</template>

<script>
export default {
    name: 'TfSelector',
    props: ['charts', 'timeframe'],
    mounted() {
        this.selected = Object.keys(this.$props.charts).indexOf(this.tf)
        this.$emit('selected', this.tf_to_ms())
    },
    computed: {
        timeframes() {
            // console.log("wow")
            return Object.keys(this.$props.charts)
        }
    },
    methods: {
        tf_to_ms() {
            let multiply_factor = 1
            if (this.tf.includes('m')) {
                multiply_factor = 6000
            }
            else if (this.tf.includes('H')) {
                multiply_factor = 6000 * 60
            }
            else if (this.tf.includes('D')) {
                multiply_factor = 6000 * 60 * 24
            }
            return parseInt(this.tf) * multiply_factor
        },
        on_click(tf, i) {
            this.tf = String(tf)
            this.$parent.tf = this.tf
            this.selected = i
            this.$emit('selected', this.tf_to_ms())
        }
    },
    data() {
        return {
            tf: this.timeframe,
            selected: 0,
            myStyle: {
                backgroundColor: "#ffffff"
            }
        }
    }
}
</script>
    
<style>
.tf-selector {
    position: absolute;
    top: 15px;
    right: 80px;
    font: 16px -apple-system, BlinkMacSystemFont,
        Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell,
        Fira Sans, Droid Sans, Helvetica Neue,
        sans-serif;
    background: #fdfdff;
    color: #ccc;
    padding: 8px;
    border-radius: 3px;
}

.timeframe {
    margin-right: 5px;
    user-select: none;
    cursor: pointer;
    font-weight: 200;
    max-width: 10px;
    color: #fdfdff;
}

.timeframe:hover {
    color: #fff;
}
</style>