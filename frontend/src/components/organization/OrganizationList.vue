<template>
  <div
    class="organizations-list-column scrollable"
    style="scrollbar-gutter: unset"
  >
    <div
      class="normal-border-box organizations-list-item"
      v-for="organization in organizationsByUser"
      :key="organization.id"
    >
      {{ $t('organization.organization') }} "{{ organization.name }}"
      <a :href="'http://' + organization.subdomain + '.' + getDomainName">
        <br />
        {{ 'https://' + organization.subdomain + '.' + getDomainName }}
      </a>
    </div>
  </div>
</template>

<script>
import organizationsByUser from '@/graphql/queries/organizationsByUser.gql';

export default {
  name: 'OrganizationList',
  components: {},
  data() {
    return {
      organizationsByUser: {},
    };
  },
  computed: {
    getDomainName() {
      let hostName = location.host;
      return hostName.substring(
        hostName.lastIndexOf('.', hostName.lastIndexOf('.') - 1) + 1
      );
    },
  },
  apollo: {
    organizationsByUser: {
      query: organizationsByUser,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_variables.scss';

h2 {
  text-align: center;
}

.organizations-list-column {
  height: calc(100vh - 139px);
  overflow-y: auto;
}

.organizations-list-item {
  padding: 1rem;
  font-family: $primary_font;
  color: $dark_text_color;
  font-size: 14px;
  margin-bottom: 0.5rem;
  margin-right: 0.5rem;
}

.new-organization-btn {
  margin-bottom: 1rem;
  width: calc(100% - 0.5rem);
}

@media screen and (max-width: 810px) {
  .organizations-list-column {
    height: calc(50vh - 48px);
  }
}
</style>
