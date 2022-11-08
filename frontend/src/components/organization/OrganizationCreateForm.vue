<template>
  <form @submit.prevent ref="organizationCreateForm">
    <TextInput
      :placeholder="$t('organization.name')"
      :disabled="formLoading"
      @input="
        newOrganization != undefined ? (newOrganization.name = $event) : ''
      "
    ></TextInput>
    <TextInput
      :placeholder="$t('organization.subdomain')"
      :disabled="formLoading"
      @input="newOrganization.subdomain = $event"
    ></TextInput>
    <TextInput
      :placeholder="$t('organization.prefix')"
      :disabled="formLoading"
      @input="newOrganization.prefix = $event"
    ></TextInput>
    <SubmitButton :disabled="formLoading" @click="createNewOrganization">
      {{ $t('buttons.create') }}
    </SubmitButton>
    <p>{{ test_data }}</p>
  </form>
</template>

<script>
import TextInput from '@/components/ui/TextInput.vue';
import SubmitButton from '@/components/ui/SubmitButton.vue';
import createOrganization from '@/graphql/mutations/organizations/createOrganization.gql';

export default {
  name: 'OrganizationCreateForm',
  components: {
    TextInput,
    SubmitButton,
  },
  data() {
    return {
      newOrganization: {
        name: '',
        subdomain: '',
        prefix: '',
      },
      formLoading: false,
      test_data: {},
    };
  },
  methods: {
    async createNewOrganization() {
      this.$store.commit('START_LOADING');
      this.formLoading = true;
      this.$apollo
        .mutate({
          mutation: createOrganization,
          variables: this.newOrganization,
        })
        .then((data) => {
          data = data.data;
          this.test_data = data;
          if (
            data.createOrganization.errors == null ||
            data.createOrganization.errors == undefined
          ) {
            if (
              data.createOrganization.organization.subdomain != null &&
              data.createOrganization.organization.subdomain != undefined
            ) {
              console.log(
                'subdomain',
                data.createOrganization.organization.subdomain
              );
            }
          }
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          this.formLoading = false;
          this.$store.commit('STOP_LOADING');
        });
    },
  },
};
</script>

<style lang="scss" scoped></style>
