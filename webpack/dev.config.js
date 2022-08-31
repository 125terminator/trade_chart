const VueLoaderPlugin = require('vue-loader/lib/plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    entry: './src/main.js',
    module: {
        rules: [{
                test: /\.vue$/,
                exclude: /node_modules/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: './src/index.html'
        })
    ],
    // devServer: {
    //     proxy: {
    //         '/api/**': {
    //             target: 'http://localhost',
    //             changeOrigin: false
    //         },
    //         '/ws/**': {
    //             target: 'ws://localhost:13254',
    //             changeOrigin: true,
    //             ws: true
    //         }
    //     }
    // }
}
