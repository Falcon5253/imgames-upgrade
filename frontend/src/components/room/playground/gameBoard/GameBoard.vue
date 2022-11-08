<template>
  <div>
    <h3>{{ $t('room.gameBoard.gameBoard') }}</h3>
    <FunnelTable></FunnelTable>
  </div>
</template>

<script>
import FunnelTable from '@/components/room/playground/gameBoard/FunnelTable.vue';

export default {
  name: 'GameBoard',
  components: {
    FunnelTable,
  },
};
</script>

<style lang="scss" scoped>
@media screen and (max-width: 610px) {
  h3 {
    display: none;
  }
}
</style>
