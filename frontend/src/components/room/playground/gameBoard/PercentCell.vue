<template>
  <td>
    <template v-if="isHide">-</template>
    <template v-else>{{ intValue }}%</template>
  </td>
</template>

<script>
export default {
  name: 'PercentCell',
  props: {
    value: {
      type: Number,
      required: true,
    },
    isHide: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    intValue() {
      return Math.round(this.value * 100);
    },
  },
};
</script>

<style lang="scss" scoped></style>
