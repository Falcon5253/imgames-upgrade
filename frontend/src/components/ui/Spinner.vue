<template>
  <div
    class="lds-ripple"
    :class="{ light: bgStyle == 'light', dark: bgStyle == 'dark' }"
  >
    <div></div>
    <div></div>
  </div>
</template>

<script>
export default {
  name: 'Spinner',
  props: {
    bgStyle: {
      type: String,
      default: 'light',
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

.lds-ripple {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
}
.lds-ripple div {
  position: absolute;
  opacity: 1;
  border-radius: 50%;
  animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}
.light div {
  border: 4px solid #fff;
}
.dark div {
  border: 4px solid $main_dark_bg_color;
}
.lds-ripple div:nth-child(2) {
  animation-delay: -0.5s;
}
@keyframes lds-ripple {
  0% {
    top: 36px;
    left: 36px;
    width: 0;
    height: 0;
    opacity: 0;
  }
  4.9% {
    top: 36px;
    left: 36px;
    width: 0;
    height: 0;
    opacity: 0;
  }
  5% {
    top: 36px;
    left: 36px;
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    top: 0px;
    left: 0px;
    width: 72px;
    height: 72px;
    opacity: 0;
  }
}
</style>
