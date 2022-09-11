<template lang="pug">
v-container
  v-card
    v-card-title(v-text="levelName")
    v-card-subtitle
      v-chip.bg-purple-darken-1.px-4.py-0(
        v-text="levelCode"
      )
      v-chip(v-text="creatorName")
    v-card-text
      v-alert.d-flex.align-center(
        v-for="diff in difficultyList"
        :key="diff.id"
        border="start"
        color="diff.secondaryColor"
        :border-color="diff.primaryColor"
      )
        v-alert-title(v-text="diff.teamName")
        v-rating(
          :model-value="diff.difficulty"
          :length="diff.maxDifficulty"
          density="compact"
          size="x-small"
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
      creatorName: "-",
      difficultyList: [],
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
                      maxDifficulty
                    }
                  }
                }
              }
            }
          }
        `,
        { levelId: this.levelId }
      )
      .then(
        ({
          level: {
            name,
            code,
            creator: { name: creatorName },
            difficultyList: { edges: difficultyList },
          },
        }) => {
          this.levelName = name;
          this.levelCode = code;
          this.creatorName = creatorName;
          this.difficultyList = difficultyList.map(
            ({ node: { id, difficulty, team } }) => {
              return {
                id,
                difficulty,
                ...team,
              };
            }
          );
        }
      );
  },
};
</script>
