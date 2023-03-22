// const GRAPHQL_URL = 'https://app.gc.subsquid.io/beta/rubick/009-rc0/graphql'
const RMRK_GRAPHQL_URL = 'https://gql-rmrk2-prod.graphcdn.app'

import {
  getClient,
  graphFetch
} from 'https://esm.sh/@kodadot1/uniquery@0.2.2-rc.0'
import { query } from 'https://esm.sh/gql-query-builder@3.8.0'

const client = getClient('rmrk2')

export async function getKodaCollection(id: string): Promise<any> {
  const collection = client.collectionById(id, ['id', 'symbol', 'blockNumber', 'max', 'issuer', 'metadata', 'name', 'supply' ] as any)
  const result = await client.fetch<{ data: any }>(collection)
  return result.data.collection
}

export async function getSingularCollection(id: string): Promise<any> {
  const q = query({
    operation: {
      alias: 'collection',
      name: 'collections_by_pk',
    },
    fields: [
      'id',
      'symbol',
      'blockNumber: block',
      'max',
      'issuer',
      'metadata',
      'name: metadata_name',
      { 'count: nfts_aggregate': [
        { 'aggregate': [
          'value :count'
        ] }
      ] }
    ],
    variables: {
      id: {
        type: 'String',
        name: 'id',
        required: true,
        value: id,
      }
    },
  })

  const result = await graphFetch<{ data: any }>(RMRK_GRAPHQL_URL, q)
  const { data: { collection } } = result 
  const x = { ...collection, blockNumber: String(collection.blockNumber), supply: collection.count.aggregate.value }
  delete x['count']
  return x
}

