// Build a single deduplicated formspec bundle for the browser.
//
// Outputs:
//   form_manager/static/form_manager/formspec/bundle.mjs
//   form_manager/static/form_manager/formspec/formspec-layout.css
//   form_manager/static/form_manager/formspec/formspec-default.css
//   form_manager/static/form_manager/formspec/<hash>.wasm
//
// CSS imports inside the package source become side-effect imports that
// esbuild extracts to bundle.css; we then also copy the two raw stylesheets
// the template links via <link rel="stylesheet">. The .wasm is emitted via
// esbuild's `file` loader so the `new URL("...wasm", import.meta.url)` in
// the engine resolves to a sibling staticfiles URL at runtime.

import { build } from "esbuild";
import { mkdirSync, copyFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outdir = resolve(here, "../../form_manager/static/form_manager/formspec");
mkdirSync(outdir, { recursive: true });

await build({
  entryPoints: [resolve(here, "entry.js")],
  outdir,
  entryNames: "bundle",
  bundle: true,
  format: "esm",
  splitting: false,
  platform: "browser",
  target: ["es2022"],
  loader: {
    ".wasm": "file",
    ".css":  "css",
    ".json": "json",
  },
  // Each bundled .wasm/.css picks up a content hash so we can change the
  // bundle without worrying about Django's staticfiles cache or browser
  // caches serving stale binaries.
  assetNames: "[name]-[hash]",
  // The engine code references `process.env.NODE_ENV` and a few node-only
  // imports (node:fs, node:url, node:path). We're targeting the browser, so
  // we replace process.env.NODE_ENV statically and let the Node imports be
  // ignored — they're inside dead branches gated on `typeof process`.
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
  external: ["node:fs", "node:url", "node:path", "node:module"],
  logLevel: "info",
  metafile: false,
});

// Also copy the raw stylesheets the template links via <link rel="stylesheet">.
const webcompDist = resolve(here, "node_modules/@formspec-org/webcomponent/dist");
for (const css of ["formspec-layout.css", "formspec-default.css"]) {
  copyFileSync(join(webcompDist, css), join(outdir, css));
}

// Copy the WASM runtime to the path the bundled engine resolves to.
// The engine code is `new URL("../wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm", import.meta.url)`.
// After bundling, `import.meta.url` is the bundle.js URL (under .../formspec/),
// so the WASM has to live at .../wasm-pkg-runtime/ -- one level up and over.
const wasmSrc = resolve(here,
  "node_modules/@formspec-org/engine/wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm");
const wasmDir = resolve(outdir, "../wasm-pkg-runtime");
mkdirSync(wasmDir, { recursive: true });
copyFileSync(wasmSrc, join(wasmDir, "formspec_wasm_runtime_bg.wasm"));

console.log("\nBundle written to", outdir);
console.log("Contents:");
for (const f of readdirSync(outdir).sort()) {
  console.log("  -", f);
}
