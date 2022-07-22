import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueSnip from 'vue-snip'
import router from './router'
import { LMap, LTileLayer, LMarker, LWMSTileLayer } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

Vue.use(VueSnip)
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-wms-tile-layer', LWMSTileLayer);
