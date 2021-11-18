<template lang="pug">
div
  h3 Choose Condition
  TeamDifficultySelector.mt-2(
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
  button.rounded-lg.w-full.mt-2.p-2.bg-purple-300(@click="chooseOne") Pick One!
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
  methods: {
    chooseOne() {
      console.log(this.teamList);
    }
  }
};
</script>

<style scoped></style>
