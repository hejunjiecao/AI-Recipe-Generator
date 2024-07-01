import Vue from 'vue';
import VueRouter from 'vue-router';
import UploadView from '../components/UploadView.vue';
import Recipe from '../components/Recipe.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'UploadView',
    component: UploadView,
  },
  {
    path: '/generate',
    name: 'Recipe',
    component: Recipe,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
