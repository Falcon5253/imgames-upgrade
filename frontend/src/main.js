import Vue from 'vue';
import store from '@/store';
import router from '@/router';

import { createProvider } from '@/apollo';

import VueYandexMetrika from 'vue-yandex-metrika';

import * as Sentry from '@sentry/vue';
import { Integrations } from '@sentry/tracing';

import App from '@/App.vue';
import './registerServiceWorker';
import i18n from './i18n';
import FlagIcon from 'vue-flag-icon';
import Vuelidate from 'vuelidate';

Vue.config.productionTip = false;

// Библиотека для валидации
Vue.use(Vuelidate);

// Компонент для иконки флагов стран
Vue.use(FlagIcon);

// Sentry для логирования ошибок фронтенда
Sentry.init({
  Vue: Vue,
  dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
  integrations: [new Integrations.BrowserTracing()],
  tracingOptions: {
    trackComponents: true,
  },
  logError: process.env.NODE_ENV === 'development',
});

// Title для каждой страницы
const DEFAULT_TITLE = 'ImGames';
router.afterEach((to, from) => {
  Vue.nextTick(() => {
    document.title = to.meta.title || DEFAULT_TITLE;
  });
});

// Документация: https://github.com/vchaptsev/vue-yandex-metrika
Vue.use(VueYandexMetrika, {
  id: process.env.VUE_APP_YANDEX_METRIKA,
  env: process.env.NODE_ENV,
  router,
});

new Vue({
  router,
  store,
  provide: createProvider().provide(),
  i18n,
  render: (h) => h(App),
}).$mount('#app');
