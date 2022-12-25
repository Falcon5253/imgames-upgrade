<template>
  <div id="playground">
    <TopBar
      type="playground"
      :roomCode="roomCode"
      :roomRound="currentRoundKey"
      :roomMonth="currentMonthKey"
      :roomTotalMonths="roomTotalMonthsNumber"
      :highlight="highlight"
    ></TopBar>
    <div class="playField" v-bind:class="{ playField_fullScreen: !isAnyMenuShown }">
      <div
        class="mobile-fade"
        v-if="
          isMobileScreen &&
          (isPlayersMenuShown || isEffectsMenuShown || isChatShown)
        "
        @click="closeMenuOpened"
      ></div>
      <template v-if="!roomIsFinished">
        <WaitingScreen
          class="first-column-full"
          v-if="!roomIsActive"
          :roomCode="roomCode"
          @reloadRound="reloadRound()"
        ></WaitingScreen>
        <template v-else>
          <GameBoard
            :class="{
              'first-column-top': isCardsListOpened,
              'd-flex': !isCardsListOpened,
              'first-column-full': !isCardsListOpened,
            }"
            class="scrollable"
          ></GameBoard>
          <transition name="slide-fade" mode="out-in">
            <CardsList
              v-if="isCardsListOpened"
              :class="{
                'first-column-bottom': isCardsListOpened,
              }"
            ></CardsList>
          </transition>
        </template>
        <transition name="slide-fade" mode="out-in">
          <PlayersList
            @closeMenu="closeMenuOpened"
            class="mobile-popup second-column-top"
            :players="players"
            :room="roomByCode"
            v-if="
              players != undefined &&
              roomByCode != undefined &&
              isPlayersMenuShown
            "
          >
          </PlayersList>
        </transition>
        <transition name="slide-fade" mode="out-in">
          <EffectsList
            class="mobile-popup second-column-bottom"
            v-if="isEffectsMenuShown"
          ></EffectsList>
        </transition>
        <transition name="slide-fade" mode="out-in">
          <Chat
            @closeMenu="closeMenuOpened"
            class="mobile-popup second-column-full"
            v-if="isChatShown"
            :messages="getChatByRoomCode"
          ></Chat>
        </transition>
      </template>
      <template v-else>
        <transition name="slide-fade" mode="out-in">
          <PlayersList
            @closeMenu="closeMenuOpened"
            class="mobile-popup second-column-top"
            :players="players"
            :room="roomByCode"
            v-if="
              players != undefined &&
              roomByCode != undefined &&
              isPlayersMenuShown
            "
          >
          </PlayersList>
        </transition>
        <transition name="slide-fade" mode="out-in">
          <EffectsList
            class="mobile-popup second-column-bottom"
            v-if="isEffectsMenuShown"
          ></EffectsList>
        </transition>
        <transition name="slide-fade" mode="out-in">
          <Chat
            @closeMenu="closeMenuOpened"
            :messages="getChatByRoomCode"
            class="mobile-popup second-column-full"
            v-if="isChatShown"
          ></Chat>
        </transition>
        <FinishScreen
          class="first-column-full"
          :roundKey="currentRoundKey"
          :roomCode="roomCode"
          @reloadRound="reloadRound()"
        ></FinishScreen>
      </template>
      <div class="navigation" v-bind:class="{ navigation_fullScreen: !isAnyMenuShown }">
        <div class="nav-btn" @click="openPlayersMenu">
          <img src="@/assets/icons/players.svg" alt="" />
          <p>{{ $t('room.navigation.players') }}</p>
        </div>
        <div class="nav-btn" @click="openEffectsMenu">
          <img src="@/assets/icons/star.svg" alt="" />
          <p>{{ $t('room.navigation.effects') }}</p>
        </div>
        <div class="nav-btn" @click="openChat">
          <img src="@/assets/icons/chat.svg" alt="" />
          <p>{{ $t('room.navigation.chat') }}</p>
        </div>
        <div class="nav-btn" @click="toggleCards">
          <img src="@/assets/icons/paper.svg" alt="" />
          <p>{{ $t('room.navigation.cards') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import roomByCode from '@/graphql/queries/rooms/roomByCode.gql';
import currentRoundByCode from '@/graphql/queries/rooms/currentRoundByCode.gql';
import roomUpdated from '@/graphql/subscriptions/rooms/roomUpdated.gql';
import currentRoundUpdated from '@/graphql/subscriptions/rooms/currentRoundUpdated.gql';
import connectRoom from '@/graphql/mutations/rooms/connectRoom.gql';
import roomParticipants from '@/graphql/queries/rooms/roomParticipants.gql';
import roomParticipantsUpdated from '@/graphql/subscriptions/rooms/roomParticipantsUpdated.gql';
import getQueueOfRoom from '@/graphql/queries/rooms/getQueueOfRoom.gql';
import queueUpdated from '@/graphql/subscriptions/rooms/queueUpdated.gql';
import monthById from '@/graphql/queries/rooms/monthById.gql';
import PlayersList from '@/components/room/playground/PlayersList.vue';
import EffectsList from '@/components/room/playground/EffectsList.vue';
import GameBoard from '@/components/room/playground/gameBoard/GameBoard.vue';
import CardsList from '@/components/room/playground/cardsList/CardsList.vue';
import WaitingScreen from '@/components/room/playground/WaitingScreen.vue';
import FinishScreen from '@/components/room/playground/FinishScreen.vue';
import TopBar from '@/components/ui/TopBar.vue';
import Chat from '@/components/room/playground/Chat.vue';
import { MAIN_PATH } from '@/pathVariables.js';
import getChatByRoomCode from '@/graphql/queries/rooms/getChatByRoomCode.gql';
import chatUpdated from '@/graphql/subscriptions/rooms/chatUpdated.gql';

export default {
  name: 'RoomPlayground',
  components: {
    PlayersList,
    EffectsList,
    GameBoard,
    CardsList,
    WaitingScreen,
    FinishScreen,
    TopBar,
    Chat,
  },
  data() {
    return {
      skip: false,
      isPlayersMenuOpened: !(window.innerWidth <= 610),
      isEffectsMenuOpened: !(window.innerWidth <= 610),
      isChatOpened: false,
      isCardsListOpened: true,
      windowWidth: window.innerWidth,
      highlight: false,
    };
  },
  computed: {
    isChatShown() {
      return this.isChatOpened;
    },
    isPlayersMenuShown() {
      return this.isPlayersMenuOpened;
    },
    isEffectsMenuShown() {
      return this.isEffectsMenuOpened;
    },
    roomCode() {
      return this.$route.params.roomCode;
    },
    currentRoundKey() {
      if (this.currentRoundByCode != undefined) {
        return this.currentRoundByCode.key;
      }
      return 0;
    },
    currentMonthKey() {
      if (this.monthById != undefined) {
        return this.monthById.key;
      }
      return 0;
    },
    currentMonthId() {
      if (this.currentRoundByCode != undefined) {
        return this.currentRoundByCode.currentMonthId;
      }
      return 0;
    },
    roomTotalMonthsNumber() {
      return this.roomByCode.numberOfTurns;
    },
    flow() {
      if (this.roomByCode != undefined) {
        if (this.roomByCode.flow != undefined) {
          return this.roomByCode.flow.title;
        }
      }
      return 0;
    },
    players() {
      if (this.roomByCode != undefined) {
        if (this.roomParticipants != undefined) {
          return this.roomParticipants;
        }
      }
      return [];
    },
    queue() {
      if (this.getQueueOfRoom != undefined) {
        return this.getQueueOfRoom;
      }
    },
    roomIsActive() {
      if (this.currentRoundByCode != undefined) {
        return this.currentRoundByCode.isActive;
      }
      return false;
    },
    roomIsFinished() {
      if (this.currentRoundByCode != undefined) {
        return this.currentRoundByCode.isFinished;
      }
      return false;
    },
    isMobileScreen() {
      return this.windowWidth <= 610;
    },
    isAnyMenuShown() {
      return this.isPlayersMenuOpened || this.isEffectsMenuOpened || this.isChatOpened;
    },
  },
  apollo: {
    roomByCode: {
      query: roomByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: roomUpdated,
        variables() {
          return {
            code: this.roomCode,
          };
        },
        skip() {
          return this.skip;
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          return { roomByCode: subscriptionData.data.roomUpdated };
        },
      },
    },
    getChatByRoomCode: {
      query: getChatByRoomCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: chatUpdated,
        variables() {
          return {
            code: this.roomCode,
            userId: this.userId,
          };
        },
        skip() {
          return this.skip;
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          let existIndex = previousResult.getChatByRoomCode.findIndex(
            (el) => {
              return el.id == subscriptionData.data.chatUpdated.id;
            }
          );
          if (existIndex == -1) {
            previousResult.getChatByRoomCode.push(
              subscriptionData.data.chatUpdated
            );
          };
        },
      }
    },
    currentRoundByCode: {
      query: currentRoundByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: currentRoundUpdated,
        variables() {
          return {
            code: this.roomCode,
          };
        },
        skip() {
          return this.skip;
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          return {
            currentRoundByCode: subscriptionData.data.currentRoundUpdated,
          };
        },
      },
    },
    monthById: {
      query: monthById,
      variables() {
        return {
          id: this.currentMonthId,
        };
      },
    },
    roomParticipants: {
      query: roomParticipants,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: roomParticipantsUpdated,
        variables() {
          return {
            code: this.roomCode,
          };
        },
        skip() {
          return this.skip;
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          let existIndex = previousResult.roomParticipants.findIndex(
            (el) => el.id == subscriptionData.data.roomParticipantsUpdated.id
          );
          if (existIndex == -1) {
            previousResult.roomParticipants.push(
              subscriptionData.data.roomParticipantsUpdated
            );
          }
          return {
            roomParticipants: previousResult.roomParticipants,
          };
        },
      },
    },
    getQueueOfRoom: {
      query: getQueueOfRoom,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: queueUpdated,
        variables() {
          return {
            code: this.roomCode,
          };
        },
        skip() {
          return this.skip;
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          return previousResult;
        },
      },
    },
  },
  methods: {
    async reloadRound() {
      console.log("RELOADING")
      this.skip = true;
      await this.$apollo.queries.roomByCode.refresh();
      await this.$apollo.queries.currentRoundByCode.refresh();
      this.skip = false;
    },
    async startHighlightAnim() {
        this.highlight=true;
        setTimeout(() => { this.highlight=false; }, 6000);
    },
    closeMenuOpened() {
      this.isPlayersMenuOpened = false;
      this.isEffectsMenuOpened = false;
      this.isChatOpened = false;
    },
    openPlayersMenu() {
      this.closeMenuOpened();
      this.isPlayersMenuOpened = true;
      if (!this.isMobileScreen) {
        this.isEffectsMenuOpened = true;
      }
    },
    openEffectsMenu() {
      this.closeMenuOpened();
      this.isEffectsMenuOpened = true;
      if (!this.isMobileScreen) {
        this.isPlayersMenuOpened = true;
      }
    },
    openChat() {
      this.closeMenuOpened();
      this.isChatOpened = true;
    },
    onResize() {
      this.windowWidth = window.innerWidth;
    },
    toggleCards() {
      this.closeMenuOpened();
      this.isCardsListOpened = !this.isCardsListOpened;
    },
    awaitIsOver() {
      this.$root.$emit("awaitIsOver");
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.window.addEventListener('resize', this.onResize);
    });
    this.$apollo
      .mutate({
        mutation: connectRoom,
        variables: {
          code: this.roomCode,
        },
      })
      .then(() => {})
      .catch(() => {
        this.$router.push(MAIN_PATH);
    });
    this.$root.$on('refreshRound', () => {
      this.$apollo.queries.currentRoundByCode.refresh();
    });
    window.addEventListener('onfocus', alert("Hi"));
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  watch: {
    currentMonthKey: {
      handler(){
        this.awaitIsOver();
        this.startHighlightAnim();
      },
      immediate: true
    },
    getQueueOfRoom: {
      async handler() {
        await this.$apollo.queries.currentRoundByCode.refresh();
      },
      immediate: true
    },
    roomByCode: { 
     async handler() {
        reloadRound();
     },
     immediate: true
   },
  }
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

