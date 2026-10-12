import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

const SCHEMA = {
  schemaVersion: 2,
  sequences: {
    "com.tldraw.store": 5,
    "com.tldraw.asset": 1,
    "com.tldraw.camera": 1,
    "com.tldraw.document": 2,
    "com.tldraw.instance": 26,
    "com.tldraw.instance_page_state": 5,
    "com.tldraw.instance_presence": 6,
    "com.tldraw.page": 1,
    "com.tldraw.pointer": 1,
    "com.tldraw.shape": 4,
    "com.tldraw.asset.bookmark": 2,
    "com.tldraw.asset.image": 5,
    "com.tldraw.asset.video": 5,
    "com.tldraw.shape.arrow": 8,
    "com.tldraw.shape.bookmark": 2,
    "com.tldraw.shape.draw": 4,
    "com.tldraw.shape.embed": 4,
    "com.tldraw.shape.frame": 1,
    "com.tldraw.shape.geo": 11,
    "com.tldraw.shape.group": 0,
    "com.tldraw.shape.highlight": 3,
    "com.tldraw.shape.image": 5,
    "com.tldraw.shape.line": 5,
    "com.tldraw.shape.note": 10,
    "com.tldraw.shape.text": 4,
    "com.tldraw.shape.video": 4,
    "com.tldraw.binding": 0,
    "com.tldraw.binding.arrow": 1,
  },
};

function buildIndexFactory() {
  const SAFE = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  const BASE = SAFE.length;
  let counter = -1;
  return () => {
    counter += 1;
    const hi = Math.floor(counter / BASE);
    const lo = counter % BASE;
    return `a${SAFE[hi] || "1"}${SAFE[lo]}`;
  };
}

function toRichText(text) {
  const lines = String(text || "").split("\n");
  return {
    type: "doc",
    content: lines.map((line) => {
      if (!line) return { type: "paragraph" };
      return {
        type: "paragraph",
        content: [{ type: "text", text: line }],
      };
    }),
  };
}

