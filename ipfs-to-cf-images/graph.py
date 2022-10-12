from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_URL = "https://app.gc.subsquid.io/beta/rubick/007/graphql"


transport = RequestsHTTPTransport(
    url=GRAPHQL_URL, verify=True, retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

def execute_query(query, variables=None):
    if variables is None:
        variables = {}
    return client.execute(query, variable_values=variables)


meta_query = gql(
    """
query missing_meta($keys: [String!]) {
  meta: metadataEntities(where: { id_in: $keys }) {
    id
    image
    animation_url: animationUrl
  }
}
"""
)

def find_meta_by_key_list(keys):
    res = execute_query(meta_query, {'keys': keys})
    return res['meta']


