<template>
  <div>
    <h2>{{ $t('room.createNewRoom') }}</h2>
    <CreateRoomForm></CreateRoomForm>
  </div>
</template>

<script>
import CreateRoomForm from '@/components/room/CreateRoomForm.vue';

export default {
  name: 'CreateRoomView',
  components: {
    CreateRoomForm,
  },
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
  top: 0;
  left: 0;
}
</style>