.mobile-fade {
  // display: none;
  // visibility: hidden;
  display: none !important;
}

#playground {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: radial-gradient(
    52.5% 97.01% at 21.67% 20.17%,
    rgba(82, 110, 255, 0.25) 0%,
    rgba(249, 216, 167, 0.25) 89.06%
  );
  .playField {
    padding-left: 20px;
    display: grid;
    grid-template-columns: 2.8fr 1fr 62px;
    grid-template-rows: 1.6fr auto;
    height: 100%;
    max-height: calc(100vh - 48px);
    column-gap: 20px;
    row-gap: 20px;
    &_fullScreen {
      grid-template-columns: 1fr 62px;
      column-gap: 0px;
    }
    & .first-column-top {
      grid-column-start: 1;
      grid-column-end: 2;
      grid-row-start: 1;
      grid-row-end: 2;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    & .first-column-bottom {
      grid-column-start: 1;
      grid-column-end: 2;
      grid-row-start: 2;
      grid-row-end: 3;
      padding-right: 18px;
    }
    & .first-column-full {
      grid-column-start: 1;
      grid-column-end: 2;
      grid-row-start: 1;
      grid-row-end: 3;
      // display: flex;
      flex-direction: column;
      justify-content: center;
    }

    & .two-column-full {
      grid-column-start: 1;
      grid-column-end: 3;
      grid-row-start: 1;
      grid-row-end: 3;
      // display: flex;
      flex-direction: column;
      justify-content: center;
    }

    & .second-column-top {
      grid-column-start: 2;
      grid-column-end: 3;
      grid-row-start: 1;
      grid-row-end: 2;
      min-height: calc((100vh - 210px) / 2);
    }
    & .second-column-bottom {
      grid-column-start: 2;
      grid-column-end: 3;
      grid-row-start: 2;
      grid-row-end: 3;
      max-height: 350px;
      min-height: calc((100vh - 210px) / 2);
    }
    & .second-column-full {
      grid-column-start: 2;
      grid-column-end: 3;
      grid-row-start: 1;
      grid-row-end: 3;
    }
    & .navigation {
      grid-column-start: 3;
      grid-column-end: 4;
      grid-row-start: 1;
      grid-row-end: 3;
    }
    & .navigation_fullScreen {
      grid-column-start: 2;
      grid-column-end: 3;
    }
  }
}
.navigation {
  border-left: 1px solid $main_dark_bg_color;
  & .nav-btn {
    padding-top: 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: 0.2s;
    & p {
      text-align: center;
      font-size: 12px;
    }
    & img {
      height: 48px;
    }
    &:hover {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateY(10px);
  opacity: 0;
}
.d-none {
  display: none !important;
}
.d-flex {
  display: flex !important;
}

@media screen and (max-width: 610px) {
  #playground {
    .playField {
      padding: 0px 10px;
      display: grid;
      grid-template-columns: 1fr;
      grid-template-rows: 1.6fr auto 88px;
      height: 100%;
      max-height: calc(100vh - 48px);
      row-gap: 0px;

      & .first-column-top {
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 1;
        grid-row-end: 2;
        overflow-x: scroll;
        width: calc(100vw - 20px);
      }
      & .first-column-bottom {
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 2;
        grid-row-end: 3;
        width: calc(100vw - 20px);
      }
      & .navigation {
        border-left: none;
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 3;
        grid-row-end: 4;
        width: 100%;
        display: flex;
        justify-content: space-around;
      }
      & .second-column-top,
      & .second-column-bottom,
      & .second-column-full {
        position: absolute;
        bottom: 0;
        left: 0;
      }
      & .mobile-fade {
        display: block !important;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.3);
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1000;
      }
      & .mobile-popup {
        z-index: 10000;
        backdrop-filter: blur(12px) saturate(100%);
        -webkit-backdrop-filter: blur(12px) saturate(100%);
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 16px 16px 0px 0px;
        padding: 1rem;
        box-sizing: border-box;
        width: 100%;
      }
    }
  }
}
</style>
