<template>
  <div id="cards-panel">
    <div class="cards-context">
      <h3 class="cards-title">{{ $t('room.card.cardsList') }}</h3>
      <p class="current-budget">Оставшийся бюджет: {{ balance }} / {{ getMoneyPerMonth() }}</p>
    </div>
    <WriteTurnPanel
      class="write-turn-panel"
      :disabled="balance < 0"
      :selectedCardsId="selectedCardsId"
      @clean="selectedCardsId = []"
    ></WriteTurnPanel>
    <div class="cards-list scrollable">
      <Card
        v-for="card in cardsByCode"
        :key="card.id"
        :data="card"
        :selected="isSelected(card.id)"
        :disabled="!canDoStepNowByCode"
        @select="addChoice($event)"
        @deselect="removeChoice($event)"
      ></Card>
    </div>
  </div>
</template>

<script>
import cardsByCode from '@/graphql/queries/gameBoard/cardsByCode.gql';
import canDoStepNowByCode from '@/graphql/queries/gameBoard/canDoStepNowByCode.gql';
import roomByCode from '@/graphql/queries/rooms/roomByCode.gql';
import Card from '@/components/room/playground/cardsList/Card.vue';
import WriteTurnPanel from '@/components/room/playground/cardsList/WriteTurnPanel.vue';

export default {
  name: 'CardsList',
  components: {
    Card,
    WriteTurnPanel,
  },
  apollo: {
    roomByCode: {
      query: roomByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    cardsByCode: {
      query: cardsByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
    canDoStepNowByCode: {
      query: canDoStepNowByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
    },
  },
  data() {
    return {
      selectedCardsId: [],
      balance: 0,
      balanceIsPositive: true,
    };
  },
  computed: {
    roomCode() {
      return this.$route.params.roomCode;
    },
  },
  methods: {
    addChoice(cardId) {
      if (!this.isSelected(cardId)) {
        this.selectedCardsId.push(+cardId);
        this.countBalance();
        console.log(this.balanceIsPositive());
      }
    },
    removeChoice(cardId) {
      if (this.isSelected(cardId)) {
        this.selectedCardsId = this.selectedCardsId.filter(
          (el) => {
            return el != cardId;
          }
        );
        this.countBalance();
        console.log(this.balanceIsPositive());
      }
    },
    isSelected(cardId) {
      return +this.selectedCardsId.findIndex((el) => +el == +cardId) !== -1;
    },
    countBalance() {
      var expenses = 0;
      this.selectedCardsId.forEach(id => {
        this.cardsByCode.forEach(card => {
          if(card.id == id) {
            expenses = expenses + card.cost;
          };
        });
      });
      this.balance = this.getMoneyPerMonth() - expenses;
    },
    getMoneyPerMonth() {
      return this.roomByCode.moneyPerMonth;
    },
  },
  updated() {
    this.countBalance();
    this.checkBalance();
  },
};
</script>

<style lang="scss" scoped>
#cards-panel {
  display: flex;
  flex-direction: column;
  min-height: 300px;

  & .cards-context {
    display: flex;
  }

  & .cards-title {
    width: 50%;
  }

  & .current-budget {
    width: 50%;
    text-align: right;
  }

  & .cards-list {
    width: 100%;
    overflow-y: hidden;
    overflow-x: auto;
    display: flex;
    padding-bottom: 0.5rem;
    max-width: 70vw;
    max-height: 300px;
  }

  & .write-turn-panel {
    margin: 0 0 0.5rem 0;
  }
}
@media screen and (max-width: 610px) {
  h3 {
    display: none;
  }
  #cards-panel {
    & .cards-list {
      max-width: 100vw;
    }
  }
  .write-turn-panel {
    margin-top: 0.5rem;
  }
}
</style>
