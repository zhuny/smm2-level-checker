import { GraphQLClient } from "graphql-request";

export const client = new GraphQLClient(process.env.VUE_APP_API_URL);
