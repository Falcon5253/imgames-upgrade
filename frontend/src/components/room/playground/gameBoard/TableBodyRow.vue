<template>
  <tr>
    <ChannelTitleCell :title="channel.name"></ChannelTitleCell>
    <CardinalNumberCell :value="+data[0]"></CardinalNumberCell>
    <template v-for="(stage, index) in stages">
      <PercentCell
        :key="'bodycell-' + monthKey + '-' + stage.id + '.1'"
        :value="+data[1 + index * 2]"
      ></PercentCell>
      <CardinalNumberCell
        :key="'bodycell-' + monthKey + '-' + stage.id + '.2'"
        :value="+data[2 + index * 2]"
        v-if="index != stages.length - 1"
      ></CardinalNumberCell>
    </template>
    <CardinalNumberCell :value="+data[data.length - 1]"></CardinalNumberCell>
  </tr>
</template>

<script>
import ChannelTitleCell from '@/components/room/playground/gameBoard/ChannelTitleCell.vue';
import CardinalNumberCell from '@/components/room/playground/gameBoard/CardinalNumberCell.vue';
import PercentCell from '@/components/room/playground/gameBoard/PercentCell.vue';

export default {
  name: 'TableBodyRow',
  components: {
    ChannelTitleCell,
    CardinalNumberCell,
    PercentCell,
  },
  props: {
    channel: {
      type: Object,
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
};
</script>

<style lang="scss" scoped></style>
