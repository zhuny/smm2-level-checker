<template>
  <RandomPick />
</template>

<script>
import { defineComponent } from "vue";

// Components
import RandomPick from "../components/RandomPick.vue";

export default defineComponent({
  name: "HomeView",

  components: {
    RandomPick,
  },
});
</script>
