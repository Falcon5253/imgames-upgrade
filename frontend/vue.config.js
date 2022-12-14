// vue.config.js
module.exports = {
  lintOnSave: false,
  css: {
    sourceMap: false,
  },
  devServer: {
    hot: true,
    hotOnly: true,
    disableHostCheck: true,
    historyApiFallback: true,
    public: '0.0.0.0:8080',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers':
        'X-Requested-With, content-type, Authorization',
    },
    watchOptions: {
      poll: 1000,
      ignored: '/app/node_modules/',
    },
  },
  pluginOptions: {
    i18n: {
      locale: 'ru',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false,
      includeLocales: false,
      enableBridge: true,
    },
  },
};
