<template>
  <Toast label="sticky" />
  <SessionDialog />
  <DynamicDialog />

  <Menubar :model="items">
    <template #end>
      <div class="branding" @click="$router.push('/transcribe/upload')" style="cursor: pointer">
        <img alt="logo" src="/ambispeech_logo_v1.png" height="40" style="margin-right: 1rem" />
        <p>Ambient Speech Recognition</p>
      </div>
    </template>
    <template #item="{ item, props, hasSubmenu }">
      <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
        <a v-ripple :href="href" v-bind="props.action" @click="navigate">
          <span :class="[item.icon, { 'router-link-active': href == $route.fullPath }]" />
          <span
            :class="{ 'router-link-active': href == $route.fullPath }"
            style="margin-left: 0.5rem"
            >{{ item.label }}</span
          >
        </a>
      </router-link>
      <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
        <span :class="item.icon" />
        <span style="margin-left: 0.5rem">{{ item.label }}</span>
        <span v-if="hasSubmenu" class="pi pi-fw pi-angle-down" style="margin-left: 0.5rem" />
      </a>
    </template>
  </Menubar>
  <Suspense>
    <router-view></router-view>
  </Suspense>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SessionDialog from './components/SessionDialog.vue';
import { useUserStore } from './stores/user';

const store = useUserStore();

const items = ref([
  {
    label: 'Datei analysieren',
    icon: 'pi pi-fw pi-upload',
    route: '/transcribe/upload'
  },
  {
    label: 'Echtzeit Aufnahme',
    icon: 'pi pi-microphone',
    route: '/transcribe/record'
  },
  {
    label: 'Einstellungen',
    icon: 'pi pi-cog',
    route: '/einstellungen'
  },
  {
    label: 'Session',
    icon: 'pi pi-sign-out',
    items: [
      {
        label: 'Patient wechseln',
        command: () => {
          store.patient = null;
        }
      },
      {
        label: 'Abmelden',
        command: () => {
          store.patient = null;
          store.practitioner = null;
        }
      }
    ]
  }
]);
</script>

<style scoped>
.p-menubar {
  padding: 0.5rem;
  margin-bottom: 2rem;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.router-link-active {
  color: var(--primary-color);
}

.branding {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
