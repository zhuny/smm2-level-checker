import { createRouter, createWebHistory } from "vue-router";
import RandomPick from "@/views/RandomPick";
import OneLevel from "@/views/OneLevel";

const routes = [
  {
    path: "/",
    name: "Home",
    component: RandomPick,
  },
  {
    path: "/level/:levelId",
    name: "OneLevel",
    component: OneLevel,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
