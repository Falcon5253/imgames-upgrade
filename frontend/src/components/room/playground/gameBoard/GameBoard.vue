<template>
  <div>
    <h3>{{ $t('room.gameBoard.gameBoard') }}</h3>
    <FunnelTable @awaitIsOver="awaitIsOver"></FunnelTable>
  </div>
</template>

<script>
import FunnelTable from '@/components/room/playground/gameBoard/FunnelTable.vue';

export default {
  name: 'GameBoard',
  components: {
    FunnelTable,
  },
  methods: {
    awaitIsOver() {
      console.log(2);
      this.$emit("awaitIsOver");
    },
  }
};
</script>

<style lang="scss" scoped>
@media screen and (max-width: 610px) {
  h3 {
    display: none;
  }
}
</style>
