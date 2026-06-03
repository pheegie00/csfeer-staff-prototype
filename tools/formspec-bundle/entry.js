// Single entry point that re-exports every symbol the browser template
// needs. esbuild walks all four @formspec-org/* packages from here and
// produces ONE deduplicated ESM bundle (one WASM-bridge module instance,
// shared between the engine, the render side, and the webcomponent).
export * from "@formspec-org/webcomponent";
export * as adapters from "@formspec-org/adapters";
export { initFormspecEngine } from "@formspec-org/engine";