function buildTldr(diagram) {
  const nextIndex = buildIndexFactory();
  const direction = (diagram.direction || "LR").toUpperCase();
  const theme = diagram.theme || "light";
  const title = diagram.title || "";

  const records = [
    {
      typeName: "document",
      id: "document:document",
      gridSize: 10,
      name: "",
      meta: {},
    },
    {
      typeName: "page",
      id: "page:page",
      name: "Page 1",
      index: "a1",
      meta: {},
    },
    {
      typeName: "camera",
      id: "camera:page:page",
      x: 0,
      y: 0,
      z: 1,
      meta: {},
    },
  ];

  // Title shape
  if (title) {
    records.push({
      typeName: "shape",
      id: "shape:title",
      type: "text",
      x: 100,
      y: 60,
      rotation: 0,
      isLocked: false,
      opacity: 1,
      parentId: "page:page",
      index: nextIndex(),
      meta: {},
      props: {
        richText: toRichText(title),
        size: "xl",
        font: "sans",
        textAlign: "start",
        color: "black",
        w: 800,
        scale: 1,
        autoSize: true,
      },
    });
  }

  // Group parsing
  const definedGroups = Array.isArray(diagram.groups) ? diagram.groups : [];
  const groupMap = new Map();
  const groupOrder = [];

  definedGroups.forEach((g) => {
    const id = g.id || g.title;
    groupMap.set(id, {
      id,
      title: g.title || id,
      color: g.color || "grey",
      nodes: [],
    });
    groupOrder.push(id);
  });

  const nodes = Array.isArray(diagram.nodes) ? diagram.nodes : [];
  nodes.forEach((node) => {
    const gid = node.group || "Default";
    if (!groupMap.has(gid)) {
      groupMap.set(gid, {
        id: gid,
        title: gid,
        color: "grey",
        nodes: [],
      });
      groupOrder.push(gid);
    }
    groupMap.get(gid).nodes.push(node);
  });

  const NODE_W = diagram.nodeWidth || 270;
  const NODE_H = diagram.nodeHeight || 110;
  const NODE_GAP_Y = 40;
  const NODE_GAP_X = 50;
  const GROUP_PADDING = 30;
  const GROUP_HEADER_H = 70;

  const nodePositions = new Map();

  let curX = 100;
  let curY = title ? 170 : 80;

  if (direction === "LR") {
    // Horizontal flow: groups are columns side by side
    const COL_GAP = diagram.groupGap || 180;

    const maxGroupNodes = Math.max(
      ...groupOrder.map((gid) => groupMap.get(gid)?.nodes.length || 0),
      1
    );
    const uniformContentH =
      maxGroupNodes * NODE_H + (maxGroupNodes - 1) * NODE_GAP_Y;
    const uniformGroupTotalH = uniformContentH + GROUP_PADDING * 2 + GROUP_HEADER_H;

    groupOrder.forEach((gid) => {
      const grp = groupMap.get(gid);
      if (!grp || grp.nodes.length === 0) return;

      const groupNodeCount = grp.nodes.length;
      const groupTotalH = uniformGroupTotalH;
      const groupTotalW = NODE_W + GROUP_PADDING * 2;
      const groupContentH =
        groupNodeCount * NODE_H + (groupNodeCount - 1) * NODE_GAP_Y;
      const verticalOffset = (uniformContentH - groupContentH) / 2;

      // Group Container Frame (Monochrome B&W)
      const frameId = `shape:grp_frame_${nextIndex()}`;
      records.push({
        typeName: "shape",
        id: frameId,
        type: "geo",
        x: curX,
        y: curY,
        rotation: 0,
        isLocked: false,
        opacity: 0.9,
        parentId: "page:page",
        index: nextIndex(),
        meta: {},
        props: {
          geo: "rectangle",
          dash: grp.dash || "draw",
          url: "",
          w: groupTotalW,
          h: groupTotalH,
          growY: 0,
          scale: 1,
          labelColor: "black",
          color: "black",
          fill: "none",
          size: "m",
          font: "sans",
          align: "middle",
          verticalAlign: "middle",
          richText: toRichText(""),
        },
      });

      // Group Header Label (Monochrome B&W)
      records.push({
        typeName: "shape",
        id: `shape:grp_title_${nextIndex()}`,
        type: "text",
        x: curX + GROUP_PADDING,
        y: curY + GROUP_PADDING / 2,
        rotation: 0,
        isLocked: false,
        opacity: 1,
        parentId: "page:page",
        index: nextIndex(),
        meta: {},
        props: {
          richText: toRichText(grp.title),
          size: "m",
          font: "sans",
          textAlign: "start",
          color: "black",
          w: groupTotalW - GROUP_PADDING * 2,
          scale: 1,
          autoSize: true,
        },
      });

      // Render Nodes within group
      grp.nodes.forEach((node, idx) => {
        const nx = curX + GROUP_PADDING;
        const ny =
          curY +
          GROUP_HEADER_H +
          GROUP_PADDING +
          verticalOffset +
          idx * (NODE_H + NODE_GAP_Y);
        const shapeId = `shape:node_${nextIndex()}`;

        records.push({
          typeName: "shape",
          id: shapeId,
          type: "geo",
          x: nx,
          y: ny,
          rotation: 0,
          isLocked: false,
          opacity: 1,
          parentId: "page:page",
          index: nextIndex(),
          meta: {},
          props: {
            geo: node.geo || "rectangle",
            dash: node.dash || "draw",
            url: "",
            w: NODE_W,
            h: NODE_H,
            growY: 0,
            scale: 1,
            labelColor: "black",
            color: "black",
            fill: node.fill || "none",
            size: "s",
            font: "sans",
            align: "middle",
            verticalAlign: "middle",
            richText: toRichText(node.label || node.id),
          },
        });

        nodePositions.set(node.id, {
          id: node.id,
          x: nx,
          y: ny,
          w: NODE_W,
          h: NODE_H,
          groupId: gid,
          groupCol: groupOrder.indexOf(gid),
        });
      });

      curX += groupTotalW + COL_GAP;
    });
  } else {
    // TD flow: groups are rows stacked vertically
    const ROW_GAP = diagram.groupGap || 90;

    groupOrder.forEach((gid) => {
      const grp = groupMap.get(gid);
      if (!grp || grp.nodes.length === 0) return;

      const groupNodeCount = grp.nodes.length;
      const groupContentW =
        groupNodeCount * NODE_W + (groupNodeCount - 1) * NODE_GAP_X;
      const groupTotalW = groupContentW + GROUP_PADDING * 2;
      const groupTotalH = NODE_H + GROUP_PADDING * 2 + GROUP_HEADER_H;

      // Group Container Frame
      records.push({
        typeName: "shape",
        id: `shape:grp_frame_${nextIndex()}`,
        type: "geo",
        x: curX,
        y: curY,
        rotation: 0,
        isLocked: false,
        opacity: 0.85,
        parentId: "page:page",
        index: nextIndex(),
        meta: {},
        props: {
          geo: "rectangle",
          dash: "draw",
          url: "",
          w: groupTotalW,
          h: groupTotalH,
          growY: 0,
          scale: 1,
          labelColor: "black",
          color: "black",
          fill: "none",
          size: "m",
          font: "sans",
          align: "middle",
          verticalAlign: "middle",
          richText: toRichText(""),
        },
      });

      // Group Header Label
      records.push({
        typeName: "shape",
        id: `shape:grp_title_${nextIndex()}`,
        type: "text",
        x: curX + GROUP_PADDING,
        y: curY + GROUP_PADDING / 2,
        rotation: 0,
        isLocked: false,
        opacity: 1,
        parentId: "page:page",
        index: nextIndex(),
        meta: {},
        props: {
          richText: toRichText(grp.title),
          size: "m",
          font: "sans",
          textAlign: "start",
          color: "black",
          w: groupTotalW - GROUP_PADDING * 2,
          scale: 1,
          autoSize: true,
        },
      });

      grp.nodes.forEach((node, idx) => {
        const nx =
          curX + GROUP_PADDING + idx * (NODE_W + NODE_GAP_X);
        const ny = curY + GROUP_HEADER_H + GROUP_PADDING;
        const shapeId = `shape:node_${nextIndex()}`;

        records.push({
          typeName: "shape",
          id: shapeId,
          type: "geo",
          x: nx,
          y: ny,
          rotation: 0,
          isLocked: false,
          opacity: 1,
          parentId: "page:page",
          index: nextIndex(),
          meta: {},
          props: {
            geo: node.geo || "rectangle",
            dash: node.dash || "draw",
            url: "",
            w: NODE_W,
            h: NODE_H,
            growY: 0,
            scale: 1,
            labelColor: "black",
            color: "black",
            fill: node.fill || "none",
            size: "s",
            font: "sans",
            align: "middle",
            verticalAlign: "middle",
            richText: toRichText(node.label || node.id),
          },
        });

        nodePositions.set(node.id, {
          id: node.id,
          x: nx,
          y: ny,
          w: NODE_W,
          h: NODE_H,
          groupId: gid,
          groupRow: groupOrder.indexOf(gid),
        });
      });

      curY += groupTotalH + ROW_GAP;
    });
  }

  // Connect edges
  const edges = Array.isArray(diagram.edges) ? diagram.edges : [];
  edges.forEach((edge, idx) => {
    const from = nodePositions.get(edge.from);
    const to = nodePositions.get(edge.to);
    if (!from || !to) {
      console.warn(`[render-tldraw] Warning: Edge ignored, unknown node: ${edge.from} -> ${edge.to}`);
      return;
    }

    let startX, startY, endX, endY;

    if (direction === "LR") {
      if (from.groupCol < to.groupCol) {
        // Left to right
        startX = from.x + from.w;
        startY = from.y + from.h / 2;
        endX = to.x;
        endY = to.y + to.h / 2;
      } else if (from.groupCol > to.groupCol) {
        // Right to left (loopback / feedback)
        startX = from.x;
        startY = from.y + from.h * 0.75;
        endX = to.x + to.w;
        endY = to.y + to.h * 0.75;
      } else {
        // Same column
        startX = from.x + from.w / 2;
        startY = from.y < to.y ? from.y + from.h : from.y;
        endX = to.x + to.w / 2;
        endY = from.y < to.y ? to.y : to.y + to.h;
      }
    } else {
      // TD
      if (from.groupRow < to.groupRow) {
        startX = from.x + from.w / 2;
        startY = from.y + from.h;
        endX = to.x + to.w / 2;
        endY = to.y;
      } else if (from.groupRow > to.groupRow) {
        startX = from.x + from.w * 0.75;
        startY = from.y;
        endX = to.x + to.w * 0.75;
        endY = to.y + to.h;
      } else {
        startX = from.x < to.x ? from.x + from.w : from.x;
        startY = from.y + from.h / 2;
        endX = from.x < to.x ? to.x : to.x + to.w;
        endY = to.y + to.h / 2;
      }
    }

    const bendVal = typeof edge.bend === "number" ? edge.bend : 0;
    const arrowKind = edge.kind || (bendVal !== 0 ? "arc" : "arc");

    records.push({
      typeName: "shape",
      id: `shape:edge_${idx}_${nextIndex()}`,
      type: "arrow",
      x: startX,
      y: startY,
      rotation: 0,
      isLocked: false,
      opacity: 1,
      parentId: "page:page",
      index: nextIndex(),
      meta: {},
      props: {
        kind: arrowKind,
        labelColor: "black",
        color: edge.color || "black",
        fill: "none",
        dash: edge.dash || "draw",
        size: edge.size || "m",
        arrowheadStart: edge.arrowheadStart || "none",
        arrowheadEnd: edge.arrowheadEnd || "arrow",
        font: "sans",
        start: { x: 0, y: 0 },
        end: { x: endX - startX, y: endY - startY },
        bend: bendVal,
        richText: toRichText(edge.label || ""),
        labelPosition: 0.5,
        scale: 1,
        elbowMidPoint: 0.5,
      },
    });
  });

  return {
    tldrawFileFormatVersion: 1,
    schema: SCHEMA,
    records,
  };
}

