<template lang="pug">
div.mt-2.p-2.rounded-lg(:style="{backgroundColor: primaryColor}")
  div.p-2
    input.mr-2(type="checkbox" v-model="thisSelected" :id="identity")
    label(:for="identity") contain this team {{ selected }}
</template>

<script>
export default {
  name: "TeamDifficultySelector",
  props: [
    "teamName",
    "primaryColor",
    "secondaryColor",
    "maxDifficulty",
    "selected",
  ],
  emits: ["update:selected"],
  computed: {
    identity() {
      return this.teamName.replace(" ", "");
    },
    thisSelected: {
      get() {
        return this.selected;
      },
      set(value) {
        this.$emit("update:selected", value);
      },
    },
  },
};
</script>

<style scoped></style>
