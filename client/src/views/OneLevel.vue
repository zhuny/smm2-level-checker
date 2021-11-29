<template lang="pug">
div
  h1.font-black.text-2xl {{ levelInfo.name }}
  div.flex.items-end
    .mt-2.px-3.py-1.rounded-full.text-sm.text-white.bg-purple-500 {{ levelInfo.code }}
    .ml-3.text-gray-500 {{ levelInfo.creator.name }}
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
        creator: {
          name: "-",
        },
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
              creator {
                name
              }
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
