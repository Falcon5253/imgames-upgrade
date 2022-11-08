<template>
  <div class="auth-page">
    <TopBar :type="'auth'"></TopBar>
    <div class="auth-view default-background">
      <div class="normal-border-box auth-box">
        <h1>{{ $t('auth.authHeader') }}</h1>
        <form @submit.prevent>
          <TextInput
            :label="$t('auth.emailLabel')"
            :placeholder="$t('auth.emailLabel')"
            :autocomplete="'email'"
            @input="email = $event"
          ></TextInput>
          <TextInput
            :label="$t('auth.passwordLabel')"
            :placeholder="$t('auth.passwordLabel')"
            :type="'password'"
            :autocomplete="'current-password'"
            @input="password = $event"
          ></TextInput>
          <SubmitButton class="enter-button" @click="tryLogIn">{{
            $t('auth.enterButton')
          }}</SubmitButton>
        </form>
        {{ $t('auth.signUpText') }}
        <SubmitButton
          class="sign-up-button"
          :type="'dark-text'"
          @click="$router.push(SIGN_UP_PATH)"
          >{{ $t('auth.signUpButton') }}</SubmitButton
        >
      </div>
    </div>
  </div>
</template>

<script>
import { MAIN_PATH, SIGN_UP_PATH } from '@/pathVariables.js';
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import TopBar from '@/components/ui/TopBar.vue';
import login from '@/graphql/mutations/login.gql';

export default {
  name: 'AuthView',
  components: {
    TextInput,
    SubmitButton,
    TopBar,
  },
  data() {
    return {
      email: '',
      password: '',
      SIGN_UP_PATH,
    };
  },
  methods: {
    tryLogIn() {
      this.$store.commit('START_LOADING');
      this.$apollo
        .mutate({
          mutation: login,
          variables: {
            email: this.email,
            password: this.password,
          },
        })
        .then((data) => {
          this.$store.commit('SET_IS_AUTHENTICATED', true);
          this.$store.commit('SET_GOT_VERIFIED_AUTH', true);
          this.$router.push(MAIN_PATH).catch((err) => {
            console.log(err);
          });
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          this.$store.commit('STOP_LOADING');
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.auth-page {
  height: 100vh;
  & .auth-view {
    height: calc(100vh - 48px);
    width: 100vw;
    display: flex;
    & .auth-box {
      margin: auto;
      max-width: 380px;
      width: 40%;
      padding: 1rem;
      box-sizing: border-box;
      h1 {
        padding-top: 0;
        padding-bottom: 1rem;
      }
      .enter-button {
        width: 100%;
        margin-bottom: 1rem;
      }
      .sign-up-button {
        padding: 0;
      }
    }
  }
}
@media screen and (max-width: 610px) {
  .auth-page {
    & .auth-view {
      & .auth-box {
        width: 70%;
      }
    }
  }
}
@media screen and (max-width: 380px) {
  .auth-page {
    & .auth-view {
      & .auth-box {
        width: 96%;

        & h1 {
          font-size: 24px;
        }
      }
    }
  }
}
</style>
