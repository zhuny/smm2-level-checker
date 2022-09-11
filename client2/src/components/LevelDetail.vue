<template lang="pug">
v-container
  v-card
    v-card-title(v-text="levelName")
    v-card-subtitle
      v-chip.bg-purple-darken-1.px-4.py-0(
        v-text="levelCode"
      )
</template>

<script>
import { client } from "../plugins/graphql";
import { gql } from "graphql-request";

export default {
  name: "LevelDetail",
  data() {
    return {
      levelId: this.$route.params.levelId,
      levelName: "-",
      levelCode: "-",
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
      .then(({ level: { name, code } }) => {
        this.levelName = name;
        this.levelCode = code;
      });
  },
};
</script>