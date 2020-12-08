
const env = process.env.NODE_ENV
const BundleTracker = require('webpack-bundle-tracker')
const WriteFilePlugin = require('write-file-webpack-plugin')

module.exports = {
  outputDir: (env === "production" ? 'bundle/pro' : 'bundle/dev'),
  productionSourceMap: false,

  devServer: {
    historyApiFallback: true,
    //host: 'localhost',
    port: '8080',
    publicPath: '/',
    hot: false,
    liveReload: false
  },

  chainWebpack: config => {
    config.optimization.splitChunks({
      cacheGroups: {
        vendors: {
          name: 'chunk-vendors',
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          chunks: 'initial'
        },
        common: {
          name: 'chunk-common',
          minChunks: 2,
          priority: -20,
          chunks: 'initial',
          reuseExistingChunk: true
        }
      }
    })
  },

  configureWebpack: {
    output: {
      filename: 'js/[name].js',
      chunkFilename: 'js/[name].js'
    },
    plugins: [
      new WriteFilePlugin(),
      (env === "production" ?
        new BundleTracker({
          filename: 'webpack-pro.json',
          publicPath: '/'
        }) :
        new BundleTracker({
          filename: 'webpack-dev.json',
          publicPath: 'http://localhost:8080/'
        })
      )
    ]
  },

  "transpileDependencies": [
    'vuetify',
    'vuex-persist'
  ]

}