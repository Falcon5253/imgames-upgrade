<template>
  <div>
    <SubmitButton
      v-if="!isDisabled"
      class="w-100"
      @click="sendCardChoice"
      :type="'bg-green'"
      :disabled="isDisabled"
      >{{ $t('room.card.send') }}</SubmitButton
    >
    <SubmitButton
      v-else
      class="w-100"
      @click="sendCardChoice"
      :type="'bg-disabled'"
      :disabled="isDisabled"
      >{{ $t('room.card.send') }}</SubmitButton
    >
  </div>
</template>

<script>
import SubmitButton from '@/components/ui/SubmitButton.vue';
import writeTurn from '@/graphql/mutations/rooms/writeTurn.gql';
import cardsByCode from '@/graphql/queries/gameBoard/cardsByCode.gql';

export default {
  name: 'WriteTurnPanel',
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    selectedCardsId: {
      type: Array,
      default: [],
    },
  },
  components: {
    SubmitButton,
  },
  data() {
    return {
      isLoading: false,
    };
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
  },
  computed: {
    roomCode() {
      return this.$route.params.roomCode;
    },
    isDisabled() {
      return this.disabled || this.isLoading;
    },
  },
  methods: {
    sendCardChoice() {
      this.isLoading = true;
      this.$apollo
        .mutate({
          mutation: writeTurn,
          variables: {
            code: this.roomCode,
            cardsId: this.selectedCardsId,
          },
          update: (store, { data: { writeTurn } }) => {
            // console.log('DATA FOR CACHE', writeTurn);
          },
        })
        .then(() => {})
        .catch((e) => {})
        .finally(() => {
          let chosenCards = this.cardsByCode.filter((el) => {
            return this.selectedCardsId.includes(+el.id);
          });
          // console.log(chosenCards);
          for (let index = 0; index < chosenCards.length; index++) {
            const card = chosenCards[index];
            console.log(chosenCards[index]);
            this.$store.commit('ADD_CHOSEN_CARD', card);
          }
          this.$emit('clean');
          this.isLoading = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
