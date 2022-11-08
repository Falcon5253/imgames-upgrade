<template>
  <div class="normal-border-box create-room-form green-border-box">
    <TextInput
      :label="$t('room.moneyPerMonth')"
      :name="'moneyPerMonth'"
      :placeholder="$t('room.moneyPerMonth')"
      :disabled="formLoading"
      :type="'number'"
      :predefined="defaultRoomSettings.moneyPerMonthDefault"
      @input="newRoom != undefined ? (newRoom.moneyPerMonth = +$event) : ''"
    ></TextInput>
    <TextInput
      :label="$t('room.numberOfTurns')"
      :name="'numberOfTurns'"
      :placeholder="$t('room.numberOfTurns')"
      :disabled="formLoading"
      :predefined="defaultRoomSettings.numberOfTurnsDefault"
      :type="'number'"
      @input="
        defaultRoomSettings != undefined
          ? (newRoom.numberOfTurns = +$event)
          : ''
      "
    ></TextInput>
    <DropdownSelector
      :label="$t('room.flow')"
      :name="'flow'"
      :options="flowsArray"
      :predefined="predefinedFlow"
      @input="newRoom != undefined ? (newRoom.flowId = +$event) : ''"
    ></DropdownSelector>
    <SubmitButton
      :type="'bg-green'"
      :disabled="formLoading"
      @click="createNewRoom"
    >
      {{ $t('buttons.create') }}
    </SubmitButton>
  </div>
</template>

<script>
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import defaultRoomSettings from '@/graphql/queries/rooms/defaultRoomSettings.gql';
import createRoom from '@/graphql/mutations/rooms/createRoom.gql';
import roomsInOrganization from '@/graphql/queries/rooms/roomsInOrganization.gql';
import { ROOMS_ROOT_PATH } from '@/pathVariables';
import DropdownSelector from '@/components/ui/DropdownSelector.vue';

export default {
  name: 'CreateRoomForm',
  components: {
    TextInput,
    SubmitButton,
    DropdownSelector,
  },
  apollo: {
    defaultRoomSettings: {
      query: defaultRoomSettings,
      variables() {
        return {
          subdomain: this.subdomain,
        };
      },
      update: function (data) {
        let settings = data.defaultRoomSettings;
        return settings;
      },
    },
  },
  data() {
    return {
      formLoading: false,
      newRoom: {
        moneyPerMonth: '',
        numberOfTurns: '',
        flowId: 0,
      },
      defaultRoomSettings: {},
    };
  },
  computed: {
    subdomain() {
      return this.$store.state.subdomain;
    },
    flowsArray() {
      if (this.defaultRoomSettings != undefined) {
        if (this.defaultRoomSettings.flowsInOrganization != undefined) {
          return this.defaultRoomSettings.flowsInOrganization.map((el) => {
            return { value: el.id, label: el.title };
          });
        }
      }
      return [];
    },
    predefinedFlow() {
      if (this.defaultRoomSettings != undefined) {
        if (this.defaultRoomSettings.flowsInOrganization != undefined) {
          return this.defaultRoomSettings.flowsInOrganization[0].id;
        }
      }
      return 0;
    },
  },
  methods: {
    // TODO: add flow selection into mutation
    createNewRoom() {
      this.newRoom.subdomain = this.subdomain;
      this.$apollo
        .mutate({
          mutation: createRoom,
          variables: this.newRoom,
          update: (store, { data: { createRoom } }) => {
            const data = store.readQuery({
              query: roomsInOrganization,
              variables: { subdomain: this.subdomain },
            });

            let roomsInOrganizationCopy = data.roomsInOrganization.slice();

            roomsInOrganizationCopy.push(createRoom.room);

            store.writeQuery({
              query: roomsInOrganization,
              variables: { subdomain: this.subdomain },
              data: { roomsInOrganization: roomsInOrganizationCopy },
            });
          },
        })
        .then((data) => {
          this.$router.push(
            ROOMS_ROOT_PATH + '/' + data.data.createRoom.room.code.toUpperCase()
          );
        })
        .catch();
    },
  },
};
</script>

<style lang="scss" scoped>
.create-room-form {
  padding: 1rem;
  & .user-input {
    & input {
      width: 100%;
      box-sizing: border-box;
    }
  }
  & .user-input-dropdown {
    & select {
      width: 100%;
      box-sizing: border-box;
    }
  }
  & button {
    width: 100%;
  }
}
</style>
