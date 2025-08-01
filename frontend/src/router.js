import { userResource } from "@/data/user";
import { createRouter, createWebHistory } from "vue-router";
import { session } from "./data/session";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/pages/Home.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/frontend"),
  routes,
});

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn;
  try {
    await userResource.promise;
  } catch (error) {
    isLoggedIn = false;
  }

  if (to.name === "Login" && isLoggedIn) {
    next({ name: "Home" });
  } else if (to.name !== "Login" && !isLoggedIn) {
    window.location.href = "/login";
  } else {
    next();
  }
});

export default router;
