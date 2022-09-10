<template lang="pug">
v-container
  v-card.mx-auto
    v-list(
      :items="teamList"
      item-title="teamName"
    )
</template>

<script>
import { client } from "../plugins/graphql";
import { gql } from "graphql-request";

export default {
  name: "RandomPick",
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
