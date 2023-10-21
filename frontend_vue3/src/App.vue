<script setup lang="ts"></script>

<template>
  <Toolbar>
    <template #start>
      <Button
        icon="pi pi-home"
        rounded
        aria-label="home"
        link
        size="large"
        @click="$router.push('/')"
      />
    </template>
    <template #center>
      <h1 style="margin: 0">Ambient Speech Recognition</h1>
    </template>
    <template #end>
      <Button
        icon="pi pi-cog"
        rounded
        aria-label="settings"
        link
        size="large"
        @click="$router.push('/einstellungen')"
      />
    </template>
  </Toolbar>
  <Suspense>
    <router-view></router-view>
  </Suspense>
</template>

<style scoped>
.p-toolbar {
  padding: 0.5rem;
  margin-bottom: 2rem;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
