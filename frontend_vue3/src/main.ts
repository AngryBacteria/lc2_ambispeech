/* eslint-disable vue/no-reserved-component-names */
/* eslint-disable vue/multi-word-component-names */
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

//Create vue app
const app = createApp(App);

// Load plugins
app.use(createPinia());
app.use(router);

// Prime vue config
import '@/assets/main.css';
import 'primevue/resources/themes/soho-dark/theme.css';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';

// Prime vue components
import Button from 'primevue/button';
import FileUpload from 'primevue/fileupload';
import ProgressBar from 'primevue/progressbar';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import Slider from 'primevue/slider';
import InputNumber from 'primevue/inputnumber';
import Menubar from 'primevue/menubar';
import ToggleButton from 'primevue/togglebutton';
import Toast from 'primevue/toast';
import ProgressSpinner from 'primevue/progressspinner';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';

app.use(PrimeVue);
app.use(ToastService);
app.component('Button', Button);
app.component('FileUpload', FileUpload);
app.component('ProgressBar', ProgressBar);
app.component('Accordion', Accordion);
app.component('AccordionTab', AccordionTab);
app.component('Textarea', Textarea);
app.component('Dropdown', Dropdown);
app.component('Slider', Slider);
app.component('InputNumber', InputNumber);
app.component('Menubar', Menubar);
app.component('ToggleButton', ToggleButton);
app.component('Toast', Toast);
app.component('ProgressSpinner', ProgressSpinner);
app.component('Dialog', Dialog);
app.component('InputText', InputText);

app.mount('#app');
