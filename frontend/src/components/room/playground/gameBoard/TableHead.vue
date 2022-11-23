<template>
  <thead>
    <tr>
      <TableHeadCell
        :textContent="$t('room.gameBoard.channelsTitle')"
      ></TableHeadCell>
      <TableHeadCell
        :textContent="$t('room.gameBoard.trafficTitle')"
      ></TableHeadCell>
      <template v-for="(stage, index) in sortedStages">
        <TableHeadCell
          :textContent="stage.name"
          :key="'head-' + monthKey + '-' + stage.id + '.1'"
        ></TableHeadCell>
        <TableHeadCell
          :textContent="$t('room.gameBoard.stageConversion')"
          :key="'head-' + monthKey + '-' + stage.id + '.2'"
          v-if="index != stages.length - 1"
        ></TableHeadCell>
      </template>
      <!-- TODO: add double column v-for -->
      <TableHeadCell :textContent="$t('room.gameBoard.total')"></TableHeadCell>
    </tr>
  </thead>
</template>

<script>
import TableHeadCell from '@/components/room/playground/gameBoard/TableHeadCell.vue';

export default {
  name: 'TableHead',
  components: {
    TableHeadCell,
  },
  props: {
    stages: {
      type: Array,
    },
    monthKey: {
      type: undefined,
      default: 0,
    },
  },
  data() {
    return {
      sortedStages: [],
    };
  },
  mounted() {
    if (Array.isArray(this.stages)) {
      this.sortedStages = this.stages.sort(
        (a, b) => a.stageinsequence.place - b.stageinsequence.place
      );
    }
  },
  watch: {
    stages(newVal) {
      if (Array.isArray(newVal)) {
        this.sortedStages = newVal
          .slice()
          .sort((a, b) => a.stageinsequence.place - b.stageinsequence.place);
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
