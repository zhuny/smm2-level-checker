<template lang="pug">
v-card(
  :color="primaryColor"
)
  v-card-title {{ teamName }}
  v-card-text
    v-checkbox(
      v-model="isSelected"
      label="Contain this team"
      density="compact"
    )
    v-range-slider(
      v-if="selected"
      :max="rangeEnd"
      :min="rangeStart"
      v-model="rangeSlider"
      step="0.5"
      density="compact"
    )
      template(v-slot:prepend)
        v-avatar(
          v-text="insideRangeStart"
          size="x-small"
        )
      template(v-slot:append)
        v-avatar(
          v-text="insideRangeEnd"
          size="x-small"
        )
</template>

<script>
export default {
  name: "RandomTeamPick",
  data() {
    return {
      insideRangeStart: this.selectedRangeStart,
      insideRangeEnd: this.selectedRangeEnd,
      insideSelected: this.selected,
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
  emits: [
    "update:selectedRangeStart",
    "update:selectedRangeEnd",
    "update:selected",
  ],
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
    isSelected: {
      get() {
        return this.insideSelected;
      },
      set(v) {
        this.insideSelected = v;
        this.$emit("update:selected", v);
      },
    },
  },
};
</script>
