import HomePageVue from '@/views/HomePage.vue';
import SettingsPageVue from '@/views/SettingsPage.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomePageVue
    },
    {
      path: '/einstellungen',
      component: SettingsPageVue
    }
  ]
});

export default router;
