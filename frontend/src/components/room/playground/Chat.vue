<template>
  <div class="chat-box">
    <h3>{{ $t('room.player.chat') }}</h3>
    <div class="messages-box scrollable" ref="messagesBox">
      <template v-if="messages.length == 0">
        <p>Напишите первое сообщение!</p>
      </template>
      <template v-for="(message, index) in messages">
        <div
          class="message-row message-row-right"
          :key="'message' + index"
          v-if="message.user.id == userId"
        >
          <div class="message normal-border-box">
            <small>{{ $t('room.player.you') }}</small>
            {{ message.text }}
          </div>
          <div class="avatar">
            <img
              class="player-avatar"
              src="@/assets/no_avatar.svg"
              alt="Аватар"
            />
          </div>
        </div>
        <div class="message-row" :key="'message' + index" v-else>
          <div class="avatar">
            <img
              class="player-avatar"
              src="@/assets/no_avatar.svg"
              alt="Аватар"
            />
          </div>
          <div class="message normal-border-box">
            <small>{{
              message.user
                ? (message.user.firstName + message.user.lastName)
                : $t('room.player.player') + ' #' + message.user.id
            }}</small>
            {{ message.text }}
          </div>
        </div>
      </template>
    </div>
    <div class="input-box">
      <TextInput
        :placeholder="'Введите сообщение...'"
        :predefined="newMessageText"
        @input="setMessage($event)"
        @enter="sendMessage"
      ></TextInput>
      <SubmitButton @click="sendMessage">Отправить</SubmitButton>
    </div>
  </div>
</template>

<script>
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';

import sendMessage from '@/graphql/mutations/rooms/sendMessage.gql';
  
export default {
  name: 'Chat',
  components: {
    TextInput,
    SubmitButton,
  },
  props: ["messages"],
  computed: {
    userId() {
      return this.$store.state.userId;
    },
    roomCode() {
      return this.$route.params.roomCode;
    },
  },
  data() {
    return {
      newMessageText: '',
    };
  },
  methods: {
    setMessage(messageText) {
      this.newMessageText = messageText;
    },
    sendMessage() {
      if (this.newMessageText != '') {
        this.$apollo
        .mutate({
          mutation: sendMessage,
          variables: {
            text: this.newMessageText,
            code: this.roomCode
          },
        });
        this.newMessageText = '';
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.chat-box {
  display: flex;
  flex-direction: column;

  & .messages-box {
    height: 100%;
    min-height: 200px;

    & .message-row {
      display: flex;

      &-right {
        justify-content: flex-end;
      }

      & .avatar {
        & img {
          height: 24px;
          margin: 0.5rem;
        }
      }

      & .message {
        padding: 0.5rem;
        line-break: anywhere;
        max-width: 180px;
        display: flex;
        flex-direction: column;
        margin-bottom: 0.25rem;
      }
    }
  }

  & .input-box {
    display: flex;
    flex-direction: column;
    align-items: flex-end;

    & .user-input {
      width: 100%;
      margin-bottom: 0.5rem;
    }

    & button {
      width: 120px;
      margin-bottom: 0.5rem;
    }
  }
}

@media screen and (max-width: 610px) {
  .chat-box {
    & .messages-box {
      max-height: 300px;
    }
  }
}
</style>
