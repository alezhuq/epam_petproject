const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const dotenv = require('dotenv');
dotenv.config();

const production = process.env.NODE_ENV === 'production';


module.exports = {
    cache: false,
    entry: { myAppName: path.resolve(__dirname, "./src/index.js") },
    output: {
        path: path.resolve(__dirname, "./build"),
        publicPath: '/',
        filename: production ? '[hash].js' : 'index.js',
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
            },
            {
                test: /\.s(a|c)ss$/,
                exclude: /node_modules/,
                use: [
                    production ? MiniCssExtractPlugin.loader : 'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: !production
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: !production
                        }
                    }
                ]
            },
            {
                test: /\.(png|jpe?g|gif|pdf|doc)$/i,
                dependency: { not: ['url'] },
                use: [
                  {
                    loader: 'file-loader',
                  },
                ],
            },
            {
                test: /\.svg$/,
                loader: 'svg-url-loader'
            }
        ],
    },
    resolve: {
        extensions: ["*", ".js", ".jsx", ".scss"],
        modules: ['node_modules'],
        alias: {
            // ...
            'react-dom$': 'react-dom/profiling',
          },
    },
    plugins: [
        new CopyPlugin({
            patterns: [
                {
                    from: path.resolve(__dirname, 'src/img'),
                    to: path.resolve(__dirname, 'build'),
                },
            ],
        }),
        new CleanWebpackPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new HtmlWebpackPlugin({
            title: "Webpack & React",
            template: "./src/index.html",
            favicon: "./src/favicon.png"
        }),
        new MiniCssExtractPlugin({
            filename: production ? '[hash].css' : 'style.css',
        }),
        new webpack.DefinePlugin({
            'process.env': JSON.stringify(process.env)
        })
    ],
    devServer: {
        port: 3000,
        hot: true,
        historyApiFallback: true,
    },
    mode: production ? 'production' : 'development'
};