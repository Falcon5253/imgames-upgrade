<template>
  <div class="container">
    <TopBar></TopBar>
    <div class="main-grid scrollable">
      <div class="rooms-list-column">
        <h2>{{ $t('room.roomsList') }}</h2>
        <RoomList></RoomList>
      </div>
      <div class="create-room">
        <CreateRoomView></CreateRoomView>
        <ConnectRoomView></ConnectRoomView>
      </div>
      <div class="organizations">
        <h2>{{ $t('headers.organizationList') }}</h2>
        <SubmitButton
          class="new-organization-btn"
          :type="'bg-outline'"
          @click="$router.push('/new')"
          >{{ $t('headers.newOrganizationBtn') }}</SubmitButton
        >
        <OrganizationList class="organizations-list"></OrganizationList>
      </div>
    </div>
  </div>
</template>

<script>
import { AUTH_PATH } from '@/pathVariables.js';

import OrganizationList from '@/components/organization/OrganizationList.vue';
import CreateRoomView from '@/components/room/CreateRoomView.vue';
import ConnectRoomView from '@/components/room/ConnectRoomView.vue';
import RoomList from '@/components/room/RoomsList.vue';
import TopBar from '@/components/ui/TopBar.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';

export default {
  name: 'Main',
  components: {
    OrganizationList,
    CreateRoomView,
    ConnectRoomView,
    RoomList,
    TopBar,
    SubmitButton,
  },
  data() {
    return {
      authPath: AUTH_PATH,
    };
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

h2 {
  text-align: center;
}
.new-organization-btn {
  width: 100%;
  margin-bottom: 4px;
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  column-gap: 1rem;
  height: calc(100vh - 48px);
  padding: 0 1rem;
  background: radial-gradient(
    52.5% 97.01% at 21.67% 20.17%,
    rgba(82, 110, 255, 0.25) 0%,
    rgba(249, 216, 167, 0.25) 89.06%
  );
}

@media screen and (max-width: 810px) {
  .main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 50vh 50vh;
    height: calc(100vh - 48px);

    & .rooms-list {
      grid-row-start: 1;
      grid-row-end: 2;
      grid-column-start: 2;
      grid-column-end: 3;
    }
    & .organizations-list {
      grid-row-start: 2;
      grid-row-end: 3;
      grid-column-start: 2;
      grid-column-end: 3;
      border-top: 1px solid $main_dark_bg_color;
    }
    & .create-room {
      grid-row-start: 1;
      grid-row-end: 3;
      grid-column-start: 1;
      grid-column-end: 2;
      display: flex;
      flex-direction: column;
      & * {
        margin: auto;
        width: 90%;
      }
    }
    & .organizations-list,
    & .create-room {
      height: calc(50vh - 24px);
    }
  }
}
@media screen and (max-width: 600px) {
  .main-grid {
    display: flex;
    flex-direction: column;
    overflow-y: auto;

    & .organizations {
      max-height: 300px;
    }

    & .organizations-list {
      height: 100%;
    }

    & .create-room {
      height: auto;
    }
  }
}
</style>
