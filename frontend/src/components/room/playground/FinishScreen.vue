<template>
  <div class="finish-screen scrollable">
    <div>
      <h2>{{ $t('room.roundFinishedHeader', { round: `R${roundKey}` }) }}</h2>

      <template v-if="isRoomOwner">
        <div class="next-round-btn">
          <SubmitButton :type="'bg-green'" @click="reStartRound">{{
            $t('room.reStartRoundButton', { nextRound: `R${roundKey + 1}` })
          }}</SubmitButton>
        </div>
      </template>
    </div>
    <h3 v-if="winnersFromCurrentRound != undefined">Призовые места</h3>
    <div class="place-box" v-if="winnersFromCurrentRound != undefined">
      <div
        class="place-card normal-border-box"
        :class="{
          'gold-border-box': userPlace == 'A_1',
          'silver-border-box': userPlace == 'A_2',
          'bronze-border-box': userPlace == 'A_3',
        }"
      >
        <div>
          <p>{{ $t('room.yourResult') }}</p>
        </div>
        <div class="place-text">
          {{ placeText(userPlace) }} ( {{ allComputedMonthsByCodeTotal }} )
        </div>
      </div>
    </div>
    <div class="place-box" v-if="winnersFromCurrentRound != undefined">
      <div class="places-row">
        <div
          class="place-card normal-border-box"
          :class="{
            'gold-border-box': winner.place == 'A_1',
            'silver-border-box': winner.place == 'A_2',
            'bronze-border-box': winner.place == 'A_3',
          }"
          v-for="winner in winnersFromCurrentRound"
          :key="winner.id"
        >
          <small>{{ $t('room.place') }}</small>
          <p class="place-text place-text-small">
            {{ placeText(winner.place) }}
          </p>
          <small>{{ $t('room.player.player') }}</small>
          <p>{{ winner.user.lastName }} {{ winner.user.firstName }}</p>
          <small>{{ $t('room.scores')}}</small>
          <p>{{ winner.result }}</p>
        </div>
      </div>
    </div>
    <div class="history-row">
      <template v-for="(monthKey, index) in monthKeys">
        <div class="history-row-item" :key="monthKey + '-' + index + '!div'">
          <small v-if="monthKey == null" :key="monthKey + '-' + index + '!'">{{
            $t('room.startMonth')
          }}</small>
          <small v-if="monthKey != null" :key="monthKey + '-' + index + '!!'"
            >{{ $t('room.month') }} №{{ monthKey }}</small
          >
          <FinishFunnelTable
            :computedChannelsByCode="computedDataForMonth(monthKey)"
            :channelsByCode="channelsByCode"
            :stagesByCode="stagesByCode"
            :key="'fft--' + index"
            :monthKey="monthKey"
          ></FinishFunnelTable>
          <FinishTurnChoices
            v-if="computedTurnForMonth(monthKey != null ? monthKey : 0) != null"
            :turn="computedTurnForMonth(monthKey != null ? monthKey : 0)"
            :monthKey="monthKey != null ? monthKey : 0"
            :key="'ftc--' + monthKey + '-' + index"
          ></FinishTurnChoices>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import isRoomOwner from '@/graphql/queries/rooms/isRoomOwner.gql';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import FinishFunnelTable from '@/components/room/playground/FinishFunnelTable.vue';
import reStartRound from '@/graphql/mutations/rooms/reStartRound.gql';
import turnsFromCurrentRound from '@/graphql/queries/rooms/turnsFromCurrentRound.gql';
import allComputedMonthsByCode from '@/graphql/queries/gameBoard/allComputedMonthsByCode.gql';
import allComputedMonthsByCodeTotal from '@/graphql/queries/gameBoard/allComputedMonthsByCodeTotal.gql';
import channelsByCode from '@/graphql/queries/gameBoard/channelsByCode.gql';
import stagesByCode from '@/graphql/queries/gameBoard/stagesByCode.gql';
import winnersFromCurrentRound from '@/graphql/queries/rooms/winnersFromCurrentRound.gql';
import FinishTurnChoices from '@/components/room/playground/FinishTurnChoices.vue';

