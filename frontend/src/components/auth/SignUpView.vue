<template>
  <div>
    <div class="sign-up-page">
      <TopBar :type="'sign-up'"></TopBar>
      <div class="sign-up-view default-background">
        <div class="normal-border-box sign-up-box">
          <template v-if="isSuccess">
            <h1>{{ $t('auth.signUpSuccessHeader') }}</h1>
            {{ $t('auth.signUpSuccessText') }}
          </template>
          <template v-else>
            <h1>{{ $t('auth.signUpHeader') }}</h1>
            <form @submit.prevent>
              <TextInput
                :label="$t('auth.emailLabel')"
                :placeholder="$t('auth.emailLabel')"
                :autocomplete="'email'"
                :isAnyError="$v.form.email.$anyError"
                :isRequiredError="
                  !$v.form.email.required && $v.form.email.$anyDirty
                "
                :disabled="isLoading"
                @input="setEmail($event)"
              ></TextInput>
              <TextInput
                :label="$t('auth.passwordLabel')"
                :placeholder="$t('auth.passwordLabel')"
                :autocomplete="'new-password'"
                :type="'password'"
                :isAnyError="$v.form.password.$anyError"
                :isRequiredError="
                  !$v.form.password.required && $v.form.password.$anyDirty
                "
                :disabled="isLoading"
                @input="setPassword($event)"
              ></TextInput>
              <TextInput
                :label="$t('auth.firstNameLabel')"
                :placeholder="$t('auth.firstNameLabel')"
                :autocomplete="'first-name'"
                :isAnyError="$v.form.firstName.$anyError"
                :isRequiredError="
                  !$v.form.firstName.required && $v.form.firstName.$anyDirty
                "
                :disabled="isLoading"
                @input="setFirstName($event)"
              ></TextInput>
              <TextInput
                :label="$t('auth.lastNameLabel')"
                :placeholder="$t('auth.lastNameLabel')"
                :autocomplete="'family-name'"
                :isAnyError="$v.form.lastName.$anyError"
                :isRequiredError="
                  !$v.form.lastName.required && $v.form.lastName.$anyDirty
                "
                :disabled="isLoading"
                @input="setLastName($event)"
              ></TextInput>
              <div class="errors">
                <div
                  class="error-message"
                  v-if="errorsContains('emailAlreadyExists')"
                >
                  Учётная запись с указанным email существует
                </div>
                <div class="error-message" v-if="errorsContains('commonError')">
                  Возникла ошибка. Попробуйте повторить позднее.
                </div>
              </div>
              <SubmitButton
                class="sign-up-button"
                :disabled="isEnterButtonDisabled || isLoading"
                @click="trySignUp"
                >{{ $t('auth.signUpButton') }}</SubmitButton
              >
            </form>
            {{ $t('auth.enterText') }}
          </template>
          <SubmitButton
            class="enter-button"
            :type="'dark-text'"
            @click="$router.push(authPath)"
            >{{ $t('auth.enterButton') }}</SubmitButton
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TopBar from '@/components/ui/TopBar.vue';
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import { AUTH_PATH } from '@/pathVariables.js';
import { required } from 'vuelidate/lib/validators';
import register from '@/graphql/mutations/register.gql';

export default {
  name: 'SignUpView',
  components: {
    TopBar,
    TextInput,
    SubmitButton,
  },
  data() {
    return {
      authPath: AUTH_PATH,
      form: {
        email: '',
        password: '',
        firstName: '',
        lastName: '',
      },
      isLoading: false,
      isSuccess: false,
      errors: [],
    };
  },
  methods: {
    setEmail(email) {
      this.form.email = email;
      this.$v.form.email.$model = email;
      this.$v.form.email.$touch();
      this.errors = [];
    },
    setPassword(password) {
      this.form.password = password;
      this.$v.form.password.$model = password;
      this.$v.form.password.$touch();
      this.errors = [];
    },
    setFirstName(firstName) {
      this.form.firstName = firstName;
      this.$v.form.firstName.$model = firstName;
      this.$v.form.firstName.$touch();
      this.errors = [];
    },
    setLastName(lastName) {
      this.form.lastName = lastName;
      this.$v.form.lastName.$model = lastName;
      this.$v.form.lastName.$touch();
      this.errors = [];
    },
    trySignUp() {
      this.$v.form.$touch();
      if (!this.$v.form.$anyError) {
        this.isLoading = true;
        this.$apollo
          .mutate({
            mutation: register,
            variables: this.form,
          })
          .then((result) => {
            console.log('result', result.data.register);
            this.isSuccess = result.data.register.success;
            this.errors = result.data.register.errors;
          })
          .catch((error) => {
            console.log('error', error);
            this.errors = ['commonError'];
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },
    errorsContains(error) {
      return this.errors.includes(error);
    },
  },
  validations: {
    form: {
      email: {
        required,
      },
      password: {
        required,
      },
      firstName: {
        required,
      },
      lastName: {
        required,
      },
    },
  },
  computed: {
    isEnterButtonDisabled() {
      return this.$v.form.$anyError;
    },
  },
};
</script>

<style lang="scss" scoped>
.sign-up-page {
  height: 100vh;
  & .sign-up-view {
    height: calc(100vh - 48px);
    width: 100vw;
    display: flex;
    & .sign-up-box {
      margin: auto;
      min-width: 320px;
      max-width: 380px;
      width: 40%;
      padding: 1rem;
      box-sizing: border-box;
      h1 {
        padding-top: 0;
        padding-bottom: 1rem;
      }
      .sign-up-button {
        width: 100%;
        margin-bottom: 1rem;
      }
      .enter-button {
        padding: 0;
      }
      .errors {
        & * {
          margin: 0.25rem 0;
        }
      }
    }
  }
}

@media screen and (max-width: 360px) {
  .sign-up-page {
    & .sign-up-view {
      & .sign-up-box {
        min-width: unset;
        width: 94%;
        & h1 {
          font-size: 24px;
        }
      }
    }
  }
}
</style>
