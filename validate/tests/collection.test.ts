import { assertEquals } from "https://deno.land/std@0.180.0/testing/asserts.ts";
import { getKodaCollection, getSingularCollection } from "../graph.ts";

Deno.test("Collection should be equal", async () => {
  const id = '5412791fffe83a9b05-AW7TG'
  const koda = await getKodaCollection(id)
  const singular = await getSingularCollection(id)

  console.log(koda)
  console.log(singular)

  assertEquals(koda, singular)
});