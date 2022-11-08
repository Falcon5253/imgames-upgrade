<template>
  <div class="effects-box">
    <h3>{{ $t('room.player.effectsList') }}</h3>
    <div class="effects-list scrollable">
      <p v-if="chosenCards.length == 0">Эффекты отсутствуют</p>
      <template v-for="(effect, index) in chosenCards">
        <div class="effect normal-border-box orange-border-box" :key="index">
          <div class="header-column" style="display: flex">
            <div style="margin: auto">
              {{ effect.header }}
            </div>
          </div>
          <div class="count-column">
            <div>
              <small>{{ $t('room.player.application') }}</small>
            </div>
            <div style="text-align: right">
              {{ effect.count }}
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EffectsList',
  computed: {
    chosenCards() {
      return this.$store.state.chosenCards;
    },
  },
};
</script>

<style lang="scss" scoped>
.effects-box {
  & .effects-list {
    height: 99%;
    & .effect {
      padding: 0.5rem;
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
    }
  }
}
@media screen and (max-width: 610px) {
  .effects-box {
    & .effects-list {
      height: 294px;
    }
  }
}
</style>
