<template lang="pug">
v-card(
  :color="primaryColor"
)
  v-card-title {{ teamName }}
</template>

<script>
export default {
  name: "RandomTeamPick",
  data() {
    return {};
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
  },
};
</script>
