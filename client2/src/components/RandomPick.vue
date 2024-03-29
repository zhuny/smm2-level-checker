<template lang="pug">
v-container
  RandomTeamPick.my-2(
    :team-name="team.teamName"
    :primary-color="team.primaryColor"
    v-model:selected="team.selected"
    :range-end="team.maxDifficulty"
    v-model:selected-range-start="team.rangeStart"
    v-model:selected-range-end="team.rangeEnd"
    v-for="team in teamList"
    key="team.id"
  )
  v-btn.my-2(
    block
    color="secondary"
    @click="pickRandomLevel"
    :disabled="!teamSelected"
  ) Pick One!
</template>

<script>
import { client } from "../plugins/graphql";
import { gql } from "graphql-request";
import RandomTeamPick from "./RandomTeamPick.vue";

export default {
  name: "RandomPick",
  components: { RandomTeamPick },
  data() {
    return {
      teamList: [],
      teamSelected: false,
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
                  searchOption {
                    selected
                    rangeStart
                    rangeEnd
                  }
                }
              }
            }
          }
        `
      )
      .then(({ allTeam: { edges } }) => {
        this.teamList = edges.map(({ node }) => {
          return {
            ...node,
            selected: false,
            rangeStart: 0,
            rangeEnd: 0,
            ...node.searchOption,
          };
        });
      });
  },
  watch: {
    teamList: {
      handler(teamList) {
        this.teamSelected = teamList.some(({ selected }) => {
          return selected;
        });
      },
      deep: true,
    },
  },
  methods: {
    pickRandomLevel() {
      if (!this.teamSelected) {
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
            lvl: this.teamList
              .filter((team) => {
                return team.selected;
              })
              .map((team) => {
                return {
                  teamId: team.id,
                  rangeStart: team.rangeStart,
                  rangeEnd: team.rangeEnd,
                };
              }),
          }
        )
        .then(({ randomLevel: { id: levelId } }) => {
          this.$router.push({
            name: "LevelDetail",
            params: { levelId },
          });
        });
    },
  },
};
</script>
