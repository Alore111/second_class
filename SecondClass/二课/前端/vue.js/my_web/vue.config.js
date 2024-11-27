const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  // 配置前端服务地址和端口
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    https: false,
    // 配置代理
    proxy: {
      '/api': {
        target: 'http://localhost:8000',//后端服务地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    },
  }
})
