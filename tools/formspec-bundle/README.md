# formspec-bundle

A standalone esbuild workspace that produces the deduplicated browser bundle
served at `/static/form_manager/formspec/bundle.js`. CDN bundlers (esm.sh,
JSDelivr `/+esm`) ship the `@formspec-org/*` packages as separate ESM
bundles, which means the WASM-bridge module that holds the `_wasmReady`
flag exists once per peer-dep bundle. Calling `initFormspecEngine()` in one
bundle leaves the render bundle's copy uninitialised, and the webcomponent
throws `"Formspec runtime WASM is not initialized"` on `.definition = …`.

Building locally produces a single ESM file where every package shares one
WASM-bridge module instance.

## Why this exists in `tools/` and not as a runtime build step

The Django app is what we ship; Node is only needed for this one-off
bundling step. The bundle outputs are checked in to `form_manager/static/`
so the runtime image (and `collectstatic`) does not need Node.

## Rebuild

```bash
cd tools/formspec-bundle
npm install
npm run build
```

Outputs:

- `form_manager/static/form_manager/formspec/bundle.js`
- `form_manager/static/form_manager/formspec/bundle.css`
- `form_manager/static/form_manager/formspec/formspec-layout.css`
- `form_manager/static/form_manager/formspec/formspec-default.css`
- `form_manager/static/form_manager/wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm`

The WASM file goes one directory up from the bundle because the engine's
bundled code is `new URL("../wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm", import.meta.url)`.

## Pinning

Versions are pinned in `package.json` (`@formspec-org/webcomponent@1.0.0`,
`@formspec-org/engine@1.0.0`, `@formspec-org/layout@1.0.0`,
`@formspec-org/adapters@0.1.0`). Bump those when adopting a new release,
re-run `npm install && npm run build`, then commit the regenerated
`form_manager/static/form_manager/formspec/*` and
`form_manager/static/form_manager/wasm-pkg-runtime/*` artifacts alongside
the `package-lock.json` bump.
