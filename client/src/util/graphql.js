import { GraphQLClient } from "graphql-request";

export const client = new GraphQLClient(
  "http://localhost:5000/api/graphql" // 환경변수로 빼 두기
);
