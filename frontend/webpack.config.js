const path = require('path');
const { ProvidePlugin } = require('webpack');

module.exports = {
  entry: {
    main: path.resolve(__dirname, './src/index.js'),
  },

  output: {
    path: path.resolve(__dirname, './dist'),
    filename: '[name].bundle.js',
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"]
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      // Добавьте другие необходимые загрузчики, например для изображений
    ]
  },

  plugins: [
    new ProvidePlugin({
      React: 'react'
    })
  ],

  resolve: {
    extensions: ['.js', '.jsx']
  }
};
