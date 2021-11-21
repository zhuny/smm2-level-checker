import {createRouter, createWebHistory} from "vue-router";
import RandomPick from "@/views/RandomPick";

const routes = [
  {
    path: "/",
    name: "Home",
    component: RandomPick,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
