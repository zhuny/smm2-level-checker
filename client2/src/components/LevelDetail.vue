<template lang="pug">
v-container
</template>

<script>
export default {
  name: "LevelDetail",
  data() {
    return {
      levelId: this.$route.params.levelId,
    };
  },
};
</script>
