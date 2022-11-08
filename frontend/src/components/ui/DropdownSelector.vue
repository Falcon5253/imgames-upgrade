<template>
  <div class="user-input-dropdown">
    <label :for="name">{{ label }}</label>
    <select
      :id="name"
      :name="name"
      :disabled="disabled"
      v-model="inputModel"
      @input="sendInput"
      @change="sendInput"
    >
      <option
        :value="option.value"
        :key="index"
        v-for="(option, index) in options"
        :selected="option.value == predefined"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'DropdownSelector',
  data() {
    return {
      inputModel: '',
    };
  },
  props: {
    options: {
      type: Array,
      required: true,
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
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

label,
select {
  font-family: $primary_font;
}
label {
  margin-bottom: 0.5rem;
}
select {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
}
.user-input-dropdown {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}
</style>
