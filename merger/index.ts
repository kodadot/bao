const buildUrl = (uuid: string) => `https://imagedelivery.net/jk5b6spi_m_-9qC4VTnjpg/${uuid}/detail`;

const final = await Deno.readTextFile("./finalmap.json").then(JSON.parse) as Record<string, string>;
const durable = await Deno.readTextFile("./durablemap.json").then(JSON.parse) as Record<string, string>;

const merged = Object.entries(final).map(([key, image]) => {
  const uuid = durable[key];
  const url = buildUrl(uuid);
  return { id: image, url };
});

await Deno.writeTextFile("./merge.json", JSON.stringify(merged, null, 2));
