<template>
  <td>{{ title }}</td>
</template>

<script>
export default {
  name: 'ChannelTitleCell',
  props: {
    title: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped></style>
