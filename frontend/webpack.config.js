const path = require('path');
const { ProvidePlugin } = require('webpack');

module.exports = {
    // ... other Webpack config
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
            // ... other loaders
        ]
    },
    plugins: [
        new ProvidePlugin({
            React: 'react'
        })
    ]
};