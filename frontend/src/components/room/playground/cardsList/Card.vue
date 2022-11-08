<template>
  <div class="normal-border-box card">
    <div class="selected-icon" v-if="selected">
      <img src="@/assets/icons/check.svg" />
    </div>
    <div class="top-part">
      <div class="card-header">
        <h4>{{ data.header }}</h4>
      </div>
      <div class="card-description">
        <p>{{ data.shortDescription }}</p>
      </div>
    </div>
    <div class="bottom-part">
      <p class="cost">{{ data.cost }} ₽</p>
      <SubmitButton
        class="w-100"
        :type="'bg-blue'"
        :disabled="canNotChoose()"
        @click="emitSelection()"
        v-if="!selected"
        >{{ $t('room.card.chooseCard') }}</SubmitButton
      >
      <SubmitButton
        class="w-100"
        :type="'bg-blue'"
        :disabled="canNotChoose()"
        @click="emitDeselect()"
        v-else
        >{{ $t('room.card.deselectCard') }}</SubmitButton
      >
    </div>
  </div>
</template>

<script>
import SubmitButton from '@/components/ui/SubmitButton.vue';

export default {
  name: 'Card',
  components: {
    SubmitButton,
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
    selected: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    emitSelection() {
      this.$emit('select', this.data.id);
    },
    emitDeselect() {
      this.$emit('deselect', this.data.id);
    },
    canNotChoose() {
      return this.disabled;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

.w-100 {
  width: 100%;
}

.card {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
  width: 190px;
  min-width: 190px;
  // height: 230px;
  margin-right: 10px;
  position: relative;

  & .selected-icon {
    position: absolute;
    right: 8px;
    top: 8px;
    z-index: 1000;
    & img {
      height: 28px;
    }
  }
}

p {
  font-family: $primary_font;
  font-size: 14px;
}

h4,
p {
  color: $dark_text_color;
  margin: 0;
}

h4,
p.cost {
  font-family: $primary_font;
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
}

.card-header,
.card-description {
  margin-bottom: 8px;
}
.card-header {
  height: 70px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
</style>
