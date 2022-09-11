<template lang="pug">
v-container
  RandomTeamPick.mt-4(
    :team-name="team.teamName"
    :primary-color="team.primaryColor"
    :selected="team.selected"
    v-for="team in teamList"
    key="team.id"
  )
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
};
</script>
