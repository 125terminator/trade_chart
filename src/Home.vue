
<template>
    <div>
        <a href="#/">Chart</a> |
        <a href="#/trade">Trade History</a>
        <component :is="currentView" />
    </div>
</template>

<script>
import App from './App.vue'
import Trade from './Trades.vue'

const routes = {
    '/': App,
    '/trade': Trade
}

export default {
    data() {
        return {
            currentPath: window.location.hash
        }
    },
    computed: {
        currentView() {
            return routes[this.currentPath.slice(1) || '/'] || NotFound
        }
    },
    mounted() {
        window.addEventListener('hashchange', () => {
            this.currentPath = window.location.hash
        })
    }
}
</script>