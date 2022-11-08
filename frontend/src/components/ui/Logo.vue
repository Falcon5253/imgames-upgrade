<template>
  <div>
    <img v-if="windowWidth > 610" src="@/assets/logo.png" alt="Лого" />
    <img v-else src="@/assets/logo_short.png" alt="Лого" />
  </div>
</template>

<script>
export default {
  name: 'Logo',
  data() {
    return {
      windowWidth: window.innerWidth,
    };
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth;
    },
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
};
</script>

<style lang="scss" scoped>
img {
  height: 48px;
  display: block;
}

@media screen and (max-width: 610px) {
  img {
    margin-left: 0.5rem;
  }
}
</style>
