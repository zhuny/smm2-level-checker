<template>
  <LevelDetail />
</template>

<script>
import { defineComponent } from "vue";

// Components
import LevelDetail from "../components/LevelDetail.vue";

export default defineComponent({
  name: "LevelDetailView",

  components: {
    LevelDetail,
  },
});
</script>
