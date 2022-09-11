<template lang="pug">
v-card
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
  },
};
</script>
