<template lang="pug">
div {{ hello }}
</template>

<script>
import gql from "graphql-tag";
import request from "graphql-request";

export default {
  name: "Home",
  data() {
    return {
      hello: "",
    };
  },
  created() {
    request(
      "http://localhost:5000/api/graphql",
      gql`
        {
          allTeam {
            edges {
              node {
                teamName
              }
            }
          }
        }
      `
    ).then((data) => {
      console.log(data);
    });
  },
};
</script>
