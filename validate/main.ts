import { parse } from "https://deno.land/std@0.180.0/flags/mod.ts"

const flags = parse(Deno.args, {
  string: ["entity", "id"],
});