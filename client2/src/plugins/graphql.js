import { GraphQLClient } from "graphql-request";

export const client = new GraphQLClient(import.meta.env.VITE_APP_API_URL);
