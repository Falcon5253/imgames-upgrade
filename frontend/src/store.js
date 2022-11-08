import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

function getSubdomain(url) {
  url = url.replace('https://www.', '');
  url = url.replace('http://www.', '');
  url = url.replace('https://', '');
  url = url.replace('http://', '');
  var temp = url.split('/');
  if (temp.length > 0) {
    var temp2 = temp[0].split('.');
    if (temp2.length > 1) {
      if (
        temp2.length > 2 ||
        temp2[1].includes(process.env.VUE_APP_MAIN_DOMAIN)
      ) {
        return temp2[0];
      }
    }
  }
  return '';
}

const store = new Vuex.Store({
  strict: true,
  state: {
    userId: false,
    isAuthenticated: false,
    isLoading: false,
    gotVerifiedAuth: false,
    subdomain: getSubdomain(window.location.host),
    packageVersion: process.env.PACKAGE_VERSION || '0',
    chosenCards: [],
    messages: [],
  },
  mutations: {
    START_LOADING(state) {
      state.isLoading = true;
    },
    STOP_LOADING(state) {
      state.isLoading = false;
    },
    SET_IS_AUTHENTICATED(state, boolean) {
      state.isAuthenticated = boolean;
    },
    SET_GOT_VERIFIED_AUTH(state, boolean) {
      state.gotVerifiedAuth = boolean;
    },
    SET_USER_ID(state, userId) {
      state.userId = userId;
    },
    ADD_CHOSEN_CARD(state, card) {
      if (card != undefined) {
        let existCardIndex = state.chosenCards.findIndex((el) => {
          console.log(el);
          return el.id === card.id;
        });
        if (existCardIndex == -1) {
          state.chosenCards.push({
            id: card.id,
            header: card.header,
            count: 1,
          });
        } else {
          state.chosenCards[existCardIndex].count += 1;
        }
      }
    },
    CLEAN_CHOSEN_CARD(state) {
      state.chosenCards = [];
    },
    ADD_MESSAGE(state, message) {
      state.messages.push(message);
    },
  },
  actions: {},
});

export default store;
