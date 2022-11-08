<template>
  <div class="waiting-screen normal-border-box green-border-box">
    <h2>{{ $t('room.waitingHeader') }}</h2>
    <template v-if="isRoomOwner">
      <p>{{ $t('room.waitingTextForOwner') }}</p>
      <SubmitButton @click="startRound" :type="'bg-green'">{{
        $t('room.startRoundButton')
      }}</SubmitButton>
    </template>
  </div>
</template>

<script>
import SubmitButton from '@/components/ui/SubmitButton.vue';
import startRound from '@/graphql/mutations/rooms/startRound.gql';
import isRoomOwner from '@/graphql/queries/rooms/isRoomOwner.gql';

export default {
  name: 'WaitingScreen',
  components: {
    SubmitButton,
  },
  props: {
    roomCode: {
      type: String,
      required: true,
    },
    roomOwner: {
      type: Object,
    },
  },
  apollo: {
    isRoomOwner: {
      query: isRoomOwner,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
  },
  methods: {
    startRound() {
      this.$apollo
        .mutate({
          mutation: startRound,
          variables: {
            code: this.roomCode,
          },
        })
        .then(() => {})
        .catch((e) => {
          console.log(e);
        })
        .finally(() => {
          this.$emit('reloadRound');
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.waiting-screen {
  padding: 1rem !important;
  margin: 1rem !important;
  display: flex;
}
</style>
