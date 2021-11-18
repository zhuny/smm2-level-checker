<template lang="pug">
div.mt-2.p-3.rounded-lg(:style="{backgroundColor: primaryColor}")
  h2.p-1 {{ teamName }}
  div.p-1
    input.mr-2(type="checkbox" v-model="thisSelected" :id="identity")
    label(:for="identity") contain this team {{ selected }}
  NumberRangeInput(
    :min-value="0"
    :max-value="10"
    v-model:range-start="rangeStart"
    v-model:range-end="rangeEnd"
  )
</template>

<script>
import NumberRangeInput from "@/components/input/NumberRangeInput";

export default {
  name: "TeamDifficultySelector",
  components: { NumberRangeInput },
  props: [
    "teamName",
    "primaryColor",
    "secondaryColor",
    "maxDifficulty",
    "selected",
    "rangeStart",
    "rangeEnd",
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
