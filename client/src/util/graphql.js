import request from "graphql-request";

class GraphqlClient {
  constructor({ url }) {
    this.url = url;
  }

  query(query) {
    return request(this.url, query);
  }
}

export const client = new GraphqlClient({
  url: "http://localhost:5000/api/graphql", // 환경변수로 빼 두기
});
