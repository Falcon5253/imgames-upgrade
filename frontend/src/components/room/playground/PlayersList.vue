<template>
  <div>
    <div class="head">
      <h3>{{ $t('room.player.playersList') }}</h3>
      <SubmitButton type="bg-blue" @click="collapse">Закрыть</SubmitButton>
    </div>
    <div class="players-list-wrapper">
      <PlayersListItem
        v-for="player in players"
        :key="player.id"
        :player="player"
        :ownerId="roomOwnerId"
      ></PlayersListItem>
    </div>
  </div>
</template>

<script>
import PlayersListItem from '@/components/room/playground/PlayersListItem.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';

export default {
  name: 'PlayersList',
  components: {
    PlayersListItem,
    SubmitButton,
  },
  props: {
    players: {
      type: Array,
      required: true,
    },
    room: {
      type: Object,
      required: true,
    },
  },
  computed: {
    roomOwnerId() {
      if (this.room.roomOwnerId != undefined) {
        return this.room.roomOwnerId
      }
      return 0;
    },
  },
  methods: {
    collapse() {
      this.$emit('closeMenu');
    }
  },

};
</script>

<style lang="scss" scoped>
.players-list-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  column-gap: 8px;
}
.head {
    display: flex;
    width: 100%;
    padding-top: 16px;
    padding-bottom: 16px;
    justify-content: space-between;
}
</style>
