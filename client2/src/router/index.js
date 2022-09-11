import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LevelDetailView from "../views/LevelDetailView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/level/:levelId",
      name: "LevelDetail",
      component: LevelDetailView,
    },
  ],
});

export default router;
