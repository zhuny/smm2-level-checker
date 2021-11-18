<template lang="pug">
div
  div.p-2(:style="{backgroundColor: primaryColor}")
    div.p-2
      input.mr-2(type="checkbox")
      label contain this team
</template>

<script>
export default {
  name: "TeamDifficultySelector",
  props: ["teamName", "primaryColor", "secondaryColor", "maxDifficulty"],
};
</script>

<style scoped></style>