export default {
  name: 'FinishScreen',
  components: {
    SubmitButton,
    FinishFunnelTable,
    FinishTurnChoices,
  },
  props: {
    roundKey: {
      type: Number,
      required: true,
    },
    roomCode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      monthKeys: [],
    };
  },
  computed: {
    userId() {
      return this.$store.state.userId;
    },
    userPlace() {
      let userRating = this.winnersFromCurrentRound.find(
        (el) => el.user.id == this.userId
      );
      if (userRating == null) {
        return '-';
      } else {
        return userRating.place;
      }
    },
  },
  apollo: {
    winnersFromCurrentRound: {
      query: winnersFromCurrentRound,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    channelsByCode: {
      query: channelsByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    stagesByCode: {
      query: stagesByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    isRoomOwner: {
      query: isRoomOwner,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    turnsFromCurrentRound: {
      query: turnsFromCurrentRound,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    allComputedMonthsByCode: {
      query: allComputedMonthsByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    allComputedMonthsByCodeTotal: {
      query: allComputedMonthsByCodeTotal,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
  },
  methods: {
    placeText(place) {
      switch (place) {
        case 'A_1':
          return this.$t('room.firstPlace');

        case 'A_2':
          return this.$t('room.secondPlace');

        case 'A_3':
          return this.$t('room.thirdPlace');

        default:
          return this.$t('room.notPrizePlace');
      }
    },
    reStartRound() {
      this.$apollo
        .mutate({
          mutation: reStartRound,
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
    computedDataForMonth(monthKey) {
      return this.allComputedMonthsByCode.filter(
        (el) => el.monthKey == monthKey
      );
    },
    computedTurnForMonth(monthKey) {
      return this.turnsFromCurrentRound.find((el) => el.month.key == monthKey);
    },
  },
  watch: {
    allComputedMonthsByCode() {
      this.$store.commit('CLEAN_CHOSEN_CARD');
      this.monthKeys = [
        ...new Set(this.allComputedMonthsByCode.map((el) => el.monthKey)),
      ].sort((a, b) => {
        if (a > b) return 1;
        if (b == null || a < b) return -1;
        return 0;
      });
      this.$apollo.queries.winnersFromCurrentRound.refresh();
    },
    allComputedMonthsByCodeTotal() {
      this.$store.commit('CLEAN_CHOSEN_CARD');
      this.monthKeys = [
        ...new Set(this.allComputedMonthsByCode.map((el) => el.monthKey)),
      ].sort((a, b) => {
        if (a > b) return 1;
        if (b == null || a < b) return -1;
        return 0;
      });
      this.$apollo.queries.winnersFromCurrentRound.refresh();
    },
  },
  mounted() {
    this.$root.$on('update', () => {
      this.$apollo.queries.allComputedMonthsByCode.refresh();
      this.$apollo.queries.allComputedMonthsByCodeTotal.refresh();
      this.$apollo.queries.winnersFromCurrentRound.refresh();
    });
  }
};
</script>

<style lang="scss" scoped>
.place-card {
  padding: 0.5rem;
}

.places-row {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin: 0.5rem auto !important;
}

.finish-screen {
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 1;
  grid-row-end: 3;
  overflow-y: auto;
}

.next-round-btn {
  margin-top: 16px;
  margin-bottom: 16px;
  position: sticky;
  top: 1rem;
  z-index: 1000;
}
.history-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;

  &-item {
    margin: auto;
    width: 100%;
  }
}
.place-box {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
  margin: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgb(48, 45, 86);

  & * {
    margin: auto;
  }
}
.place-text {
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;

  &-small {
    font-size: 1rem;
  }
}
</style>
