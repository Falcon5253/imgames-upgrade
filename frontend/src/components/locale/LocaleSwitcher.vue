<template>
  <select v-model="$i18n.locale" class="locale-switcher">
    <option :value="locale.code" v-for="locale in locales" :key="locale.code">
      <flag :iso="locale.code" /> {{ locale.name }}
    </option>
  </select>
</template>

<script>
import { getSupportedLocales } from '@/util/i18n/supported-locales';
export default {
  name: 'LocaleSwitcher',
  data() {
    return {
      locales: getSupportedLocales(),
    };
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

select.locale-switcher {
  background-color: transparent;
  color: $light_text_color;
  border: 0px;
  & option {
    color: $dark_text_color;
  }
}
</style>
