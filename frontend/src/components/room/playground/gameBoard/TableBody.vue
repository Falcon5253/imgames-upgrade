<template>
  <tbody>
    <TableBodyRow
      v-for="channel in channels"
      :key="'body-' + monthKey + '-' + channel.id"
      :channel="channel"
      :stages="stages"
      :data="rowData(channel.id)"
      :monthKey="monthKey"
    ></TableBodyRow>
  </tbody>
</template>

<script>
import TableBodyRow from '@/components/room/playground/gameBoard/TableBodyRow.vue';

export default {
  name: 'TableBody',
  components: {
    TableBodyRow,
  },
  props: {
    channels: {
      type: Array,
    },
    stages: {
      type: Array,
    },
    data: {
      type: Array,
    },
    monthKey: {
      type: undefined,
      default: 0,
    },
  },
  methods: {
    rowData(channelId) {
      let dataObject = this.data.find((el) => {
        return +el.channel.id == +channelId;
      });
      if (dataObject != undefined) {
        return dataObject.data;
      }
      return {};
    },
  },
};
</script>

<style lang="scss" scoped></style>
