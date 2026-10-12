import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

// Simple parser for Mermaid flowchart (LR / TD)
export function parseMermaidFlowchart(mermaidCode) {
  const lines = mermaidCode.split(/\r?\n/);
  let direction = "LR";
  let title = "Sơ đồ hệ thống";

  const groups = [];
  const nodes = [];
  const edges = [];

  let currentGroup = null;
  const nodeMap = new Map();

  for (let rawLine of lines) {
    let line = rawLine.trim();
    if (!line || line.startsWith("%%") || line.startsWith("---")) continue;

    // Check direction
    if (line.match(/^(flowchart|graph)\s+(LR|TD|TB|RL)/i)) {
      const match = line.match(/^(flowchart|graph)\s+(LR|TD|TB|RL)/i);
      const dir = match[2].toUpperCase();
      direction = dir === "TB" ? "TD" : dir;
      continue;
    }

    // Subgraph
    if (line.startsWith("subgraph")) {
      const subMatch = line.match(/^subgraph\s+([A-Za-z0-9_-]+)(?:\["?(.*?)"?\])?/);
      if (subMatch) {
        const gid = subMatch[1];
        const gtitle = subMatch[2] || gid;
        currentGroup = gid;
        if (!groups.some((g) => g.id === gid)) {
          groups.push({ id: gid, title: gtitle, color: "grey" });
        }
      }
      continue;
    }

    if (line === "end") {
      currentGroup = null;
      continue;
    }

    // Edge check: e.g. A --> B, A -->|label| B, A -- label --> B
    const edgeMatch = line.match(
      /([A-Za-z0-9_-]+)(?:\["?(.*?)"?\])?\s*-->\s*(?:\|(.*?)\|)?\s*([A-Za-z0-9_-]+)(?:\["?(.*?)"?\])?/
    );

    if (edgeMatch) {
      const fromId = edgeMatch[1];
      const fromLabel = edgeMatch[2] || fromId;
      const edgeLabel = edgeMatch[3] || "";
      const toId = edgeMatch[4];
      const toLabel = edgeMatch[5] || toId;

      if (!nodeMap.has(fromId)) {
        const n = { id: fromId, label: fromLabel, group: currentGroup || "Default" };
        nodes.push(n);
        nodeMap.set(fromId, n);
      }
      if (!nodeMap.has(toId)) {
        const n = { id: toId, label: toLabel, group: currentGroup || "Default" };
        nodes.push(n);
        nodeMap.set(toId, n);
      }

      edges.push({
        from: fromId,
        to: toId,
        label: edgeLabel,
        bend: 0,
      });
      continue;
    }

    // Single node definition: e.g. A["Label here"]
    const nodeOnlyMatch = line.match(/^([A-Za-z0-9_-]+)\["?(.*?)"?\]/);
    if (nodeOnlyMatch) {
      const id = nodeOnlyMatch[1];
      const label = nodeOnlyMatch[2] || id;
      if (!nodeMap.has(id)) {
        const n = { id, label, group: currentGroup || "Default" };
        nodes.push(n);
        nodeMap.set(id, n);
      }
      continue;
    }
  }

  return {
    title,
    direction,
    groups: groups.length > 0 ? groups : undefined,
    nodes,
    edges,
  };
}

function main() {
  const args = process.argv.slice(2);
  const mmdPath = args[0];
  if (!mmdPath) {
    console.log("Usage: node mermaid-to-tldr.mjs <diagram.mmd> [--png]");
    process.exit(1);
  }

  const cwd = process.cwd();
  const absPath = path.resolve(cwd, mmdPath);
  if (!fs.existsSync(absPath)) {
    console.error(`Error: File not found: ${absPath}`);
    process.exit(1);
  }

  const content = fs.readFileSync(absPath, "utf8");
  const diagramJson = parseMermaidFlowchart(content);

  const baseName = path.basename(mmdPath, path.extname(mmdPath));
  const dirName = path.dirname(mmdPath);
  const jsonPath = path.resolve(cwd, dirName, `${baseName}.tldraw.json`);

  fs.writeFileSync(jsonPath, JSON.stringify(diagramJson, null, 2), "utf8");
  console.log(`[convert] Generated JSON: ${jsonPath}`);

  import("node:url").then(({ fileURLToPath }) => {
    const renderScript = fileURLToPath(new URL("render.mjs", import.meta.url));
    const exportPng = args.includes("--png") ? "--png" : "";

    execSync(`node "${renderScript}" --in "${jsonPath}" ${exportPng}`, { stdio: "inherit" });
  });
}

if (process.argv[1] && process.argv[1].includes("mermaid-to-tldr.mjs")) {
  main();
}
