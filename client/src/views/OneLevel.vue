<template lang="pug">
div
  h1 HI
</template>

<script>
import gql from "graphql-tag";
import { client } from "@/util/graphql";

export default {
  name: "OneLevel",
  data() {
    return {
      levelInfo: {
        name: "",
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
