<template>
  <button
    @click="sendClick"
    :disabled="disabled"
    :class="{
      'dark-text': type == 'dark-text',
      'light-text': type == 'light-text',
      'bg-blue': type == 'bg-blue',
      'bg-green': type == 'bg-green',
      'bg-outline': type == 'bg-outline',
    }"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'SubmitButton',
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: 'bg-blue',
    },
  },
  methods: {
    sendClick() {
      this.$emit('click');
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

button {
  cursor: pointer;
}

.dark-text {
  background-color: transparent;
  border: 0;
  color: $dark_text_color;
  font-family: $primary_font;
  font-size: 1rem;

  &:hover {
    text-decoration: underline;
  }
}

.light-text {
  background-color: transparent;
  border: 0;
  color: $light_text_color;
  font-family: $primary_font;
  font-size: 1rem;

  &:hover {
    text-decoration: underline;
  }
}
.bg-blue {
  border: 0px;
  background: linear-gradient(135deg, #72edf2 0%, #5151e5 100%);
  border-radius: 8px;
  font-family: $primary_font;
  color: $light_text_color;
  font-weight: bold;
  font-size: 14px;
  height: 40px;
  min-width: 100px;
}
.bg-green {
  border: 0px;
  background: linear-gradient(135deg, #4fcd33 0%, #2d9c8c 100%);
  border-radius: 8px;
  font-family: $primary_font;
  color: $light_text_color;
  font-weight: bold;
  font-size: 14px;
  height: 40px;
  min-width: 100px;
}
.bg-outline {
  border: 1px solid $main_dark_bg_color;
  font-family: $primary_font;
  color: $dark_text_color;
  font-size: 14px;
  font-weight: bold;
  height: 40px;
  border-radius: 8px;
  background: transparent;
}
</style>
