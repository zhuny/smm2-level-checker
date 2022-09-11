<template lang="pug">
v-card(
  :color="primaryColor"
)
  v-card-title {{ teamName }}
  v-checkbox(
    v-model="selected"
    label="Contain this team"
  )
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
    selected: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
