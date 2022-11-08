<template>
  <div class="user-input">
    <label :for="name" :class="{ 'error-message': isAnyError }">{{
      label
    }}</label>
    <input
      :id="name"
      :name="name"
      :type="type"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      :disabled="disabled"
      v-model="inputModel"
      @input="sendInput"
      @keyup.enter="sendEnter"
      :class="{ 'error-input': isAnyError }"
    />
    <div class="errors">
      <span class="error-message" v-if="isRequiredError">{{
        $t('textInput.requiredError')
      }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextInput',
  data() {
    return {
      inputModel: '',
    };
  },
  props: {
    placeholder: {
      type: String,
      required: true,
    },
    autocomplete: {
      type: String,
      default: 'false',
    },
    type: {
      type: String,
      default: 'text',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    predefined: {
      type: undefined,
      default: '',
    },
    label: {
      type: String,
    },
    name: {
      type: String,
    },
    // isRequired: {
    //   type: Boolean,
    //   default: false,
    // },
    isAnyError: {
      type: Boolean,
      default: false,
    },
    isRequiredError: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    predefined(newValue) {
      this.inputModel = newValue;
      this.sendInput();
    },
  },
  methods: {
    sendInput() {
      this.$emit('input', this.inputModel);
      if (this.$v != undefined) this.$v.inputModel.$touch();
    },
    sendEnter() {
      this.$emit('enter');
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

label,
input {
  font-family: $primary_font;
  color: $dark_text_color;
}
input {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  min-height: 40px;
  box-sizing: border-box;
}
.user-input {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
.errors {
  & span {
    font-size: 14px;
    margin-bottom: 0.5rem;
  }
}
</style>
