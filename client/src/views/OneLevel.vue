<template lang="pug">
div
  h1.font-black.text-2xl {{ levelInfo.name }}
  div
    .mt-2.text-sm.px-3.py-1.rounded-full.bg-purple-300 {{ levelInfo.code }}
</template>

<script>
import gql from "graphql-tag";
import { client } from "@/util/graphql";

export default {
  name: "OneLevel",
  data() {
    return {
      levelInfo: {
        name: "-",
        code: "-",
      },
    };
  },
  created() {
    client
      .request(
        gql`
          query getLevel($levelId: ID!) {
            level(id: $levelId) {
              code
              name
            }
          }
        `,
        { levelId: this.$route.params.levelId }
      )
      .then(({ level }) => {
        this.levelInfo = level;
      });
  },
};
</script>

<style scoped></style>
