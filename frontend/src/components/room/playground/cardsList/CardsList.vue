<template>
  <div id="cards-panel">
    <h3>{{ $t('room.card.cardsList') }}</h3>
    <WriteTurnPanel
      class="write-turn-panel"
      :disabled="!canDoStepNowByCode"
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
import Card from '@/components/room/playground/cardsList/Card.vue';
import WriteTurnPanel from '@/components/room/playground/cardsList/WriteTurnPanel.vue';

export default {
  name: 'CardsList',
  components: {
    Card,
    WriteTurnPanel,
  },
  apollo: {
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
      }
    },
    removeChoice(cardId) {
      if (this.isSelected(cardId)) {
        this.selectedCardsId = this.selectedCardsId.filter(
          (el) => +el !== +cardId
        );
      }
    },
    isSelected(cardId) {
      return +this.selectedCardsId.findIndex((el) => +el == +cardId) !== -1;
    },
  },
};
</script>

<style lang="scss" scoped>
#cards-panel {
  display: flex;
  flex-direction: column;
  min-height: 300px;

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
