#!/usr/bin/env node

import fetch from "node-fetch";
import yargs from "yargs";

const argv = yargs(process.argv.slice(2))
  .option("commit", { type: "string", demandOption: true })
  .option("repo", { type: "string", demandOption: true })
  .argv;

const url = `http://localhost:8000/impact?commit=${argv.commit}&repo=${argv.repo}`;

const res = await fetch(url);
const data = await res.json();

console.log("\nImpacted tests:\n");

if (data.length === 0) {
  console.log("No tests impacted.");
} else {
  data.forEach(t => {
    console.log(`- ${t.type.toUpperCase()}: "${t.test}" (${t.file})`);
  });
}
