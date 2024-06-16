import Vue from 'vue';
import VueRouter from 'vue-router';
import UploadView from '../components/UploadView.vue';

Vue.use(VueRouter);

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'UploadView',
            component: UploadView,
        },
    ],
});