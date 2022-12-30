<template>
  <div id="top-bar">
    <Logo></Logo>
    <div class="menu-block" v-if="type == 'playground'">
      <div class="left-block">
        <div class="menu-link menu-link-bold room-data">
          {{ $t('room.room') }} {{ roomCode }} / {{ $t('room.round') }} {{
            roomRound
          }}
          /
          <span style='margin-left:0.25em; display:inline-block;' v-bind:class="{ highlight : highlight }">{{ $t('room.monthNumber.'+(roomMonth)) }} ({{ $t('room.periodIs') }} {{ roomTotalMonths }} {{ $t('room.numberOfMonths') }}) </span>
        </div>
      </div>
      <div class="right-block">
        <router-link class="menu-link" :to="mainPath"
          >{{ $t('buttons.toMainPage') }} →</router-link
        >
      </div>
    </div>
    <div class="menu-block" v-else-if="type == 'auth'">
      <div class="left-block"></div>
      <div class="right-block">
        <LocaleSwitcher></LocaleSwitcher>
        <SubmitButton
          class="menu-link"
          :type="'light-text'"
          @click="$router.push(signUpPath)"
          >{{ $t('auth.signUpButton') }}</SubmitButton
        >
      </div>
    </div>
    <div class="menu-block" v-else-if="type == 'sign-up'">
      <div class="left-block"></div>
      <div class="right-block">
        <LocaleSwitcher></LocaleSwitcher>
        <SubmitButton
          class="menu-link"
          :type="'light-text'"
          @click="$router.push(authPath);"
          >{{ $t('auth.enterButton') }}</SubmitButton
        >
      </div>
    </div>
    <div class="menu-block" v-else>
      <div class="left-block"></div>
      <div class="right-block">
        <LocaleSwitcher></LocaleSwitcher>
        <p class='userName'> {{ this.$store.state.userName }} </p>
        <LogOutButton class="menu-link"></LogOutButton>
      </div>
    </div>
  </div>
</template>

<script>
import { MAIN_PATH, SIGN_UP_PATH, AUTH_PATH } from '@/pathVariables';
import Logo from '@/components/ui/Logo.vue';
import LogOutButton from '@/components/auth/LogOutButton.vue';
import LocaleSwitcher from '@/components/locale/LocaleSwitcher.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';

export default {
  name: 'TopBar',
  components: { Logo, LogOutButton, LocaleSwitcher, SubmitButton },
  props: {
    type: {
      type: String,
    },
    roomCode: {
      type: String,
    },
    roomRound: {
      type: Number,
    },
    roomMonth: {
      type: Number,
    },
    roomTotalMonths: {
      type: Number,
    },
    highlight: {
      type: Boolean,
    },
  },
  data() {
    return {
      mainPath: MAIN_PATH,
      signUpPath: SIGN_UP_PATH,
      authPath: AUTH_PATH,
    };
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

#top-bar {
  background-color: $main_dark_bg_color;
  display: flex;
  height: 48px;

  .menu-block {
    display: flex;
    justify-content: space-between;
    font-family: $primary_font;
    width: 100%;

    .left-block,
    .right-block {
      display: flex;

      a {
        &:hover {
          text-decoration: underline;
        }
      }

      .menu-link {
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        padding: 0 1rem;
        color: $light_text_color;
        font-size: 1rem;

        &-bold {
          font-family: $primary_font_bold;
        }
      }
    }
    .room-data-short {
      display: none;
    }
  }
}
.highlight {
  color: $light_text_color;
  animation: blink 2s 3 linear ;
}

.userName {
  background-color: transparent;
  color: $light_text_color;
  border: 0px;
  margin-top: 6px;
  padding-left: 30px;
  padding-right: 20px;
  & option {
    color: $dark_text_color;
  }
}

@media (max-width: 768px) {
  .userName {
    display: none;
  }
}

@keyframes blink {  
	0% { color: $light_text_color; }
	25% { color: #FBB; }
	50% { color: #F00; } 
  75% { color: #FBB; }
  100% { color: $light_text_color; }
}

@media screen and (max-width: 600px) {
  .room-data {
    display: none !important;
  }
}
</style>