function main() {
  const args = process.argv.slice(2);
  let inputPath = null;
  let outputPath = null;
  let exportPng = false;
  let scale = 2;
  let transparent = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--in" || arg === "-i") {
      inputPath = args[++i];
    } else if (arg === "--out" || arg === "-o") {
      outputPath = args[++i];
    } else if (arg === "--png") {
      exportPng = true;
    } else if (arg === "--scale") {
      scale = parseInt(args[++i], 10) || 2;
    } else if (arg === "--transparent" || arg === "-t") {
      transparent = true;
    }
  }

  if (!inputPath) {
    console.error("Usage: node render.mjs --in diagram.json [--out diagram.svg] [--png] [--scale 2]");
    process.exit(1);
  }

  const cwd = process.cwd();
  const absInput = path.resolve(cwd, inputPath);
  if (!fs.existsSync(absInput)) {
    console.error(`Error: File not found: ${absInput}`);
    process.exit(1);
  }

  const rawJson = fs.readFileSync(absInput, "utf8").replace(/^\uFEFF/, "");
  const diagram = JSON.parse(rawJson);

  const tldrData = buildTldr(diagram);
  const baseName = path.basename(inputPath, path.extname(inputPath));
  const dirName = path.dirname(inputPath);

  const tldrPath = path.resolve(cwd, dirName, `${baseName}.tldr`);
  fs.writeFileSync(tldrPath, JSON.stringify(tldrData, null, 2), "utf8");
  console.log(`[tldraw] Created: ${tldrPath}`);

  // Default output SVG
  const svgOutput = outputPath || path.resolve(cwd, dirName, `${baseName}.svg`);
  const svgDir = path.dirname(svgOutput);
  const svgName = path.basename(svgOutput, path.extname(svgOutput));

  console.log(`[tldraw] Exporting SVG...`);
  execSync(
    `npx @kitschpatrol/tldraw-cli export "${tldrPath}" --format svg --output "${svgDir}" --name "${svgName}" ${transparent ? "-t" : ""}`,
    { stdio: "inherit" }
  );

  if (exportPng) {
    console.log(`[tldraw] Exporting PNG (scale ${scale}x)...`);
    execSync(
      `npx @kitschpatrol/tldraw-cli export "${tldrPath}" --format png --scale ${scale} --output "${svgDir}" --name "${svgName}" ${transparent ? "-t" : ""}`,
      { stdio: "inherit" }
    );
  }

  console.log(`[tldraw] Done! Outputs:`);
  console.log(`  - TLDR: ${tldrPath}`);
  console.log(`  - SVG:  ${path.join(svgDir, svgName + ".svg")}`);
  if (exportPng) {
    console.log(`  - PNG:  ${path.join(svgDir, svgName + ".png")}`);
  }
}

main();
