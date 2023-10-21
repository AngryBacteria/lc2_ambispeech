/* eslint-disable vue/no-reserved-component-names */
/* eslint-disable vue/multi-word-component-names */
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

import '@/assets/main.css';
//import 'primevue/resources/themes/lara-dark-indigo/theme.css'
//import 'primevue/resources/themes/bootstrap4-dark-blue/theme.css'
//import 'primevue/resources/themes/bootstrap4-dark-purple/theme.css'
//import 'primevue/resources/themes/md-dark-indigo/theme.css'
//import 'primevue/resources/themes/md-dark-deeppurple/theme.css'
//import 'primevue/resources/themes/mdc-dark-indigo/theme.css'
//import 'primevue/resources/themes/mdc-dark-deeppurple/theme.css
//import 'primevue/resources/themes/lara-light-teal/theme.css'
//import 'primevue/resources/themes/lara-dark-blue/theme.css'
//import 'primevue/resources/themes/lara-dark-purple/theme.css'
//import 'primevue/resources/themes/lara-dark-teal/theme.css'
import 'primevue/resources/themes/soho-dark/theme.css';
//import 'primevue/resources/themes/viva-dark/theme.css'

import PrimeVue from 'primevue/config';
import Button from 'primevue/button';
import FileUpload from 'primevue/fileupload';
import ProgressBar from 'primevue/progressbar';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import Textarea from 'primevue/textarea';
import Toolbar from 'primevue/toolbar';
import Dropdown from 'primevue/dropdown';
import Slider from 'primevue/slider';
import InputNumber from 'primevue/inputnumber';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.use(PrimeVue);
app.component('Button', Button);
app.component('FileUpload', FileUpload);
app.component('ProgressBar', ProgressBar);
app.component('Accordion', Accordion);
app.component('AccordionTab', AccordionTab);
app.component('Textarea', Textarea);
app.component('Toolbar', Toolbar);
app.component('Dropdown', Dropdown);
app.component('Slider', Slider);
app.component('InputNumber', InputNumber);

app.mount('#app');
