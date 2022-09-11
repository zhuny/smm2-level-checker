<template lang="pug">
v-container
</template>

<script>
import { client } from "../plugins/graphql";
import { gql } from "graphql-request";

export default {
  name: "LevelDetail",
  data() {
    return {
      levelId: this.$route.params.levelId,
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
              clearInfo {
                clearAt
              }
              difficultyList {
                edges {
                  node {
                    id
                    difficulty
                    team {
                      teamName
                      primaryColor
                      secondaryColor
                    }
                  }
                }
              }
            }
          }
        `,
        { levelId: this.levelId }
      )
      .then((info) => {
        console.log(info);
      });
  },
};
</script>
