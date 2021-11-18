<template lang="pug">
div
  h3 Choose Condition
  TeamDifficultySelector(
    v-for="team in teamList"
    :key="team.node.teamName"
    :teamName="team.node.teamName"
    :primaryColor="team.node.primaryColor"
    :secondaryColor="team.node.secondaryColor"
    :maxDifficulty="team.node.maxDifficulty"
    v-model:selected="team.selected"
    v-model:rangeStart="team.rangeStart"
    v-model:rangeEnd="team.rangeEnd"
    )
</template>

<script>
import { client } from "@/util/graphql";
import gql from "graphql-tag";
import TeamDifficultySelector from "@/components/TeamDifficultySelector";

export default {
  name: "RandomPick",
  components: { TeamDifficultySelector },
  data() {
    return {
      teamList: [],
    };
  },
  created() {
    client
      .query(
        gql`
          {
            allTeam {
              edges {
                node {
                  teamName
                  primaryColor
                  secondaryColor
                  maxDifficulty
                }
              }
            }
          }
        `
      )
      .then(({ allTeam: { edges } }) => {
        this.teamList = edges.map(({ node }) => {
          return {
            node,
            selected: false,
            rangeStart: 0,
            rangeEnd: 0,
          };
        });
      });
  },
};
</script>

<style scoped></style>
