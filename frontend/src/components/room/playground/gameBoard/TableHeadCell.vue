<template>
  <th>{{ textContent }}</th>
</template>

<script>
export default {
  name: 'TableHeadCell',
  props: {
    textContent: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped></style>
