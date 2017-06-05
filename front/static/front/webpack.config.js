var webpack = require('webpack')
const ExtractTextPlugin = require("extract-text-webpack-plugin");
module.exports = {
  devtool: 'false',
  entry:{
    "index" : __dirname + "/main.js",
    "vendor":["react","react-dom","jquery"]
  }, 
  output: {
    path: __dirname + "/public",
    filename: "bundle.js" 
  },
  plugins:[
     new webpack.optimize.CommonsChunkPlugin({
      name: "vendor",

      filename: "vendor.js",
      // (Give the chunk a different name)
      minChunks: Infinity,
      // (with more entries, this ensures that no other module
      //  goes into the vendor chunk)
    })
  ],
  module:{
    loaders:[
      {
        test:/\.json$/,
        loader:"json-loader"
      },
      {
        test:/\.js$/,
        exclude:/node_modules/,
        loader:'babel-loader',
        query:{
          presets:['es2015','react']
        }
      }
    ]
  },
  devServer: {
    contentBase: "./public",
    // colors: true,
    historyApiFallback: true,
    inline: true
  }
}