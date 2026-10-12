import fs from "node:fs";
import path from "node:path";

const KROKI_URL = process.env.KROKI_URL || "https://kroki.io";

async function renderGraphviz(dotContent, format = "svg") {
  const url = `${KROKI_URL}/graphviz/${format}`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
    },
    body: dotContent,
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Kroki Graphviz render failed [${response.status}]: ${errText}`);
  }

  if (format === "svg") {
    return await response.text();
  } else {
    const arrayBuffer = await response.arrayBuffer();
    return Buffer.from(arrayBuffer);
  }
}

async function main() {
  const args = process.argv.slice(2);
  let inputPath = null;
  let outputPath = null;
  let exportPng = true;
  let exportSvg = true;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--in" || arg === "-i") {
      inputPath = args[++i];
    } else if (arg === "--out" || arg === "-o") {
      outputPath = args[++i];
    } else if (arg === "--no-png") {
      exportPng = false;
    } else if (arg === "--no-svg") {
      exportSvg = false;
    }
  }

  if (!inputPath) {
    console.error("Usage: node render-graphviz.mjs --in diagram.dot [--out diagram.svg]");
    process.exit(1);
  }

  const cwd = process.cwd();
  const absInput = path.resolve(cwd, inputPath);
  if (!fs.existsSync(absInput)) {
    console.error(`Error: File not found: ${absInput}`);
    process.exit(1);
  }

  const dotContent = fs.readFileSync(absInput, "utf8");
  const dirName = outputPath ? path.dirname(path.resolve(cwd, outputPath)) : path.dirname(absInput);
  const baseName = outputPath
    ? path.basename(outputPath, path.extname(outputPath))
    : path.basename(absInput, path.extname(absInput));

  fs.mkdirSync(dirName, { recursive: true });

  async function safeWrite(filePath, data, encoding) {
    for (let i = 0; i < 5; i++) {
      try {
        if (encoding) fs.writeFileSync(filePath, data, encoding);
        else fs.writeFileSync(filePath, data);
        return;
      } catch (e) {
        if (i === 4) throw e;
        await new Promise((r) => setTimeout(r, 600));
      }
    }
  }

  if (exportSvg) {
    const svgPath = path.join(dirName, `${baseName}.svg`);
    console.log(`[graphviz] Rendering SVG via Kroki...`);
    const svgData = await renderGraphviz(dotContent, "svg");
    await safeWrite(svgPath, svgData, "utf8");
    console.log(`  ✓ Created SVG: ${svgPath}`);
  }

  if (exportPng) {
    const pngPath = path.join(dirName, `${baseName}.png`);
    console.log(`[graphviz] Rendering PNG via Kroki...`);
    const pngBuffer = await renderGraphviz(dotContent, "png");
    await safeWrite(pngPath, pngBuffer);
    console.log(`  ✓ Created PNG: ${pngPath}`);
  }

  console.log(`[graphviz] Complete!`);
}

main().catch((err) => {
  console.error(`[graphviz] Error:`, err.message);
  process.exit(1);
});
