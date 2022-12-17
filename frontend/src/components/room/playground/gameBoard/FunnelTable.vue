<template>
  <table cellspacing="0" class="funnel-table normal-border-box">
    <TableHead :stages="stagesByCode"></TableHead>
    <TableBody
      :stages="stagesByCode"
      :channels="channelsByCode"
      :data="bodyData"
    ></TableBody>
    <TableFooter :stages="stagesByCode" :data="footerData"></TableFooter>
  </table>
</template>

<script>
import channelsByCode from '@/graphql/queries/gameBoard/channelsByCode.gql';
import stagesByCode from '@/graphql/queries/gameBoard/stagesByCode.gql';
import computedChannelsByCode from '@/graphql/queries/gameBoard/computedChannelsByCode.gql';
import computedChannelsByCodeUpdated from '@/graphql/subscriptions/rooms/computedChannelsByCodeUpdated.gql';

import TableBody from '@/components/room/playground/gameBoard/TableBody.vue';
import TableFooter from '@/components/room/playground/gameBoard/TableFooter.vue';
import TableHead from '@/components/room/playground/gameBoard/TableHead.vue';

export default {
  name: 'FunnelTable',
  components: {
    TableHead,
    TableBody,
    TableFooter,
  },
  apollo: {
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
    computedChannelsByCode: {
      query: computedChannelsByCode,
      variables() {
        return {
          code: this.roomCode,
        };
      },
      subscribeToMore: {
        document: computedChannelsByCodeUpdated,
        variables() {
          return {
            code: this.roomCode,
            userId: this.userId,
          };
        },
        updateQuery: (previousResult, { subscriptionData }) => {
          let newData = {
            computedChannelsByCode:
              subscriptionData.data.computedChannelsByCodeUpdated,
          };
          return newData;
        },
      },
    },
  },
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
  watch: {
    computedChannelsByCode: {
      handler() {
        this.$root.$emit("refreshRound");
      },
      immediate: true,
    }
  }
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
