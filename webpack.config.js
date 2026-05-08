const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: {
    global: "js/global.js",
    styles: "scss/styles.scss",
  },
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "frontend", "built"),
    clean: true,
  },
  context: path.resolve(__dirname, "frontend", "src"),
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              url: true,
              sourceMap: true,
            },
          },
          {
            loader: "sass-loader",
            options: {
              sassOptions: {
                includePaths: ["./node_modules/@uswds/uswds/packages"],
              },
            },
          },
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)$/i,
        // More information here https://webpack.js.org/guides/asset-modules/
        type: "asset",
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: path.resolve(
            __dirname,
            "node_modules",
            "@uswds",
            "uswds",
            "dist",
            "img"
          ),
          to: "uswds/img",
        },
        {
          from: path.resolve(
            __dirname,
            "frontend", "src", "img"
          ),
          to: "img",
        },
      ],
    }),
    new MiniCssExtractPlugin(),
  ],

  devtool: "source-map",
  devServer: {
    static: "./dist",
  },
  resolve: {
    modules: [path.resolve(__dirname, "frontend", "src"), "node_modules"],
    alias: {
      "uswds-img-dist": path.resolve(
        __dirname,
        "node_modules",
        "@uswds",
        "uswds",
        "dist",
        "img"
      ),
      "uswds-fonts-dist": path.resolve(
        __dirname,
        "node_modules",
        "@uswds",
        "uswds",
        "dist",
        "fonts"
      ),
    },
  },
};
