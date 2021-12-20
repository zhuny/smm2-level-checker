<template lang="pug">
div
  h1 Choose Condition
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
  button.rounded-lg.w-full.mt-2.p-2(
    @click="chooseOne"
    :class="{'bg-gray-300': !hasSelected, 'bg-purple-300': hasSelected}"
  ) Pick One!
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
      .request(
        gql`
          {
            allTeam {
              edges {
                node {
                  id
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
      if (!this.hasSelected) {
        return;
      }

      client
        .request(
          gql`
            mutation getRandomLevel($lvl: [DifficultyRangeInput]) {
              randomLevel(teamInfoList: $lvl) {
                id
              }
            }
          `,
          {
            lvl: this.selectedTeam.map((team) => {
              return {
                teamId: team.node.id,
                rangeStart: team.rangeStart,
                rangeEnd: team.rangeEnd,
              };
            }),
          }
        )
        .then(({ randomLevel: { id: levelId } }) => {
          this.$router.push({
            name: "OneLevel",
            params: { levelId },
          });
        });
    },
  },
  computed: {
    hasSelected() {
      return this.selectedTeam.length > 0;
    },
    selectedTeam() {
      return this.teamList.filter((team) => {
        return team.selected;
      });
    },
  },
};
</script>

<style scoped></style>
