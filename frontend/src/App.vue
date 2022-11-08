<template lang="html">
  <div>
    <div class="spinner-box" v-if="isLoading">
      <Spinner></Spinner>
    </div> 
    <router-view />
  </div>
</template>

<script>
import Spinner from '@/components/ui/Spinner.vue';
import { version } from '../package.json';

export default {
  name: 'App',
  components: { Spinner },
  computed: {
    isLoading() {
      return this.$store.state.isLoading;
    },
    packageVersion() {
      return version;
    },
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
    path() {
      return window.location.host;
    },
    subdomain() {
      return this.$store.state.subdomain;
    },
  }
};
</script>

<style lang="scss">
@import '@/scss/_variables.scss';


body {
  padding: 0;
  margin: 0;
  overflow-x: hidden;
  overflow-y: hidden;
  font-family: $primary_font;
}


h1, h2, h3, p {
  font-family: $primary_font;
  margin: 0;
  padding: 0.5rem 0;
  color: $dark_text_color;
}

a {
  color: $dark_text_color;
  &:visited, &:active {
    color: $dark_text_color;
  }
  &:hover {
     color: lighten($dark_text_color, 10);
  }
  
  
}


.scrollable {
  overflow-y: auto;
  scrollbar-gutter: stable;
  &::-webkit-scrollbar {
    width: 16px;
  }
  &::-webkit-scrollbar-track {
    width: 16px;
    background-color: rgba(0,0,0,.1);
  }
  &::-webkit-scrollbar-thumb {
    backdrop-filter: blur(12px) saturate(100%);
    -webkit-backdrop-filter: blur(12px) saturate(100%);
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 12px;
    border: 1px solid rgba(209, 213, 219, 0.3);
  }
}

.normal-border-box {
  position: relative;
  backdrop-filter: blur(12px) saturate(100%);
  -webkit-backdrop-filter: blur(12px) saturate(100%);
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  z-index: 1;
  position: relative;
  border: none;
}

.normal-border-box::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 8px;
  padding: 2px;
  background: linear-gradient(
    288.78deg,
    #6a3f7e 0%,
    #cddfe9 43.75%,
    #1da1ac 100%
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  z-index: -1;
}

.gold-border-box::before {
  background: conic-gradient(#edc800, #e3b600, #f3cf00, #ffe800,
								#edc800, #e3b600, #f3cf00, #ffe800,
								#edc800, #e3b600, #f3cf00, #ffe800,
								#edc800, #e3b600, #f3cf00, #ffe800);
}

.silver-border-box::before {
  background: conic-gradient(#d7d7d7, #c3c3c3, #cccccc, #c6c6c6,
								#d7d7d7, #c3c3c3, #cccccc, #c6c6c6,
								#d7d7d7, #c3c3c3, #cccccc, #c6c6c6,
								#d7d7d7, #c3c3c3, #cccccc, #c6c6c6);
}

.bronze-border-box::before {
  background: conic-gradient(#d95641, #b14439, #b2453a, #d25645, 
								#d95641, #b14439, #b2453a, #d25645,
								#d95641, #b14439, #b2453a, #d25645,
								#d95641, #b14439, #b2453a, #d25645);
}

.green-border-box::before {
  background: linear-gradient(151.73deg, #4CC938 0%, #30A083 100%);
}

.orange-border-box::before {
  background: linear-gradient(151.73deg, #FDE2AE 0%, #F65775 100%);
}


.default-background {
  background: radial-gradient(52.5% 97.01% at 21.67% 20.17%, rgba(82, 110, 255, 0.25) 0%, rgba(249, 216, 167, 0.25) 89.06%);
}

.error-message {
  color: $error;
}

.error-input {
  outline: 1px solid $error;
}

.w-100 {
  width: 100%;
}

.spinner-box {
  position: absolute;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,.4);
  display: flex;
  z-index: 10000;

  & * {
    margin: auto;
  }
}

@font-face {
  font-family: "PT Sans";
  src: local("PT Sans"), url(./assets/fonts/PTSans/PTSans-Regular.ttf) format("truetype");
}

@font-face {
  font-family: "PT Sans Bold";
  src: local("PT Sans Bold"), url(./assets/fonts/PTSans/PTSans-Bold.ttf) format("truetype");
}
</style>
  
</style>
