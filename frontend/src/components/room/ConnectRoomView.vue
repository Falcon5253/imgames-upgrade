<template>
  <div>
    <h2>{{ $t('room.connectRoom') }}</h2>
    <div class="normal-border-box connect-room-form green-border-box">
      <TextInput
        :label="$t('room.roomCode')"
        :name="'roomCode'"
        :placeholder="$t('room.roomCode')"
        :disabled="formLoading"
        :type="'text'"
        @input="roomCode = $event"
      ></TextInput>
      <SubmitButton
        :type="'bg-green'"
        :disabled="formLoading"
        @click="joinRoom"
      >
        {{ $t('buttons.connect') }}
      </SubmitButton>
    </div>
  </div>
</template>

<script>
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import connectRoom from '@/graphql/mutations/rooms/connectRoom.gql';
import { ROOMS_ROOT_PATH } from '@/pathVariables.js';

export default {
  name: 'ConnectRoomView',
  components: {
    TextInput,
    SubmitButton,
  },
  data() {
    return {
      roomCode: '',
      formLoading: false,
    };
  },
  methods: {
    joinRoom() {
      this.formLoading = true;
      this.$apollo
        .mutate({
          mutation: connectRoom,
          variables: {
            code: this.roomCode,
          },
        })
        .then((result) => {
          if (result.data.connectRoom.success) {
            let roomCode = this.roomCode;
            this.roomCode = '';
            this.$router.push(ROOMS_ROOT_PATH + '/' + roomCode.toUpperCase());
          }
        })
        .catch()
        .finally(() => {
          this.formLoading = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
}
.connect-room-form {
  padding: 1rem;
  & .user-input {
    & input {
      width: 100%;
      box-sizing: border-box;
    }
  }
  & button {
    width: 100%;
  }
}
</style>
