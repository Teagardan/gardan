const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './agent-system/src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'public'),
  },
  resolve: {
    modules: [path.resolve(__dirname, 'agent-system/src'), 'node_modules'],
    fallback: { 
      "fs": false, // Provide empty module for 'fs'
      "path": require.resolve("path-browserify"), // Use 'path-browserify' polyfill for 'path'
      "util": require.resolve("util") // Add polyfill for 'util' - separated by comma
    }
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/, 
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', 
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './agent-system/public/index.html',
    }),
  ],
};