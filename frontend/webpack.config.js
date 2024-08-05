const path = require('path');
const { ProvidePlugin } = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development', // или 'production', в зависимости от нужд

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
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
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
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, './public/index.html'), // путь к вашему шаблону HTML
            filename: 'index.html', // имя выходного HTML файла
        }),
        new ProvidePlugin({
            React: 'react'
        })
    ],

    resolve: {
        extensions: ['.js', '.jsx']
    }
};