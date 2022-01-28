from datelib import graphql_ago


LAST_MINTED_QUERY = "query lastMinted($ago: DateTime) {\n  nFTEntities(orderBy: blockNumber_DESC, where: { createdAt_gte: $ago }) {\n    createdAt\n    meta {\n      id\n      image\n      animationUrl\n    }\n  }\n}"

def last_minted_query():
  return {
    "query": LAST_MINTED_QUERY,
    "variables": {
      "ago": graphql_ago(30)
    },
    "operationName": "lastMinted"
  }