<template>
  <table
    cellspacing="0"
    class="funnel-table normal-border-box orange-border-box"
  >
    <TableHead :stages="stagesByCode" :monthKey="monthKey"></TableHead>
    <TableBody
      :stages="stagesByCode"
      :channels="channelsByCode"
      :data="bodyData"
      :monthKey="monthKey"
    ></TableBody>
    <TableFooter
      :stages="stagesByCode"
      :data="footerData"
      :monthKey="monthKey"
    ></TableFooter>
  </table>
</template>

<script>
// import computedChannelsByCode from '@/graphql/queries/gameBoard/computedChannelsByCode.gql';
// import computedChannelsByCodeUpdated from '@/graphql/subscriptions/rooms/computedChannelsByCodeUpdated.gql';

import TableBody from '@/components/room/playground/gameBoard/TableBody.vue';
import TableFooter from '@/components/room/playground/gameBoard/TableFooter.vue';
import TableHead from '@/components/room/playground/gameBoard/TableHead.vue';

export default {
  name: 'FinishFunnelTable',
  props: {
    computedChannelsByCode: {
      type: Array,
    },
    channelsByCode: {
      type: undefined,
    },
    stagesByCode: {
      type: undefined,
    },
    monthKey: {
      type: undefined,
    },
  },
  components: {
    TableHead,
    TableBody,
    TableFooter,
  },
  // apollo: {
  // computedChannelsByCode: {
  //   query: computedChannelsByCode,
  //   variables() {
  //     return {
  //       code: this.roomCode,
  //     };
  //   },
  //   subscribeToMore: {
  //     document: computedChannelsByCodeUpdated,
  //     variables() {
  //       return {
  //         code: this.roomCode,
  //         userId: this.userId,
  //       };
  //     },
  //     updateQuery: (previousResult, { subscriptionData }) => {
  //       let newData = {
  //         computedChannelsByCode:
  //           subscriptionData.data.computedChannelsByCodeUpdated,
  //       };
  //       return newData;
  //     },
  //   },
  // },
  // },
  computed: {
    userId() {
      return this.$store.state.userId;
    },
    roomCode() {
      return this.$route.params.roomCode;
    },
    footerData() {
      let dataArray = this.computedChannelsByCode.filter((el) => el.isTotal);
      if (dataArray[0] != undefined) {
        if (dataArray[0].data != undefined) {
          return dataArray[0].data;
        }
      }
      return [];
    },
    bodyData() {
      let dataArray = this.computedChannelsByCode.filter((el) => !el.isTotal);
      return dataArray;
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_variables.scss';

table.funnel-table {
  padding: 8px;

  & tr {
    border: 0px;

    & td,
    & th {
      border: 0px;
      border-bottom: 1px solid #000000;
      font-family: $primary_font;
      color: $dark_text_color;
    }

    & td:not(:first-child),
    & th:not(:first-child) {
      text-align: center;
    }
  }
}
</style>
