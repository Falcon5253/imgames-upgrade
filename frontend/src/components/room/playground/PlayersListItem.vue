<template>
  <div class="players-list-item normal-border-box" :class="{ userMadeTurn: player.isTurnMade }">
    <div v-if="ownerId == player.user.id" class="room-owner-icon">
      <img src="@/assets/icons/inner-star.svg" />
    </div>
    <img class="player-avatar" src="@/assets/no_avatar.svg" alt="Аватар" />
    {{ player.user.firstName }}
    {{ player.user.lastName }}
  </div>
</template>

<script>
export default {
  name: 'PlayersListItem',
  props: {
    player: {
      type: Object,
      required: true,
    },
    ownerId: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

.players-list-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 8px;
  font-family: $primary_font;
  color: $dark_text_color;
  text-align: center;
  font-size: 14px;
  position: relative;

  & .room-owner-icon {
    position: absolute;
    top: -12px;
    right: -8px;
    & img {
      height: 28px;
    }
  }

  .player-avatar {
    height: 38px;
  }
}
.userMadeTurn {
  background: linear-gradient(135deg, #4fcd33 0%, #2d9c8c 100%);
}
</style>
