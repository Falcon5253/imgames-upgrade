<template>
  <div>
    <div>
      <img class="card-choices-arrow" src="@/assets/icons/arrow-down.svg" />
    </div>
    <small>{{ $t('room.step') }} №{{ monthKey + 1 }}</small>
    <div class="cards-row">
      <p v-if="turn.cardchoiceSet.length == 0">{{ $t('room.passStep') }}</p>
      <template v-for="(cardChoice, index) in turn.cardchoiceSet">
        <div
          class="card-box normal-border-box orange-border-box"
          :key="'M' + monthKey + '-' + cardChoice.id"
        >
          {{ cardChoice.card.header }}
        </div>
        <div
          v-if="index + 1 != turn.cardchoiceSet.length"
          class="card-plus"
          :key="'PLUS' + monthKey + '-' + cardChoice.id"
        >
          <div>+</div>
        </div>
      </template>
    </div>
    <div>
      <img class="card-choices-arrow" src="@/assets/icons/arrow-down.svg" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'FinishTurnChoices',
  props: {
    turn: {
      type: Object,
    },
    monthKey: {
      type: Number,
    },
  },
};
</script>

<style lang="scss" scoped>
.cards-row {
  display: flex;
}
.card-box {
  max-width: 200px;
  padding: 1rem;
}
.card-plus {
  display: flex;
  & > * {
    margin: auto 0.5rem;
  }
}
.card-choices-arrow {
  margin-top: 8px;
  height: 28px;
}
</style>
