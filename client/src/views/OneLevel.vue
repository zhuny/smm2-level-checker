<template lang="pug">
div
  h1.font-black.text-2xl {{ levelInfo.name }}
  div.flex.items-end
    .mt-2.px-3.py-1.rounded-full.text-sm.text-white.bg-purple-500 {{ levelInfo.code }}
    .ml-3.text-gray-500 {{ levelInfo.creator.name }}
  div.pt-2
    .rounded-md.mt-2.p-3.bg-purple-500.flex(
      v-for="diff in levelInfo.difficultyList"
      key="1"
      :style="{backgroundColor: diff.team.primaryColor}"
    )
      div.font-bold(
        :style="{color: diff.team.secondaryColor}"
      ) {{ diff.team.teamName }} :
      div.pl-2 {{ diff.difficulty }}
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
        difficultyList: [],
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
              difficultyList {
                edges {
                  node {
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
        { levelId: this.$route.params.levelId }
      )
      .then(
        ({
          level: {
            difficultyList: { edges: diffEdge },
            ...level
          },
        }) => {
          this.levelInfo = level;
          this.levelInfo.difficultyList = diffEdge.map(({ node: diff }) => {
            return diff;
          });
          console.log(this.levelInfo);
        }
      );
  },
};
</script>

<style scoped></style>
