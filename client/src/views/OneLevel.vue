<template lang="pug">
div
  h1.font-black.text-2xl {{ levelInfo.name }}
  div.flex.items-end
    .mt-2.px-3.py-1.rounded-full.text-sm.text-white.bg-purple-500 {{ levelInfo.code }}
    .ml-3.text-gray-500 {{ levelInfo.creator.name }}
  div.py-1.px-0
    .rounded-md.mt-2.p-3.flex(
      v-for="diff in levelInfo.difficultyList"
      :key="diff.id"
      :style="{backgroundColor: diff.team.primaryColor}"
    )
      div.font-bold(
        :style="{color: diff.team.secondaryColor}"
      ) {{ diff.team.teamName }} :
      div.pl-2 {{ diff.difficulty }}
  div.pt-2
    button.bg-purple-500.text-white.rounded-md.p-3.w-full(
      @click="clearLevel"
      v-if="!levelInfo.clearInfo"
    ) CLEAR
    div.bg-purple-300.text-white.rounded-md.p-3.w-full.text-center(
      v-else=""
    ) DONE - {{ levelInfo.clearInfo.clearAt }}
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
        clearInfo: null,
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
        }
      );
  },
  methods: {
    clearLevel() {
      console.log("HI");
      client
        .request(
          gql`
            mutation postClearLevel($levelId: Base64Key) {
              clearLevel(levelId: $levelId) {
                clearInfo {
                  clearAt
                }
              }
            }
          `,
          { levelId: this.$route.params.levelId }
        )
        .then(({ clearLevel: { clearInfo } }) => {
          this.levelInfo.clearInfo = clearInfo;
        });
    },
  },
};
</script>

<style scoped></style>
