<template>
  <Toast label="sticky" />
  <Menubar :model="items">
    <template #end>
      <div class="branding">
        <img
          alt="logo"
          src="./assets/ambispeech_logo_v1.png"
          height="40"
          style="margin-right: 1rem; cursor: pointer"
          @click="$router.push('/upload')"
        />
        <p>Ambient Speech Recognition</p>
      </div>
    </template>
    <template #item="{ label, item, props }">
      <router-link v-slot="routerProps" :to="item.route" custom>
        <a :href="routerProps.href" v-bind="props.action" @click="routerProps.navigate">
          <span v-bind="props.icon" :class="{ 'router-link-active': routerProps.isActive }" />
          <span v-bind="props.label" :class="{ 'router-link-active': routerProps.isActive }">{{
            label
          }}</span>
        </a>
      </router-link>
    </template>
  </Menubar>
  <Suspense>
    <router-view></router-view>
  </Suspense>
</template>

<script setup lang="ts">
import { ref } from 'vue';

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
    label: 'Analysieren',
    icon: 'pi pi-eye',
    route: '/analyze'
  },
  {
    label: 'Einstellungen',
    icon: 'pi pi-cog',
    route: '/einstellungen'
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
