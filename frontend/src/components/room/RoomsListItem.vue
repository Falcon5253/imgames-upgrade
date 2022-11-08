<template>
  <div class="normal-border-box rooms-list-item">
    <div class="left-part">
      {{ $t('room.room') }}<br /><b>{{ room.code }}</b>
    </div>
    <div class="right-part">
      <router-link :to="'/r/' + room.code.toUpperCase()"
        >{{ $t('room.goToRoom') }} →
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RoomsListItem',
  props: {
    room: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

.rooms-list-item {
  font-family: $primary_font;
  color: $dark_text_color;
  font-size: 14px;
  margin-bottom: 0.5rem;
  padding: 1rem;
  margin-right: 0.5rem;
  display: flex;
  justify-content: space-between;

  & .left-part,
  & .right-part {
    display: flex;
    align-items: center;
  }

  & .left-part {
    flex-direction: column;
  }

  & .right-part {
    text-align: right;
  }
}
</style>
