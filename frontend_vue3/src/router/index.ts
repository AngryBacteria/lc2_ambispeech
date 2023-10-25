import HomePageVue from '@/views/HomePage.vue';
import SettingsPageVue from '@/views/SettingsPage.vue';
import TextAnalyzer from '@/views/AnalyzingPage.vue';
import { createRouter, createWebHistory } from 'vue-router';
import FileRecorderVue from '@/components/FileRecorder.vue';
import FileUploaderVue from '@/components/FileUploader.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/upload',
      component: HomePageVue,
      children: [
        {
          path: '/record',
          name: 'record',
          component: FileRecorderVue
        },
        {
          path: '/upload',
          name: 'file',
          component: FileUploaderVue
        }
      ]
    },
    {
      path: '/einstellungen',
      component: SettingsPageVue
    },
    {
      path: '/analyze',
      component: TextAnalyzer
    }
  ]
});

export default router;
