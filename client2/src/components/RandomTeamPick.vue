<template lang="pug">
v-card(
  :color="primaryColor"
)
  v-card-title {{ teamName }}
  v-card-text
    v-checkbox(
      v-model="selected"
      label="Contain this team"
    )
    v-range-slider(
      :max="rangeEnd"
      :min="rangeStart"
      v-model="rangeSlider"
      step="0.5"
    )
</template>

<script>
export default {
  name: "RandomTeamPick",
  data() {
    return {
      insideRangeStart: this.selectedRangeStart,
      insideRangeEnd: this.selectedRangeEnd,
    };
  },
  props: {
    teamName: {
      type: String,
      required: true,
    },
    primaryColor: {
      type: String,
      default: "#ffffff",
    },
    selected: {
      type: Boolean,
      default: false,
    },
    rangeStart: {
      type: Number,
      default: 0,
    },
    rangeEnd: {
      type: Number,
      default: 10,
    },
    selectedRangeStart: {
      type: Number,
      default: 0,
    },
    selectedRangeEnd: {
      type: Number,
      default: 1,
    },
  },
  emits: ["update:selectedRangeStart", "update:selectedRangeEnd"],
  computed: {
    rangeSlider: {
      get() {
        return [this.insideRangeStart, this.insideRangeEnd];
      },
      set(v) {
        this.insideRangeStart = v[0];
        this.insideRangeEnd = v[1];
        this.$emit("update:selectedRangeStart", v[0]);
        this.$emit("update:selectedRangeEnd", v[1]);
      },
    },
  },
};
</script>
