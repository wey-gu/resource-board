import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'
import store from './store'
import VueRouter from 'vue-router'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(new VueSocketIO({
  debug: true,
  connection: 'http://localhost:5000',
  vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
  }
}))

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
