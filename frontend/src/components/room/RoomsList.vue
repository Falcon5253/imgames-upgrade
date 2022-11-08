<template>
  <div class="rooms-list scrollable">
    <RoomsListItem
      v-for="room in roomsInOrganization"
      :key="room.id"
      :room="room"
    ></RoomsListItem>
  </div>
</template>

<script>
import RoomsListItem from '@/components/room/RoomsListItem.vue';
import roomsInOrganization from '@/graphql/queries/rooms/roomsInOrganization.gql';

export default {
  name: 'RoomList',
  components: {
    RoomsListItem,
  },
  apollo: {
    roomsInOrganization: {
      query: roomsInOrganization,
      variables() {
        return {
          subdomain: this.subdomain,
        };
      },
    },
  },
  computed: {
    subdomain() {
      return this.$store.state.subdomain;
    },
  },
};
</script>

<style lang="scss" scoped>
.rooms-list {
  height: calc(100vh - 95px);
  overflow-y: auto;
}
@media screen and (max-width: 810px) {
  .rooms-list {
    height: calc(50vh - 48px);
  }
}
</style>
