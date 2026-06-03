var __defProp = Object.defineProperty;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __esm = (fn, res) => function __init() {
  return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// node_modules/@formspec-org/engine/dist/wasm-bridge-shared.js
async function resolveWasmAssetPathForNode(relativeToThisModule) {
  const { fileURLToPath } = await import(
    /* @vite-ignore */
    nodeUrlModuleName
  );
  const { dirname, join } = await import(
    /* @vite-ignore */
    nodePathModuleName
  );
  const { createRequire } = await import(
    /* @vite-ignore */
    nodeModuleModuleName
  );
  const meta = import.meta.url;
  if (meta.startsWith("file:")) {
    return fileURLToPath(new URL(relativeToThisModule, meta));
  }
  try {
    const require2 = createRequire(join(process.cwd(), "package.json"));
    const engineRoot = dirname(require2.resolve("@formspec-org/engine/package.json"));
    const tail = relativeToThisModule.replace(/^\.\.\//, "");
    return join(engineRoot, tail);
  } catch {
    const tail = relativeToThisModule.replace(/^\.\.\//, "");
    return join(process.cwd(), "..", "formspec-engine", tail);
  }
}
var nodeFsModuleName, nodeUrlModuleName, nodePathModuleName, nodeModuleModuleName;
var init_wasm_bridge_shared = __esm({
  "node_modules/@formspec-org/engine/dist/wasm-bridge-shared.js"() {
    nodeFsModuleName = "node:fs";
    nodeUrlModuleName = "node:url";
    nodePathModuleName = "node:path";
    nodeModuleModuleName = "node:module";
  }
});

// node_modules/@formspec-org/engine/wasm-pkg-runtime/formspec_wasm_runtime.js
var formspec_wasm_runtime_exports = {};
__export(formspec_wasm_runtime_exports, {
  analyzeFEL: () => analyzeFEL,
  applyMigrationsToResponseData: () => applyMigrationsToResponseData,
  coerceFieldValue: () => coerceFieldValue,
  computeDependencyGroups: () => computeDependencyGroups,
  default: () => __wbg_init,
  evalFEL: () => evalFEL,
  evalFELWithContext: () => evalFELWithContext,
  evaluateDefinition: () => evaluateDefinition,
  evaluateScreener: () => evaluateScreener,
  formspecWasmSplitAbiVersion: () => formspecWasmSplitAbiVersion,
  getFELDependencies: () => getFELDependencies,
  initSync: () => initSync,
  isValidFelIdentifier: () => isValidFelIdentifier,
  itemAtPath: () => itemAtPath,
  itemLocationAtPath: () => itemLocationAtPath,
  normalizeIndexedPath: () => normalizeIndexedPath,
  prepareFelExpression: () => prepareFelExpression,
  resolveOptionSetsOnDefinition: () => resolveOptionSetsOnDefinition,
  sanitizeFelIdentifier: () => sanitizeFelIdentifier
});
function analyzeFEL(expression) {
  let deferred3_0;
  let deferred3_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(expression, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.analyzeFEL(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr2 = r0;
    var len2 = r1;
    if (r3) {
      ptr2 = 0;
      len2 = 0;
      throw takeObject(r2);
    }
    deferred3_0 = ptr2;
    deferred3_1 = len2;
    return getStringFromWasm0(ptr2, len2);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred3_0, deferred3_1, 1);
  }
}
function applyMigrationsToResponseData(definition_json, response_data_json, from_version, now_iso) {
  let deferred6_0;
  let deferred6_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(definition_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(response_data_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    const ptr2 = passStringToWasm0(from_version, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len2 = WASM_VECTOR_LEN;
    const ptr3 = passStringToWasm0(now_iso, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len3 = WASM_VECTOR_LEN;
    wasm.applyMigrationsToResponseData(retptr, ptr0, len0, ptr1, len1, ptr2, len2, ptr3, len3);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr5 = r0;
    var len5 = r1;
    if (r3) {
      ptr5 = 0;
      len5 = 0;
      throw takeObject(r2);
    }
    deferred6_0 = ptr5;
    deferred6_1 = len5;
    return getStringFromWasm0(ptr5, len5);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred6_0, deferred6_1, 1);
  }
}
function coerceFieldValue(item_json, bind_json, definition_json, value_json) {
  let deferred6_0;
  let deferred6_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(item_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(bind_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    const ptr2 = passStringToWasm0(definition_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len2 = WASM_VECTOR_LEN;
    const ptr3 = passStringToWasm0(value_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len3 = WASM_VECTOR_LEN;
    wasm.coerceFieldValue(retptr, ptr0, len0, ptr1, len1, ptr2, len2, ptr3, len3);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr5 = r0;
    var len5 = r1;
    if (r3) {
      ptr5 = 0;
      len5 = 0;
      throw takeObject(r2);
    }
    deferred6_0 = ptr5;
    deferred6_1 = len5;
    return getStringFromWasm0(ptr5, len5);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred6_0, deferred6_1, 1);
  }
}
function computeDependencyGroups(entries_json) {
  let deferred3_0;
  let deferred3_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(entries_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.computeDependencyGroups(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr2 = r0;
    var len2 = r1;
    if (r3) {
      ptr2 = 0;
      len2 = 0;
      throw takeObject(r2);
    }
    deferred3_0 = ptr2;
    deferred3_1 = len2;
    return getStringFromWasm0(ptr2, len2);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred3_0, deferred3_1, 1);
  }
}
function evalFEL(expression, fields_json) {
  let deferred4_0;
  let deferred4_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(expression, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(fields_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    wasm.evalFEL(retptr, ptr0, len0, ptr1, len1);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr3 = r0;
    var len3 = r1;
    if (r3) {
      ptr3 = 0;
      len3 = 0;
      throw takeObject(r2);
    }
    deferred4_0 = ptr3;
    deferred4_1 = len3;
    return getStringFromWasm0(ptr3, len3);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred4_0, deferred4_1, 1);
  }
}
function evalFELWithContext(expression, context_json) {
  let deferred4_0;
  let deferred4_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(expression, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(context_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    wasm.evalFELWithContext(retptr, ptr0, len0, ptr1, len1);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr3 = r0;
    var len3 = r1;
    if (r3) {
      ptr3 = 0;
      len3 = 0;
      throw takeObject(r2);
    }
    deferred4_0 = ptr3;
    deferred4_1 = len3;
    return getStringFromWasm0(ptr3, len3);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred4_0, deferred4_1, 1);
  }
}
function evaluateDefinition(definition_json, data_json, context_json) {
  let deferred5_0;
  let deferred5_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(definition_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(data_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    var ptr2 = isLikeNone(context_json) ? 0 : passStringToWasm0(context_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    var len2 = WASM_VECTOR_LEN;
    wasm.evaluateDefinition(retptr, ptr0, len0, ptr1, len1, ptr2, len2);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr4 = r0;
    var len4 = r1;
    if (r3) {
      ptr4 = 0;
      len4 = 0;
      throw takeObject(r2);
    }
    deferred5_0 = ptr4;
    deferred5_1 = len4;
    return getStringFromWasm0(ptr4, len4);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred5_0, deferred5_1, 1);
  }
}
function evaluateScreener(definition_json, answers_json) {
  let deferred4_0;
  let deferred4_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(definition_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(answers_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    wasm.evaluateScreener(retptr, ptr0, len0, ptr1, len1);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr3 = r0;
    var len3 = r1;
    if (r3) {
      ptr3 = 0;
      len3 = 0;
      throw takeObject(r2);
    }
    deferred4_0 = ptr3;
    deferred4_1 = len3;
    return getStringFromWasm0(ptr3, len3);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred4_0, deferred4_1, 1);
  }
}
function formspecWasmSplitAbiVersion() {
  let deferred1_0;
  let deferred1_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    wasm.formspecWasmSplitAbiVersion(retptr);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    deferred1_0 = r0;
    deferred1_1 = r1;
    return getStringFromWasm0(r0, r1);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred1_0, deferred1_1, 1);
  }
}
function getFELDependencies(expression) {
  let deferred3_0;
  let deferred3_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(expression, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.getFELDependencies(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr2 = r0;
    var len2 = r1;
    if (r3) {
      ptr2 = 0;
      len2 = 0;
      throw takeObject(r2);
    }
    deferred3_0 = ptr2;
    deferred3_1 = len2;
    return getStringFromWasm0(ptr2, len2);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred3_0, deferred3_1, 1);
  }
}
function isValidFelIdentifier(s2) {
  const ptr0 = passStringToWasm0(s2, wasm.__wbindgen_export, wasm.__wbindgen_export2);
  const len0 = WASM_VECTOR_LEN;
  const ret = wasm.isValidFelIdentifier(ptr0, len0);
  return ret !== 0;
}
function itemAtPath(items_json, path) {
  let deferred4_0;
  let deferred4_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(items_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(path, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    wasm.itemAtPath(retptr, ptr0, len0, ptr1, len1);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr3 = r0;
    var len3 = r1;
    if (r3) {
      ptr3 = 0;
      len3 = 0;
      throw takeObject(r2);
    }
    deferred4_0 = ptr3;
    deferred4_1 = len3;
    return getStringFromWasm0(ptr3, len3);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred4_0, deferred4_1, 1);
  }
}
function itemLocationAtPath(items_json, path) {
  let deferred4_0;
  let deferred4_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(items_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passStringToWasm0(path, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len1 = WASM_VECTOR_LEN;
    wasm.itemLocationAtPath(retptr, ptr0, len0, ptr1, len1);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr3 = r0;
    var len3 = r1;
    if (r3) {
      ptr3 = 0;
      len3 = 0;
      throw takeObject(r2);
    }
    deferred4_0 = ptr3;
    deferred4_1 = len3;
    return getStringFromWasm0(ptr3, len3);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred4_0, deferred4_1, 1);
  }
}
function normalizeIndexedPath(path) {
  let deferred2_0;
  let deferred2_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(path, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.normalizeIndexedPath(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    deferred2_0 = r0;
    deferred2_1 = r1;
    return getStringFromWasm0(r0, r1);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred2_0, deferred2_1, 1);
  }
}
function prepareFelExpression(options_json) {
  let deferred3_0;
  let deferred3_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(options_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.prepareFelExpression(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr2 = r0;
    var len2 = r1;
    if (r3) {
      ptr2 = 0;
      len2 = 0;
      throw takeObject(r2);
    }
    deferred3_0 = ptr2;
    deferred3_1 = len2;
    return getStringFromWasm0(ptr2, len2);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred3_0, deferred3_1, 1);
  }
}
function resolveOptionSetsOnDefinition(definition_json) {
  let deferred3_0;
  let deferred3_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(definition_json, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.resolveOptionSetsOnDefinition(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    var r2 = getDataViewMemory0().getInt32(retptr + 4 * 2, true);
    var r3 = getDataViewMemory0().getInt32(retptr + 4 * 3, true);
    var ptr2 = r0;
    var len2 = r1;
    if (r3) {
      ptr2 = 0;
      len2 = 0;
      throw takeObject(r2);
    }
    deferred3_0 = ptr2;
    deferred3_1 = len2;
    return getStringFromWasm0(ptr2, len2);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred3_0, deferred3_1, 1);
  }
}
function sanitizeFelIdentifier(s2) {
  let deferred2_0;
  let deferred2_1;
  try {
    const retptr = wasm.__wbindgen_add_to_stack_pointer(-16);
    const ptr0 = passStringToWasm0(s2, wasm.__wbindgen_export, wasm.__wbindgen_export2);
    const len0 = WASM_VECTOR_LEN;
    wasm.sanitizeFelIdentifier(retptr, ptr0, len0);
    var r0 = getDataViewMemory0().getInt32(retptr + 4 * 0, true);
    var r1 = getDataViewMemory0().getInt32(retptr + 4 * 1, true);
    deferred2_0 = r0;
    deferred2_1 = r1;
    return getStringFromWasm0(r0, r1);
  } finally {
    wasm.__wbindgen_add_to_stack_pointer(16);
    wasm.__wbindgen_export3(deferred2_0, deferred2_1, 1);
  }
}
function __wbg_get_imports() {
  const import0 = {
    __proto__: null,
    __wbg_Error_83742b46f01ce22d: function(arg0, arg1) {
      const ret = Error(getStringFromWasm0(arg0, arg1));
      return addHeapObject(ret);
    }
  };
  return {
    __proto__: null,
    "./formspec_wasm_runtime_bg.js": import0
  };
}
function addHeapObject(obj) {
  if (heap_next === heap.length) heap.push(heap.length + 1);
  const idx = heap_next;
  heap_next = heap[idx];
  heap[idx] = obj;
  return idx;
}
function dropObject(idx) {
  if (idx < 1028) return;
  heap[idx] = heap_next;
  heap_next = idx;
}
function getDataViewMemory0() {
  if (cachedDataViewMemory0 === null || cachedDataViewMemory0.buffer.detached === true || cachedDataViewMemory0.buffer.detached === void 0 && cachedDataViewMemory0.buffer !== wasm.memory.buffer) {
    cachedDataViewMemory0 = new DataView(wasm.memory.buffer);
  }
  return cachedDataViewMemory0;
}
function getStringFromWasm0(ptr, len) {
  ptr = ptr >>> 0;
  return decodeText(ptr, len);
}
function getUint8ArrayMemory0() {
  if (cachedUint8ArrayMemory0 === null || cachedUint8ArrayMemory0.byteLength === 0) {
    cachedUint8ArrayMemory0 = new Uint8Array(wasm.memory.buffer);
  }
  return cachedUint8ArrayMemory0;
}
function getObject(idx) {
  return heap[idx];
}
function isLikeNone(x2) {
  return x2 === void 0 || x2 === null;
}
function passStringToWasm0(arg, malloc, realloc) {
  if (realloc === void 0) {
    const buf = cachedTextEncoder.encode(arg);
    const ptr2 = malloc(buf.length, 1) >>> 0;
    getUint8ArrayMemory0().subarray(ptr2, ptr2 + buf.length).set(buf);
    WASM_VECTOR_LEN = buf.length;
    return ptr2;
  }
  let len = arg.length;
  let ptr = malloc(len, 1) >>> 0;
  const mem = getUint8ArrayMemory0();
  let offset = 0;
  for (; offset < len; offset++) {
    const code = arg.charCodeAt(offset);
    if (code > 127) break;
    mem[ptr + offset] = code;
  }
  if (offset !== len) {
    if (offset !== 0) {
      arg = arg.slice(offset);
    }
    ptr = realloc(ptr, len, len = offset + arg.length * 3, 1) >>> 0;
    const view = getUint8ArrayMemory0().subarray(ptr + offset, ptr + len);
    const ret = cachedTextEncoder.encodeInto(arg, view);
    offset += ret.written;
    ptr = realloc(ptr, len, offset, 1) >>> 0;
  }
  WASM_VECTOR_LEN = offset;
  return ptr;
}
function takeObject(idx) {
  const ret = getObject(idx);
  dropObject(idx);
  return ret;
}
function decodeText(ptr, len) {
  numBytesDecoded += len;
  if (numBytesDecoded >= MAX_SAFARI_DECODE_BYTES) {
    cachedTextDecoder = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
    cachedTextDecoder.decode();
    numBytesDecoded = len;
  }
  return cachedTextDecoder.decode(getUint8ArrayMemory0().subarray(ptr, ptr + len));
}
function __wbg_finalize_init(instance, module) {
  wasm = instance.exports;
  wasmModule = module;
  cachedDataViewMemory0 = null;
  cachedUint8ArrayMemory0 = null;
  return wasm;
}
async function __wbg_load(module, imports) {
  if (typeof Response === "function" && module instanceof Response) {
    if (typeof WebAssembly.instantiateStreaming === "function") {
      try {
        return await WebAssembly.instantiateStreaming(module, imports);
      } catch (e2) {
        const validResponse = module.ok && expectedResponseType(module.type);
        if (validResponse && module.headers.get("Content-Type") !== "application/wasm") {
          console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve Wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n", e2);
        } else {
          throw e2;
        }
      }
    }
    const bytes = await module.arrayBuffer();
    return await WebAssembly.instantiate(bytes, imports);
  } else {
    const instance = await WebAssembly.instantiate(module, imports);
    if (instance instanceof WebAssembly.Instance) {
      return { instance, module };
    } else {
      return instance;
    }
  }
  function expectedResponseType(type) {
    switch (type) {
      case "basic":
      case "cors":
      case "default":
        return true;
    }
    return false;
  }
}
function initSync(module) {
  if (wasm !== void 0) return wasm;
  if (module !== void 0) {
    if (Object.getPrototypeOf(module) === Object.prototype) {
      ({ module } = module);
    } else {
      console.warn("using deprecated parameters for `initSync()`; pass a single object instead");
    }
  }
  const imports = __wbg_get_imports();
  if (!(module instanceof WebAssembly.Module)) {
    module = new WebAssembly.Module(module);
  }
  const instance = new WebAssembly.Instance(module, imports);
  return __wbg_finalize_init(instance, module);
}
async function __wbg_init(module_or_path) {
  if (wasm !== void 0) return wasm;
  if (module_or_path !== void 0) {
    if (Object.getPrototypeOf(module_or_path) === Object.prototype) {
      ({ module_or_path } = module_or_path);
    } else {
      console.warn("using deprecated parameters for the initialization function; pass a single object instead");
    }
  }
  if (module_or_path === void 0) {
    module_or_path = new URL("formspec_wasm_runtime_bg.wasm", import.meta.url);
  }
  const imports = __wbg_get_imports();
  if (typeof module_or_path === "string" || typeof Request === "function" && module_or_path instanceof Request || typeof URL === "function" && module_or_path instanceof URL) {
    module_or_path = fetch(module_or_path);
  }
  const { instance, module } = await __wbg_load(await module_or_path, imports);
  return __wbg_finalize_init(instance, module);
}
var cachedDataViewMemory0, cachedUint8ArrayMemory0, heap, heap_next, cachedTextDecoder, MAX_SAFARI_DECODE_BYTES, numBytesDecoded, cachedTextEncoder, WASM_VECTOR_LEN, wasmModule, wasm;
var init_formspec_wasm_runtime = __esm({
  "node_modules/@formspec-org/engine/wasm-pkg-runtime/formspec_wasm_runtime.js"() {
    cachedDataViewMemory0 = null;
    cachedUint8ArrayMemory0 = null;
    heap = new Array(1024).fill(void 0);
    heap.push(void 0, null, true, false);
    heap_next = heap.length;
    cachedTextDecoder = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
    cachedTextDecoder.decode();
    MAX_SAFARI_DECODE_BYTES = 2146435072;
    numBytesDecoded = 0;
    cachedTextEncoder = new TextEncoder();
    if (!("encodeInto" in cachedTextEncoder)) {
      cachedTextEncoder.encodeInto = function(arg, view) {
        const buf = cachedTextEncoder.encode(arg);
        view.set(buf);
        return {
          read: arg.length,
          written: buf.length
        };
      };
    }
    WASM_VECTOR_LEN = 0;
  }
});

// node_modules/@formspec-org/engine/dist/wasm-bridge-runtime.js
function isWasmReady() {
  return _wasmReady;
}
async function initWasm() {
  if (_wasmReady)
    return;
  if (_initPromise)
    return _initPromise;
  _initPromise = (async () => {
    try {
      const runtime = await Promise.resolve().then(() => (init_formspec_wasm_runtime(), formspec_wasm_runtime_exports));
      const runningInNode = typeof globalThis.process !== "undefined" && globalThis.process.versions?.node;
      let wasmBytes = null;
      if (runningInNode && typeof runtime.initSync === "function") {
        const { readFileSync } = await import(
          /* @vite-ignore */
          nodeFsModuleName
        );
        const wasmPath = await resolveWasmAssetPathForNode("../wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm");
        wasmBytes = readFileSync(wasmPath);
      }
      if (typeof runtime.initSync === "function" && wasmBytes) {
        runtime.initSync({ module: wasmBytes });
      } else if (typeof runtime.default === "function") {
        await runtime.default({
          module_or_path: new URL("../wasm-pkg-runtime/formspec_wasm_runtime_bg.wasm", import.meta.url)
        });
      }
      _wasm = runtime;
      _wasmReady = true;
    } catch (e2) {
      _initPromise = null;
      throw e2;
    }
  })();
  return _initPromise;
}
function wasm2() {
  if (!_wasm || !_wasmReady) {
    throw new Error("Formspec runtime WASM is not initialized. Call await initFormspecEngine() (or await initWasm()) before using the engine.");
  }
  return _wasm;
}
function wasmEvalFELWithContext(expression, context) {
  const resultJson = wasm2().evalFELWithContext(expression, JSON.stringify(context));
  return JSON.parse(resultJson);
}
function wasmPrepareFelExpression(optionsJson) {
  return wasm2().prepareFelExpression(optionsJson);
}
function wasmResolveOptionSetsOnDefinition(definitionJson) {
  return wasm2().resolveOptionSetsOnDefinition(definitionJson);
}
function wasmApplyMigrationsToResponseData(definitionJson, responseDataJson, fromVersion, nowIso) {
  return wasm2().applyMigrationsToResponseData(definitionJson, responseDataJson, fromVersion, nowIso);
}
function wasmCoerceFieldValue(itemJson, bindJson, definitionJson, valueJson) {
  return wasm2().coerceFieldValue(itemJson, bindJson, definitionJson, valueJson);
}
function wasmGetFELDependencies(expression) {
  const resultJson = wasm2().getFELDependencies(expression);
  return JSON.parse(resultJson);
}
function wasmNormalizeIndexedPath(path) {
  return wasm2().normalizeIndexedPath(path);
}
function wasmEvaluateDefinition(definition, data, context) {
  const resultJson = wasm2().evaluateDefinition(JSON.stringify(definition), JSON.stringify(data), context ? JSON.stringify(context) : void 0);
  return JSON.parse(resultJson);
}
function wasmEvaluateScreener(definition, answers) {
  const resultJson = wasm2().evaluateScreener(JSON.stringify(definition), JSON.stringify(answers));
  return JSON.parse(resultJson);
}
function wasmAnalyzeFEL(expression) {
  const resultJson = wasm2().analyzeFEL(expression);
  return JSON.parse(resultJson);
}
var _wasmReady, _initPromise, _wasm;
var init_wasm_bridge_runtime = __esm({
  "node_modules/@formspec-org/engine/dist/wasm-bridge-runtime.js"() {
    init_wasm_bridge_shared();
    _wasmReady = false;
    _initPromise = null;
    _wasm = null;
  }
});

// node_modules/@formspec-org/engine/dist/wasm-bridge-tools.js
var init_wasm_bridge_tools = __esm({
  "node_modules/@formspec-org/engine/dist/wasm-bridge-tools.js"() {
    init_wasm_bridge_shared();
    init_wasm_bridge_runtime();
  }
});

// node_modules/@formspec-org/engine/dist/init-formspec-engine.js
init_wasm_bridge_runtime();
async function initFormspecEngine() {
  return initWasm();
}
function isFormspecEngineInitialized() {
  return isWasmReady();
}

// node_modules/@formspec-org/webcomponent/dist/registry.js
var INTEGRATION_STYLE_ID = "formspec-adapter-integration";
var ComponentRegistry = class {
  constructor() {
    this.plugins = /* @__PURE__ */ new Map();
    this.adapters = /* @__PURE__ */ new Map();
    this.activeAdapter = "default";
  }
  /**
   * Register a component plugin, keyed by its `type` string.
   * If a plugin with the same type already exists it is silently replaced.
   *
   * @param plugin - The plugin to register.
   */
  register(plugin) {
    this.plugins.set(plugin.type, plugin);
  }
  /**
   * Look up a registered plugin by component type.
   *
   * @param type - Component type identifier (e.g. `"TextInput"`, `"Wizard"`).
   * @returns The matching plugin, or `undefined` if no plugin is registered for that type.
   */
  get(type) {
    return this.plugins.get(type);
  }
  /** The number of currently registered component plugins. */
  get size() {
    return this.plugins.size;
  }
  /** Register a render adapter. The 'default' adapter is always the fallback. */
  registerAdapter(adapter) {
    this.adapters.set(adapter.name, adapter);
  }
  /** Set the active adapter by name. Warns and keeps current if name is unknown. */
  setAdapter(name) {
    if (!this.adapters.has(name)) {
      console.warn(`Adapter '${name}' not registered, keeping current adapter.`);
      return;
    }
    this.activeAdapter = name;
    this.applyIntegrationCSS();
  }
  /** Inject or remove the active adapter's integrationCSS in the document head. */
  applyIntegrationCSS() {
    const existing = document.getElementById(INTEGRATION_STYLE_ID);
    if (existing)
      existing.remove();
    const adapter = this.adapters.get(this.activeAdapter);
    if (adapter?.integrationCSS) {
      const style = document.createElement("style");
      style.id = INTEGRATION_STYLE_ID;
      style.textContent = adapter.integrationCSS;
      document.head.appendChild(style);
    }
  }
  /** Resolve the render function for a component type. Falls back to default adapter. */
  resolveAdapterFn(componentType) {
    const active = this.adapters.get(this.activeAdapter);
    return active?.components[componentType] ?? this.adapters.get("default")?.components[componentType];
  }
  /** Get the name of the currently active adapter. */
  get activeAdapterName() {
    return this.activeAdapter;
  }
};
var globalRegistry = new ComponentRegistry();

// node_modules/@formspec-org/webcomponent/dist/adapters/default/shared.js
function createFieldDOM(behavior, actx, options) {
  const p2 = behavior.presentation;
  const slots = behavior.widgetClassSlots;
  const fieldId = behavior.id;
  const hintId = `${fieldId}-hint`;
  const errorId = `${fieldId}-error`;
  const describedBy = [];
  const root = document.createElement("div");
  root.className = "formspec-field";
  root.dataset.name = behavior.fieldPath;
  if (slots.root)
    actx.applyClassValue(root, slots.root);
  const effectiveLabelPosition = p2.labelPosition || "top";
  const label = document.createElement("label");
  label.className = "formspec-label";
  label.textContent = behavior.label;
  if (options?.labelFor !== false) {
    label.htmlFor = fieldId;
  }
  if (slots.label)
    actx.applyClassValue(label, slots.label);
  if (effectiveLabelPosition === "hidden") {
    label.classList.add("formspec-sr-only");
  } else if (effectiveLabelPosition === "start") {
    root.classList.add("formspec-field--inline");
  }
  root.appendChild(label);
  if (behavior.description) {
    const descId = `${fieldId}-desc`;
    const desc = document.createElement("div");
    desc.className = "formspec-description";
    desc.id = descId;
    desc.textContent = behavior.description;
    root.appendChild(desc);
    describedBy.push(descId);
  }
  let hint;
  if (behavior.hint) {
    hint = document.createElement("div");
    hint.className = "formspec-hint";
    hint.id = hintId;
    hint.textContent = behavior.hint;
    if (slots.hint)
      actx.applyClassValue(hint, slots.hint);
    root.appendChild(hint);
    describedBy.push(hintId);
  }
  const error = document.createElement("div");
  error.className = "formspec-error";
  error.id = errorId;
  error.setAttribute("role", "alert");
  error.setAttribute("aria-live", "polite");
  if (slots.error)
    actx.applyClassValue(error, slots.error);
  describedBy.push(errorId);
  return { root, label, hint, error, describedBy };
}
function finalizeFieldDOM(fieldDOM, behavior, actx) {
  const ros = behavior.remoteOptionsState;
  if (ros.loading || ros.error) {
    const status = document.createElement("div");
    status.className = "formspec-hint formspec-remote-options-status";
    if (ros.loading) {
      status.textContent = "Loading options...";
    } else if (ros.error) {
      status.textContent = behavior.options().length > 0 ? "Remote options unavailable; using fallback options." : "Failed to load options.";
    }
    fieldDOM.root.appendChild(status);
  }
  fieldDOM.root.appendChild(fieldDOM.error);
  actx.applyCssClass(fieldDOM.root, behavior.presentation);
  actx.applyStyle(fieldDOM.root, behavior.presentation.style);
  actx.applyAccessibility(fieldDOM.root, behavior.presentation);
  if (behavior.compOverrides.accessibility) {
    actx.applyAccessibility(fieldDOM.root, behavior.compOverrides);
  }
  if (behavior.compOverrides.cssClass) {
    actx.applyCssClass(fieldDOM.root, behavior.compOverrides);
  }
  if (behavior.compOverrides.style) {
    actx.applyStyle(fieldDOM.root, behavior.compOverrides.style);
  }
}
function applyControlSlotClass(control, behavior, actx, isGroup = false) {
  const controlSlot = behavior.widgetClassSlots.control;
  if (!controlSlot)
    return;
  if (isGroup) {
    control.querySelectorAll("input").forEach((el2) => actx.applyClassValue(el2, controlSlot));
  } else {
    const target = control.querySelector("input") || control.querySelector("select") || control.querySelector("textarea") || control;
    if (target instanceof HTMLElement)
      actx.applyClassValue(target, controlSlot);
  }
}

// node_modules/@formspec-org/webcomponent/dist/adapters/default/text-input.js
var renderTextInput = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  let control;
  if (behavior.maxLines && behavior.maxLines > 1) {
    const textarea = document.createElement("textarea");
    textarea.className = "formspec-input";
    textarea.name = behavior.fieldPath;
    textarea.rows = behavior.maxLines;
    if (behavior.placeholder)
      textarea.placeholder = behavior.placeholder;
    textarea.id = behavior.id;
    textarea.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
    control = textarea;
  } else if (behavior.prefix || behavior.suffix) {
    const wrapper = document.createElement("div");
    wrapper.className = "formspec-input-wrapper";
    if (behavior.prefix) {
      const prefixEl = document.createElement("span");
      prefixEl.className = "formspec-prefix";
      prefixEl.textContent = behavior.prefix;
      wrapper.appendChild(prefixEl);
    }
    const input = document.createElement("input");
    input.type = behavior.resolvedInputType || "text";
    input.className = "formspec-input";
    input.name = behavior.fieldPath;
    input.id = behavior.id;
    if (behavior.placeholder)
      input.placeholder = behavior.placeholder;
    if (behavior.inputMode)
      input.inputMode = behavior.inputMode;
    for (const [attr, val] of Object.entries(behavior.extensionAttrs)) {
      if (attr === "inputMode")
        input.inputMode = val;
      else if (attr === "maxLength")
        input.maxLength = Number(val);
      else
        input.setAttribute(attr, val);
    }
    input.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
    wrapper.appendChild(input);
    if (behavior.suffix) {
      const suffixEl = document.createElement("span");
      suffixEl.className = "formspec-suffix";
      suffixEl.textContent = behavior.suffix;
      wrapper.appendChild(suffixEl);
    }
    control = wrapper;
  } else {
    const input = document.createElement("input");
    input.type = behavior.resolvedInputType || "text";
    input.className = "formspec-input";
    input.name = behavior.fieldPath;
    input.id = behavior.id;
    if (behavior.placeholder)
      input.placeholder = behavior.placeholder;
    if (behavior.inputMode)
      input.inputMode = behavior.inputMode;
    for (const [attr, val] of Object.entries(behavior.extensionAttrs)) {
      if (attr === "inputMode")
        input.inputMode = val;
      else if (attr === "maxLength")
        input.maxLength = Number(val);
      else
        input.setAttribute(attr, val);
    }
    input.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
    control = input;
  }
  fieldDOM.root.appendChild(control);
  applyControlSlotClass(control, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/number-input.js
var renderNumberInput = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const input = document.createElement("input");
  input.type = "number";
  input.className = "formspec-input";
  input.name = behavior.fieldPath;
  input.id = behavior.id;
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  input.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  fieldDOM.root.appendChild(input);
  applyControlSlotClass(input, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: input,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/radio-group.js
var renderRadioGroup = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx, { labelFor: false });
  const labelId = `${behavior.id}-label`;
  fieldDOM.label.id = labelId;
  const container = document.createElement("div");
  container.className = "formspec-radio-group";
  container.setAttribute("role", "radiogroup");
  container.setAttribute("aria-labelledby", labelId);
  container.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  if (behavior.orientation)
    container.dataset.orientation = behavior.orientation;
  const optionControls = /* @__PURE__ */ new Map();
  const options = behavior.options();
  for (const opt of options) {
    const lbl = document.createElement("label");
    const rb = document.createElement("input");
    rb.type = "radio";
    rb.value = opt.value;
    rb.name = behavior.inputName;
    optionControls.set(opt.value, rb);
    lbl.appendChild(rb);
    lbl.appendChild(document.createTextNode(` ${opt.label}`));
    container.appendChild(lbl);
  }
  fieldDOM.root.appendChild(container);
  applyControlSlotClass(container, behavior, actx, true);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: container,
    hint: fieldDOM.hint,
    error: fieldDOM.error,
    optionControls
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/checkbox-group.js
var renderCheckboxGroup = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx, { labelFor: false });
  const labelId = `${behavior.id}-label`;
  fieldDOM.label.id = labelId;
  const container = document.createElement("div");
  container.className = "formspec-checkbox-group";
  container.setAttribute("role", "group");
  container.setAttribute("aria-labelledby", labelId);
  container.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  if (behavior.columns && behavior.columns > 1) {
    container.dataset.columns = String(behavior.columns);
  }
  const optionControls = /* @__PURE__ */ new Map();
  const options = behavior.options();
  if (options.length > 0 && behavior.selectAll) {
    const selectAllLbl = document.createElement("label");
    selectAllLbl.className = "formspec-select-all";
    const selectAllCb = document.createElement("input");
    selectAllCb.type = "checkbox";
    selectAllCb.addEventListener("change", () => {
      const checked = [];
      for (const [optVal, cb] of optionControls) {
        cb.checked = selectAllCb.checked;
        if (cb.checked)
          checked.push(optVal);
      }
      behavior.setValue(checked);
    });
    selectAllLbl.appendChild(selectAllCb);
    selectAllLbl.appendChild(document.createTextNode(" Select All"));
    container.appendChild(selectAllLbl);
  }
  for (const opt of options) {
    const lbl = document.createElement("label");
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.value = opt.value;
    cb.name = behavior.fieldPath;
    optionControls.set(opt.value, cb);
    lbl.appendChild(cb);
    lbl.appendChild(document.createTextNode(` ${opt.label}`));
    container.appendChild(lbl);
  }
  fieldDOM.root.appendChild(container);
  applyControlSlotClass(container, behavior, actx, true);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: container,
    hint: fieldDOM.hint,
    error: fieldDOM.error,
    optionControls
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/select.js
var renderSelect = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const select = document.createElement("select");
  select.className = "formspec-input";
  select.name = behavior.fieldPath;
  select.id = behavior.id;
  if (behavior.placeholder) {
    const placeholderOpt = document.createElement("option");
    placeholderOpt.value = "";
    placeholderOpt.textContent = behavior.placeholder;
    placeholderOpt.disabled = true;
    placeholderOpt.selected = true;
    select.appendChild(placeholderOpt);
  }
  if (behavior.clearable) {
    const clearOpt = document.createElement("option");
    clearOpt.value = "";
    clearOpt.textContent = "\u2014 Clear \u2014";
    select.appendChild(clearOpt);
  }
  const options = behavior.options();
  for (const opt of options) {
    const option = document.createElement("option");
    option.value = opt.value;
    option.textContent = opt.label;
    select.appendChild(option);
  }
  select.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  fieldDOM.root.appendChild(select);
  applyControlSlotClass(select, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: select,
    hint: fieldDOM.hint,
    error: fieldDOM.error,
    rebuildOptions: (_container, newOptions) => {
      const keepCount = (behavior.placeholder ? 1 : 0) + (behavior.clearable ? 1 : 0);
      while (select.options.length > keepCount)
        select.remove(select.options.length - 1);
      const controls = /* @__PURE__ */ new Map();
      for (const opt of newOptions) {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label;
        select.appendChild(option);
      }
      return controls;
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/toggle.js
var renderToggle = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const effectiveLP = behavior.presentation.labelPosition || "top";
  if (effectiveLP === "top") {
    fieldDOM.root.classList.add("formspec-field--inline");
  }
  const toggleContainer = document.createElement("div");
  toggleContainer.className = "formspec-toggle";
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "formspec-input";
  checkbox.name = behavior.fieldPath;
  checkbox.id = behavior.id;
  checkbox.setAttribute("role", "switch");
  checkbox.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  toggleContainer.appendChild(checkbox);
  if (behavior.onLabel || behavior.offLabel) {
    const toggleLabel = document.createElement("span");
    toggleLabel.className = "formspec-toggle-label";
    toggleLabel.id = `${behavior.id}-toggle-label`;
    toggleLabel.textContent = behavior.offLabel || "";
    toggleContainer.appendChild(toggleLabel);
    const existing = checkbox.getAttribute("aria-describedby") || "";
    checkbox.setAttribute("aria-describedby", `${existing} ${toggleLabel.id}`.trim());
  }
  fieldDOM.root.appendChild(toggleContainer);
  applyControlSlotClass(toggleContainer, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: toggleContainer,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/checkbox.js
var renderCheckbox = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const effectiveLP = behavior.presentation.labelPosition || "top";
  if (effectiveLP === "top") {
    fieldDOM.root.classList.add("formspec-field--inline");
  }
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "formspec-input";
  checkbox.name = behavior.fieldPath;
  checkbox.id = behavior.id;
  checkbox.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  fieldDOM.root.appendChild(checkbox);
  applyControlSlotClass(checkbox, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: checkbox,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/date-picker.js
var renderDatePicker = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const input = document.createElement("input");
  input.type = behavior.inputType;
  input.className = "formspec-input";
  input.name = behavior.fieldPath;
  input.id = behavior.id;
  if (behavior.minDate)
    input.min = behavior.minDate;
  if (behavior.maxDate)
    input.max = behavior.maxDate;
  input.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  fieldDOM.root.appendChild(input);
  applyControlSlotClass(input, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: input,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/money-input.js
var renderMoneyInput = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  const container = document.createElement("div");
  container.className = "formspec-money";
  const amountInput = document.createElement("input");
  amountInput.type = "number";
  amountInput.className = "formspec-input";
  amountInput.placeholder = behavior.placeholder || "Amount";
  amountInput.name = `${behavior.fieldPath}__amount`;
  amountInput.id = behavior.id;
  if (behavior.step != null)
    amountInput.step = String(behavior.step);
  if (behavior.min != null)
    amountInput.min = String(behavior.min);
  if (behavior.max != null)
    amountInput.max = String(behavior.max);
  amountInput.setAttribute("aria-describedby", fieldDOM.describedBy.join(" "));
  container.appendChild(amountInput);
  if (behavior.resolvedCurrency) {
    const badge = document.createElement("span");
    badge.className = "formspec-money-currency";
    badge.textContent = behavior.resolvedCurrency;
    badge.setAttribute("aria-label", `Currency: ${behavior.resolvedCurrency}`);
    container.appendChild(badge);
  } else {
    const currencyInput = document.createElement("input");
    currencyInput.type = "text";
    currencyInput.className = "formspec-input formspec-money-currency-input";
    currencyInput.placeholder = "Currency";
    currencyInput.name = `${behavior.fieldPath}__currency`;
    currencyInput.setAttribute("aria-label", "Currency code");
    container.appendChild(currencyInput);
  }
  fieldDOM.root.appendChild(container);
  applyControlSlotClass(container, behavior, actx);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: container,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/slider.js
var renderSlider = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  fieldDOM.root.classList.add("formspec-slider");
  const sliderContainer = document.createElement("div");
  sliderContainer.className = "formspec-slider-track";
  const input = document.createElement("input");
  input.type = "range";
  input.className = "formspec-input";
  input.name = behavior.fieldPath;
  input.id = behavior.id;
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.showTicks && behavior.min != null && behavior.max != null && behavior.step != null) {
    const tickCount = Math.floor((behavior.max - behavior.min) / behavior.step) + 1;
    if (tickCount > 0 && tickCount <= 200) {
      const listId = `formspec-ticks-${behavior.fieldPath.replace(/\./g, "-")}`;
      const datalist = document.createElement("datalist");
      datalist.id = listId;
      for (let v2 = behavior.min; v2 <= behavior.max; v2 += behavior.step) {
        const opt = document.createElement("option");
        opt.value = String(v2);
        datalist.appendChild(opt);
      }
      sliderContainer.appendChild(datalist);
      input.setAttribute("list", listId);
    }
  }
  sliderContainer.appendChild(input);
  const valueDisplay = document.createElement("span");
  valueDisplay.className = "formspec-slider-value";
  if (behavior.showValue) {
    sliderContainer.appendChild(valueDisplay);
  }
  fieldDOM.root.appendChild(sliderContainer);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: sliderContainer,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/rating.js
var renderRating = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  fieldDOM.root.classList.add("formspec-rating");
  const container = document.createElement("div");
  container.className = "formspec-rating-stars";
  container.setAttribute("role", "slider");
  container.setAttribute("tabindex", "0");
  container.setAttribute("aria-valuemin", "0");
  container.setAttribute("aria-valuemax", String(behavior.maxRating));
  container.setAttribute("aria-valuenow", "0");
  container.setAttribute("aria-valuetext", `0 of ${behavior.maxRating}`);
  container.setAttribute("aria-label", behavior.label);
  const step = behavior.allowHalf ? 0.5 : 1;
  let currentValue = 0;
  const updateValue = (value) => {
    currentValue = Math.max(0, Math.min(value, behavior.maxRating));
    container.setAttribute("aria-valuenow", String(currentValue));
    container.setAttribute("aria-valuetext", `${currentValue} of ${behavior.maxRating}`);
    behavior.setValue(currentValue);
  };
  container.addEventListener("keydown", (e2) => {
    switch (e2.key) {
      case "ArrowRight":
      case "ArrowUp":
        e2.preventDefault();
        updateValue(currentValue + step);
        break;
      case "ArrowLeft":
      case "ArrowDown":
        e2.preventDefault();
        updateValue(currentValue - step);
        break;
      case "Home":
        e2.preventDefault();
        updateValue(0);
        break;
      case "End":
        e2.preventDefault();
        updateValue(behavior.maxRating);
        break;
    }
  });
  for (let i2 = 1; i2 <= behavior.maxRating; i2++) {
    const star = document.createElement("span");
    star.className = "formspec-rating-star";
    star.textContent = behavior.icon;
    star.dataset.value = String(i2);
    star.addEventListener("click", (event) => {
      let value = i2;
      if (behavior.allowHalf) {
        const rect = star.getBoundingClientRect();
        const clickedLeftHalf = rect.width > 0 && event.clientX - rect.left < rect.width / 2;
        value = clickedLeftHalf ? i2 - 0.5 : i2;
      }
      updateValue(value);
    });
    container.appendChild(star);
  }
  fieldDOM.root.appendChild(container);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: container,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/file-upload.js
var renderFileUpload = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  fieldDOM.root.classList.add("formspec-file-upload");
  const input = document.createElement("input");
  input.type = "file";
  input.className = "formspec-file-input-hidden";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  if (behavior.accept)
    input.accept = behavior.accept;
  if (behavior.multiple)
    input.multiple = true;
  const browseBtn = document.createElement("button");
  browseBtn.type = "button";
  browseBtn.className = "formspec-file-browse-btn";
  browseBtn.textContent = behavior.multiple ? "Choose files" : "Choose file";
  browseBtn.addEventListener("click", () => input.click());
  const fileListEl = document.createElement("ul");
  fileListEl.className = "formspec-file-list";
  fileListEl.setAttribute("aria-label", "Selected files");
  const rebuildFileList = () => {
    fileListEl.innerHTML = "";
    const files = behavior.files();
    if (files.length === 0)
      return;
    for (let i2 = 0; i2 < files.length; i2++) {
      const f2 = files[i2];
      const li = document.createElement("li");
      li.className = "formspec-file-list-item";
      const nameSpan = document.createElement("span");
      nameSpan.className = "formspec-file-list-name";
      nameSpan.textContent = f2.name;
      li.appendChild(nameSpan);
      const sizeSpan = document.createElement("span");
      sizeSpan.className = "formspec-file-list-size";
      sizeSpan.textContent = formatBytes(f2.size);
      li.appendChild(sizeSpan);
      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "formspec-file-list-remove";
      removeBtn.setAttribute("aria-label", `Remove ${f2.name}`);
      removeBtn.innerHTML = '<span aria-hidden="true">\xD7</span>';
      const idx = i2;
      removeBtn.addEventListener("click", () => behavior.removeFile(idx));
      li.appendChild(removeBtn);
      fileListEl.appendChild(li);
    }
    if (behavior.multiple && files.length > 1) {
      const actionsLi = document.createElement("li");
      actionsLi.className = "formspec-file-list-actions";
      const clearBtn = document.createElement("button");
      clearBtn.type = "button";
      clearBtn.className = "formspec-file-list-clear";
      clearBtn.textContent = "Clear all";
      clearBtn.addEventListener("click", () => behavior.clearFiles());
      actionsLi.appendChild(clearBtn);
      fileListEl.appendChild(actionsLi);
    }
  };
  if (behavior.dragDrop) {
    const dropZone = document.createElement("div");
    dropZone.className = "formspec-file-drop-zone formspec-drop-zone";
    const content = document.createElement("div");
    content.className = "formspec-file-drop-content";
    const icon = document.createElement("span");
    icon.className = "formspec-file-drop-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "\u21D5";
    const label = document.createElement("span");
    label.className = "formspec-file-drop-label";
    label.textContent = "Drop files here";
    content.appendChild(icon);
    content.appendChild(label);
    content.appendChild(browseBtn);
    dropZone.appendChild(content);
    dropZone.setAttribute("tabindex", "0");
    dropZone.setAttribute("role", "button");
    dropZone.setAttribute("aria-label", "Drop files here or click to browse");
    dropZone.addEventListener("keydown", (e2) => {
      if (e2.key === "Enter" || e2.key === " ") {
        e2.preventDefault();
        input.click();
      }
    });
    dropZone.addEventListener("dragover", (e2) => {
      e2.preventDefault();
      dropZone.classList.add("formspec-file-drop-zone--active");
    });
    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("formspec-file-drop-zone--active");
    });
    dropZone.addEventListener("drop", (e2) => {
      e2.preventDefault();
      dropZone.classList.remove("formspec-file-drop-zone--active");
      const files = Array.from(e2.dataTransfer?.files || []);
      const fileData = files.map((f2) => ({ name: f2.name, size: f2.size, type: f2.type }));
      fieldDOM.root.dispatchEvent(new CustomEvent("formspec-files-dropped", {
        detail: { fileData, multiple: behavior.multiple },
        bubbles: false
      }));
    });
    fieldDOM.root.appendChild(dropZone);
    fieldDOM.root.appendChild(input);
  } else {
    fieldDOM.root.appendChild(input);
    fieldDOM.root.appendChild(browseBtn);
  }
  fieldDOM.root.appendChild(fileListEl);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const refs = {
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: input,
    hint: fieldDOM.hint,
    error: fieldDOM.error,
    _rebuildFileList: rebuildFileList
  };
  const dispose = behavior.bind(refs);
  actx.onDispose(dispose);
};
function formatBytes(bytes) {
  if (bytes === 0)
    return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const i2 = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const val = bytes / Math.pow(1024, i2);
  return `${val < 10 ? val.toFixed(1) : Math.round(val)} ${units[i2]}`;
}

// node_modules/@formspec-org/webcomponent/dist/adapters/signature-canvas.js
function createSignatureCanvas(config) {
  const { height, strokeColor, eventTarget } = config;
  const canvas = document.createElement("canvas");
  canvas.className = "formspec-signature-canvas";
  canvas.style.height = `${height}px`;
  const dpr = window.devicePixelRatio || 1;
  const ctx = canvas.getContext("2d");
  const resizeCanvas = () => {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    if (ctx.setTransform) {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    } else {
      ctx.scale(dpr, dpr);
    }
  };
  resizeCanvas();
  const ro = new ResizeObserver(resizeCanvas);
  ro.observe(canvas);
  let drawing = false;
  const getPos = (e2) => {
    const rect = canvas.getBoundingClientRect();
    return { x: e2.clientX - rect.left, y: e2.clientY - rect.top };
  };
  const beginStroke = (pos) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  };
  const continueStroke = (pos) => {
    if (!drawing)
      return;
    ctx.lineTo(pos.x, pos.y);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();
  };
  const endStroke = () => {
    drawing = false;
    eventTarget.dispatchEvent(new CustomEvent("formspec-signature-drawn", {
      detail: { dataUrl: canvas.toDataURL() },
      bubbles: false
    }));
  };
  const cancelStroke = () => {
    drawing = false;
  };
  canvas.addEventListener("mousedown", (e2) => beginStroke(getPos(e2)));
  canvas.addEventListener("mousemove", (e2) => continueStroke(getPos(e2)));
  canvas.addEventListener("mouseup", endStroke);
  canvas.addEventListener("mouseleave", cancelStroke);
  canvas.addEventListener("touchstart", (e2) => {
    e2.preventDefault();
    beginStroke(getPos(e2.touches[0]));
  }, { passive: false });
  canvas.addEventListener("touchmove", (e2) => {
    if (!drawing)
      return;
    e2.preventDefault();
    continueStroke(getPos(e2.touches[0]));
  }, { passive: false });
  canvas.addEventListener("touchend", endStroke);
  canvas.addEventListener("touchcancel", cancelStroke);
  const clear = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    eventTarget.dispatchEvent(new CustomEvent("formspec-signature-cleared", {
      bubbles: false
    }));
  };
  const dispose = () => {
    ro.disconnect();
  };
  return { canvas, clear, dispose };
}

// node_modules/@formspec-org/webcomponent/dist/adapters/default/signature.js
var renderSignature = (behavior, parent, actx) => {
  const fieldDOM = createFieldDOM(behavior, actx);
  fieldDOM.root.classList.add("formspec-signature");
  const { canvas, clear, dispose: canvasDispose } = createSignatureCanvas({
    height: behavior.height,
    strokeColor: behavior.strokeColor,
    eventTarget: fieldDOM.root
  });
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-roledescription", "signature pad");
  canvas.setAttribute("aria-label", "Signature canvas. Draw your signature or use the Clear button to reset.");
  fieldDOM.root.appendChild(canvas);
  actx.onDispose(canvasDispose);
  const clearBtn = document.createElement("button");
  clearBtn.type = "button";
  clearBtn.textContent = "Clear";
  clearBtn.className = "formspec-signature-clear";
  clearBtn.addEventListener("click", clear);
  fieldDOM.root.appendChild(clearBtn);
  finalizeFieldDOM(fieldDOM, behavior, actx);
  parent.appendChild(fieldDOM.root);
  const dispose = behavior.bind({
    root: fieldDOM.root,
    label: fieldDOM.label,
    control: canvas,
    hint: fieldDOM.hint,
    error: fieldDOM.error
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/wizard.js
var renderWizard = (behavior, parent, actx) => {
  const el2 = document.createElement("div");
  if (behavior.id)
    el2.id = behavior.id;
  el2.className = "formspec-wizard";
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(el2, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(el2, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(el2, behavior.compOverrides.style);
  parent.appendChild(el2);
  if (behavior.totalSteps() === 0)
    return;
  const showSideNav = behavior.showSideNav;
  let container = el2;
  let sidenavItems;
  if (showSideNav) {
    el2.classList.add("formspec-wizard--with-sidenav");
    const sidenav = document.createElement("nav");
    sidenav.className = "formspec-wizard-sidenav";
    sidenav.setAttribute("aria-label", "Form steps");
    el2.appendChild(sidenav);
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "formspec-wizard-sidenav-toggle";
    toggleBtn.setAttribute("aria-label", "Collapse navigation");
    toggleBtn.title = "Collapse";
    toggleBtn.innerHTML = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>';
    sidenav.appendChild(toggleBtn);
    let collapsed = false;
    toggleBtn.addEventListener("click", () => {
      collapsed = !collapsed;
      sidenav.classList.toggle("formspec-wizard-sidenav--collapsed", collapsed);
      toggleBtn.setAttribute("aria-label", collapsed ? "Expand navigation" : "Collapse navigation");
      toggleBtn.title = collapsed ? "Expand" : "Collapse";
      toggleBtn.innerHTML = collapsed ? '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>' : '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>';
    });
    const stepList = document.createElement("ol");
    stepList.className = "formspec-wizard-sidenav-list";
    sidenav.appendChild(stepList);
    sidenavItems = [];
    for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
      const item = document.createElement("li");
      item.className = "formspec-wizard-sidenav-item";
      if (i2 === 0)
        item.classList.add("formspec-wizard-sidenav-item--active");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "formspec-wizard-sidenav-btn";
      btn.setAttribute("aria-current", i2 === 0 ? "step" : "false");
      const circle = document.createElement("span");
      circle.className = "formspec-wizard-sidenav-step";
      circle.textContent = String(i2 + 1);
      btn.appendChild(circle);
      const label = document.createElement("span");
      label.className = "formspec-wizard-sidenav-label";
      label.textContent = behavior.steps[i2]?.title || `Step ${i2 + 1}`;
      btn.appendChild(label);
      const idx = i2;
      btn.addEventListener("click", () => behavior.goToStep(idx));
      item.appendChild(btn);
      stepList.appendChild(item);
      sidenavItems.push({ item, button: btn, circle });
    }
    const content = document.createElement("div");
    content.className = "formspec-wizard-content";
    el2.appendChild(content);
    container = content;
  }
  let progressItems;
  if (behavior.showProgress) {
    const progress = document.createElement("div");
    progress.className = "formspec-wizard-steps";
    progress.classList.toggle("formspec-hidden", showSideNav);
    container.appendChild(progress);
    progressItems = [];
    for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
      const wrapper = document.createElement("div");
      wrapper.className = "formspec-wizard-step-wrapper";
      const indicator = document.createElement("span");
      indicator.className = "formspec-wizard-step";
      if (i2 === 0)
        indicator.classList.add("formspec-wizard-step--active");
      indicator.textContent = `${i2 + 1}`;
      wrapper.appendChild(indicator);
      const stepTitle = behavior.steps[i2]?.title;
      let labelEl;
      if (stepTitle) {
        labelEl = document.createElement("span");
        labelEl.className = "formspec-wizard-step-label";
        if (i2 === 0)
          labelEl.classList.add("formspec-wizard-step-label--active");
        labelEl.textContent = stepTitle;
        wrapper.appendChild(labelEl);
      }
      progress.appendChild(wrapper);
      progressItems.push({ indicator, label: labelEl });
    }
  }
  const panels = [];
  for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-wizard-panel";
    panel.setAttribute("role", "region");
    panel.setAttribute("aria-label", behavior.steps[i2]?.title || `Step ${i2 + 1}`);
    if (i2 !== 0)
      panel.classList.add("formspec-hidden");
    behavior.renderStep(i2, panel);
    container.appendChild(panel);
    panels.push(panel);
  }
  const nav = document.createElement("div");
  nav.className = "formspec-wizard-nav";
  const prevBtn = document.createElement("button");
  prevBtn.type = "button";
  prevBtn.className = "formspec-wizard-prev";
  prevBtn.textContent = "Previous";
  nav.appendChild(prevBtn);
  let skipBtn;
  if (behavior.allowSkip) {
    skipBtn = document.createElement("button");
    skipBtn.type = "button";
    skipBtn.className = "formspec-wizard-skip";
    skipBtn.textContent = "Skip";
    skipBtn.addEventListener("click", () => {
      if (behavior.canGoNext())
        behavior.goToStep(behavior.activeStep() + 1);
    });
    nav.appendChild(skipBtn);
  }
  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.className = "formspec-wizard-next";
  nextBtn.textContent = "Next";
  nav.appendChild(nextBtn);
  container.appendChild(nav);
  const announcer = document.createElement("div");
  announcer.className = "formspec-sr-only";
  announcer.setAttribute("aria-live", "polite");
  announcer.setAttribute("role", "status");
  container.appendChild(announcer);
  const dispose = behavior.bind({
    root: el2,
    panels,
    prevButton: prevBtn,
    nextButton: nextBtn,
    stepContent: container,
    skipButton: skipBtn,
    sidenavItems,
    progressItems
  });
  actx.onDispose(dispose);
  el2.addEventListener("formspec-page-change", ((e2) => {
    const { index, total, title } = e2.detail;
    const stepLabel = title || `Step ${index + 1}`;
    announcer.textContent = index === total - 1 ? `${stepLabel}. Next will submit the form.` : `${stepLabel}. Step ${index + 1} of ${total}.`;
  }));
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/tabs.js
var renderTabs = (behavior, parent, actx) => {
  const el2 = document.createElement("div");
  if (behavior.id)
    el2.id = behavior.id;
  el2.className = "formspec-tabs";
  if (behavior.position !== "top")
    el2.dataset.position = behavior.position;
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(el2, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(el2, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(el2, behavior.compOverrides.style);
  parent.appendChild(el2);
  const count = behavior.tabCount;
  const idBase = behavior.id || "tabs";
  const tabBar = document.createElement("div");
  tabBar.className = "formspec-tab-bar";
  tabBar.setAttribute("role", "tablist");
  const panelContainer = document.createElement("div");
  panelContainer.className = "formspec-tab-panels";
  const panels = [];
  for (let i2 = 0; i2 < count; i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-tab-panel";
    panel.setAttribute("role", "tabpanel");
    panel.id = `${idBase}-panel-${i2}`;
    panel.setAttribute("aria-labelledby", `${idBase}-tab-${i2}`);
    panel.setAttribute("tabindex", "0");
    if (i2 !== behavior.defaultTab)
      panel.classList.add("formspec-hidden");
    behavior.renderTab(i2, panel);
    panelContainer.appendChild(panel);
    panels.push(panel);
  }
  const buttons = [];
  for (let i2 = 0; i2 < count; i2++) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = behavior.tabLabels[i2] || `Tab ${i2 + 1}`;
    btn.className = "formspec-tab";
    btn.setAttribute("role", "tab");
    btn.id = `${idBase}-tab-${i2}`;
    btn.setAttribute("aria-controls", `${idBase}-panel-${i2}`);
    btn.setAttribute("aria-selected", i2 === behavior.defaultTab ? "true" : "false");
    btn.setAttribute("tabindex", i2 === behavior.defaultTab ? "0" : "-1");
    tabBar.appendChild(btn);
    buttons.push(btn);
  }
  if (behavior.position === "bottom") {
    el2.appendChild(panelContainer);
    el2.appendChild(tabBar);
  } else {
    el2.appendChild(tabBar);
    el2.appendChild(panelContainer);
  }
  const dispose = behavior.bind({
    root: el2,
    tabBar,
    panels,
    buttons
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/webcomponent/dist/adapters/default/index.js
var defaultAdapter = {
  name: "default",
  components: {
    TextInput: renderTextInput,
    NumberInput: renderNumberInput,
    RadioGroup: renderRadioGroup,
    CheckboxGroup: renderCheckboxGroup,
    Select: renderSelect,
    Toggle: renderToggle,
    Checkbox: renderCheckbox,
    DatePicker: renderDatePicker,
    MoneyInput: renderMoneyInput,
    Slider: renderSlider,
    Rating: renderRating,
    FileUpload: renderFileUpload,
    Signature: renderSignature,
    Wizard: renderWizard,
    Tabs: renderTabs
  }
};

// node_modules/@preact/signals-core/dist/signals-core.module.js
var i = Symbol.for("preact-signals");
function t() {
  if (!(s > 1)) {
    var i2, t2 = false;
    !(function() {
      var i3 = c;
      c = void 0;
      while (void 0 !== i3) {
        if (i3.S.v === i3.v) i3.S.i = i3.i;
        i3 = i3.o;
      }
    })();
    while (void 0 !== h) {
      var n2 = h;
      h = void 0;
      v++;
      while (void 0 !== n2) {
        var r2 = n2.u;
        n2.u = void 0;
        n2.f &= -3;
        if (!(8 & n2.f) && w(n2)) try {
          n2.c();
        } catch (n3) {
          if (!t2) {
            i2 = n3;
            t2 = true;
          }
        }
        n2 = r2;
      }
    }
    v = 0;
    s--;
    if (t2) throw i2;
  } else s--;
}
function n(i2) {
  if (s > 0) return i2();
  e = ++u;
  s++;
  try {
    return i2();
  } finally {
    t();
  }
}
var r = void 0;
function o(i2) {
  var t2 = r;
  r = void 0;
  try {
    return i2();
  } finally {
    r = t2;
  }
}
var f;
var h = void 0;
var s = 0;
var v = 0;
var u = 0;
var e = 0;
var c = void 0;
var d = 0;
function a(i2) {
  if (void 0 !== r) {
    var t2 = i2.n;
    if (void 0 === t2 || t2.t !== r) {
      t2 = { i: 0, S: i2, p: r.s, n: void 0, t: r, e: void 0, x: void 0, r: t2 };
      if (void 0 !== r.s) r.s.n = t2;
      r.s = t2;
      i2.n = t2;
      if (32 & r.f) i2.S(t2);
      return t2;
    } else if (-1 === t2.i) {
      t2.i = 0;
      if (void 0 !== t2.n) {
        t2.n.p = t2.p;
        if (void 0 !== t2.p) t2.p.n = t2.n;
        t2.p = r.s;
        t2.n = void 0;
        r.s.n = t2;
        r.s = t2;
      }
      return t2;
    }
  }
}
function l(i2, t2) {
  this.v = i2;
  this.i = 0;
  this.n = void 0;
  this.t = void 0;
  this.l = 0;
  this.W = null == t2 ? void 0 : t2.watched;
  this.Z = null == t2 ? void 0 : t2.unwatched;
  this.name = null == t2 ? void 0 : t2.name;
}
l.prototype.brand = i;
l.prototype.h = function() {
  return true;
};
l.prototype.S = function(i2) {
  var t2 = this, n2 = this.t;
  if (n2 !== i2 && void 0 === i2.e) {
    i2.x = n2;
    this.t = i2;
    if (void 0 !== n2) n2.e = i2;
    else o(function() {
      var i3;
      null == (i3 = t2.W) || i3.call(t2);
    });
  }
};
l.prototype.U = function(i2) {
  var t2 = this;
  if (void 0 !== this.t) {
    var n2 = i2.e, r2 = i2.x;
    if (void 0 !== n2) {
      n2.x = r2;
      i2.e = void 0;
    }
    if (void 0 !== r2) {
      r2.e = n2;
      i2.x = void 0;
    }
    if (i2 === this.t) {
      this.t = r2;
      if (void 0 === r2) o(function() {
        var i3;
        null == (i3 = t2.Z) || i3.call(t2);
      });
    }
  }
};
l.prototype.subscribe = function(i2) {
  var t2 = this;
  return j(function() {
    var n2 = t2.value, o2 = r;
    r = void 0;
    try {
      i2(n2);
    } finally {
      r = o2;
    }
  }, { name: "sub" });
};
l.prototype.valueOf = function() {
  return this.value;
};
l.prototype.toString = function() {
  return this.value + "";
};
l.prototype.toJSON = function() {
  return this.value;
};
l.prototype.peek = function() {
  var i2 = this;
  return o(function() {
    return i2.value;
  });
};
Object.defineProperty(l.prototype, "value", { get: function() {
  var i2 = a(this);
  if (void 0 !== i2) i2.i = this.i;
  return this.v;
}, set: function(i2) {
  if (i2 !== this.v) {
    if (v > 100) throw new Error("Cycle detected");
    !(function(i3) {
      if (0 !== s && 0 === v) {
        if (i3.l !== e) {
          i3.l = e;
          c = { S: i3, v: i3.v, i: i3.i, o: c };
        }
      }
    })(this);
    this.v = i2;
    this.i++;
    d++;
    s++;
    try {
      for (var n2 = this.t; void 0 !== n2; n2 = n2.x) n2.t.N();
    } finally {
      t();
    }
  }
} });
function y(i2, t2) {
  return new l(i2, t2);
}
function w(i2) {
  for (var t2 = i2.s; void 0 !== t2; t2 = t2.n) if (t2.S.i !== t2.i || !t2.S.h() || t2.S.i !== t2.i) return true;
  return false;
}
function _(i2) {
  for (var t2 = i2.s; void 0 !== t2; t2 = t2.n) {
    var n2 = t2.S.n;
    if (void 0 !== n2) t2.r = n2;
    t2.S.n = t2;
    t2.i = -1;
    if (void 0 === t2.n) {
      i2.s = t2;
      break;
    }
  }
}
function b(i2) {
  var t2 = i2.s, n2 = void 0;
  while (void 0 !== t2) {
    var r2 = t2.p;
    if (-1 === t2.i) {
      t2.S.U(t2);
      if (void 0 !== r2) r2.n = t2.n;
      if (void 0 !== t2.n) t2.n.p = r2;
    } else n2 = t2;
    t2.S.n = t2.r;
    if (void 0 !== t2.r) t2.r = void 0;
    t2 = r2;
  }
  i2.s = n2;
}
function p(i2, t2) {
  l.call(this, void 0);
  this.x = i2;
  this.s = void 0;
  this.g = d - 1;
  this.f = 4;
  this.W = null == t2 ? void 0 : t2.watched;
  this.Z = null == t2 ? void 0 : t2.unwatched;
  this.name = null == t2 ? void 0 : t2.name;
}
p.prototype = new l();
p.prototype.h = function() {
  this.f &= -3;
  if (1 & this.f) return false;
  if (32 == (36 & this.f)) return true;
  this.f &= -5;
  if (this.g === d) return true;
  this.g = d;
  this.f |= 1;
  if (this.i > 0 && !w(this)) {
    this.f &= -2;
    return true;
  }
  var i2 = r;
  try {
    _(this);
    r = this;
    var t2 = this.x();
    if (16 & this.f || this.v !== t2 || 0 === this.i) {
      this.v = t2;
      this.f &= -17;
      this.i++;
    }
  } catch (i3) {
    this.v = i3;
    this.f |= 16;
    this.i++;
  }
  r = i2;
  b(this);
  this.f &= -2;
  return true;
};
p.prototype.S = function(i2) {
  if (void 0 === this.t) {
    this.f |= 36;
    for (var t2 = this.s; void 0 !== t2; t2 = t2.n) t2.S.S(t2);
  }
  l.prototype.S.call(this, i2);
};
p.prototype.U = function(i2) {
  if (void 0 !== this.t) {
    l.prototype.U.call(this, i2);
    if (void 0 === this.t) {
      this.f &= -33;
      for (var t2 = this.s; void 0 !== t2; t2 = t2.n) t2.S.U(t2);
    }
  }
};
p.prototype.N = function() {
  if (!(2 & this.f)) {
    this.f |= 6;
    for (var i2 = this.t; void 0 !== i2; i2 = i2.x) i2.t.N();
  }
};
Object.defineProperty(p.prototype, "value", { get: function() {
  if (1 & this.f) throw new Error("Cycle detected");
  var i2 = a(this);
  this.h();
  if (void 0 !== i2) i2.i = this.i;
  if (16 & this.f) throw this.v;
  return this.v;
} });
function g(i2, t2) {
  return new p(i2, t2);
}
function S(i2) {
  var n2 = i2.m;
  i2.m = void 0;
  if ("function" == typeof n2) {
    s++;
    var o2 = r;
    r = void 0;
    try {
      n2();
    } catch (t2) {
      i2.f &= -2;
      i2.f |= 8;
      m(i2);
      throw t2;
    } finally {
      r = o2;
      t();
    }
  }
}
function m(i2) {
  for (var t2 = i2.s; void 0 !== t2; t2 = t2.n) t2.S.U(t2);
  i2.x = void 0;
  i2.s = void 0;
  S(i2);
}
function x(i2) {
  if (r !== this) throw new Error("Out-of-order effect");
  b(this);
  r = i2;
  this.f &= -2;
  if (8 & this.f) m(this);
  t();
}
function E(i2, t2) {
  this.x = i2;
  this.m = void 0;
  this.s = void 0;
  this.u = void 0;
  this.f = 32;
  this.name = null == t2 ? void 0 : t2.name;
  if (f) f.push(this);
}
E.prototype.c = function() {
  var i2 = this.S();
  try {
    if (8 & this.f) return;
    if (void 0 === this.x) return;
    var t2 = this.x();
    if ("function" == typeof t2) this.m = t2;
  } finally {
    i2();
  }
};
E.prototype.S = function() {
  if (1 & this.f) throw new Error("Cycle detected");
  this.f |= 1;
  this.f &= -9;
  S(this);
  _(this);
  s++;
  var i2 = r;
  r = this;
  return x.bind(this, i2);
};
E.prototype.N = function() {
  if (!(2 & this.f)) {
    this.f |= 2;
    this.u = h;
    h = this;
  }
};
E.prototype.d = function() {
  this.f |= 8;
  if (!(1 & this.f)) m(this);
};
E.prototype.dispose = function() {
  this.d();
};
function j(i2, t2) {
  var n2 = new E(i2, t2);
  try {
    n2.c();
  } catch (i3) {
    n2.d();
    throw i3;
  }
  var r2 = n2.d.bind(n2);
  r2[Symbol.dispose] = r2;
  return r2;
}

// node_modules/@formspec-org/webcomponent/dist/dom-utils.js
var FOCUSABLE_SELECTOR = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
function focusFirstIn(container) {
  const target = container.querySelector(FOCUSABLE_SELECTOR);
  (target || container).focus();
  return target || container;
}

// node_modules/@formspec-org/webcomponent/dist/components/layout.js
var POPUP_EDGE_PADDING = 8;
var POPUP_TRIGGER_GAP = 8;
function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}
function positionOverlayNearTrigger(triggerEl, overlayEl, placement = "bottom") {
  const triggerRect = triggerEl.getBoundingClientRect();
  const overlayRect = overlayEl.getBoundingClientRect();
  if (overlayRect.width <= 0 || overlayRect.height <= 0)
    return;
  let left = triggerRect.left + (triggerRect.width - overlayRect.width) / 2;
  let top = triggerRect.bottom + POPUP_TRIGGER_GAP;
  if (placement === "top") {
    top = triggerRect.top - overlayRect.height - POPUP_TRIGGER_GAP;
  } else if (placement === "right") {
    left = triggerRect.right + POPUP_TRIGGER_GAP;
    top = triggerRect.top + (triggerRect.height - overlayRect.height) / 2;
  } else if (placement === "left") {
    left = triggerRect.left - overlayRect.width - POPUP_TRIGGER_GAP;
    top = triggerRect.top + (triggerRect.height - overlayRect.height) / 2;
  }
  left = clamp(left, POPUP_EDGE_PADDING, Math.max(POPUP_EDGE_PADDING, window.innerWidth - overlayRect.width - POPUP_EDGE_PADDING));
  top = clamp(top, POPUP_EDGE_PADDING, Math.max(POPUP_EDGE_PADDING, window.innerHeight - overlayRect.height - POPUP_EDGE_PADDING));
  overlayEl.style.position = "fixed";
  overlayEl.style.inset = "auto";
  overlayEl.style.left = `${Math.round(left)}px`;
  overlayEl.style.top = `${Math.round(top)}px`;
  overlayEl.style.margin = "0";
  overlayEl.style.maxHeight = `${Math.max(120, window.innerHeight - POPUP_EDGE_PADDING * 2)}px`;
}
var PagePlugin = {
  type: "Page",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("section");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-page";
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    if (comp.title) {
      const headingLevel = comp.headingLevel || "h2";
      const h2 = document.createElement(headingLevel);
      h2.textContent = comp.title;
      el2.appendChild(h2);
    }
    if (comp.description) {
      const desc = document.createElement("p");
      desc.className = "formspec-page-description";
      desc.textContent = comp.description;
      el2.appendChild(desc);
    }
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var StackPlugin = {
  type: "Stack",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-stack";
    if (comp.direction === "horizontal")
      el2.classList.add("formspec-stack--horizontal");
    if (comp.align)
      el2.dataset.align = comp.align;
    if (comp.wrap)
      el2.classList.add("formspec-stack--wrap");
    if (comp.gap)
      el2.style.gap = String(ctx.resolveToken(comp.gap));
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var GridPlugin = {
  type: "Grid",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-grid";
    if (comp.columns != null) {
      if (typeof comp.columns === "number") {
        el2.dataset.columns = String(comp.columns);
      } else {
        el2.style.gridTemplateColumns = comp.columns;
      }
    }
    if (comp.gap)
      el2.style.gap = String(ctx.resolveToken(comp.gap));
    if (comp.rowGap)
      el2.style.rowGap = String(comp.rowGap);
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var DividerPlugin = {
  type: "Divider",
  render: (comp, parent, ctx) => {
    if (comp.label) {
      const wrapper = document.createElement("div");
      if (comp.id)
        wrapper.id = comp.id;
      wrapper.className = "formspec-divider formspec-divider--labeled";
      const lineBefore = document.createElement("hr");
      lineBefore.className = "formspec-divider-line";
      const labelEl = document.createElement("span");
      labelEl.className = "formspec-divider-label";
      labelEl.textContent = comp.label;
      const lineAfter = document.createElement("hr");
      lineAfter.className = "formspec-divider-line";
      wrapper.appendChild(lineBefore);
      wrapper.appendChild(labelEl);
      wrapper.appendChild(lineAfter);
      ctx.applyCssClass(wrapper, comp);
      ctx.applyAccessibility(wrapper, comp);
      ctx.applyStyle(wrapper, comp.style);
      parent.appendChild(wrapper);
    } else {
      const hr = document.createElement("hr");
      if (comp.id)
        hr.id = comp.id;
      hr.className = "formspec-divider";
      ctx.applyCssClass(hr, comp);
      ctx.applyAccessibility(hr, comp);
      ctx.applyStyle(hr, comp.style);
      parent.appendChild(hr);
    }
  }
};
var CollapsiblePlugin = {
  type: "Collapsible",
  render: (comp, parent, ctx) => {
    const details = document.createElement("details");
    if (comp.id)
      details.id = comp.id;
    details.className = "formspec-collapsible";
    if (comp.defaultOpen)
      details.open = true;
    const summary = document.createElement("summary");
    summary.textContent = comp.title || "Details";
    details.appendChild(summary);
    const content = document.createElement("div");
    content.className = "formspec-collapsible-content";
    details.appendChild(content);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, content, ctx.prefix);
      }
    }
    ctx.applyCssClass(details, comp);
    ctx.applyAccessibility(details, comp);
    ctx.applyStyle(details, comp.style);
    parent.appendChild(details);
  }
};
var ColumnsPlugin = {
  type: "Columns",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-columns";
    if (Array.isArray(comp.widths) && comp.widths.length > 0) {
      el2.style.gridTemplateColumns = comp.widths.join(" ");
    } else if (comp.columnCount) {
      el2.dataset.columns = String(comp.columnCount);
    }
    if (comp.gap)
      el2.style.gap = String(ctx.resolveToken(comp.gap));
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var PanelPlugin = {
  type: "Panel",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-panel";
    if (comp.position) {
      el2.dataset.position = comp.position;
      el2.style.order = comp.position === "left" ? "-1" : "1";
    }
    if (comp.width)
      el2.style.width = comp.width;
    if (comp.title) {
      const header = document.createElement("div");
      header.className = "formspec-panel-header";
      header.textContent = comp.title;
      el2.appendChild(header);
    }
    const body = document.createElement("div");
    body.className = "formspec-panel-body";
    el2.appendChild(body);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, body, ctx.prefix);
      }
    }
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var AccordionPlugin = {
  type: "Accordion",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-accordion";
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    const bindKey = comp.bind;
    const labels = comp.labels || [];
    const detailsEls = [];
    let previousCount = 0;
    if (bindKey) {
      const fullName = ctx.prefix ? `${ctx.prefix}.${bindKey}` : bindKey;
      const item = ctx.findItemByKey(bindKey);
      ctx.cleanupFns.push(j(() => {
        const count = ctx.engine.repeats[fullName]?.value || 0;
        const expandedIndex = typeof comp.defaultOpen === "number" ? comp.defaultOpen : count > 0 ? count - 1 : -1;
        el2.replaceChildren();
        detailsEls.length = 0;
        for (let i2 = 0; i2 < count; i2++) {
          const details = document.createElement("details");
          details.className = "formspec-accordion-item";
          if (i2 === expandedIndex || count > previousCount && i2 === count - 1) {
            details.open = true;
          }
          const summary = document.createElement("summary");
          summary.textContent = labels[i2] || `Section ${i2 + 1}`;
          details.appendChild(summary);
          const content = document.createElement("div");
          content.className = "formspec-accordion-content";
          const instancePrefix = `${fullName}[${i2}]`;
          for (const child of comp.children || []) {
            ctx.renderComponent(child, content, instancePrefix);
          }
          const removeBtn = document.createElement("button");
          removeBtn.type = "button";
          removeBtn.className = "formspec-repeat-add";
          removeBtn.textContent = `Remove ${item?.label || bindKey}`;
          removeBtn.addEventListener("click", () => {
            ctx.engine.removeRepeatInstance(fullName, i2);
          });
          content.appendChild(removeBtn);
          details.appendChild(content);
          details.addEventListener("toggle", () => {
            if (details.open && !comp.allowMultiple) {
              detailsEls.forEach((d2) => {
                if (d2 !== details)
                  d2.open = false;
              });
            }
          });
          el2.appendChild(details);
          detailsEls.push(details);
        }
        previousCount = count;
      }));
      const addBtn = document.createElement("button");
      addBtn.type = "button";
      addBtn.className = "formspec-repeat-add";
      addBtn.textContent = `Add ${item?.label || bindKey}`;
      addBtn.addEventListener("click", () => {
        ctx.engine.addRepeatInstance(fullName);
      });
      parent.appendChild(addBtn);
    } else {
      const children = comp.children || [];
      for (let i2 = 0; i2 < children.length; i2++) {
        const details = document.createElement("details");
        details.className = "formspec-accordion-item";
        if (comp.defaultOpen === i2)
          details.open = true;
        const summary = document.createElement("summary");
        summary.textContent = labels[i2] || `Section ${i2 + 1}`;
        details.appendChild(summary);
        const content = document.createElement("div");
        content.className = "formspec-accordion-content";
        ctx.renderComponent(children[i2], content, ctx.prefix);
        details.appendChild(content);
        details.addEventListener("toggle", () => {
          if (details.open && !comp.allowMultiple) {
            detailsEls.forEach((d2) => {
              if (d2 !== details)
                d2.open = false;
            });
          }
        });
        el2.appendChild(details);
        detailsEls.push(details);
      }
    }
  }
};
var ModalPlugin = {
  type: "Modal",
  render: (comp, parent, ctx) => {
    const placement = comp.placement || "bottom";
    const dialog = document.createElement("dialog");
    if (comp.id)
      dialog.id = comp.id;
    dialog.className = "formspec-modal";
    if (comp.size)
      dialog.dataset.size = comp.size;
    if (comp.closable !== false) {
      const closeBtn = document.createElement("button");
      closeBtn.type = "button";
      closeBtn.className = "formspec-modal-close";
      closeBtn.innerHTML = '<span aria-hidden="true">\xD7</span>';
      closeBtn.setAttribute("aria-label", "Close");
      closeBtn.addEventListener("click", () => dialog.close());
      dialog.appendChild(closeBtn);
    }
    if (comp.title) {
      const titleId = `${comp.id || "modal"}-title`;
      const titleEl = document.createElement("h2");
      titleEl.className = "formspec-modal-title";
      titleEl.id = titleId;
      titleEl.textContent = comp.title;
      dialog.appendChild(titleEl);
      dialog.setAttribute("aria-labelledby", titleId);
    } else if (comp.triggerLabel) {
      dialog.setAttribute("aria-label", comp.triggerLabel);
    }
    const content = document.createElement("div");
    content.className = "formspec-modal-content";
    dialog.appendChild(content);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, content, ctx.prefix);
      }
    }
    ctx.applyCssClass(dialog, comp);
    ctx.applyAccessibility(dialog, comp);
    ctx.applyStyle(dialog, comp.style);
    parent.appendChild(dialog);
    const triggerMode = comp.trigger || "button";
    if (triggerMode === "auto") {
      if (comp.when) {
        const exprFn = ctx.engine.compileExpression(comp.when, ctx.prefix);
        ctx.cleanupFns.push(j(() => {
          const shouldOpen = !!exprFn();
          if (shouldOpen && !dialog.open) {
            dialog.showModal();
            queueMicrotask(() => focusFirstIn(dialog));
          } else if (!shouldOpen && dialog.open) {
            dialog.close();
          }
        }));
      } else {
        queueMicrotask(() => {
          if (!dialog.open)
            dialog.showModal();
          focusFirstIn(dialog);
        });
      }
      return;
    }
    const triggerBtn = document.createElement("button");
    triggerBtn.type = "button";
    triggerBtn.className = "formspec-modal-trigger";
    triggerBtn.textContent = comp.triggerLabel || "Open";
    const repositionDialog = () => {
      if (dialog.open)
        positionOverlayNearTrigger(triggerBtn, dialog, placement);
    };
    triggerBtn.addEventListener("click", () => {
      if (!dialog.open)
        dialog.showModal();
      queueMicrotask(() => {
        repositionDialog();
        focusFirstIn(dialog);
      });
    });
    window.addEventListener("resize", repositionDialog);
    window.addEventListener("scroll", repositionDialog, true);
    ctx.cleanupFns.push(() => {
      window.removeEventListener("resize", repositionDialog);
      window.removeEventListener("scroll", repositionDialog, true);
    });
    dialog.addEventListener("close", () => triggerBtn.focus());
    parent.appendChild(triggerBtn);
  }
};
var PopoverPlugin = {
  type: "Popover",
  render: (comp, parent, ctx) => {
    const placement = comp.placement || "bottom";
    const wrapper = document.createElement("div");
    if (comp.id)
      wrapper.id = comp.id;
    wrapper.className = "formspec-popover";
    const triggerBtn = document.createElement("button");
    triggerBtn.type = "button";
    triggerBtn.className = "formspec-popover-trigger";
    triggerBtn.setAttribute("aria-haspopup", "dialog");
    triggerBtn.setAttribute("aria-expanded", "false");
    const triggerPath = comp.triggerBind ? ctx.prefix ? `${ctx.prefix}.${comp.triggerBind}` : comp.triggerBind : null;
    const triggerSignal = triggerPath ? ctx.engine.signals[triggerPath] : null;
    const fallbackLabel = comp.triggerLabel || "Open";
    if (triggerSignal) {
      ctx.cleanupFns.push(j(() => {
        const val = triggerSignal.value;
        triggerBtn.textContent = val === void 0 || val === null || val === "" ? fallbackLabel : String(val);
      }));
    } else {
      triggerBtn.textContent = fallbackLabel;
    }
    const content = document.createElement("div");
    content.className = "formspec-popover-content";
    content.setAttribute("role", "dialog");
    content.setAttribute("aria-label", comp.title || comp.triggerLabel || "Popover");
    if (comp.placement) {
      content.dataset.placement = comp.placement;
    }
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, content, ctx.prefix);
      }
    }
    const focusFirstInContent = () => focusFirstIn(content);
    const closePopover = () => {
      const contentAny2 = content;
      if (typeof contentAny2.hidePopover === "function") {
        try {
          contentAny2.hidePopover();
        } catch {
        }
      } else {
        content.hidden = true;
      }
      triggerBtn.setAttribute("aria-expanded", "false");
      triggerBtn.focus();
    };
    content.addEventListener("keydown", (e2) => {
      if (e2.key === "Escape") {
        e2.stopPropagation();
        closePopover();
      }
    });
    const contentAny = content;
    if (typeof contentAny.showPopover === "function") {
      contentAny.popover = "auto";
      triggerBtn.addEventListener("click", () => {
        contentAny.togglePopover();
        const isOpen = contentAny.matches(":popover-open");
        triggerBtn.setAttribute("aria-expanded", String(isOpen));
        if (isOpen) {
          queueMicrotask(() => {
            positionOverlayNearTrigger(triggerBtn, content, placement);
            focusFirstInContent();
          });
        }
      });
    } else {
      content.hidden = true;
      const onClickOutside = (e2) => {
        if (!wrapper.contains(e2.target))
          closePopover();
      };
      triggerBtn.addEventListener("click", () => {
        content.hidden = !content.hidden;
        triggerBtn.setAttribute("aria-expanded", String(!content.hidden));
        if (!content.hidden) {
          queueMicrotask(() => {
            positionOverlayNearTrigger(triggerBtn, content, placement);
            focusFirstInContent();
          });
          document.addEventListener("click", onClickOutside, true);
        } else {
          document.removeEventListener("click", onClickOutside, true);
        }
      });
      ctx.cleanupFns.push(() => document.removeEventListener("click", onClickOutside, true));
    }
    wrapper.appendChild(triggerBtn);
    wrapper.appendChild(content);
    ctx.applyCssClass(wrapper, comp);
    ctx.applyAccessibility(wrapper, comp);
    ctx.applyStyle(wrapper, comp.style);
    parent.appendChild(wrapper);
  }
};

// node_modules/@formspec-org/types/dist/widget-vocabulary.js
var KNOWN_COMPONENT_TYPES = /* @__PURE__ */ new Set([
  "TextInput",
  "NumberInput",
  "Select",
  "Toggle",
  "Checkbox",
  "DatePicker",
  "RadioGroup",
  "CheckboxGroup",
  "Slider",
  "Rating",
  "FileUpload",
  "Signature",
  "MoneyInput",
  "Stack",
  "Card",
  "Accordion",
  "Collapsible",
  "Heading",
  "Text",
  "Divider",
  "Alert",
  "Tabs",
  "Page"
]);
var SPEC_WIDGET_TO_COMPONENT = {
  textinput: "TextInput",
  textarea: "TextInput",
  richtext: "TextInput",
  password: "TextInput",
  color: "TextInput",
  numberinput: "NumberInput",
  stepper: "NumberInput",
  slider: "Slider",
  rating: "Rating",
  checkbox: "Checkbox",
  toggle: "Toggle",
  yesno: "Toggle",
  datepicker: "DatePicker",
  datetimepicker: "DatePicker",
  timepicker: "DatePicker",
  dateinput: "TextInput",
  datetimeinput: "TextInput",
  timeinput: "TextInput",
  dropdown: "Select",
  radio: "RadioGroup",
  autocomplete: "Select",
  segmented: "RadioGroup",
  likert: "RadioGroup",
  checkboxgroup: "CheckboxGroup",
  multiselect: "CheckboxGroup",
  fileupload: "FileUpload",
  camera: "FileUpload",
  signature: "Signature",
  moneyinput: "MoneyInput",
  urlinput: "TextInput",
  section: "Stack",
  card: "Card",
  accordion: "Accordion",
  tab: "Stack",
  heading: "Heading",
  paragraph: "Text",
  divider: "Divider",
  banner: "Alert"
};
var COMPATIBILITY_MATRIX = {
  string: ["TextInput", "Select", "RadioGroup"],
  text: ["TextInput"],
  decimal: ["NumberInput", "Slider", "Rating", "TextInput"],
  integer: ["NumberInput", "Slider", "Rating", "TextInput"],
  boolean: ["Toggle", "Checkbox"],
  date: ["DatePicker", "TextInput"],
  dateTime: ["DatePicker", "TextInput"],
  time: ["DatePicker", "TextInput"],
  uri: ["TextInput"],
  choice: ["Select", "RadioGroup", "TextInput"],
  multiChoice: ["CheckboxGroup"],
  attachment: ["FileUpload", "Signature"],
  money: ["MoneyInput", "NumberInput", "TextInput"]
};
function normalizeWidgetToken(widget) {
  return widget.replace(/[\s_-]+/g, "").toLowerCase();
}
function widgetTokenToComponent(widget) {
  if (!widget)
    return null;
  if (widget.startsWith("x-"))
    return widget;
  if (KNOWN_COMPONENT_TYPES.has(widget))
    return widget;
  return SPEC_WIDGET_TO_COMPONENT[normalizeWidgetToken(widget)] ?? null;
}

// node_modules/@formspec-org/layout/dist/theme-resolver.js
function normalizeCssClass(val) {
  if (!val)
    return [];
  if (Array.isArray(val))
    return val.flatMap((c2) => c2.split(/\s+/).filter(Boolean));
  return val.split(/\s+/).filter(Boolean);
}
function extractUtilityPrefix(cls) {
  const match = cls.match(/^(-?[a-z]+)-/);
  return match ? match[1] + "-" : null;
}
var twMergeFn = null;
function applyClassStrategy(classes, strategy) {
  if (strategy === "tailwind-merge") {
    if (!twMergeFn) {
      console.warn('classStrategy "tailwind-merge" requires calling setTailwindMerge(twMerge) at startup. Falling back to union strategy.');
      return classes;
    }
    const merged = twMergeFn(classes.join(" "));
    return merged.split(/\s+/).filter(Boolean);
  }
  return classes;
}
function asRecord(val) {
  if (!val || typeof val !== "object" || Array.isArray(val))
    return null;
  return val;
}
function mergeBlocks(lower, higher) {
  const merged = { ...lower };
  if (higher.widget !== void 0)
    merged.widget = higher.widget;
  if (higher.labelPosition !== void 0)
    merged.labelPosition = higher.labelPosition;
  if (higher.fallback !== void 0)
    merged.fallback = higher.fallback;
  const replaceClasses = normalizeCssClass(higher.cssClassReplace);
  if (replaceClasses.length > 0) {
    const lowerClasses2 = normalizeCssClass(merged.cssClass);
    const replaceSet = new Set(replaceClasses);
    const replacePrefixes = replaceClasses.map(extractUtilityPrefix).filter(Boolean);
    const filtered = lowerClasses2.filter((cls) => {
      if (replaceSet.has(cls))
        return false;
      const prefix = extractUtilityPrefix(cls);
      if (prefix && replacePrefixes.includes(prefix))
        return false;
      return true;
    });
    const union = /* @__PURE__ */ new Set([...filtered, ...replaceClasses]);
    merged.cssClass = [...union];
    const lowerReplace = normalizeCssClass(merged.cssClassReplace);
    merged.cssClassReplace = [.../* @__PURE__ */ new Set([...lowerReplace, ...replaceClasses])];
  }
  const lowerClasses = normalizeCssClass(merged.cssClass);
  const higherClasses = normalizeCssClass(higher.cssClass);
  if (higherClasses.length > 0) {
    const union = /* @__PURE__ */ new Set([...lowerClasses, ...higherClasses]);
    merged.cssClass = [...union];
  }
  if (higher.widgetConfig !== void 0) {
    const lowerCfg = asRecord(merged.widgetConfig) || {};
    const higherCfg = asRecord(higher.widgetConfig) || {};
    const combined = { ...lowerCfg, ...higherCfg };
    const lowerSlots = asRecord(lowerCfg["x-classes"]);
    const higherSlots = asRecord(higherCfg["x-classes"]);
    if (lowerSlots || higherSlots) {
      combined["x-classes"] = {
        ...lowerSlots || {},
        ...higherSlots || {}
      };
    }
    merged.widgetConfig = combined;
  }
  if (higher.style !== void 0) {
    merged.style = { ...merged.style, ...higher.style };
  }
  if (higher.accessibility !== void 0) {
    merged.accessibility = { ...merged.accessibility, ...higher.accessibility };
  }
  return merged;
}
function selectorMatches(match, item) {
  if (match.type === void 0 && match.dataType === void 0)
    return false;
  if (match.type !== void 0 && match.type !== item.type)
    return false;
  if (match.dataType !== void 0 && match.dataType !== item.dataType)
    return false;
  return true;
}
function resolvePresentation(theme, item, tier1) {
  let result = {};
  if (tier1?.formPresentation) {
    const fp = tier1.formPresentation;
    if (fp.labelPosition)
      result.labelPosition = fp.labelPosition;
  }
  if (tier1?.itemPresentation) {
    const ip = tier1.itemPresentation;
    if (ip.widgetHint)
      result.widget = ip.widgetHint;
    if (ip.layout?.collapsible) {
    }
  }
  if (!theme)
    return result;
  if (theme.defaults) {
    result = mergeBlocks(result, theme.defaults);
  }
  if (theme.selectors) {
    for (const selector of theme.selectors) {
      if (selectorMatches(selector.match, item)) {
        result = mergeBlocks(result, selector.apply);
      }
    }
  }
  if (theme.items?.[item.key]) {
    result = mergeBlocks(result, theme.items[item.key]);
  }
  if (theme.classStrategy === "tailwind-merge" && result.cssClass) {
    result = { ...result, cssClass: applyClassStrategy(normalizeCssClass(result.cssClass), theme.classStrategy) };
  }
  delete result.cssClassReplace;
  return result;
}
function resolveWidget(presentation, isAvailable) {
  if (!presentation.widget)
    return null;
  const preferred = widgetTokenToComponent(presentation.widget);
  if (preferred && isAvailable(preferred))
    return preferred;
  if (presentation.fallback) {
    for (const fb of presentation.fallback) {
      const fallback = widgetTokenToComponent(fb);
      if (fallback && isAvailable(fallback))
        return fallback;
    }
  }
  const tried = [presentation.widget, ...presentation.fallback || []].join(", ");
  console.warn(`Theme widget unavailable: tried [${tried}]. Falling back to default.`);
  return null;
}

// node_modules/@formspec-org/layout/dist/tokens.js
function resolveToken(val, componentTokens, themeTokens) {
  if (typeof val === "string" && val.startsWith("$token.")) {
    const tokenKey = val.substring(7);
    if (componentTokens && componentTokens[tokenKey] !== void 0) {
      return componentTokens[tokenKey];
    }
    if (themeTokens && themeTokens[tokenKey] !== void 0) {
      return themeTokens[tokenKey];
    }
    console.warn(`Unresolved token reference: ${val}`);
  }
  return val;
}

// node_modules/@formspec-org/layout/dist/responsive.js
function resolveResponsiveProps(comp, activeBreakpoint, breakpoints) {
  if (!comp.responsive || !activeBreakpoint)
    return comp;
  const numericBreakpoints = breakpoints ? (() => {
    const entries = Object.entries(breakpoints).filter((e2) => typeof e2[1] === "number");
    return entries.length > 0 ? Object.fromEntries(entries) : null;
  })() : null;
  if (!numericBreakpoints) {
    const overrides = comp.responsive[activeBreakpoint];
    if (!overrides)
      return comp;
    return { ...comp, ...overrides };
  }
  const activeWidth = numericBreakpoints[activeBreakpoint];
  if (activeWidth == null)
    return comp;
  const sortedNames = Object.entries(numericBreakpoints).filter(([name]) => comp.responsive[name]).sort(([, a2], [, b2]) => a2 - b2).filter(([, width]) => width <= activeWidth).map(([name]) => name);
  if (sortedNames.length === 0)
    return comp;
  let result = { ...comp };
  for (const name of sortedNames) {
    result = { ...result, ...comp.responsive[name] };
  }
  return result;
}

// node_modules/@formspec-org/layout/dist/params.js
function interpolateParams(node, params) {
  for (const key of Object.keys(node)) {
    if (typeof node[key] === "string") {
      node[key] = node[key].replace(/\{(\w+)\}/g, (_2, param) => {
        return params[param] !== void 0 ? params[param] : `{${param}}`;
      });
    } else if (Array.isArray(node[key])) {
      for (const child of node[key]) {
        if (typeof child === "object" && child !== null) {
          interpolateParams(child, params);
        }
      }
    } else if (typeof node[key] === "object" && node[key] !== null) {
      interpolateParams(node[key], params);
    }
  }
}

// node_modules/@formspec-org/layout/dist/defaults.js
function getDefaultComponent(item) {
  switch (item.dataType) {
    case "string":
      return "TextInput";
    case "text":
      return "TextInput";
    case "integer":
    case "decimal":
    case "number":
      return "NumberInput";
    case "boolean":
      return "Toggle";
    case "date":
      return "DatePicker";
    case "dateTime":
      return "DatePicker";
    case "time":
      return "DatePicker";
    case "uri":
      return "TextInput";
    case "choice":
      return "Select";
    case "multiChoice":
      return "CheckboxGroup";
    case "attachment":
      return "FileUpload";
    case "money":
      return "NumberInput";
    default:
      return "TextInput";
  }
}

// node_modules/@formspec-org/layout/dist/planner.js
var LAYOUT_COMPONENTS = /* @__PURE__ */ new Set([
  "Page",
  "Stack",
  "Grid",
  "Divider",
  "Collapsible",
  "Columns",
  "Panel",
  "Accordion",
  "Modal",
  "Popover"
]);
var INPUT_COMPONENTS = /* @__PURE__ */ new Set([
  "TextInput",
  "NumberInput",
  "Select",
  "Toggle",
  "Checkbox",
  "DatePicker",
  "RadioGroup",
  "CheckboxGroup",
  "Slider",
  "Rating",
  "FileUpload",
  "Signature",
  "MoneyInput"
]);
var DISPLAY_COMPONENTS = /* @__PURE__ */ new Set([
  "Heading",
  "Text",
  "Card",
  "Spacer",
  "Alert",
  "Badge",
  "ProgressBar",
  "Summary",
  "ValidationSummary"
]);
var INTERACTIVE_COMPONENTS = /* @__PURE__ */ new Set([
  "Tabs",
  "SubmitButton"
]);
var SPECIAL_COMPONENTS = /* @__PURE__ */ new Set([
  "ConditionalGroup",
  "DataTable"
]);
function classifyComponent(type) {
  if (LAYOUT_COMPONENTS.has(type))
    return "layout";
  if (INPUT_COMPONENTS.has(type))
    return "field";
  if (DISPLAY_COMPONENTS.has(type))
    return "display";
  if (INTERACTIVE_COMPONENTS.has(type))
    return "interactive";
  if (SPECIAL_COMPONENTS.has(type))
    return "special";
  return "layout";
}
var nodeIdCounter = 0;
function nextId(prefix) {
  return `${prefix}-${++nodeIdCounter}`;
}
function resolveTokenInContext(val, ctx) {
  return resolveToken(val, ctx.componentDocument?.tokens, ctx.theme?.tokens);
}
function resolveStyleTokens(style, ctx) {
  if (!style)
    return void 0;
  const resolved = {};
  for (const [k, v2] of Object.entries(style)) {
    resolved[k] = resolveTokenInContext(v2, ctx);
  }
  return resolved;
}
function normalizeCssClass2(val) {
  if (!val)
    return [];
  if (Array.isArray(val))
    return val.flatMap((c2) => c2.split(/\s+/).filter(Boolean));
  return val.split(/\s+/).filter(Boolean);
}
function resolveCssClasses(comp, ctx) {
  const raw = normalizeCssClass2(comp.cssClass);
  return raw.map((c2) => String(resolveTokenInContext(c2, ctx)));
}
var STRUCTURAL_KEYS = /* @__PURE__ */ new Set([
  "component",
  "children",
  "when",
  "responsive",
  "style",
  "cssClass",
  "accessibility",
  "params"
]);
function extractProps(comp) {
  const props = {};
  for (const key of Object.keys(comp)) {
    if (!STRUCTURAL_KEYS.has(key)) {
      props[key] = comp[key];
    }
  }
  return props;
}
function planComponentTree(tree, ctx, prefix = "", customComponentStack, applyThemePages = prefix === "") {
  if (!customComponentStack)
    customComponentStack = /* @__PURE__ */ new Set();
  if (applyThemePages && !prefix && ctx.theme?.pages?.length) {
    const themed = planThemePagesFromComponentTree(tree, ctx, customComponentStack);
    if (themed) {
      return applyGeneratedPageMode(themed, themed.component, ctx);
    }
  }
  const comp = resolveResponsiveProps(tree, ctx.activeBreakpoint ?? null, ctx.componentDocument?.breakpoints);
  const componentType = comp.component;
  const customComponents = ctx.componentDocument?.components;
  if (customComponents?.[componentType]) {
    if (customComponentStack.has(componentType)) {
      return {
        id: nextId("err"),
        component: "Text",
        category: "display",
        props: { text: `[Recursive component: ${componentType}]` },
        cssClasses: [],
        children: []
      };
    }
    const customDef = customComponents[componentType];
    const template = JSON.parse(JSON.stringify(customDef.tree));
    interpolateParams(template, comp.params || comp);
    customComponentStack.add(componentType);
    const result = planComponentTree(template, ctx, prefix, customComponentStack, false);
    customComponentStack.delete(componentType);
    return result;
  }
  const bindKey = comp.bind;
  const fullBindPath = bindKey ? prefix ? `${prefix}.${bindKey}` : bindKey : void 0;
  const item = fullBindPath ? ctx.findItem(fullBindPath) : null;
  const isRepeatGroup = item?.type === "group" && item?.repeatable === true && componentType !== "DataTable" && componentType !== "Accordion";
  const props = extractProps(comp);
  if (componentType === "TextInput" && item?.dataType === "text" && props.maxLines == null) {
    props.maxLines = 3;
  }
  if (props.gap !== void 0)
    props.gap = resolveTokenInContext(props.gap, ctx);
  if (props.size !== void 0)
    props.size = resolveTokenInContext(props.size, ctx);
  const node = {
    id: nextId(componentType.toLowerCase()),
    component: componentType,
    category: classifyComponent(componentType),
    props,
    style: resolveStyleTokens(comp.style, ctx),
    cssClasses: resolveCssClasses(comp, ctx),
    children: []
  };
  if (comp.accessibility) {
    node.accessibility = { ...comp.accessibility };
  }
  if (fullBindPath) {
    node.bindPath = fullBindPath;
  }
  if (item && item.type === "field") {
    node.fieldItem = {
      key: item.key ?? bindKey,
      label: item.label ?? bindKey,
      hint: item.hint,
      dataType: item.dataType
    };
    const itemDesc = {
      key: bindKey,
      type: "field",
      dataType: item.dataType
    };
    const tier1 = {
      formPresentation: ctx.formPresentation,
      itemPresentation: item.presentation
    };
    const presentation = resolvePresentation(ctx.theme, itemDesc, tier1);
    node.presentation = presentation;
    node.labelPosition = presentation.labelPosition ?? "top";
    const presClasses = normalizeCssClass2(presentation.cssClass);
    if (presClasses.length > 0) {
      const union = /* @__PURE__ */ new Set([...node.cssClasses, ...presClasses]);
      node.cssClasses = [...union];
    }
  }
  if (item && item.type === "display") {
    if (props.text == null) {
      props.text = item.label ?? "";
    }
    delete props.bind;
  }
  if (comp.when) {
    node.when = comp.when;
    node.whenPrefix = prefix;
    if (comp.fallback) {
      node.fallback = comp.fallback;
    }
  }
  if (isRepeatGroup && fullBindPath) {
    node.repeatGroup = bindKey;
    node.repeatPath = fullBindPath;
    node.isRepeatTemplate = true;
  }
  const SELF_MANAGED_GROUP_COMPONENTS = /* @__PURE__ */ new Set(["DataTable", "Accordion"]);
  if (fullBindPath && item?.type === "group" && !SELF_MANAGED_GROUP_COMPONENTS.has(componentType)) {
    node.scopeChange = true;
  }
  const childPrefix = isRepeatGroup && fullBindPath ? `${fullBindPath}[0]` : fullBindPath && item?.type === "group" ? fullBindPath : prefix;
  if (Array.isArray(comp.children)) {
    for (const child of comp.children) {
      node.children.push(planComponentTree(child, ctx, childPrefix, customComponentStack, false));
    }
  }
  if (applyThemePages) {
    return applyGeneratedPageMode(node, componentType, ctx);
  }
  return node;
}
function planDefinitionFallback(items, ctx, prefix = "", applyThemePages = prefix === "") {
  if (applyThemePages && !prefix && ctx.theme?.pages?.length) {
    const themed = planThemePagesFromDefinitionItems(items, ctx);
    if (themed.length > 0) {
      return themed;
    }
  }
  const nodes = [];
  for (const item of items) {
    nodes.push(planDefinitionItem(item, ctx, prefix));
  }
  return !prefix ? applyDefinitionPageMode(nodes, ctx) : nodes;
}
function applyDefinitionPageMode(nodes, ctx) {
  const pageMode = ctx.formPresentation?.pageMode;
  if (pageMode !== "wizard" && pageMode !== "tabs") {
    return nodes;
  }
  const { orphans, pages } = buildDefinitionPages(nodes, ctx.items);
  if (pages.length === 0) {
    return nodes;
  }
  return emitPageModePages(orphans, pages);
}
function planDefinitionItem(item, ctx, prefix = "") {
  const key = item.key || item.name;
  const fullPath = prefix ? `${prefix}.${key}` : key;
  const itemDesc = {
    key,
    type: item.type,
    dataType: item.dataType
  };
  const tier1 = {
    formPresentation: ctx.formPresentation,
    itemPresentation: item.presentation
  };
  const presentation = resolvePresentation(ctx.theme, itemDesc, tier1);
  if (item.type === "group") {
    const isRepeat = item.repeatable === true;
    const groupNode = {
      id: nextId("group"),
      component: "Stack",
      category: "layout",
      props: { title: item.label || key, bind: key },
      cssClasses: normalizeCssClass2(presentation.cssClass),
      children: [],
      bindPath: fullPath,
      scopeChange: true
    };
    if (isRepeat) {
      groupNode.repeatGroup = key;
      groupNode.repeatPath = fullPath;
      groupNode.isRepeatTemplate = true;
    }
    const childPrefix = isRepeat ? `${fullPath}[0]` : fullPath;
    if (Array.isArray(item.children)) {
      groupNode.children = planDefinitionFallback(item.children, ctx, childPrefix, false);
    }
    return groupNode;
  }
  if (item.type === "field") {
    const isAvailable = ctx.isComponentAvailable ?? (() => true);
    const themeWidget = resolveWidget(presentation, isAvailable);
    const tier1Widget = widgetTokenToComponent(item.presentation?.widgetHint);
    const widget = themeWidget || tier1Widget || getDefaultComponent(item);
    const fieldProps = { bind: key };
    if (widget === "TextInput" && item.dataType === "text") {
      fieldProps.maxLines = 3;
    }
    return {
      id: nextId("field"),
      component: widget,
      category: "field",
      props: fieldProps,
      cssClasses: normalizeCssClass2(presentation.cssClass),
      children: [],
      bindPath: fullPath,
      fieldItem: {
        key,
        label: item.label ?? key,
        hint: item.hint,
        dataType: item.dataType,
        options: item.options,
        optionSet: item.optionSet
      },
      presentation,
      labelPosition: presentation.labelPosition ?? "top"
    };
  }
  const displayWidget = widgetTokenToComponent(item.presentation?.widgetHint) ?? "Text";
  const displayNode = {
    id: nextId("display"),
    component: displayWidget,
    category: "display",
    props: { text: item.label || "" },
    cssClasses: normalizeCssClass2(presentation.cssClass),
    children: []
  };
  if (item.relevant) {
    displayNode.when = item.relevant;
    displayNode.whenPrefix = prefix;
  }
  return displayNode;
}
function planThemePagesFromDefinitionItems(items, ctx) {
  const pageNodes = buildThemePageNodes((regionPath) => {
    const item = findItemAtPath(items, regionPath);
    if (!item)
      return null;
    const parentPath = getParentPath(regionPath);
    return planDefinitionItem(item, ctx, parentPath);
  }, items, ctx);
  if (pageNodes.length === 0) {
    return [];
  }
  const assignedTopLevelKeys = collectAssignedTopLevelKeys(items, ctx.theme.pages);
  const unassigned = items.filter((item) => !assignedTopLevelKeys.has(item.key)).map((item) => planDefinitionItem(item, ctx, ""));
  const pageMode = ctx.formPresentation?.pageMode;
  if ((pageMode === "wizard" || pageMode === "tabs") && pageNodes.length > 0) {
    const pages = pageNodes.map((pn) => ({
      title: String(pn.props?.title || ""),
      children: pn.children
    }));
    return emitPageModePages(unassigned, pages);
  }
  return [...pageNodes, ...unassigned];
}
function planThemePagesFromComponentTree(tree, ctx, customComponentStack) {
  const baseCtx = withoutThemePages(ctx);
  const root = planComponentTree(tree, baseCtx, "", customComponentStack, false);
  const pageNodes = buildThemePageNodes((regionPath) => {
    const componentNode = findComponentNodeByPath(ctx.items, tree, regionPath);
    if (!componentNode) {
      return null;
    }
    return planComponentTree(componentNode, baseCtx, "", customComponentStack, false);
  }, ctx.items, ctx);
  if (pageNodes.length === 0) {
    return null;
  }
  const assignedTopLevelKeys = collectAssignedTopLevelKeys(ctx.items, ctx.theme.pages);
  const unassigned = ctx.items.filter((item) => !assignedTopLevelKeys.has(item.key)).map((item) => {
    const componentNode = findComponentNodeByPath(ctx.items, tree, item.key);
    return componentNode ? planComponentTree(componentNode, baseCtx, "", customComponentStack, false) : planDefinitionItem(item, baseCtx, "");
  });
  return {
    ...root,
    children: [...pageNodes, ...unassigned]
  };
}
function buildThemePageNodes(planRegionNode, items, ctx) {
  const pages = Array.isArray(ctx.theme?.pages) ? ctx.theme.pages : [];
  const nodes = [];
  for (const page of pages) {
    const regionNodes = [];
    for (const region of Array.isArray(page.regions) ? page.regions : []) {
      const regionPath = findItemPathByKey(items, region.key);
      if (!regionPath)
        continue;
      const plannedNode = planRegionNode(regionPath);
      if (!plannedNode)
        continue;
      if (regionPath.includes(".") && plannedNode.props?.bind) {
        plannedNode.props.bind = regionPath;
        if (plannedNode.bindPath && plannedNode.bindPath !== regionPath) {
          plannedNode.bindPath = regionPath;
        }
      }
      const wrapped = wrapRegionNode(plannedNode, region, ctx.activeBreakpoint ?? null);
      if (wrapped) {
        regionNodes.push(wrapped);
      }
    }
    if (regionNodes.length === 0)
      continue;
    nodes.push({
      id: nextId("page"),
      component: "Page",
      category: "layout",
      props: {
        id: page.id,
        title: page.title,
        ...page.description ? { description: page.description } : {}
      },
      cssClasses: [],
      children: [
        {
          id: nextId("grid"),
          component: "Grid",
          category: "layout",
          props: { columns: 12 },
          cssClasses: [],
          children: regionNodes
        }
      ]
    });
  }
  return nodes;
}
function wrapRegionNode(node, region, activeBreakpoint) {
  const resolved = resolveRegionPlacement(region, activeBreakpoint);
  if (resolved.hidden) {
    return null;
  }
  const style = {
    gridColumn: resolved.start !== void 0 ? `${resolved.start} / span ${resolved.span}` : `span ${resolved.span}`
  };
  return {
    id: nextId("region"),
    component: "Stack",
    category: "layout",
    props: {},
    style,
    cssClasses: [],
    children: [node]
  };
}
function emitPageModePages(orphans, pages) {
  if (pages.length === 0) {
    return orphans;
  }
  const pageNodes = pages.map((page, index) => ({
    id: nextId("page"),
    component: "Page",
    category: "layout",
    props: { title: page.title || `Page ${index + 1}` },
    cssClasses: [],
    children: page.children
  }));
  return [...orphans, ...pageNodes];
}
function applyGeneratedPageMode(rootNode, componentType, ctx) {
  const pageMode = ctx.formPresentation?.pageMode;
  if (pageMode !== "wizard" && pageMode !== "tabs") {
    return rootNode;
  }
  if (!isStudioGeneratedComponentDoc(ctx.componentDocument)) {
    return rootNode;
  }
  if (componentType !== "Stack" && componentType !== "Root") {
    return rootNode;
  }
  if (!Array.isArray(rootNode.children) || rootNode.children.length === 0) {
    return rootNode;
  }
  if (rootNode.children.some((child) => child.component === "Page")) {
    const orphans = rootNode.children.filter((node) => node.component !== "Page");
    const pages2 = rootNode.children.filter((node) => node.component === "Page");
    return {
      ...rootNode,
      children: [...orphans, ...pages2]
    };
  }
  const topLevelNodes = rootNode.children.slice(0, ctx.items.length);
  const preservedExtras = rootNode.children.slice(ctx.items.length);
  const orphanChildren = [];
  const pages = [];
  const pageByName = /* @__PURE__ */ new Map();
  let lastPage = null;
  let sawExplicitPage = false;
  for (let index = 0; index < ctx.items.length; index += 1) {
    const item = ctx.items[index];
    const node = topLevelNodes[index];
    if (!node)
      continue;
    if (item?.type === "group") {
      const pageName = getItemPageName(item);
      if (pageName) {
        sawExplicitPage = true;
        const page = pageByName.get(pageName) ?? { title: pageName, children: [] };
        if (!pageByName.has(pageName)) {
          pageByName.set(pageName, page);
          pages.push(page);
        }
        page.children.push(stripTitleFromGroupNode(node));
        lastPage = page;
      } else if (lastPage && sawExplicitPage) {
        lastPage.children.push(stripTitleFromGroupNode(node));
      } else {
        const title = String(item.label || node.props.title || node.props.bind || item.key || `Page ${pages.length + 1}`);
        pages.push({
          title,
          children: [stripTitleFromGroupNode(node)]
        });
        lastPage = pages[pages.length - 1];
      }
    } else {
      orphanChildren.push(node);
    }
  }
  if (pages.length === 0) {
    return rootNode;
  }
  return {
    ...rootNode,
    children: [...emitPageModePages(orphanChildren, pages), ...preservedExtras]
  };
}
function isStudioGeneratedComponentDoc(doc) {
  if (!doc || typeof doc !== "object")
    return false;
  return doc["x-studio-generated"] === true || doc.$formspecComponent == null;
}
function buildDefinitionPages(nodes, items) {
  const pageByName = /* @__PURE__ */ new Map();
  const pages = [];
  const orphans = [];
  let lastPage = null;
  let sawExplicitPage = false;
  for (let index = 0; index < items.length; index += 1) {
    const item = items[index];
    const node = nodes[index];
    if (!node)
      continue;
    if (item?.type !== "group") {
      orphans.push(node);
      continue;
    }
    const pageName = getItemPageName(item);
    if (pageName) {
      sawExplicitPage = true;
      const page = pageByName.get(pageName) ?? { title: pageName, children: [] };
      if (!pageByName.has(pageName)) {
        pageByName.set(pageName, page);
        pages.push(page);
      }
      page.children.push(stripTitleFromGroupNode(node));
      lastPage = page;
    } else if (lastPage && sawExplicitPage) {
      lastPage.children.push(stripTitleFromGroupNode(node));
    } else {
      const title = String(item.label || node.props.title || node.props.bind || item.key || `Page ${pages.length + 1}`);
      pages.push({
        title,
        children: [stripTitleFromGroupNode(node)]
      });
      lastPage = pages[pages.length - 1];
    }
  }
  for (let index = items.length; index < nodes.length; index += 1) {
    orphans.push(nodes[index]);
  }
  return { orphans, pages };
}
function getItemPageName(item) {
  const page = item?.presentation?.layout?.page;
  return typeof page === "string" && page.trim().length > 0 ? page.trim() : null;
}
function stripTitleFromGroupNode(node) {
  if (node.component !== "Stack") {
    return node;
  }
  const { title: _title, ...restProps } = node.props;
  return {
    ...node,
    props: restProps
  };
}
function resolveRegionPlacement(region, activeBreakpoint) {
  const override = activeBreakpoint && region?.responsive ? region.responsive[activeBreakpoint] : null;
  const span = typeof override?.span === "number" ? override.span : typeof region?.span === "number" ? region.span : 12;
  const start = typeof override?.start === "number" ? override.start : typeof region?.start === "number" ? region.start : void 0;
  const hidden = override?.hidden === true;
  return { span, start, hidden };
}
function collectAssignedTopLevelKeys(items, pages) {
  const assigned = /* @__PURE__ */ new Set();
  for (const page of Array.isArray(pages) ? pages : []) {
    for (const region of Array.isArray(page.regions) ? page.regions : []) {
      const path = findItemPathByKey(items, region.key);
      if (!path)
        continue;
      const topKey = path.includes(".") ? path.split(".")[0] : path;
      assigned.add(topKey);
    }
  }
  return assigned;
}
function withoutThemePages(ctx) {
  if (!ctx.theme?.pages) {
    return ctx;
  }
  const theme = { ...ctx.theme };
  delete theme.pages;
  return { ...ctx, theme };
}
function findItemPathByKey(items, key, prefix = "") {
  if (key.includes(".")) {
    return findItemAtPath(items, key) ? key : null;
  }
  for (const item of items) {
    const itemKey = item?.key || item?.name;
    if (!itemKey)
      continue;
    const fullPath = prefix ? `${prefix}.${itemKey}` : itemKey;
    if (itemKey === key) {
      return fullPath;
    }
    if (Array.isArray(item.children)) {
      const nested = findItemPathByKey(item.children, key, fullPath);
      if (nested)
        return nested;
    }
  }
  return null;
}
function findItemAtPath(items, path) {
  const segments = path.split(".").filter(Boolean);
  let current = items;
  for (let index = 0; index < segments.length; index += 1) {
    const segment = segments[index];
    const found = current.find((item) => item?.key === segment || item?.name === segment);
    if (!found)
      return null;
    if (index === segments.length - 1) {
      return found;
    }
    current = Array.isArray(found.children) ? found.children : [];
  }
  return null;
}
function getParentPath(path) {
  const segments = path.split(".").filter(Boolean);
  return segments.slice(0, -1).join(".");
}
function findComponentNodeByPath(_items, rootNode, path) {
  return findNodeByBindPath(rootNode, path, "");
}
function findNodeByBindPath(node, targetPath, currentPrefix) {
  const bindKey = node.bind;
  const fullPath = bindKey ? currentPrefix ? `${currentPrefix}.${bindKey}` : bindKey : currentPrefix;
  if (fullPath === targetPath && bindKey) {
    return node;
  }
  if (Array.isArray(node.children)) {
    for (const child of node.children) {
      const found = findNodeByBindPath(child, targetPath, fullPath);
      if (found)
        return found;
    }
  }
  return null;
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/shared.js
function resolveFieldPath(bind, prefix) {
  return prefix ? `${prefix}.${bind}` : bind;
}
function toFieldId(fieldPath) {
  return `field-${fieldPath.replace(/[\.\[\]]/g, "-")}`;
}
function resolveAndStripTokens(block, resolveToken3, comp) {
  const resolved = { ...block };
  if (resolved.style) {
    resolved.style = Object.fromEntries(Object.entries(resolved.style).map(([k, v2]) => [k, resolveToken3(v2)]));
  }
  if (resolved.cssClass) {
    resolved.cssClass = Array.isArray(resolved.cssClass) ? resolved.cssClass.map((c2) => resolveToken3(c2)) : resolveToken3(resolved.cssClass);
  }
  if (comp?.labelPosition) {
    resolved.labelPosition = comp.labelPosition;
  }
  return resolved;
}
function warnIfIncompatible(componentType, dataType) {
  if (COMPATIBILITY_MATRIX[dataType] && !COMPATIBILITY_MATRIX[dataType].includes(componentType)) {
    console.warn(`Incompatible component ${componentType} for dataType ${dataType}.`);
  }
}
function bindSharedFieldEffects(ctx, fieldPath, labelText, refs) {
  const disposers = [];
  const actualInput = refs.control.querySelector("input") || refs.control.querySelector("select") || refs.control.querySelector("textarea") || refs.control;
  disposers.push(j(() => {
    const isRequired = ctx.engine.requiredSignals[fieldPath]?.value ?? false;
    refs.label.textContent = labelText;
    if (isRequired) {
      const indicator = document.createElement("span");
      indicator.className = "formspec-required";
      indicator.setAttribute("aria-hidden", "true");
      indicator.textContent = " *";
      refs.label.appendChild(indicator);
    }
    actualInput.setAttribute("aria-required", String(isRequired));
  }));
  disposers.push(j(() => {
    ctx.touchedVersion.value;
    const error = ctx.engine.errorSignals[fieldPath]?.value;
    const submitDetail = ctx.latestSubmitDetailSignal?.value;
    const externalPath = fieldPath.replace(/\[(\d+)\]/g, (_2, p1) => `[${parseInt(p1) + 1}]`);
    const submitError = submitDetail?.validationReport?.results?.find((r2) => r2.severity === "error" && (r2.path === fieldPath || r2.path === externalPath || r2.path === `${fieldPath}[*]`))?.message;
    const effectiveError = error || submitError;
    const showError = ctx.touchedFields.has(fieldPath) ? effectiveError || "" : "";
    if (refs.error)
      refs.error.textContent = showError;
    actualInput.setAttribute("aria-invalid", String(!!showError));
    if (refs.onValidationChange)
      refs.onValidationChange(!!showError, showError);
  }));
  disposers.push(j(() => {
    const isReadonly = ctx.engine.readonlySignals[fieldPath]?.value ?? false;
    if (actualInput instanceof HTMLInputElement || actualInput instanceof HTMLTextAreaElement) {
      actualInput.readOnly = isReadonly;
    } else if (actualInput instanceof HTMLSelectElement) {
      actualInput.disabled = isReadonly;
    }
    actualInput.setAttribute("aria-readonly", String(isReadonly));
    refs.root.classList.toggle("formspec-field--readonly", isReadonly);
  }));
  disposers.push(j(() => {
    const isRelevant = ctx.engine.relevantSignals[fieldPath]?.value ?? true;
    refs.root.classList.toggle("formspec-hidden", !isRelevant);
    if (!isRelevant) {
      refs.root.setAttribute("aria-hidden", "true");
      refs.root.inert = true;
    } else {
      refs.root.removeAttribute("aria-hidden");
      refs.root.inert = false;
    }
  }));
  const markTouched = () => {
    if (!ctx.touchedFields.has(fieldPath)) {
      ctx.touchedFields.add(fieldPath);
      ctx.touchedVersion.value += 1;
    }
  };
  refs.root.addEventListener("focusout", markTouched);
  refs.root.addEventListener("change", markTouched);
  disposers.push(() => {
    refs.root.removeEventListener("focusout", markTouched);
    refs.root.removeEventListener("change", markTouched);
  });
  return disposers;
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/text-input.js
function useTextInput(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("TextInput", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "string" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const extensionAttrs = {};
  let resolvedInputType;
  const exts = item?.extensions;
  if (exts && typeof exts === "object") {
    for (const [extName, extEnabled] of Object.entries(exts)) {
      if (!extEnabled)
        continue;
      const entry = ctx.registryEntries.get(extName);
      if (!entry)
        continue;
      const meta = entry.metadata;
      const constraints = entry.constraints;
      if (meta?.inputType) {
        resolvedInputType = meta.inputType;
      } else if (meta?.inputMode === "email") {
        resolvedInputType = "email";
      } else if (meta?.inputMode === "tel") {
        resolvedInputType = "tel";
      }
      if (meta?.inputMode && !comp.inputMode)
        extensionAttrs.inputMode = meta.inputMode;
      if (meta?.autocomplete)
        extensionAttrs.autocomplete = meta.autocomplete;
      if (meta?.sensitive)
        extensionAttrs.autocomplete = "off";
      if (constraints?.maxLength != null)
        extensionAttrs.maxLength = String(constraints.maxLength);
      if (constraints?.pattern)
        extensionAttrs.pattern = constraints.pattern;
      if (meta?.mask && !comp.placeholder)
        extensionAttrs.placeholder = meta.mask;
    }
  }
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    placeholder: comp.placeholder,
    inputMode: comp.inputMode,
    maxLines: comp.maxLines,
    prefix: comp.prefix,
    suffix: comp.suffix,
    resolvedInputType,
    extensionAttrs,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const inputEl = refs.control.querySelector("input") || refs.control.querySelector("textarea") || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (document.activeElement !== inputEl) {
          inputEl.value = val ?? "";
        }
      }));
      inputEl.addEventListener("input", (e2) => {
        ctx.engine.setValue(fieldPath, e2.target.value);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/number-input.js
function useNumberInput(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("NumberInput", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "decimal" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    min: comp.min,
    max: comp.max,
    step: comp.step,
    dataType: item?.dataType || "decimal",
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const bindableInput = refs.control.querySelector("input") || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (document.activeElement !== bindableInput) {
          bindableInput.value = val ?? "";
        }
      }));
      bindableInput.addEventListener("input", (e2) => {
        const target = e2.target;
        let val = target.value === "" ? null : Number(target.value);
        if (val !== null && !isNaN(val)) {
          if (comp.min !== void 0 && val < Number(comp.min))
            val = Number(comp.min);
          if (comp.max !== void 0 && val > Number(comp.max))
            val = Number(comp.max);
        }
        if (String(val) !== target.value) {
          target.value = val === null ? "" : String(val);
        }
        ctx.engine.setValue(fieldPath, val);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/radio-group.js
function useRadioGroup(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("RadioGroup", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "choice" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const optionSignal = ctx.engine.getOptionsSignal?.(fieldPath);
  const optionStateSignal = ctx.engine.getOptionsStateSignal?.(fieldPath);
  if (optionSignal || optionStateSignal) {
    let initialized = false;
    ctx.cleanupFns.push(j(() => {
      optionSignal?.value;
      optionStateSignal?.value;
      if (!initialized) {
        initialized = true;
        return;
      }
      ctx.rerender();
    }));
  }
  const remoteOptionsState = ctx.engine.getOptionsState?.(fieldPath) || { loading: false, error: null };
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState,
    options: () => ctx.engine.getOptions?.(fieldPath) || item?.options || [],
    groupRole: "radiogroup",
    inputName: fieldPath,
    orientation: comp.orientation,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      if (refs.optionControls) {
        for (const [_value, radio] of refs.optionControls) {
          radio.addEventListener("change", () => {
            if (radio.checked) {
              ctx.engine.setValue(fieldPath, radio.value);
            }
          });
        }
      }
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (refs.optionControls) {
          for (const [optVal, radio] of refs.optionControls) {
            radio.checked = optVal === String(val ?? "");
          }
        }
      }));
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/checkbox-group.js
function useCheckboxGroup(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("CheckboxGroup", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "multiChoice" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const optionSignal = ctx.engine.getOptionsSignal?.(fieldPath);
  const optionStateSignal = ctx.engine.getOptionsStateSignal?.(fieldPath);
  if (optionSignal || optionStateSignal) {
    let initialized = false;
    ctx.cleanupFns.push(j(() => {
      optionSignal?.value;
      optionStateSignal?.value;
      if (!initialized) {
        initialized = true;
        return;
      }
      ctx.rerender();
    }));
  }
  const remoteOptionsState = ctx.engine.getOptionsState?.(fieldPath) || { loading: false, error: null };
  let currentOptionControls;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState,
    options: () => ctx.engine.getOptions?.(fieldPath) || item?.options || [],
    groupRole: "group",
    selectAll: !!comp.selectAll,
    columns: comp.columns,
    setValue(val) {
      ctx.engine.setValue(fieldPath, val);
    },
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      currentOptionControls = refs.optionControls;
      if (refs.optionControls) {
        for (const [_value, cb] of refs.optionControls) {
          cb.addEventListener("change", () => {
            const checked = [];
            if (currentOptionControls) {
              for (const [optVal, optCb] of currentOptionControls) {
                if (optCb.checked)
                  checked.push(optVal);
              }
            }
            ctx.engine.setValue(fieldPath, checked);
          });
        }
      }
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = Array.isArray(sig.value) ? sig.value : [];
        if (currentOptionControls) {
          for (const [optVal, cb] of currentOptionControls) {
            cb.checked = val.includes(optVal);
          }
        }
      }));
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/select.js
function useSelect(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Select", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "choice" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const optionSignal = ctx.engine.getOptionsSignal?.(fieldPath);
  const optionStateSignal = ctx.engine.getOptionsStateSignal?.(fieldPath);
  if (optionSignal || optionStateSignal) {
    let initialized = false;
    ctx.cleanupFns.push(j(() => {
      optionSignal?.value;
      optionStateSignal?.value;
      if (!initialized) {
        initialized = true;
        return;
      }
      ctx.rerender();
    }));
  }
  const remoteOptionsState = ctx.engine.getOptionsState?.(fieldPath) || { loading: false, error: null };
  const dataType = item?.dataType || "choice";
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState,
    options: () => ctx.engine.getOptions?.(fieldPath) || item?.options || [],
    placeholder: comp.placeholder,
    clearable: comp.clearable,
    dataType,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const selectEl = refs.control.querySelector("select") || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (document.activeElement !== selectEl) {
          selectEl.value = val ?? "";
        }
      }));
      selectEl.addEventListener("change", (e2) => {
        const raw = e2.target.value;
        let val = raw;
        if (["integer", "decimal", "number"].includes(dataType)) {
          val = raw === "" ? null : Number(raw);
        }
        ctx.engine.setValue(fieldPath, val);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/toggle.js
function useToggle(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Toggle", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "boolean" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  if (!presentation.labelPosition || presentation.labelPosition === "top") {
    presentation.labelPosition = "start";
  }
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    onLabel: comp.onLabel,
    offLabel: comp.offLabel,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const checkbox = refs.control.querySelector('input[type="checkbox"]') || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        if (document.activeElement !== checkbox) {
          checkbox.checked = !!sig.value;
        }
      }));
      if (comp.onLabel || comp.offLabel) {
        const toggleLabel = refs.control.querySelector(".formspec-toggle-label");
        if (toggleLabel) {
          disposers.push(j(() => {
            const sig = ctx.engine.signals[fieldPath];
            toggleLabel.textContent = sig?.value ? comp.onLabel || "" : comp.offLabel || "";
          }));
        }
      }
      checkbox.addEventListener("input", (e2) => {
        ctx.engine.setValue(fieldPath, e2.target.checked);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/checkbox.js
function useCheckbox(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Checkbox", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "boolean" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  if (!presentation.labelPosition || presentation.labelPosition === "top") {
    presentation.labelPosition = "start";
  }
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const checkbox = refs.control.querySelector('input[type="checkbox"]') || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        if (document.activeElement !== checkbox) {
          checkbox.checked = !!sig.value;
        }
      }));
      checkbox.addEventListener("input", (e2) => {
        ctx.engine.setValue(fieldPath, e2.target.checked);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/date-picker.js
function useDatePicker(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("DatePicker", item?.dataType || "string");
  const dataType = item?.dataType || "date";
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  let inputType = dataType === "date" ? "date" : dataType === "time" ? "time" : "datetime-local";
  if (comp.showTime === true && inputType === "date")
    inputType = "datetime-local";
  if (comp.showTime === false && inputType === "datetime-local")
    inputType = "date";
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    inputType,
    minDate: comp.minDate,
    maxDate: comp.maxDate,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const bindableInput = refs.control.querySelector("input") || refs.control;
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (document.activeElement !== bindableInput) {
          bindableInput.value = val ?? "";
        }
      }));
      bindableInput.addEventListener("input", (e2) => {
        ctx.engine.setValue(fieldPath, e2.target.value);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/money-input.js
function useMoneyInput(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("MoneyInput", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "money" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const resolvedCurrency = item?.currency || ctx.definition?.formPresentation?.defaultCurrency || null;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    min: comp.min,
    max: comp.max,
    step: comp.step,
    placeholder: comp.placeholder,
    resolvedCurrency,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const amountInput = refs.control.querySelector('input[type="number"]');
      const currencyInput = refs.control.querySelector(".formspec-money-currency-input");
      const getCurrency = () => {
        if (resolvedCurrency)
          return resolvedCurrency;
        return currencyInput?.value || "";
      };
      if (amountInput) {
        const updateMoney = () => {
          let amount = amountInput.value === "" ? null : Number(amountInput.value);
          if (amount !== null && !isNaN(amount)) {
            if (comp.min !== void 0 && amount < Number(comp.min))
              amount = Number(comp.min);
            if (comp.max !== void 0 && amount > Number(comp.max))
              amount = Number(comp.max);
          }
          ctx.engine.setValue(fieldPath, { amount, currency: getCurrency() });
        };
        amountInput.addEventListener("input", updateMoney);
        disposers.push(j(() => {
          const sig = ctx.engine.signals[fieldPath];
          if (!sig)
            return;
          const v2 = sig.value;
          if (document.activeElement !== amountInput) {
            if (v2 !== null && v2 !== void 0 && typeof v2 === "object" && "amount" in v2) {
              const a2 = v2.amount;
              amountInput.value = a2 !== null && a2 !== void 0 ? String(Math.round(a2 * 100) / 100) : "";
            } else if (typeof v2 === "number") {
              amountInput.value = String(Math.round(v2 * 100) / 100);
            }
          }
        }));
      }
      if (currencyInput) {
        currencyInput.addEventListener("input", () => {
          const amount = amountInput ? amountInput.value === "" ? null : Number(amountInput.value) : null;
          ctx.engine.setValue(fieldPath, { amount, currency: currencyInput.value });
        });
        disposers.push(j(() => {
          const sig = ctx.engine.signals[fieldPath];
          if (!sig)
            return;
          const v2 = sig.value;
          if (document.activeElement !== currencyInput && v2 != null && typeof v2 === "object" && "currency" in v2) {
            currencyInput.value = v2.currency || "";
          }
        }));
      }
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/slider.js
function useSlider(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Slider", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "decimal" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    min: comp.min ?? void 0,
    max: comp.max ?? void 0,
    step: comp.step ?? void 0,
    showTicks: comp.showTicks === true,
    showValue: comp.showValue !== false,
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const rangeInput = refs.control.querySelector('input[type="range"]') || refs.control;
      rangeInput.addEventListener("input", () => {
        const val = rangeInput.value === "" ? null : Number(rangeInput.value);
        ctx.engine.setValue(fieldPath, val);
      });
      const valueDisplay = refs.root.querySelector(".formspec-slider-value");
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        if (!sig)
          return;
        const val = sig.value;
        if (document.activeElement !== rangeInput) {
          rangeInput.value = val ?? "";
        }
        if (valueDisplay) {
          valueDisplay.textContent = val != null ? String(val) : rangeInput.value;
        }
      }));
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/rating.js
var RATING_ICON_MAP = {
  star: "\u2605",
  heart: "\u2665",
  circle: "\u25CF"
};
function resolveRatingIcon(icon) {
  if (!icon)
    return RATING_ICON_MAP.star;
  return RATING_ICON_MAP[icon] || icon;
}
function useRating(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Rating", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "decimal" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const maxRating = comp.max || 5;
  const isInteger = item?.dataType === "integer";
  const allowHalf = comp.allowHalf === true;
  const icon = resolveRatingIcon(comp.icon);
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    maxRating,
    icon,
    allowHalf,
    isInteger,
    setValue(value) {
      const finalValue = isInteger ? Math.round(value) : value;
      ctx.engine.setValue(fieldPath, finalValue);
    },
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      const stars = refs.control.querySelectorAll(".formspec-rating-star");
      disposers.push(j(() => {
        const sig = ctx.engine.signals[fieldPath];
        const val = sig?.value ?? 0;
        stars.forEach((star, idx) => {
          const fullValue = idx + 1;
          const halfValue = idx + 0.5;
          const isSelected = fullValue <= val;
          const isHalfSelected = allowHalf && !isSelected && halfValue <= val;
          star.classList.toggle("formspec-rating-star--selected", isSelected);
          star.classList.toggle("formspec-rating-star--half", isHalfSelected);
        });
      }));
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/file-upload.js
function useFileUpload(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("FileUpload", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "string" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  const multiple = comp.multiple === true;
  const maxSize = typeof comp.maxSize === "number" ? comp.maxSize : void 0;
  let accumulated = [];
  let fileListCallback = null;
  const syncToEngine = () => {
    ctx.engine.setValue(fieldPath, multiple ? [...accumulated] : accumulated[0] || null);
    fileListCallback?.();
  };
  const addFiles = (incoming) => {
    if (maxSize != null) {
      const oversized = incoming.find((f2) => f2.size > maxSize);
      if (oversized)
        return `"${oversized.name}" exceeds the maximum size of ${formatBytes2(maxSize)}.`;
    }
    if (multiple) {
      for (const f2 of incoming) {
        if (!accumulated.some((e2) => e2.name === f2.name && e2.size === f2.size)) {
          accumulated.push(f2);
        }
      }
    } else {
      accumulated = [incoming[0]];
    }
    syncToEngine();
    return null;
  };
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    accept: comp.accept,
    multiple,
    dragDrop: comp.dragDrop === true,
    maxSize,
    files: () => accumulated,
    removeFile(index) {
      accumulated = accumulated.filter((_2, i2) => i2 !== index);
      syncToEngine();
    },
    clearFiles() {
      accumulated = [];
      syncToEngine();
    },
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      fileListCallback = refs._rebuildFileList || null;
      const fileInput = refs.control.tagName === "INPUT" ? refs.control : refs.control.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.addEventListener("change", () => {
          const files = Array.from(fileInput.files || []);
          const err = addFiles(files.map((f2) => ({ name: f2.name, size: f2.size, type: f2.type })));
          if (err && refs.error)
            refs.error.textContent = err;
          else if (refs.error)
            refs.error.textContent = "";
          fileInput.value = "";
        });
      }
      const onFilesDrop = (e2) => {
        const detail = e2.detail;
        if (detail?.fileData) {
          const err = addFiles(detail.fileData);
          if (err && refs.error)
            refs.error.textContent = err;
          else if (refs.error)
            refs.error.textContent = "";
        }
      };
      refs.root.addEventListener("formspec-files-dropped", onFilesDrop);
      return () => disposers.forEach((d2) => d2());
    }
  };
}
function formatBytes2(bytes) {
  if (bytes === 0)
    return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const i2 = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const val = bytes / Math.pow(1024, i2);
  return `${val < 10 ? val.toFixed(1) : Math.round(val)} ${units[i2]}`;
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/signature.js
function useSignature(ctx, comp) {
  const fieldPath = resolveFieldPath(comp.bind, ctx.prefix);
  const id = comp.id || toFieldId(fieldPath);
  const item = ctx.findItemByKey(comp.bind);
  warnIfIncompatible("Signature", item?.dataType || "string");
  const itemDesc = { key: item?.key || comp.bind, type: "field", dataType: item?.dataType || "string" };
  const rawPresentation = ctx.resolveItemPresentation(itemDesc);
  const presentation = resolveAndStripTokens(rawPresentation, ctx.resolveToken, comp);
  const widgetClassSlots = ctx.resolveWidgetClassSlots(rawPresentation);
  const labelText = comp.labelOverride || item?.label || item?.key || comp.bind;
  return {
    fieldPath,
    id,
    label: labelText,
    hint: comp.hintOverride || item?.hint || null,
    description: item?.description || null,
    presentation,
    widgetClassSlots,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    remoteOptionsState: { loading: false, error: null },
    options: () => [],
    height: comp.height || 200,
    strokeColor: comp.strokeColor || "#000",
    bind(refs) {
      const disposers = bindSharedFieldEffects(ctx, fieldPath, labelText, refs);
      refs.root.addEventListener("formspec-signature-drawn", (e2) => {
        const detail = e2.detail;
        if (detail?.dataUrl)
          ctx.engine.setValue(fieldPath, detail.dataUrl);
      });
      refs.root.addEventListener("formspec-signature-cleared", () => {
        ctx.engine.setValue(fieldPath, null);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/components/inputs.js
var TextInputPlugin = {
  type: "TextInput",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useTextInput(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("TextInput");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var NumberInputPlugin = {
  type: "NumberInput",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useNumberInput(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("NumberInput");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var SelectPlugin = {
  type: "Select",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useSelect(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Select");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var TogglePlugin = {
  type: "Toggle",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useToggle(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Toggle");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var CheckboxPlugin = {
  type: "Checkbox",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useCheckbox(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Checkbox");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var DatePickerPlugin = {
  type: "DatePicker",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useDatePicker(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("DatePicker");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var RadioGroupPlugin = {
  type: "RadioGroup",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useRadioGroup(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("RadioGroup");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var CheckboxGroupPlugin = {
  type: "CheckboxGroup",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useCheckboxGroup(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("CheckboxGroup");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var SliderPlugin = {
  type: "Slider",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useSlider(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Slider");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var RatingPlugin = {
  type: "Rating",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useRating(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Rating");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var FileUploadPlugin = {
  type: "FileUpload",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useFileUpload(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("FileUpload");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var SignaturePlugin = {
  type: "Signature",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useSignature(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Signature");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var MoneyInputPlugin = {
  type: "MoneyInput",
  render: (comp, parent, ctx) => {
    if (!comp.bind)
      return;
    const behavior = useMoneyInput(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("MoneyInput");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var InputPlugins = [
  TextInputPlugin,
  NumberInputPlugin,
  SelectPlugin,
  TogglePlugin,
  CheckboxPlugin,
  DatePickerPlugin,
  RadioGroupPlugin,
  CheckboxGroupPlugin,
  SliderPlugin,
  RatingPlugin,
  FileUploadPlugin,
  SignaturePlugin,
  MoneyInputPlugin
];

// node_modules/@formspec-org/webcomponent/dist/format.js
function formatMoney(moneyVal, locale = "en-US") {
  if (moneyVal == null || moneyVal.amount == null)
    return "";
  const n2 = typeof moneyVal.amount === "number" ? moneyVal.amount : parseFloat(moneyVal.amount);
  if (!isFinite(n2))
    return "";
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: moneyVal.currency || "USD"
  }).format(n2);
}

// node_modules/@formspec-org/webcomponent/dist/components/display.js
function renderMarkdown(src) {
  let html = src.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const lines = html.split("\n");
  const out = [];
  let inUl = false;
  let inOl = false;
  for (const line of lines) {
    const trimmed = line.trim();
    if (/^[-*]\s+/.test(trimmed)) {
      if (!inUl) {
        out.push("<ul>");
        inUl = true;
      }
      if (inOl) {
        out.push("</ol>");
        inOl = false;
      }
      out.push(`<li>${trimmed.replace(/^[-*]\s+/, "")}</li>`);
      continue;
    }
    if (/^\d+\.\s+/.test(trimmed)) {
      if (!inOl) {
        out.push("<ol>");
        inOl = true;
      }
      if (inUl) {
        out.push("</ul>");
        inUl = false;
      }
      out.push(`<li>${trimmed.replace(/^\d+\.\s+/, "")}</li>`);
      continue;
    }
    if (inUl) {
      out.push("</ul>");
      inUl = false;
    }
    if (inOl) {
      out.push("</ol>");
      inOl = false;
    }
    if (trimmed === "") {
      out.push("<br>");
    } else {
      out.push(`<p>${trimmed}</p>`);
    }
  }
  if (inUl)
    out.push("</ul>");
  if (inOl)
    out.push("</ol>");
  let result = out.join("\n");
  result = result.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  result = result.replace(/\*(.+?)\*/g, "<em>$1</em>");
  result = result.replace(/`(.+?)`/g, "<code>$1</code>");
  return result;
}
var HeadingPlugin = {
  type: "Heading",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement(`h${comp.level || 1}`);
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-heading";
    if (comp.bind) {
      const itemFullName = ctx.prefix ? `${ctx.prefix}.${comp.bind}` : comp.bind;
      ctx.cleanupFns.push(j(() => {
        const sig = ctx.engine.signals[itemFullName] ?? ctx.engine.variableSignals?.[`#:${comp.bind}`];
        const v2 = sig?.value;
        el2.textContent = v2 != null ? String(v2) : "";
      }));
    } else {
      el2.textContent = comp.text || "";
    }
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var TextPlugin = {
  type: "Text",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("p");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-text";
    if (comp.format === "markdown")
      el2.classList.add("formspec-text--markdown");
    const isMarkdown = comp.format === "markdown";
    if (comp.bind) {
      const itemFullName = ctx.prefix ? `${ctx.prefix}.${comp.bind}` : comp.bind;
      const varKey = `#:${comp.bind}`;
      ctx.cleanupFns.push(j(() => {
        const sig = ctx.engine.signals[itemFullName] ?? ctx.engine.variableSignals?.[varKey];
        const v2 = sig?.value;
        if (v2 != null && typeof v2 === "object" && "amount" in v2) {
          el2.textContent = formatMoney(v2);
        } else if (isMarkdown && v2 != null) {
          el2.innerHTML = renderMarkdown(String(v2));
        } else {
          el2.textContent = v2 != null ? String(v2) : "";
        }
      }));
    } else if (isMarkdown && comp.text) {
      el2.innerHTML = renderMarkdown(comp.text);
    } else {
      el2.textContent = comp.text || "";
    }
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var CardPlugin = {
  type: "Card",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-card";
    if (comp.elevation != null && comp.elevation > 0) {
      el2.dataset.elevation = String(comp.elevation);
    }
    if (comp.title) {
      const h3 = document.createElement("h3");
      h3.className = "formspec-card-title";
      h3.textContent = comp.title;
      el2.appendChild(h3);
    }
    if (comp.subtitle) {
      const sub = document.createElement("p");
      sub.className = "formspec-card-subtitle";
      sub.textContent = comp.subtitle;
      el2.appendChild(sub);
    }
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var SpacerPlugin = {
  type: "Spacer",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-spacer";
    if (comp.size)
      el2.style.height = String(ctx.resolveToken(comp.size));
    ctx.applyCssClass(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var AlertPlugin = {
  type: "Alert",
  render: (comp, parent, ctx) => {
    const severity = comp.severity || "info";
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = `formspec-alert formspec-alert--${severity}`;
    el2.setAttribute("role", severity === "error" || severity === "warning" ? "alert" : "status");
    if (comp.dismissible) {
      el2.classList.add("formspec-alert--dismissible");
      const closeBtn = document.createElement("button");
      closeBtn.type = "button";
      closeBtn.className = "formspec-alert-close";
      closeBtn.textContent = "\xD7";
      closeBtn.setAttribute("aria-label", "Dismiss");
      closeBtn.addEventListener("click", () => {
        el2.remove();
      });
      el2.appendChild(closeBtn);
    }
    const textSpan = document.createElement("span");
    if (comp.bind) {
      const itemFullName = ctx.prefix ? `${ctx.prefix}.${comp.bind}` : comp.bind;
      ctx.cleanupFns.push(j(() => {
        const sig = ctx.engine.signals[itemFullName] ?? ctx.engine.variableSignals?.[`#:${comp.bind}`];
        const v2 = sig?.value;
        textSpan.textContent = v2 != null ? String(v2) : "";
      }));
    } else {
      textSpan.textContent = comp.text || "";
    }
    el2.appendChild(textSpan);
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var BadgePlugin = {
  type: "Badge",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("span");
    if (comp.id)
      el2.id = comp.id;
    el2.className = `formspec-badge formspec-badge--${comp.variant || "default"}`;
    el2.textContent = comp.text || "";
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var ProgressBarPlugin = {
  type: "ProgressBar",
  render: (comp, parent, ctx) => {
    const wrapper = document.createElement("div");
    if (comp.id)
      wrapper.id = comp.id;
    wrapper.className = "formspec-progress-bar";
    const progressEl = document.createElement("progress");
    const maxVal = comp.max || 100;
    progressEl.max = maxVal;
    if (comp.label)
      progressEl.setAttribute("aria-label", comp.label);
    if (comp.bind) {
      const fullName = ctx.prefix ? `${ctx.prefix}.${comp.bind}` : comp.bind;
      const percentLabel = document.createElement("span");
      percentLabel.className = "formspec-progress-percent";
      ctx.cleanupFns.push(j(() => {
        const sig = ctx.engine.signals[fullName];
        const val = Number(sig?.value ?? comp.value ?? 0);
        progressEl.value = val;
        if (comp.showPercent) {
          percentLabel.textContent = `${Math.round(val / maxVal * 100)}%`;
        }
      }));
      wrapper.appendChild(progressEl);
      if (comp.showPercent)
        wrapper.appendChild(percentLabel);
    } else {
      progressEl.value = comp.value || 0;
      wrapper.appendChild(progressEl);
      if (comp.showPercent) {
        const percentLabel = document.createElement("span");
        percentLabel.className = "formspec-progress-percent";
        percentLabel.textContent = `${Math.round((comp.value || 0) / maxVal * 100)}%`;
        wrapper.appendChild(percentLabel);
      }
    }
    ctx.applyCssClass(wrapper, comp);
    ctx.applyAccessibility(wrapper, comp);
    ctx.applyStyle(wrapper, comp.style);
    parent.appendChild(wrapper);
  }
};
var SummaryPlugin = {
  type: "Summary",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("dl");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-summary";
    if (comp.items) {
      for (const item of comp.items) {
        const dt = document.createElement("dt");
        dt.textContent = item.label || "";
        el2.appendChild(dt);
        const dd = document.createElement("dd");
        el2.appendChild(dd);
        if (item.bind) {
          const fullName = ctx.prefix ? `${ctx.prefix}.${item.bind}` : item.bind;
          const varKey = `#:${item.bind}`;
          ctx.cleanupFns.push(j(() => {
            const sig = ctx.engine.signals[fullName] ?? ctx.engine.variableSignals?.[varKey];
            const v2 = sig?.value;
            if (v2 != null && typeof v2 === "object" && "amount" in v2) {
              dd.textContent = formatMoney(v2);
            } else if (v2 != null && item.optionSet) {
              const def = ctx.engine.getDefinition?.();
              const entry = def?.optionSets?.[item.optionSet];
              const opts = Array.isArray(entry) ? entry : entry?.options ?? [];
              const match = opts.find((o2) => o2.value === String(v2));
              dd.textContent = match ? match.label : String(v2);
            } else {
              dd.textContent = v2 != null ? String(v2) : "\u2014";
            }
          }));
        }
      }
    }
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
  }
};
var ValidationSummaryPlugin = {
  type: "ValidationSummary",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-validation-summary";
    el2.setAttribute("aria-live", "polite");
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    const source = comp.source || "live";
    const mode = comp.mode || "continuous";
    const showFieldErrors = comp.showFieldErrors === true;
    const jumpLinks = comp.jumpLinks === true;
    const dedupe = comp.dedupe !== false;
    ctx.cleanupFns.push(j(() => {
      let rawResults = [];
      if (source === "submit") {
        const detail = ctx.latestSubmitDetailSignal.value;
        const fromReport = detail?.validationReport?.results;
        const fromResponse = detail?.response?.validationResults;
        rawResults = Array.isArray(fromReport) ? fromReport : Array.isArray(fromResponse) ? fromResponse : [];
      } else {
        const submitOccurred = ctx.latestSubmitDetailSignal.value !== null;
        const wizardNavigated = ctx.touchedVersion.value > 0;
        const gateOpen = mode === "submit" ? submitOccurred : submitOccurred || wizardNavigated;
        if (!gateOpen) {
          el2.replaceChildren();
          el2.classList.remove("formspec-validation-summary--visible");
          return;
        }
        ctx.engine.structureVersion.value;
        rawResults = ctx.engine.getValidationReport({ mode }).results;
      }
      const filteredResults = rawResults.filter((r2) => {
        if (showFieldErrors)
          return true;
        return r2.source === "shape" || r2.constraintKind === "shape";
      });
      const resolved = filteredResults.map((result) => ({
        result,
        target: ctx.resolveValidationTarget(result)
      }));
      const rows = dedupe ? (() => {
        const seen = /* @__PURE__ */ new Set();
        return resolved.filter(({ result, target }) => {
          const key = `${result?.severity || "error"}|${target.path || result?.path || ""}|${result?.message || ""}`;
          if (seen.has(key))
            return false;
          seen.add(key);
          return true;
        });
      })() : resolved;
      el2.replaceChildren();
      if (rows.length === 0) {
        el2.classList.remove("formspec-validation-summary--visible");
        return;
      }
      el2.classList.add("formspec-validation-summary--visible");
      const errorCount = rows.filter(({ result }) => (result.severity || "error") === "error").length;
      const header = document.createElement("p");
      header.className = "formspec-validation-summary-header";
      header.textContent = errorCount > 0 ? `Please fix ${errorCount === 1 ? "this error" : `these ${errorCount} errors`} before continuing:` : "Please review the following before continuing:";
      el2.appendChild(header);
      const severityIcon = { error: "\u2715", warning: "!", info: "i" };
      for (const { result, target } of rows) {
        const div = document.createElement("div");
        const severity = result.severity || "error";
        div.className = `formspec-shape-${severity}`;
        const icon = document.createElement("span");
        icon.className = "formspec-shape-icon";
        icon.setAttribute("aria-hidden", "true");
        icon.textContent = severityIcon[severity] ?? "!";
        const message = result?.message || "Validation error";
        const withLabel = target.formLevel ? message : `${target.label}: ${message}`;
        if (jumpLinks && target.jumpable) {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "formspec-validation-summary-link";
          button.textContent = withLabel;
          button.addEventListener("click", () => {
            ctx.focusField(target.path);
          });
          div.appendChild(icon);
          div.appendChild(button);
        } else {
          div.appendChild(icon);
          div.appendChild(document.createTextNode(withLabel));
        }
        el2.appendChild(div);
      }
    }));
  }
};

// node_modules/@formspec-org/webcomponent/dist/behaviors/tabs.js
function useTabs(ctx, comp) {
  const children = comp.children || [];
  const tabLabels = comp.tabLabels || [];
  const position = comp.position || "top";
  const defaultTab = comp.defaultTab || 0;
  const activeTabSignal = y(defaultTab);
  const setActiveTab = (nextTab) => {
    const bounded = Math.max(0, Math.min(children.length - 1, Math.trunc(nextTab)));
    activeTabSignal.value = bounded;
  };
  return {
    id: comp.id,
    compOverrides: {
      cssClass: comp.cssClass,
      style: comp.style,
      accessibility: comp.accessibility
    },
    tabLabels,
    tabCount: children.length,
    position,
    defaultTab,
    activeTab() {
      return activeTabSignal.value;
    },
    setActiveTab,
    renderTab(index, parent) {
      ctx.renderComponent(children[index], parent, ctx.prefix);
    },
    bind(refs) {
      const disposers = [];
      const tabCount = refs.buttons.length;
      const activateTab = (index) => {
        setActiveTab(index);
        refs.buttons[activeTabSignal.value]?.focus();
      };
      disposers.push(j(() => {
        const active = activeTabSignal.value;
        refs.panels.forEach((p2, idx) => p2.classList.toggle("formspec-hidden", idx !== active));
        refs.buttons.forEach((b2, idx) => {
          const isActive = idx === active;
          b2.classList.toggle("formspec-tab--active", isActive);
          b2.setAttribute("aria-selected", String(isActive));
          b2.setAttribute("tabindex", isActive ? "0" : "-1");
        });
      }));
      refs.buttons.forEach((btn, i2) => {
        btn.addEventListener("click", () => setActiveTab(i2));
      });
      const onKeyDown = (event) => {
        const active = activeTabSignal.value;
        let nextIndex;
        switch (event.key) {
          case "ArrowRight":
          case "ArrowDown":
            nextIndex = (active + 1) % tabCount;
            break;
          case "ArrowLeft":
          case "ArrowUp":
            nextIndex = (active - 1 + tabCount) % tabCount;
            break;
          case "Home":
            nextIndex = 0;
            break;
          case "End":
            nextIndex = tabCount - 1;
            break;
        }
        if (nextIndex !== void 0) {
          event.preventDefault();
          activateTab(nextIndex);
        }
      };
      refs.tabBar.addEventListener("keydown", onKeyDown);
      disposers.push(() => refs.tabBar.removeEventListener("keydown", onKeyDown));
      const onSetActive = (event) => {
        const customEvent = event;
        const requestedIndex = Number(customEvent.detail?.index);
        if (!Number.isFinite(requestedIndex))
          return;
        setActiveTab(requestedIndex);
        event.stopPropagation();
      };
      refs.root.addEventListener("formspec-tabs-set-active", onSetActive);
      disposers.push(() => {
        refs.root.removeEventListener("formspec-tabs-set-active", onSetActive);
      });
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/components/interactive.js
var TabsPlugin = {
  type: "Tabs",
  render: (comp, parent, ctx) => {
    const behavior = useTabs(ctx.behaviorContext, comp);
    const adapterFn = globalRegistry.resolveAdapterFn("Tabs");
    if (adapterFn)
      adapterFn(behavior, parent, ctx.adapterContext);
  }
};
var SubmitButtonPlugin = {
  type: "SubmitButton",
  render: (comp, parent, ctx) => {
    const button = document.createElement("button");
    if (comp.id)
      button.id = comp.id;
    button.type = "button";
    button.className = "formspec-submit";
    const defaultLabel = comp.label || "Submit";
    const pendingLabel = comp.pendingLabel || "Submitting\u2026";
    const disableWhenPending = comp.disableWhenPending !== false;
    button.textContent = defaultLabel;
    ctx.applyCssClass(button, comp);
    ctx.applyAccessibility(button, comp);
    ctx.applyStyle(button, comp.style);
    ctx.cleanupFns.push(j(() => {
      const pending = ctx.submitPendingSignal.value;
      button.textContent = pending ? pendingLabel : defaultLabel;
      button.disabled = disableWhenPending ? pending : false;
    }));
    button.addEventListener("click", () => {
      ctx.submit({
        mode: comp.mode || "submit",
        emitEvent: comp.emitEvent !== false
      });
    });
    parent.appendChild(button);
  }
};

// node_modules/@formspec-org/webcomponent/dist/components/special.js
var ConditionalGroupPlugin = {
  type: "ConditionalGroup",
  render: (comp, parent, ctx) => {
    const el2 = document.createElement("div");
    if (comp.id)
      el2.id = comp.id;
    el2.className = "formspec-conditional-group";
    ctx.applyCssClass(el2, comp);
    ctx.applyAccessibility(el2, comp);
    ctx.applyStyle(el2, comp.style);
    parent.appendChild(el2);
    if (comp.children) {
      for (const child of comp.children) {
        ctx.renderComponent(child, el2, ctx.prefix);
      }
    }
  }
};
var DataTablePlugin = {
  type: "DataTable",
  render: (comp, parent, ctx) => {
    const wrapper = document.createElement("div");
    wrapper.className = "formspec-data-table-wrapper";
    parent.appendChild(wrapper);
    const table = document.createElement("table");
    if (comp.id)
      table.id = comp.id;
    table.className = "formspec-data-table";
    ctx.applyCssClass(table, comp);
    ctx.applyAccessibility(table, comp);
    ctx.applyStyle(table, comp.style);
    wrapper.appendChild(table);
    if (comp.title) {
      const caption = document.createElement("caption");
      caption.textContent = comp.title;
      table.appendChild(caption);
    }
    const columns = comp.columns || [];
    const bindKey = comp.bind;
    if (!bindKey || columns.length === 0)
      return;
    const showRowNumbers = comp.showRowNumbers === true;
    const allowAdd = comp.allowAdd === true;
    const allowRemove = comp.allowRemove === true;
    const editableCells = allowAdd || allowRemove;
    const groupItem = ctx.findItemByKey(bindKey);
    const fieldByKey = /* @__PURE__ */ new Map();
    if (groupItem?.type === "group" && Array.isArray(groupItem.children)) {
      for (const child of groupItem.children) {
        if (child?.type === "field" && child.key) {
          fieldByKey.set(child.key, child);
        }
      }
    }
    const defaultCurrency = ctx.engine.definition?.formPresentation?.defaultCurrency || "USD";
    const coerceInputValue = (raw, dataType, fieldDef, col) => {
      const trimmed = raw.trim();
      if (trimmed === "")
        return null;
      let val;
      if (dataType === "integer") {
        const parsed = Number.parseInt(trimmed, 10);
        val = Number.isFinite(parsed) ? parsed : null;
      } else if (dataType === "decimal" || dataType === "money") {
        const parsed = Number.parseFloat(trimmed);
        val = Number.isFinite(parsed) ? parsed : null;
      } else {
        val = raw;
      }
      if (typeof val === "number" && col) {
        if (col.min !== void 0 && val < col.min)
          val = col.min;
        if (col.max !== void 0 && val > col.max)
          val = col.max;
      }
      if (dataType === "money" && val !== null) {
        const currency = fieldDef?.currency || defaultCurrency;
        return { amount: val, currency };
      }
      return val;
    };
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    if (showRowNumbers) {
      const th = document.createElement("th");
      th.textContent = "#";
      th.setAttribute("scope", "col");
      headerRow.appendChild(th);
    }
    for (let ci = 0; ci < columns.length; ci++) {
      const col = columns[ci];
      const th = document.createElement("th");
      th.textContent = col.header;
      th.setAttribute("scope", "col");
      th.id = `${comp.id || "dt"}-col-${ci}`;
      headerRow.appendChild(th);
    }
    if (allowRemove) {
      const th = document.createElement("th");
      th.textContent = "";
      headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);
    const tbody = document.createElement("tbody");
    table.appendChild(tbody);
    const fullName = ctx.prefix ? `${ctx.prefix}.${bindKey}` : bindKey;
    let cellEffectDisposers = [];
    const clearCellEffects = () => {
      for (const dispose of cellEffectDisposers) {
        dispose();
      }
      cellEffectDisposers = [];
    };
    ctx.cleanupFns.push(() => clearCellEffects());
    ctx.cleanupFns.push(j(() => {
      const count = ctx.engine.repeats[fullName]?.value || 0;
      clearCellEffects();
      tbody.innerHTML = "";
      for (let i2 = 0; i2 < count; i2++) {
        const tr = document.createElement("tr");
        if (showRowNumbers) {
          const td = document.createElement("td");
          td.textContent = String(i2 + 1);
          td.className = "formspec-row-number";
          tr.appendChild(td);
        }
        for (const col of columns) {
          const td = document.createElement("td");
          const sigPath = `${fullName}[${i2}].${col.bind}`;
          const sig = ctx.engine.signals[sigPath];
          const dataType = fieldByKey.get(col.bind)?.dataType;
          if (sig && editableCells) {
            const fieldDef = fieldByKey.get(col.bind);
            const prefix = fieldDef?.prefix;
            const suffix = fieldDef?.suffix;
            const isChoice = fieldDef?.dataType === "choice" && (fieldDef.optionSet || fieldDef.options);
            let inputEl;
            if (isChoice) {
              const select = document.createElement("select");
              select.className = "formspec-datatable-input";
              select.name = sigPath;
              const emptyOpt = document.createElement("option");
              emptyOpt.value = "";
              emptyOpt.textContent = "";
              select.appendChild(emptyOpt);
              let options = [];
              if (fieldDef.optionSet) {
                const def = ctx.engine.definition;
                const entry = def?.optionSets?.[fieldDef.optionSet];
                options = Array.isArray(entry) ? entry : entry?.options ?? [];
              } else if (Array.isArray(fieldDef.options)) {
                options = fieldDef.options;
              }
              for (const opt of options) {
                const optEl = document.createElement("option");
                optEl.value = opt.value;
                optEl.textContent = opt.label || opt.value;
                select.appendChild(optEl);
              }
              select.addEventListener("change", () => {
                ctx.engine.setValue(sigPath, select.value || null);
              });
              inputEl = select;
            } else {
              const input = document.createElement("input");
              input.className = "formspec-datatable-input";
              input.name = sigPath;
              input.type = dataType === "integer" || dataType === "decimal" || dataType === "money" ? "number" : "text";
              if (input.type === "number") {
                const step = col.step ?? (dataType === "integer" ? 1 : null);
                input.step = step != null ? String(step) : dataType === "integer" ? "1" : "any";
                if (col.min != null)
                  input.min = String(col.min);
                if (col.max != null)
                  input.max = String(col.max);
              }
              input.addEventListener("input", () => {
                let nextValue = coerceInputValue(input.value, dataType, fieldDef, col);
                ctx.engine.setValue(sigPath, nextValue);
                if (dataType === "integer" || dataType === "decimal" || dataType === "money") {
                  const displayVal = nextValue && typeof nextValue === "object" && "amount" in nextValue ? nextValue.amount : nextValue;
                  const sVal = displayVal === null ? "" : String(displayVal);
                  if (sVal !== input.value) {
                    input.value = sVal;
                  }
                }
              });
              inputEl = input;
            }
            inputEl.setAttribute("aria-label", `${col.header}, Row ${i2 + 1}`);
            if (prefix || suffix) {
              const wrapper2 = document.createElement("div");
              wrapper2.className = "formspec-datatable-cell-wrapper";
              if (prefix) {
                const pre = document.createElement("span");
                pre.className = "formspec-datatable-prefix";
                pre.textContent = prefix;
                wrapper2.appendChild(pre);
              }
              wrapper2.appendChild(inputEl);
              if (suffix) {
                const suf = document.createElement("span");
                suf.className = "formspec-datatable-prefix";
                suf.textContent = suffix;
                wrapper2.appendChild(suf);
              }
              td.appendChild(wrapper2);
            } else {
              td.appendChild(inputEl);
            }
            const readonlySig = ctx.engine.readonlySignals[sigPath];
            const syncInput = j(() => {
              const value = sig.value;
              const readonly = readonlySig?.value ?? false;
              if (document.activeElement !== inputEl) {
                if (value !== null && value !== void 0 && typeof value === "object" && "amount" in value) {
                  inputEl.value = value.amount !== null ? String(value.amount) : "";
                } else {
                  inputEl.value = value === null || value === void 0 || typeof value === "number" && isNaN(value) ? "" : String(value);
                }
              }
              inputEl.disabled = readonly;
            });
            cellEffectDisposers.push(syncInput);
          } else if (sig) {
            const valueEl = document.createElement("span");
            td.appendChild(valueEl);
            const syncText = j(() => {
              const v2 = sig.value;
              if (v2 !== null && v2 !== void 0 && typeof v2 === "object" && "amount" in v2) {
                valueEl.textContent = formatMoney(v2);
              } else {
                valueEl.textContent = v2 === null || v2 === void 0 ? "" : String(v2);
              }
            });
            cellEffectDisposers.push(syncText);
          } else {
            td.textContent = "";
          }
          tr.appendChild(td);
        }
        if (allowRemove) {
          const td = document.createElement("td");
          const removeBtn = document.createElement("button");
          removeBtn.type = "button";
          removeBtn.className = "formspec-datatable-remove";
          removeBtn.textContent = "Remove";
          removeBtn.setAttribute("aria-label", `Remove row ${i2 + 1}`);
          const idx = i2;
          removeBtn.addEventListener("click", () => {
            ctx.engine.removeRepeatInstance(fullName, idx);
          });
          td.appendChild(removeBtn);
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      }
    }));
    if (allowAdd) {
      const addBtn = document.createElement("button");
      addBtn.type = "button";
      addBtn.className = "formspec-datatable-add";
      addBtn.textContent = `Add Row`;
      addBtn.addEventListener("click", () => {
        ctx.engine.addRepeatInstance(fullName);
      });
      parent.appendChild(addBtn);
    }
  }
};

// node_modules/@formspec-org/webcomponent/dist/components/index.js
function registerDefaultComponents() {
  globalRegistry.register(PagePlugin);
  globalRegistry.register(StackPlugin);
  globalRegistry.register(GridPlugin);
  globalRegistry.register(DividerPlugin);
  globalRegistry.register(CollapsiblePlugin);
  globalRegistry.register(ColumnsPlugin);
  globalRegistry.register(PanelPlugin);
  globalRegistry.register(AccordionPlugin);
  globalRegistry.register(ModalPlugin);
  globalRegistry.register(PopoverPlugin);
  InputPlugins.forEach((p2) => globalRegistry.register(p2));
  globalRegistry.register(HeadingPlugin);
  globalRegistry.register(TextPlugin);
  globalRegistry.register(CardPlugin);
  globalRegistry.register(SpacerPlugin);
  globalRegistry.register(AlertPlugin);
  globalRegistry.register(BadgePlugin);
  globalRegistry.register(ProgressBarPlugin);
  globalRegistry.register(SummaryPlugin);
  globalRegistry.register(TabsPlugin);
  globalRegistry.register(SubmitButtonPlugin);
  globalRegistry.register(ValidationSummaryPlugin);
  globalRegistry.register(ConditionalGroupPlugin);
  globalRegistry.register(DataTablePlugin);
  globalRegistry.registerAdapter(defaultAdapter);
}

// node_modules/@formspec-org/engine/dist/reactivity/preact-runtime.js
var preactReactiveRuntime = {
  signal: (initial) => y(initial),
  computed: (fn) => g(fn),
  effect: (fn) => j(fn),
  batch: (fn) => n(fn)
};

// node_modules/@formspec-org/engine/dist/engine/response-assembly.js
init_wasm_bridge_runtime();

// node_modules/@formspec-org/engine/dist/engine/helpers.js
init_wasm_bridge_runtime();
function normalizeRemoteOptions(payload) {
  const options = Array.isArray(payload) ? payload : Array.isArray(payload?.options) ? payload.options : null;
  if (!options) {
    throw new Error("Remote options response must be an array or { options: [...] }");
  }
  return options.filter((option) => option && typeof option === "object" && option.value !== void 0 && option.label !== void 0).map((option) => ({
    value: String(option.value),
    label: String(option.label)
  }));
}
function makeValidationResult(result) {
  return {
    $formspecValidationResult: "1.0",
    ...result,
    path: toFelIndexedPath(result.path)
  };
}
function toValidationResult(result) {
  return {
    ...result,
    $formspecValidationResult: "1.0",
    path: toFelIndexedPath(result.path)
  };
}
function toValidationResults(results) {
  return results.map(toValidationResult);
}
function emptyValueForItem(item) {
  if (item.type !== "field") {
    return null;
  }
  switch (item.dataType) {
    case "integer":
    case "decimal":
    case "money":
    case "date":
    case "dateTime":
    case "time":
      return null;
    case "boolean":
      return false;
    case "multiChoice":
      return [];
    default:
      return "";
  }
}
function coerceInitialValue(item, value) {
  if (item.dataType === "boolean" && value === "") {
    return false;
  }
  if (["integer", "decimal"].includes(item.dataType ?? "") && value === "") {
    return null;
  }
  if (item.dataType === "money" && typeof value === "number") {
    return { amount: value, currency: item.currency ?? "" };
  }
  if (item.dataType === "money" && value && typeof value === "object" && typeof value.amount === "string") {
    const parsed = value.amount === "" ? null : Number(value.amount);
    return {
      ...value,
      amount: parsed === null || !Number.isNaN(parsed) ? parsed : value.amount
    };
  }
  return cloneValue(value);
}
function coerceFieldValue2(item, bind, definition, value) {
  if (value === void 0) {
    return void 0;
  }
  const bindJson = bind === void 0 ? "" : JSON.stringify(bind);
  const out = wasmCoerceFieldValue(JSON.stringify(item), bindJson, JSON.stringify(definition), JSON.stringify(value));
  return JSON.parse(out);
}
function validateDataType(value, dataType) {
  switch (dataType) {
    case "string":
      return typeof value === "string";
    case "boolean":
      return typeof value === "boolean";
    case "integer":
      return typeof value === "number" && Number.isInteger(value);
    case "decimal":
      return typeof value === "number" && !Number.isNaN(value);
    case "money":
      return value && typeof value === "object" && typeof value.amount === "number";
    case "array":
      return Array.isArray(value);
    case "object":
      return value !== null && typeof value === "object" && !Array.isArray(value);
    default:
      return true;
  }
}
function cloneValue(value) {
  if (value === null || value === void 0 || typeof value !== "object") {
    return value;
  }
  const copier = globalThis.structuredClone;
  if (typeof copier === "function") {
    return copier(value);
  }
  return JSON.parse(JSON.stringify(value));
}
function normalizeWasmValue(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => normalizeWasmValue(entry));
  }
  if (value && typeof value === "object") {
    const record = value;
    if (record.$type === "money" && "amount" in record && "currency" in record) {
      return {
        amount: normalizeWasmValue(record.amount),
        currency: normalizeWasmValue(record.currency)
      };
    }
    return Object.fromEntries(Object.entries(record).filter(([key]) => key !== "$type").map(([key, entry]) => [key, normalizeWasmValue(entry)]));
  }
  return cloneValue(value);
}
function toWasmContextValue(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => toWasmContextValue(entry));
  }
  if (value && typeof value === "object") {
    const record = value;
    if (!("$type" in record) && "amount" in record && "currency" in record) {
      return {
        $type: "money",
        amount: toWasmContextValue(record.amount),
        currency: toWasmContextValue(record.currency)
      };
    }
    return Object.fromEntries(Object.entries(record).map(([key, entry]) => [key, toWasmContextValue(entry)]));
  }
  return cloneValue(value);
}
function deepEqual(left, right) {
  if (Object.is(left, right)) {
    return true;
  }
  if (Array.isArray(left) && Array.isArray(right)) {
    return left.length === right.length && left.every((entry, index) => deepEqual(entry, right[index]));
  }
  if (left && right && typeof left === "object" && typeof right === "object") {
    const leftKeys = Object.keys(left).sort();
    const rightKeys = Object.keys(right).sort();
    if (!deepEqual(leftKeys, rightKeys)) {
      return false;
    }
    return leftKeys.every((key) => deepEqual(left[key], right[key]));
  }
  return false;
}
function resolveNowProvider(now) {
  if (typeof now === "function") {
    return () => coerceDate(now());
  }
  if (now !== void 0) {
    const fixed = coerceDate(now);
    return () => new Date(fixed.getTime());
  }
  return () => /* @__PURE__ */ new Date();
}
function coerceDate(value) {
  if (value instanceof Date) {
    return new Date(value.getTime());
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? /* @__PURE__ */ new Date() : parsed;
}
function toBasePath(path) {
  return wasmNormalizeIndexedPath(path).replace(/\[\*\]/g, "");
}
function parseInstanceTarget(path) {
  const explicit = path.match(/^instances\.([a-zA-Z][a-zA-Z0-9_]*)\.?(.*)$/);
  if (explicit) {
    return {
      instanceName: explicit[1],
      instancePath: explicit[2] || void 0
    };
  }
  const felSyntax = path.match(/^@instance\((['"])([^'"]+)\1\)\.?(.*)$/);
  if (felSyntax) {
    return {
      instanceName: felSyntax[2],
      instancePath: felSyntax[3] || void 0
    };
  }
  return null;
}
function splitIndexedPath(path) {
  return path.match(/[^.[\]]+|\[\d+\]/g)?.map((segment) => segment.startsWith("[") ? segment : segment) ?? [];
}
function appendPath(base, segment) {
  return segment.startsWith("[") ? `${base}${segment}` : `${base}.${segment}`;
}
function parentPathOf(path) {
  if (!path) {
    return "";
  }
  const segments = path.match(/[^.[\]]+|\[\d+\]/g) ?? [];
  if (segments.length <= 1) {
    return "";
  }
  const parts = segments.slice(0, -1);
  let current = parts[0] ?? "";
  for (let index = 1; index < parts.length; index += 1) {
    current = appendPath(current, parts[index]);
  }
  return current;
}
function getAncestorBasePaths(path) {
  const segments = splitIndexedPath(toBasePath(path));
  const result = [];
  for (let index = segments.length; index >= 1; index -= 1) {
    result.push(segments.slice(0, index).join("."));
  }
  return result;
}
function getScopeAncestors(scopePath) {
  const stripped = toBasePath(scopePath);
  if (!stripped) {
    return [];
  }
  const parts = stripped.split(".").filter(Boolean);
  const scopes = [];
  for (let index = 1; index <= parts.length; index += 1) {
    scopes.push(parts.slice(0, index).join("."));
  }
  return scopes;
}
function getNestedValue(target, path) {
  const tokens = path.match(/[^.[\]]+|\[(\d+)\]/g) ?? [];
  let current = target;
  for (const token of tokens) {
    if (current === null || current === void 0) {
      return void 0;
    }
    if (token.startsWith("[")) {
      const index = Number(token.slice(1, -1));
      current = current[index];
    } else {
      current = current[token];
    }
  }
  return current;
}
function setNestedPathValue(target, path, value) {
  const tokens = path.match(/[^.[\]]+|\[(\d+)\]/g) ?? [];
  let current = target;
  for (let index = 0; index < tokens.length - 1; index += 1) {
    const token = tokens[index];
    const next = tokens[index + 1];
    if (token.startsWith("[")) {
      const arrayIndex = Number(token.slice(1, -1));
      current[arrayIndex] ?? (current[arrayIndex] = next?.startsWith("[") ? [] : {});
      current = current[arrayIndex];
      continue;
    }
    current[token] ?? (current[token] = next?.startsWith("[") ? [] : {});
    current = current[token];
  }
  const last = tokens[tokens.length - 1];
  if (!last) {
    return;
  }
  if (last.startsWith("[")) {
    current[Number(last.slice(1, -1))] = value;
  } else {
    current[last] = value;
  }
}
function setExpressionContextValue(target, path, value) {
  const tokens = path.match(/[^.[\]]+|\[(\d+)\]/g) ?? [];
  if (tokens.length === 0) {
    return;
  }
  let current = target;
  for (let index = 0; index < tokens.length - 1; index += 1) {
    if (current === null || current === void 0 || typeof current !== "object") {
      return;
    }
    const token = tokens[index];
    const next = tokens[index + 1];
    if (token.startsWith("[")) {
      const arrayIndex = Number(token.slice(1, -1));
      const existing2 = current[arrayIndex];
      if (existing2 !== void 0 && (existing2 === null || typeof existing2 !== "object")) {
        return;
      }
      current[arrayIndex] ?? (current[arrayIndex] = next?.startsWith("[") ? [] : {});
      current = current[arrayIndex];
      continue;
    }
    const existing = current[token];
    if (existing !== void 0 && (existing === null || typeof existing !== "object")) {
      return;
    }
    current[token] ?? (current[token] = next?.startsWith("[") ? [] : {});
    current = current[token];
  }
  if (current === null || current === void 0 || typeof current !== "object") {
    return;
  }
  const last = tokens[tokens.length - 1];
  if (last.startsWith("[")) {
    current[Number(last.slice(1, -1))] = value;
  } else {
    current[last] = value;
  }
}
function setResponsePathValue(target, path, value) {
  const tokens = path.match(/[^.[\]]+|\[(\d+)\]/g) ?? [];
  if (tokens.length === 0) {
    return;
  }
  let current = target;
  for (let index = 0; index < tokens.length - 1; index += 1) {
    const token = tokens[index];
    const next = tokens[index + 1];
    if (token.startsWith("[")) {
      const arrayIndex = Number(token.slice(1, -1));
      const existing2 = current[arrayIndex];
      if (existing2 !== void 0 && (existing2 === null || typeof existing2 !== "object")) {
        const fallbackPath = tokens.slice(index + 1).join(".");
        setResponsePathValue(target, fallbackPath, value);
        return;
      }
      current[arrayIndex] ?? (current[arrayIndex] = next?.startsWith("[") ? [] : {});
      current = current[arrayIndex];
      continue;
    }
    const existing = current[token];
    if (existing !== void 0 && (existing === null || typeof existing !== "object")) {
      const fallbackPath = tokens.slice(0, index).concat(tokens.slice(index + 1)).join(".");
      setResponsePathValue(target, fallbackPath, value);
      return;
    }
    current[token] ?? (current[token] = next?.startsWith("[") ? [] : {});
    current = current[token];
  }
  const last = tokens[tokens.length - 1];
  if (last.startsWith("[")) {
    current[Number(last.slice(1, -1))] = value;
  } else {
    current[last] = value;
  }
}
function buildGroupSnapshotForPath(prefix, signals) {
  const snapshot = {};
  for (const [path, signalRef] of Object.entries(signals)) {
    if (!path.startsWith(`${prefix}.`)) {
      continue;
    }
    const relative = path.slice(prefix.length + 1);
    if (!relative || relative.includes("[")) {
      continue;
    }
    setNestedPathValue(snapshot, relative, cloneValue(signalRef.value));
  }
  return snapshot;
}
function buildRepeatCollection(groupPath, count, signals) {
  const rows = [];
  for (let index = 0; index < count; index += 1) {
    const prefix = `${groupPath}[${index}]`;
    const row = {};
    for (const [path, signalRef] of Object.entries(signals)) {
      if (!path.startsWith(`${prefix}.`)) {
        continue;
      }
      const relative = path.slice(prefix.length + 1);
      setResponsePathValue(row, relative, cloneValue(signalRef.value));
    }
    rows.push(row);
  }
  return rows;
}
function getRepeatAncestors(currentItemPath, repeats) {
  const matches = currentItemPath.match(/[^.[\]]+\[\d+\]|[^.[\]]+/g) ?? [];
  const ancestors = [];
  let current = "";
  for (const segment of matches) {
    const repeatMatch = segment.match(/^(.+)\[(\d+)\]$/);
    if (repeatMatch) {
      current = current ? `${current}.${repeatMatch[1]}` : repeatMatch[1];
      if (repeats[current]) {
        ancestors.push({
          groupPath: current,
          index: Number(repeatMatch[2]),
          count: repeats[current].value
        });
      }
      current = `${current}[${repeatMatch[2]}]`;
    } else {
      current = current ? `${current}.${segment}` : segment;
    }
  }
  return ancestors;
}
function isEmptyValue(value) {
  return value === null || value === void 0 || value === "" || Array.isArray(value) && value.length === 0;
}
function safeEvaluateExpression(expression, context) {
  try {
    return wasmEvalFELWithContext(expression, context);
  } catch {
    return null;
  }
}
function extractInlineBind(item, path) {
  const bind = { path };
  let used = false;
  for (const key of [
    "calculate",
    "constraint",
    "constraintMessage",
    "relevant",
    "required",
    "readonly",
    "default",
    "precision",
    "disabledDisplay",
    "whitespace",
    "nonRelevantBehavior",
    "remoteOptions",
    "excludedValue"
  ]) {
    if (item[key] !== void 0) {
      bind[key] = item[key];
      used = true;
    }
  }
  if (item.visible !== void 0 && bind.relevant === void 0) {
    bind.relevant = item.visible;
    used = true;
  }
  return used ? bind : null;
}
function detectNamedCycle(graph, message) {
  const visiting = /* @__PURE__ */ new Set();
  const visited = /* @__PURE__ */ new Set();
  const visit = (node) => {
    if (visited.has(node)) {
      return;
    }
    if (visiting.has(node)) {
      throw new Error(message);
    }
    visiting.add(node);
    for (const dep of graph.get(node) ?? []) {
      if (graph.has(dep)) {
        visit(dep);
      }
    }
    visiting.delete(node);
    visited.add(node);
  };
  for (const node of graph.keys()) {
    visit(node);
  }
}
function snapshotSignals(signals) {
  const snapshot = {};
  for (const [path, signalRef] of Object.entries(signals)) {
    snapshot[path] = cloneValue(signalRef.value);
  }
  return snapshot;
}
function toFelIndexedPath(path) {
  return path.replace(/\[(\d+)\]/g, (_match, index) => `[${Number(index) + 1}]`);
}
function resolveRelativeDependency(dep, parentPath, selfPath) {
  if (!dep) {
    return selfPath;
  }
  if (dep.includes(".")) {
    return dep;
  }
  return parentPath ? `${parentPath}.${dep}` : dep;
}

// node_modules/@formspec-org/engine/dist/engine/response-assembly.js
function buildFormspecResponseEnvelope(options) {
  const response = {
    $formspecResponse: "1.0",
    definitionUrl: options.definition.url ?? "http://example.org/form",
    definitionVersion: options.definition.version ?? "1.0.0",
    status: options.report.valid ? "completed" : "in-progress",
    data: options.data,
    validationResults: options.report.results,
    authored: options.timestamp
  };
  if (options.meta?.id) {
    response.id = options.meta.id;
  }
  if (options.meta?.author) {
    response.author = options.meta.author;
  }
  if (options.meta?.subject) {
    response.subject = options.meta.subject;
  }
  return response;
}
function collectSubmitModeShapeValidationResults(submitEval, shapeTiming) {
  const results = [];
  for (const validation of submitEval.validations) {
    if (!validation.shapeId) {
      continue;
    }
    if ((shapeTiming.get(validation.shapeId) ?? "continuous") === "submit") {
      results.push(toValidationResult(validation));
    }
  }
  return results;
}
function buildValidationReportEnvelope(results, timestamp) {
  const finalResults = results.map((result) => {
    if (result.constraintKind === "cardinality") {
      const { source: _source, ...rest } = result;
      return rest;
    }
    return result;
  });
  const counts = { error: 0, warning: 0, info: 0 };
  for (const result of finalResults) {
    counts[result.severity] += 1;
  }
  return {
    $formspecValidationReport: "1.0",
    valid: counts.error === 0,
    results: finalResults,
    counts,
    timestamp
  };
}
function migrateResponseData(definition, responseData, fromVersion, options) {
  if (!Array.isArray(definition.migrations)) {
    return responseData;
  }
  return JSON.parse(wasmApplyMigrationsToResponseData(JSON.stringify(definition), JSON.stringify(responseData), fromVersion, options.nowIso));
}
function resolvePinnedDefinition(response, definitions) {
  const exact = definitions.find((definition) => definition.url === response.definitionUrl && definition.version === response.definitionVersion);
  if (exact) {
    return exact;
  }
  const availableVersions = definitions.filter((definition) => definition.url === response.definitionUrl).map((definition) => definition.version).filter((version) => typeof version === "string").sort();
  let message = `No definition found for pinned response ${response.definitionUrl}@${response.definitionVersion}`;
  if (availableVersions.length > 0) {
    message += `; available versions: ${availableVersions.join(", ")}`;
  }
  throw new Error(message);
}

// node_modules/@formspec-org/engine/dist/diff.js
function isPlainObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
function deepEqual2(left, right) {
  if (Object.is(left, right)) {
    return true;
  }
  if (Array.isArray(left) && Array.isArray(right)) {
    if (left.length !== right.length) {
      return false;
    }
    for (let index = 0; index < left.length; index += 1) {
      if (!deepEqual2(left[index], right[index])) {
        return false;
      }
    }
    return true;
  }
  if (isPlainObject(left) && isPlainObject(right)) {
    const leftKeys = Object.keys(left).sort();
    const rightKeys = Object.keys(right).sort();
    if (!deepEqual2(leftKeys, rightKeys)) {
      return false;
    }
    for (const key of leftKeys) {
      if (!deepEqual2(left[key], right[key])) {
        return false;
      }
    }
    return true;
  }
  return false;
}
function diffRecord(previous, next) {
  const changed = {};
  const removed = [];
  const keys = /* @__PURE__ */ new Set([...Object.keys(previous), ...Object.keys(next)]);
  for (const key of keys) {
    const hasPrevious = Object.prototype.hasOwnProperty.call(previous, key);
    const hasNext = Object.prototype.hasOwnProperty.call(next, key);
    if (!hasNext) {
      removed.push(key);
      continue;
    }
    if (!hasPrevious || !deepEqual2(previous[key], next[key])) {
      changed[key] = next[key];
    }
  }
  removed.sort();
  return { changed, removed };
}
function groupValidations(validations) {
  const grouped = {};
  for (const validation of validations) {
    if (validation.shapeId) {
      continue;
    }
    const key = validation.path;
    (grouped[key] ?? (grouped[key] = [])).push(validation);
  }
  return grouped;
}
function groupShapeResults(validations) {
  var _a;
  const grouped = {};
  for (const validation of validations) {
    if (!validation.shapeId) {
      continue;
    }
    (grouped[_a = validation.shapeId] ?? (grouped[_a] = [])).push(validation);
  }
  return grouped;
}
function diffEvalResults(previous, next) {
  const previousValues = previous?.values ?? {};
  const previousVariables = previous?.variables ?? {};
  const previousRequired = previous?.required ?? {};
  const previousReadonly = previous?.readonly ?? {};
  const previousNonRelevant = new Set(previous?.nonRelevant ?? []);
  const nextNonRelevant = new Set(next.nonRelevant);
  const relevant = {};
  const relevanceKeys = /* @__PURE__ */ new Set([...previousNonRelevant, ...nextNonRelevant]);
  for (const key of relevanceKeys) {
    const previousRelevant = !previousNonRelevant.has(key);
    const nextRelevant = !nextNonRelevant.has(key);
    if (previous === null || previousRelevant !== nextRelevant) {
      relevant[key] = nextRelevant;
    }
  }
  const validationGroups = groupValidations(next.validations);
  const previousValidationGroups = groupValidations(previous?.validations ?? []);
  const validationDiff = diffRecord(previousValidationGroups, validationGroups);
  const shapeGroups = groupShapeResults(next.validations);
  const previousShapeGroups = groupShapeResults(previous?.validations ?? []);
  const shapeDiff = diffRecord(previousShapeGroups, shapeGroups);
  const valueDiff = diffRecord(previousValues, next.values);
  const variableDiff = diffRecord(previousVariables, next.variables);
  const requiredDiff = diffRecord(previousRequired, next.required);
  const readonlyDiff = diffRecord(previousReadonly, next.readonly);
  const delta = {
    values: valueDiff.changed,
    removedValues: valueDiff.removed,
    relevant,
    required: requiredDiff.changed,
    readonly: readonlyDiff.changed,
    validations: validationDiff.changed,
    removedValidationPaths: validationDiff.removed,
    shapeResults: shapeDiff.changed,
    removedShapeIds: shapeDiff.removed,
    variables: variableDiff.changed,
    removedVariables: variableDiff.removed
  };
  Object.defineProperties(delta, {
    valueUpdates: { value: delta.values, enumerable: false },
    relevantUpdates: { value: delta.relevant, enumerable: false },
    requiredUpdates: { value: delta.required, enumerable: false },
    readonlyUpdates: { value: delta.readonly, enumerable: false },
    validationUpdates: { value: delta.validations, enumerable: false },
    shapeUpdates: { value: delta.shapeResults, enumerable: false },
    variableUpdates: { value: delta.variables, enumerable: false }
  });
  return delta;
}

// node_modules/@formspec-org/engine/dist/locale.js
var LocaleStore = class _LocaleStore {
  constructor(rx, directionMode) {
    this._documents = /* @__PURE__ */ new Map();
    this._rx = rx;
    this._directionMode = directionMode ?? "ltr";
    this.activeLocale = rx.signal("");
    this.version = rx.signal(0);
    this._directionVersion = rx.signal(0);
    this.direction = rx.computed(() => {
      this.activeLocale.value;
      this._directionVersion.value;
      if (this._directionMode !== "auto")
        return this._directionMode;
      const lang = this.activeLocale.value.split("-")[0].toLowerCase();
      return _LocaleStore.RTL_LANGUAGES.has(lang) ? "rtl" : "ltr";
    });
  }
  setDirectionMode(mode) {
    this._directionMode = mode;
    this._directionVersion.value += 1;
  }
  loadLocale(doc) {
    const code = _LocaleStore.normalizeCode(doc.locale);
    this._documents.set(code, { ...doc, locale: code });
    this.version.value += 1;
  }
  setLocale(code) {
    this.activeLocale.value = _LocaleStore.normalizeCode(code);
    this.version.value += 1;
  }
  getAvailableLocales() {
    return [...this._documents.keys()];
  }
  lookupKey(key) {
    return this.lookupKeyWithMeta(key).value;
  }
  lookupKeyWithMeta(key) {
    const activeCode = this.activeLocale.value;
    if (!activeCode)
      return { value: null, source: null };
    return this._cascadeLookup(key, activeCode, /* @__PURE__ */ new Set());
  }
  _cascadeLookup(key, code, visited) {
    if (visited.has(code))
      return { value: null, source: null };
    visited.add(code);
    const doc = this._documents.get(code);
    if (doc && key in doc.strings) {
      const isActive = code === this.activeLocale.value;
      return {
        value: doc.strings[key],
        source: isActive ? "regional" : doc.fallback != null ? "fallback" : "implicit",
        localeCode: code
      };
    }
    if (doc?.fallback) {
      const fallbackCode = _LocaleStore.normalizeCode(doc.fallback);
      const result = this._cascadeLookup(key, fallbackCode, visited);
      if (result.value !== null) {
        return { ...result, source: "fallback" };
      }
    }
    const dashIdx = code.indexOf("-");
    if (dashIdx > 0) {
      const baseCode = code.substring(0, dashIdx);
      if (!visited.has(baseCode)) {
        const result = this._cascadeLookup(key, baseCode, visited);
        if (result.value !== null) {
          return { ...result, source: "implicit" };
        }
      }
    }
    return { value: null, source: null };
  }
  /**
   * Normalize BCP 47: lowercase language, title-case script (4 chars),
   * uppercase region (2 chars), lowercase variants/extensions.
   */
  static normalizeCode(code) {
    const parts = code.split("-");
    parts[0] = parts[0].toLowerCase();
    for (let i2 = 1; i2 < parts.length; i2++) {
      const p2 = parts[i2];
      if (p2.length === 2) {
        parts[i2] = p2.toUpperCase();
      } else if (p2.length === 4 && /^[a-zA-Z]+$/.test(p2)) {
        parts[i2] = p2.charAt(0).toUpperCase() + p2.slice(1).toLowerCase();
      } else {
        parts[i2] = p2.toLowerCase();
      }
    }
    return parts.join("-");
  }
};
LocaleStore.RTL_LANGUAGES = /* @__PURE__ */ new Set([
  "ar",
  "he",
  "fa",
  "ur",
  "ps",
  "sd",
  "yi"
]);

// node_modules/@formspec-org/engine/dist/interpolate-message.js
function interpolateMessage(template, evaluator) {
  if (!template)
    return { text: template, warnings: [] };
  const warnings = [];
  const SENTINEL_OPEN = "\0ESC_OPEN\0";
  let work = template.replace(/\{\{\{\{/g, SENTINEL_OPEN);
  const pattern = /\{\{((?:[^}]|\}(?!\}))*)\}\}/g;
  const segments = [];
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(work)) !== null) {
    segments.push(work.slice(lastIndex, match.index));
    const expr = match[1];
    try {
      const raw = evaluator(expr);
      segments.push(coerce(raw));
    } catch (err) {
      segments.push(match[0]);
      warnings.push({
        expression: expr,
        error: err instanceof Error ? err.message : String(err)
      });
    }
    lastIndex = match.index + match[0].length;
  }
  segments.push(work.slice(lastIndex));
  const joined = segments.join("");
  const text = joined.replace(new RegExp(SENTINEL_OPEN, "g"), "{{");
  return { text, warnings };
}
function coerce(value) {
  if (value === null || value === void 0)
    return "";
  if (typeof value === "boolean")
    return value ? "true" : "false";
  return String(value);
}

// node_modules/@formspec-org/engine/dist/field-view-model.js
var CODE_SYNTHESIS = {
  required: "REQUIRED",
  type: "TYPE_MISMATCH",
  constraint: "CONSTRAINT_FAILED",
  shape: "SHAPE_FAILED",
  external: "EXTERNAL_FAILED"
};
function createFieldViewModel(deps) {
  const { rx, localeStore, templatePath, evalFEL: evalFEL2 } = deps;
  function resolveLocaleString(key, fallback) {
    localeStore.version.value;
    const localized = localeStore.lookupKey(key);
    const raw = localized ?? fallback ?? null;
    if (raw === null)
      return null;
    const { text } = interpolateMessage(raw, evalFEL2);
    return text;
  }
  const label = rx.computed(() => {
    localeStore.version.value;
    const context = deps.getLabelContext();
    const labels = deps.getItemLabels();
    const inlineLabel = deps.getItemLabel();
    if (context) {
      const contextKey = `${templatePath}.label@${context}`;
      const fromLocale2 = localeStore.lookupKey(contextKey);
      if (fromLocale2 !== null) {
        return interpolateMessage(fromLocale2, evalFEL2).text;
      }
      const plainKey2 = `${templatePath}.label`;
      const plainFromLocale = localeStore.lookupKey(plainKey2);
      if (plainFromLocale !== null) {
        return interpolateMessage(plainFromLocale, evalFEL2).text;
      }
      if (labels?.[context]) {
        return interpolateMessage(labels[context], evalFEL2).text;
      }
      return interpolateMessage(inlineLabel, evalFEL2).text;
    }
    const plainKey = `${templatePath}.label`;
    const fromLocale = localeStore.lookupKey(plainKey);
    if (fromLocale !== null) {
      return interpolateMessage(fromLocale, evalFEL2).text;
    }
    return interpolateMessage(inlineLabel, evalFEL2).text;
  });
  const hint = rx.computed(() => {
    return resolveLocaleString(`${templatePath}.hint`, deps.getItemHint());
  });
  const description = rx.computed(() => {
    return resolveLocaleString(`${templatePath}.description`, deps.getItemDescription());
  });
  const value = rx.computed(() => deps.getFieldValue().value);
  const required = rx.computed(() => deps.getRequired().value);
  const visible = rx.computed(() => deps.getVisible().value);
  const readonly_ = rx.computed(() => deps.getReadonly().value);
  const errors = rx.computed(() => {
    localeStore.version.value;
    const rawErrors = deps.getErrors().value;
    if (!rawErrors.length)
      return [];
    return rawErrors.map((err) => {
      const code = err.code ?? CODE_SYNTHESIS[err.constraintKind] ?? "UNKNOWN";
      const resolvedMessage = resolveValidationMessage(err, code);
      return {
        path: err.path,
        severity: err.severity,
        constraintKind: err.constraintKind ?? "unknown",
        code,
        message: resolvedMessage
      };
    });
  });
  const firstError = rx.computed(() => {
    const errs = errors.value;
    const firstErr = errs.find((e2) => e2.severity === "error");
    return firstErr?.message ?? null;
  });
  const options = rx.computed(() => {
    localeStore.version.value;
    const rawOptions = deps.getOptions().value;
    const optionSetName = deps.getOptionSetName();
    return rawOptions.map((opt) => ({
      value: opt.value,
      label: resolveOptionLabel(opt, optionSetName)
    }));
  });
  const optionsState = rx.computed(() => deps.getOptionsState().value);
  function resolveValidationMessage(err, code) {
    const codeKey = `${templatePath}.errors.${code}`;
    const fromCode = localeStore.lookupKey(codeKey);
    if (fromCode !== null) {
      return interpolateMessage(fromCode, evalFEL2).text;
    }
    if (err.constraintKind === "required") {
      const reqKey = `${templatePath}.requiredMessage`;
      const fromReq = localeStore.lookupKey(reqKey);
      if (fromReq !== null)
        return interpolateMessage(fromReq, evalFEL2).text;
    } else {
      const constKey = `${templatePath}.constraintMessage`;
      const fromConst = localeStore.lookupKey(constKey);
      if (fromConst !== null)
        return interpolateMessage(fromConst, evalFEL2).text;
    }
    if (err.constraintMessage)
      return interpolateMessage(err.constraintMessage, evalFEL2).text;
    return err.message ?? "Validation error";
  }
  function resolveOptionLabel(opt, optionSetName) {
    const escapedValue = escapeOptionValue(opt.value);
    const fieldKey = `${templatePath}.options.${escapedValue}.label`;
    const fromField = localeStore.lookupKey(fieldKey);
    if (fromField !== null)
      return interpolateMessage(fromField, evalFEL2).text;
    if (optionSetName) {
      const setKey = `$optionSet.${optionSetName}.${escapedValue}.label`;
      const fromSet = localeStore.lookupKey(setKey);
      if (fromSet !== null)
        return interpolateMessage(fromSet, evalFEL2).text;
    }
    return opt.label;
  }
  return {
    templatePath: deps.templatePath,
    instancePath: deps.instancePath,
    id: deps.id,
    itemKey: deps.itemKey,
    dataType: deps.dataType,
    disabledDisplay: deps.getDisabledDisplay(),
    label,
    hint,
    description,
    value,
    required,
    visible,
    readonly: readonly_,
    errors,
    firstError,
    options,
    optionsState,
    setValue: deps.setFieldValue
  };
}
function escapeOptionValue(value) {
  return value.replace(/\\/g, "\\\\").replace(/\./g, "\\.");
}

// node_modules/@formspec-org/engine/dist/form-view-model.js
function createFormViewModel(deps) {
  const { rx, localeStore, getDefinitionTitle, getDefinitionDescription, getPageTitle, getPageDescription, evalFEL: evalFEL2, getValidationCounts, getIsValid } = deps;
  const pageTitleCache = /* @__PURE__ */ new Map();
  const pageDescCache = /* @__PURE__ */ new Map();
  function resolveString(key, fallback, evaluate) {
    localeStore.version.value;
    const localized = localeStore.lookupKey(key);
    const raw = localized ?? fallback ?? "";
    const { text } = interpolateMessage(raw, evaluate);
    return text;
  }
  const title = rx.computed(() => resolveString("$form.title", getDefinitionTitle(), evalFEL2));
  const description = rx.computed(() => resolveString("$form.description", getDefinitionDescription(), evalFEL2));
  const isValid = rx.computed(() => getIsValid());
  const validationSummary = rx.computed(() => getValidationCounts());
  return {
    title,
    description,
    pageTitle(pageId) {
      let sig = pageTitleCache.get(pageId);
      if (!sig) {
        sig = rx.computed(() => resolveString(`$page.${pageId}.title`, getPageTitle(pageId), evalFEL2));
        pageTitleCache.set(pageId, sig);
      }
      return sig;
    },
    pageDescription(pageId) {
      let sig = pageDescCache.get(pageId);
      if (!sig) {
        sig = rx.computed(() => resolveString(`$page.${pageId}.description`, getPageDescription(pageId), evalFEL2));
        pageDescCache.set(pageId, sig);
      }
      return sig;
    },
    isValid,
    validationSummary
  };
}

// node_modules/@formspec-org/engine/dist/engine/FormEngine.js
init_wasm_bridge_runtime();

// node_modules/@formspec-org/engine/dist/engine/definition-setup.js
init_wasm_bridge_runtime();
function resolveOptionSetsOnDefinition2(definition) {
  return JSON.parse(wasmResolveOptionSetsOnDefinition(JSON.stringify(definition)));
}
function validateVariableDefinitionCycles(variableDefs) {
  const graph = /* @__PURE__ */ new Map();
  for (const variableDef of variableDefs) {
    const deps = /* @__PURE__ */ new Set();
    for (const name of wasmAnalyzeFEL(variableDef.expression).variables) {
      deps.add(name);
    }
    graph.set(variableDef.name, deps);
  }
  detectNamedCycle(graph, "Circular variable dependency");
}
function validateCalculateBindCycles(bindConfigs) {
  const graph = /* @__PURE__ */ new Map();
  for (const [path, bind] of Object.entries(bindConfigs)) {
    if (!bind.calculate || parseInstanceTarget(path)) {
      continue;
    }
    const deps = /* @__PURE__ */ new Set();
    const parentPath = parentPathOf(path);
    for (const dep of wasmGetFELDependencies(bind.calculate)) {
      const resolved = resolveRelativeDependency(dep, parentPath, path);
      if (resolved) {
        deps.add(toBasePath(resolved));
      }
    }
    graph.set(path, deps);
  }
  detectNamedCycle(graph, "Cyclic dependency detected");
}

// node_modules/@formspec-org/engine/dist/engine/instance-schema.js
function validateInstanceDataAgainstSchema(instanceName, data, schema) {
  if (!schema || typeof schema !== "object") {
    return;
  }
  for (const [path, dataType] of Object.entries(schema)) {
    if (typeof dataType !== "string") {
      continue;
    }
    const value = getNestedValue(data, path);
    if (value === void 0 || value === null) {
      continue;
    }
    if (!validateDataType(value, dataType)) {
      throw new Error(`Instance '${instanceName}' schema mismatch at '${path}': expected ${dataType}`);
    }
  }
}

// node_modules/@formspec-org/engine/dist/engine/reactive-patches.js
function patchValueSignalsFromWasm(options) {
  for (const [path, value] of Object.entries(options.values)) {
    const sig = options.signals[path];
    if (!sig) {
      continue;
    }
    const basePath = toBasePath(path);
    const item = options.fieldItems.get(basePath);
    const normalizedValue = normalizeWasmValue(value);
    const moneyAmount = normalizedValue?.amount;
    const parsedMoneyAmount = typeof moneyAmount === "string" && moneyAmount !== "" ? Number(moneyAmount) : moneyAmount === "" ? null : moneyAmount;
    const coercedValue = item?.dataType === "money" && normalizedValue && typeof normalizedValue === "object" && typeof moneyAmount === "string" ? {
      ...normalizedValue,
      amount: parsedMoneyAmount !== null && Number.isNaN(parsedMoneyAmount) ? moneyAmount : parsedMoneyAmount
    } : normalizedValue;
    const hasExpressionInitial = typeof item?.initialValue === "string" && item.initialValue.startsWith("=");
    if (!options.calculatedFields.has(basePath) && hasExpressionInitial && !(path in options.data)) {
      options.data[path] = cloneValue(coercedValue);
    } else if (!options.calculatedFields.has(basePath) && options.bindConfigs[basePath]?.default !== void 0 && path in options.data && isEmptyValue(options.data[path]) && !deepEqual(options.data[path], coercedValue)) {
      options.data[path] = cloneValue(coercedValue);
    }
    let rawValue;
    if (!options.calculatedFields.has(basePath) && path in options.data) {
      rawValue = options.data[path];
    } else {
      rawValue = coercedValue;
    }
    sig.value = normalizeWasmValue(rawValue);
  }
}
function patchDeltaSignalsFromWasm(rx, delta, options) {
  var _a, _b, _c, _d, _e, _f;
  for (const [path, relevant] of Object.entries(delta.relevant)) {
    (_a = options.relevantSignals)[path] ?? (_a[path] = rx.signal(true));
    options.relevantSignals[path].value = relevant;
  }
  for (const [path, required] of Object.entries(delta.required)) {
    (_b = options.requiredSignals)[path] ?? (_b[path] = rx.signal(false));
    options.requiredSignals[path].value = required;
  }
  for (const [path, readonly] of Object.entries(delta.readonly)) {
    (_c = options.readonlySignals)[path] ?? (_c[path] = rx.signal(false));
    options.readonlySignals[path].value = readonly || options.prePopulateReadonly.has(path);
  }
  for (const [path, results] of Object.entries(delta.validations)) {
    (_d = options.validationResults)[path] ?? (_d[path] = rx.signal([]));
    options.validationResults[path].value = toValidationResults(results);
  }
  for (const path of delta.removedValidationPaths) {
    if (options.validationResults[path]) {
      options.validationResults[path].value = [];
    }
  }
  for (const [shapeId, results] of Object.entries(delta.shapeResults)) {
    (_e = options.shapeResults)[shapeId] ?? (_e[shapeId] = rx.signal([]));
    options.shapeResults[shapeId].value = toValidationResults(results);
  }
  for (const shapeId of delta.removedShapeIds) {
    if (options.shapeResults[shapeId]) {
      options.shapeResults[shapeId].value = [];
    }
  }
  for (const [name, value] of Object.entries(delta.variables)) {
    const signalKeys = options.variableSignalKeys.get(name) ?? [name];
    for (const key of signalKeys) {
      (_f = options.variableSignals)[key] ?? (_f[key] = rx.signal(void 0));
      options.variableSignals[key].value = normalizeWasmValue(value);
    }
  }
  for (const name of delta.removedVariables) {
    const signalKeys = options.variableSignalKeys.get(name) ?? [name];
    for (const key of signalKeys) {
      if (options.variableSignals[key]) {
        options.variableSignals[key].value = void 0;
      }
    }
  }
}
function patchErrorSignalsFromWasm(rx, options) {
  var _a;
  for (const [path, signalRef] of Object.entries(options.validationResults)) {
    const firstError = signalRef.value.find((result) => result.severity === "error")?.message ?? null;
    (_a = options.errorSignals)[path] ?? (_a[path] = rx.signal(null));
    options.errorSignals[path].value = firstError;
  }
}

// node_modules/@formspec-org/engine/dist/engine/repeat-ops.js
function clearRepeatIndexedSubtree(options) {
  const prefix = `${options.rootRepeatPath}[`;
  const stores = [
    options.signals,
    options.relevantSignals,
    options.requiredSignals,
    options.readonlySignals,
    options.errorSignals,
    options.validationResults,
    options.optionSignals,
    options.optionStateSignals,
    options.repeats
  ];
  for (const store of stores) {
    for (const key of Object.keys(store)) {
      if (key.startsWith(prefix)) {
        delete store[key];
      }
    }
  }
  for (const key of Object.keys(options.data)) {
    if (key.startsWith(prefix)) {
      delete options.data[key];
    }
  }
}
function snapshotRepeatGroupTree(items, prefix, readFieldValue, getRepeatCount) {
  const snapshot = {};
  for (const item of items) {
    const path = `${prefix}.${item.key}`;
    if (item.type === "field") {
      snapshot[item.key] = readFieldValue(path);
      continue;
    }
    if (item.type === "group") {
      if (item.repeatable) {
        const count = getRepeatCount(path);
        const rows = [];
        for (let index = 0; index < count; index += 1) {
          rows.push(snapshotRepeatGroupTree(item.children ?? [], `${path}[${index}]`, readFieldValue, getRepeatCount));
        }
        snapshot[item.key] = rows;
      } else {
        snapshot[item.key] = snapshotRepeatGroupTree(item.children ?? [], path, readFieldValue, getRepeatCount);
      }
    }
  }
  return snapshot;
}
function applyRepeatGroupTreeSnapshot(items, prefix, snapshot, writeField) {
  for (const item of items) {
    const path = `${prefix}.${item.key}`;
    if (item.type === "field") {
      writeField(path, snapshot?.[item.key]);
      continue;
    }
    if (item.type === "group") {
      if (item.repeatable) {
        const rows = Array.isArray(snapshot?.[item.key]) ? snapshot[item.key] : [];
        for (let index = 0; index < rows.length; index += 1) {
          applyRepeatGroupTreeSnapshot(item.children ?? [], `${path}[${index}]`, rows[index] ?? {}, writeField);
        }
      } else {
        applyRepeatGroupTreeSnapshot(item.children ?? [], path, snapshot?.[item.key], writeField);
      }
    }
  }
}

// node_modules/@formspec-org/engine/dist/engine/wasm-fel.js
init_wasm_bridge_runtime();
function wasmEvaluateDefinitionPayload(options) {
  return {
    nowIso: options.nowIso,
    ...options.trigger !== void 0 ? { trigger: options.trigger } : {},
    previousValidations: options.previousResult?.validations,
    previousNonRelevant: options.previousResult?.nonRelevant,
    instances: options.instances,
    registryDocuments: options.registryDocuments,
    repeatCounts: options.repeatCounts
  };
}
function mergeWasmEvalWithExternalValidations(result, options) {
  return {
    ...result,
    validations: [...result.validations, ...options.externalValidations]
  };
}
function normalizeExpressionForWasmEvaluation(options) {
  const repeatCounts = {};
  for (const [path, sig] of Object.entries(options.repeats)) {
    repeatCounts[path] = sig.value;
  }
  return wasmPrepareFelExpression(JSON.stringify({
    expression: options.expression,
    currentItemPath: options.currentItemPath,
    replaceSelfRef: options.replaceSelfRef,
    repeatCounts,
    valuesByPath: snapshotSignals(options.fieldSignals)
  }));
}
function resolveFelFieldValueForWasm(path, value, bindConfigs, fieldIsIrrelevant) {
  const bind = bindConfigs[toBasePath(path)];
  if (bind?.excludedValue === "null" && fieldIsIrrelevant(path)) {
    return null;
  }
  return value;
}
function visibleScopedVariableValues(scopePath, variableDefs, variableSignals, overrides) {
  const visible = {};
  const candidates = ["#", ...getScopeAncestors(scopePath)];
  for (const scope of candidates) {
    for (const variableDef of variableDefs) {
      if ((variableDef.scope ?? "#") !== scope) {
        continue;
      }
      const key = `${variableDef.scope ?? "#"}:${variableDef.name}`;
      visible[variableDef.name] = overrides && Object.prototype.hasOwnProperty.call(overrides, key) ? overrides[key] : variableSignals[key]?.value ?? null;
    }
  }
  return visible;
}
function buildFelRepeatWasmContext(options) {
  const repeatAncestors = getRepeatAncestors(options.currentItemPath, options.repeats);
  if (repeatAncestors.length === 0) {
    return void 0;
  }
  let parent;
  for (const entry of repeatAncestors) {
    const collection = buildRepeatCollection(entry.groupPath, entry.count, options.fieldSignals);
    parent = {
      current: collection[entry.index] ?? null,
      index: entry.index + 1,
      count: entry.count,
      collection,
      parent
    };
  }
  const outerParentPath = parentPathOf(repeatAncestors[repeatAncestors.length - 1].groupPath);
  if (parent && outerParentPath) {
    parent.parent = {
      current: buildGroupSnapshotForPath(outerParentPath, options.fieldSignals),
      index: 1,
      count: 1,
      collection: [buildGroupSnapshotForPath(outerParentPath, options.fieldSignals)],
      parent: parent.parent
    };
  }
  return parent;
}
function buildWasmFelExpressionContext(options) {
  const result = options.resultOverride ?? options.fullResult;
  const rawFields = {
    ...options.dataOverride ?? options.data,
    ...result?.values ?? {},
    ...snapshotSignals(options.fieldSignals)
  };
  const irrelevant = (path) => options.relevantSignals[path]?.value === false;
  const fields = {};
  for (const [path, value] of Object.entries(rawFields)) {
    setExpressionContextValue(fields, path, toWasmContextValue(resolveFelFieldValueForWasm(path, value, options.bindConfigs, irrelevant)));
  }
  const scopePath = parentPathOf(options.currentItemPath);
  if (scopePath) {
    const prefixA = `${scopePath}.`;
    const prefixB = `${scopePath}[`;
    for (const [path, value] of Object.entries(rawFields)) {
      if (path.startsWith(prefixA)) {
        setExpressionContextValue(fields, path.slice(prefixA.length), toWasmContextValue(value));
      } else if (path.startsWith(prefixB)) {
        setExpressionContextValue(fields, path.slice(scopePath.length + 1), toWasmContextValue(value));
      }
    }
  }
  const mipStates = {};
  for (const path of Object.keys(options.fieldSignals)) {
    const state = {
      valid: (options.validationResults[path]?.value ?? []).every((r2) => r2.severity !== "error"),
      relevant: options.relevantSignals[path]?.value ?? true,
      readonly: options.readonlySignals[path]?.value ?? false,
      required: options.requiredSignals[path]?.value ?? false
    };
    if (path.includes("[")) {
      mipStates[toFelIndexedPath(path)] = { ...state };
    } else {
      mipStates[path] = state;
    }
    if (scopePath) {
      const prefixA = `${scopePath}.`;
      const prefixB = `${scopePath}[`;
      if (path.startsWith(prefixA)) {
        mipStates[path.slice(prefixA.length)] = { ...state };
      } else if (path.startsWith(prefixB)) {
        mipStates[path.slice(scopePath.length + 1)] = { ...state };
      }
    }
  }
  return {
    fields,
    variables: Object.fromEntries(Object.entries(visibleScopedVariableValues(options.currentItemPath, options.variableDefs, options.variableSignals, options.scopedVariableOverrides)).map(([key, value]) => [key, toWasmContextValue(value)])),
    mipStates,
    repeatContext: buildFelRepeatWasmContext({
      currentItemPath: options.currentItemPath,
      repeats: options.repeats,
      fieldSignals: options.fieldSignals
    }),
    instances: cloneValue(options.instanceData),
    nowIso: options.nowIso,
    locale: options.locale,
    meta: options.meta
  };
}

// node_modules/@formspec-org/engine/dist/engine/FormEngine.js
var FormEngine = class _FormEngine {
  constructor(definition, runtimeContext, registryEntries, reactiveRuntime = preactReactiveRuntime) {
    this.signals = {};
    this.relevantSignals = {};
    this.requiredSignals = {};
    this.readonlySignals = {};
    this.errorSignals = {};
    this.validationResults = {};
    this.shapeResults = {};
    this.repeats = {};
    this.optionSignals = {};
    this.optionStateSignals = {};
    this.variableSignals = {};
    this.instanceData = {};
    this._bindConfigs = {};
    this._fieldItems = /* @__PURE__ */ new Map();
    this._groupItems = /* @__PURE__ */ new Map();
    this._shapeTiming = /* @__PURE__ */ new Map();
    this._instanceCalculateBinds = [];
    this._displaySignalPaths = /* @__PURE__ */ new Set();
    this._prePopulateReadonly = /* @__PURE__ */ new Set();
    this._calculatedFields = /* @__PURE__ */ new Set();
    this._registryEntries = /* @__PURE__ */ new Map();
    this._registryDocuments = [];
    this._remoteOptionsTasks = [];
    this._instanceSourceTasks = [];
    this._variableSignalKeys = /* @__PURE__ */ new Map();
    this._externalValidation = [];
    this._fieldViewModels = {};
    this._data = {};
    this._previousEvalResult = null;
    this._fullResult = null;
    this._labelContext = null;
    this._runtimeContext = {
      nowProvider: () => /* @__PURE__ */ new Date()
    };
    this._rx = reactiveRuntime;
    this.instanceVersion = this._rx.signal(0);
    this.structureVersion = this._rx.signal(0);
    this._evaluationVersion = this._rx.signal(0);
    this._labelContextSignal = this._rx.signal(null);
    this.definition = cloneValue(definition);
    const directionMode = definition.formPresentation?.direction ?? "ltr";
    this._localeStore = new LocaleStore(this._rx, directionMode);
    this._variableDefs = [...this.definition.variables ?? []];
    if (runtimeContext) {
      this.setRuntimeContext(runtimeContext);
    }
    if (registryEntries) {
      for (const entry of registryEntries) {
        if (entry?.name) {
          this._registryEntries.set(entry.name, entry);
        }
      }
      this._registryDocuments = [{ entries: registryEntries }];
    }
    this.definition = resolveOptionSetsOnDefinition2(this.definition);
    this.initializeOptionSignals();
    this.initializeInstances();
    this.initializeBindConfigs(this.definition.items);
    this.collectInstanceCalculateBinds();
    this.validateInstanceCalculateTargets();
    validateVariableDefinitionCycles(this._variableDefs);
    validateCalculateBindCycles(this._bindConfigs);
    this.registerItems(this.definition.items);
    this.initializeRemoteOptions();
    this._evaluate();
    this._formViewModel = createFormViewModel({
      rx: this._rx,
      localeStore: this._localeStore,
      getDefinitionTitle: () => this.definition.title ?? "",
      getDefinitionDescription: () => this.definition.description,
      getPageTitle: () => void 0,
      getPageDescription: () => void 0,
      evalFEL: (expr) => wasmEvalFELWithContext(expr, this._buildLocaleFELContext()),
      getValidationCounts: () => {
        const report = this.getValidationReport();
        return {
          errors: report.counts?.error ?? 0,
          warnings: report.counts?.warning ?? 0,
          infos: report.counts?.info ?? 0
        };
      },
      getIsValid: () => this.getValidationReport().valid
    });
  }
  static resolvePinnedDefinition(response, definitions) {
    return resolvePinnedDefinition(response, definitions);
  }
  get formPresentation() {
    return this.definition.formPresentation ?? null;
  }
  setRuntimeContext(context = {}) {
    if (Object.prototype.hasOwnProperty.call(context, "now")) {
      this._runtimeContext.nowProvider = resolveNowProvider(context.now);
    }
    if (Object.prototype.hasOwnProperty.call(context, "locale") && context.locale) {
      this._runtimeContext.locale = context.locale;
      this._localeStore.setLocale(context.locale);
    }
    if (Object.prototype.hasOwnProperty.call(context, "timeZone")) {
      this._runtimeContext.timeZone = context.timeZone;
    }
    if (Object.prototype.hasOwnProperty.call(context, "seed")) {
      this._runtimeContext.seed = context.seed;
    }
    if (Object.prototype.hasOwnProperty.call(context, "meta")) {
      this._runtimeContext.meta = context.meta;
    }
    if (this._fullResult) {
      this._evaluate();
    }
  }
  getOptions(path) {
    return this.optionSignals[toBasePath(path)]?.value ?? [];
  }
  getOptionsSignal(path) {
    return this.optionSignals[toBasePath(path)];
  }
  getOptionsState(path) {
    return this.optionStateSignals[toBasePath(path)]?.value ?? { loading: false, error: null };
  }
  getOptionsStateSignal(path) {
    return this.optionStateSignals[toBasePath(path)];
  }
  async waitForRemoteOptions() {
    await Promise.allSettled(this._remoteOptionsTasks);
  }
  async waitForInstanceSources() {
    await Promise.allSettled(this._instanceSourceTasks);
  }
  setInstanceValue(name, path, value) {
    this.writeInstanceValue(name, path, value);
    this._evaluate();
  }
  getInstanceData(name, path) {
    const data = this.instanceData[name];
    if (data === void 0) {
      return void 0;
    }
    return path ? getNestedValue(data, path) : data;
  }
  getDisabledDisplay(path) {
    return this._bindConfigs[toBasePath(path)]?.disabledDisplay ?? "hidden";
  }
  getVariableValue(name, scopePath) {
    const visible = visibleScopedVariableValues(scopePath, this._variableDefs, this.variableSignals);
    return visible[name];
  }
  addRepeatInstance(itemName) {
    const path = this.resolveRepeatPath(itemName);
    const item = this._groupItems.get(path);
    if (!item?.repeatable) {
      return void 0;
    }
    const index = this.repeats[path]?.value ?? 0;
    this._rx.batch(() => {
      this.repeats[path].value = index + 1;
      this.registerItemChildren(item.children ?? [], `${path}[${index}]`);
      this.structureVersion.value += 1;
    });
    this._evaluate();
    return index;
  }
  removeRepeatInstance(itemName, index) {
    const path = this.resolveRepeatPath(itemName);
    const item = this._groupItems.get(path);
    const count = this.repeats[path]?.value ?? 0;
    if (!item?.repeatable || index < 0 || index >= count) {
      return;
    }
    const rows = [];
    for (let current = 0; current < count; current += 1) {
      rows.push(snapshotRepeatGroupTree(item.children ?? [], `${path}[${current}]`, (fieldPath) => cloneValue(this.signals[fieldPath]?.value), (repeatPath) => this.repeats[repeatPath]?.value ?? 0));
    }
    rows.splice(index, 1);
    this._rx.batch(() => {
      this.clearRepeatSubtree(path);
      this.repeats[path].value = rows.length;
      for (let current = 0; current < rows.length; current += 1) {
        this.registerItemChildren(item.children ?? [], `${path}[${current}]`);
        applyRepeatGroupTreeSnapshot(item.children ?? [], `${path}[${current}]`, rows[current], (fieldPath, value) => {
          const v2 = cloneValue(value);
          this._data[fieldPath] = v2;
          if (this.signals[fieldPath]) {
            this.signals[fieldPath].value = v2;
          }
        });
      }
      this.structureVersion.value += 1;
    });
    this._evaluate();
  }
  compileExpression(expression, currentItemName = "") {
    return () => {
      this._evaluationVersion.value;
      this.instanceVersion.value;
      this.structureVersion.value;
      return wasmEvalFELWithContext(this.normalizeExpressionForWasm(expression, currentItemName), buildWasmFelExpressionContext({
        currentItemPath: currentItemName,
        data: this._data,
        fullResult: this._fullResult,
        fieldSignals: this.signals,
        validationResults: this.validationResults,
        relevantSignals: this.relevantSignals,
        readonlySignals: this.readonlySignals,
        requiredSignals: this.requiredSignals,
        repeats: this.repeats,
        bindConfigs: this._bindConfigs,
        variableDefs: this._variableDefs,
        variableSignals: this.variableSignals,
        instanceData: this.instanceData,
        nowIso: this.nowISO(),
        locale: this._runtimeContext.locale,
        meta: this._runtimeContext.meta
      }));
    };
  }
  setValue(name, value) {
    if (typeof name !== "string") {
      throw new TypeError("setValue path cannot be null");
    }
    const instanceTarget = parseInstanceTarget(name);
    if (instanceTarget) {
      this.writeInstanceValue(instanceTarget.instanceName, instanceTarget.instancePath, value);
      this._evaluate();
      return;
    }
    const basePath = toBasePath(name);
    if (this._calculatedFields.has(basePath)) {
      return;
    }
    const item = this._fieldItems.get(basePath);
    if (!item) {
      return;
    }
    const bind = this._bindConfigs[basePath];
    const nextValue = coerceFieldValue2(item, bind, this.definition, value);
    this._data[name] = cloneValue(nextValue);
    this._evaluate();
  }
  getValidationReport(options) {
    const mode = options?.mode ?? "continuous";
    const results = [];
    for (const [path, signalRef] of Object.entries(this.validationResults)) {
      if (this.isPathRelevant(path)) {
        results.push(...signalRef.value);
      }
    }
    for (const signalRef of Object.values(this.shapeResults)) {
      results.push(...signalRef.value);
    }
    if (mode === "submit") {
      const submitResult = this.evaluateResultForTrigger("submit");
      results.push(...collectSubmitModeShapeValidationResults(submitResult, this._shapeTiming));
    }
    return buildValidationReportEnvelope(results, this.nowISO());
  }
  evaluateShape(shapeId) {
    const timing = this._shapeTiming.get(shapeId) ?? "continuous";
    if (timing === "demand") {
      return this.evaluateResultForTrigger("demand").validations.filter((result) => result.shapeId === shapeId).map(toValidationResult);
    }
    if (!this._fullResult) {
      this._evaluate();
    }
    return this._fullResult?.validations.filter((result) => result.shapeId === shapeId).map(toValidationResult) ?? [];
  }
  isPathRelevant(path) {
    if (!path) {
      return true;
    }
    const segments = splitIndexedPath(path);
    let current = "";
    for (const segment of segments) {
      current = current ? appendPath(current, segment) : segment;
      if (this.relevantSignals[current] && !this.relevantSignals[current].value) {
        return false;
      }
    }
    return true;
  }
  getResponse(meta) {
    const data = {};
    const mode = meta?.mode ?? "continuous";
    const defaultBehavior = this.definition.nonRelevantBehavior ?? "remove";
    for (const [path, signalRef] of Object.entries(this.signals)) {
      if (this._displaySignalPaths.has(path)) {
        continue;
      }
      const relevant = this.isPathRelevant(path);
      let behavior = defaultBehavior;
      for (const ancestor of getAncestorBasePaths(path)) {
        const bind = this._bindConfigs[ancestor];
        if (bind?.nonRelevantBehavior) {
          behavior = bind.nonRelevantBehavior;
          break;
        }
      }
      if (!relevant && behavior === "remove") {
        continue;
      }
      const value = !relevant && behavior === "empty" ? null : cloneValue(signalRef.value);
      setResponsePathValue(data, path, value);
    }
    const report = this.getValidationReport({ mode });
    return buildFormspecResponseEnvelope({
      definition: this.definition,
      data,
      report,
      timestamp: this.nowISO(),
      meta
    });
  }
  getDiagnosticsSnapshot(options) {
    const values = {};
    const mips = {};
    const repeats = {};
    for (const [path, repeatSignal] of Object.entries(this.repeats)) {
      repeats[path] = repeatSignal.value;
    }
    for (const [path, signalRef] of Object.entries(this.signals)) {
      values[path] = cloneValue(signalRef.value);
      mips[path] = {
        relevant: this.relevantSignals[path]?.value ?? true,
        required: this.requiredSignals[path]?.value ?? false,
        readonly: this.readonlySignals[path]?.value ?? false,
        error: this.errorSignals[path]?.value ?? null
      };
    }
    const timestamp = this.nowISO();
    return {
      definition: {
        url: this.definition.url,
        version: this.definition.version,
        title: this.definition.title
      },
      timestamp,
      structureVersion: this.structureVersion.value,
      repeats,
      values,
      mips,
      validation: this.getValidationReport(options),
      runtimeContext: {
        now: timestamp,
        locale: this._runtimeContext.locale,
        timeZone: this._runtimeContext.timeZone,
        seed: this._runtimeContext.seed
      }
    };
  }
  applyReplayEvent(event) {
    try {
      switch (event.type) {
        case "setValue":
          this.setValue(event.path, event.value);
          return { ok: true, event };
        case "addRepeatInstance":
          return { ok: true, event, output: this.addRepeatInstance(event.path) };
        case "removeRepeatInstance":
          this.removeRepeatInstance(event.path, event.index);
          return { ok: true, event };
        case "evaluateShape":
          return { ok: true, event, output: this.evaluateShape(event.shapeId) };
        case "getValidationReport":
          return { ok: true, event, output: this.getValidationReport({ mode: event.mode }) };
        case "getResponse":
          return { ok: true, event, output: this.getResponse({ mode: event.mode }) };
        default: {
          const neverType = event;
          throw new Error(`Unsupported replay event: ${neverType.type}`);
        }
      }
    } catch (error) {
      return {
        ok: false,
        event,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }
  replay(events, options) {
    const results = [];
    const errors = [];
    let applied = 0;
    for (let index = 0; index < events.length; index += 1) {
      const result = this.applyReplayEvent(events[index]);
      results.push(result);
      if (result.ok) {
        applied += 1;
        continue;
      }
      errors.push({
        index,
        event: events[index],
        error: result.error ?? "Unknown replay error"
      });
      if (options?.stopOnError) {
        break;
      }
    }
    return { applied, results, errors };
  }
  getDefinition() {
    return this.definition;
  }
  setLabelContext(context) {
    this._labelContext = context;
    this._labelContextSignal.value = context;
  }
  getLabel(item) {
    if (this._labelContext && item.labels?.[this._labelContext]) {
      return item.labels[this._labelContext];
    }
    return item.label;
  }
  loadLocale(doc) {
    this._localeStore.loadLocale(doc);
  }
  setLocale(code) {
    this._localeStore.setLocale(code);
  }
  getActiveLocale() {
    return this._localeStore.activeLocale.value;
  }
  getAvailableLocales() {
    return this._localeStore.getAvailableLocales();
  }
  getLocaleDirection() {
    return this._localeStore.direction.value;
  }
  getFieldVM(path) {
    return this._fieldViewModels[path];
  }
  getFormVM() {
    return this._formViewModel;
  }
  injectExternalValidation(results) {
    this._externalValidation.splice(0, this._externalValidation.length, ...results.map((result) => makeValidationResult({
      path: result.path,
      severity: result.severity,
      constraintKind: "constraint",
      code: result.code,
      message: result.message,
      source: result.source ?? "external"
    })));
    this._evaluate();
  }
  clearExternalValidation(path) {
    if (!path) {
      this._externalValidation.splice(0, this._externalValidation.length);
    } else {
      const base = toBasePath(path);
      for (let index = this._externalValidation.length - 1; index >= 0; index -= 1) {
        if (toBasePath(this._externalValidation[index].path) === base) {
          this._externalValidation.splice(index, 1);
        }
      }
    }
    this._evaluate();
  }
  dispose() {
  }
  setRegistryEntries(entries) {
    this._registryEntries.clear();
    for (const entry of entries) {
      if (entry?.name) {
        this._registryEntries.set(entry.name, entry);
      }
    }
    this._registryDocuments = [{ entries }];
    this._evaluate();
  }
  evaluateScreener(answers) {
    return wasmEvaluateScreener(this.definition, answers);
  }
  migrateResponse(responseData, fromVersion) {
    return migrateResponseData(this.definition, responseData, fromVersion, {
      nowIso: this.nowISO()
    });
  }
  nowISO() {
    return this._runtimeContext.nowProvider().toISOString();
  }
  initializeOptionSignals() {
    const visit = (items, prefix = "") => {
      for (const item of items) {
        const path = prefix ? `${prefix}.${item.key}` : item.key;
        if (item.type === "field") {
          const options = Array.isArray(item.options) ? item.options.map((option) => ({
            value: String(option.value),
            label: String(option.label)
          })) : [];
          this.optionSignals[path] = this._rx.signal(options);
          this.optionStateSignals[path] = this._rx.signal({ loading: false, error: null });
        }
        if (item.children) {
          visit(item.children, path);
        }
      }
    };
    visit(this.definition.items);
  }
  initializeInstances() {
    const instances = this.definition.instances;
    if (!instances) {
      return;
    }
    for (const [name, instance] of Object.entries(instances)) {
      if (instance.data !== void 0) {
        const seedData = cloneValue(instance.data);
        this.validateInstanceSchema(name, seedData);
        this.instanceData[name] = seedData;
      }
      this.initializeInstanceSource(name, instance);
    }
  }
  initializeInstanceSource(name, instance) {
    if (!instance.source) {
      return;
    }
    if (instance.static && _FormEngine.instanceSourceCache.has(instance.source)) {
      this.instanceData[name] = cloneValue(_FormEngine.instanceSourceCache.get(instance.source));
      return;
    }
    const task = fetch(instance.source).then((response) => {
      if (!response.ok) {
        throw new Error(`Instance source fetch failed (${response.status})`);
      }
      return response.json();
    }).then((payload) => {
      this.validateInstanceSchema(name, payload);
      const nextValue = cloneValue(payload);
      if (instance.static) {
        _FormEngine.instanceSourceCache.set(instance.source, cloneValue(nextValue));
      }
      this.instanceData[name] = nextValue;
      this.instanceVersion.value += 1;
      this._evaluate();
    }).catch((error) => {
      console.error(`Failed to load instance source '${name}':`, error);
    });
    this._instanceSourceTasks.push(task);
  }
  initializeBindConfigs(items, prefix = "") {
    for (const item of items) {
      const path = prefix ? `${prefix}.${item.key}` : item.key;
      this._groupItems.set(path, item);
      const inlineBind = extractInlineBind(item, path);
      if (inlineBind) {
        this._bindConfigs[path] = { ...this._bindConfigs[path], ...inlineBind };
        if (inlineBind.calculate && !parseInstanceTarget(path)) {
          this._calculatedFields.add(path);
        }
      }
      if (item.children) {
        this.initializeBindConfigs(item.children, path);
      }
    }
    for (const bind of this.definition.binds ?? []) {
      const path = toBasePath(bind.path);
      this._bindConfigs[path] = { ...this._bindConfigs[path], ...bind, path };
      if (bind.calculate && !parseInstanceTarget(bind.path)) {
        this._calculatedFields.add(path);
      }
    }
    for (const shape of this.definition.shapes ?? []) {
      if (shape.id) {
        this._shapeTiming.set(shape.id, shape.timing ?? "continuous");
        if (!this.shapeResults[shape.id]) {
          this.shapeResults[shape.id] = this._rx.signal([]);
        }
      }
    }
    for (const variableDef of this._variableDefs) {
      const key = `${variableDef.scope ?? "#"}:${variableDef.name}`;
      this.variableSignals[key] = this._rx.signal(null);
      const existing = this._variableSignalKeys.get(variableDef.name) ?? [];
      existing.push(key);
      this._variableSignalKeys.set(variableDef.name, existing);
    }
  }
  collectInstanceCalculateBinds() {
    for (const bind of Object.values(this._bindConfigs)) {
      if (bind.calculate && parseInstanceTarget(bind.path)) {
        this._instanceCalculateBinds.push(bind);
      }
    }
  }
  validateInstanceCalculateTargets() {
    for (const bind of this._instanceCalculateBinds) {
      const target = parseInstanceTarget(bind.path);
      if (!target) {
        continue;
      }
      const instance = this.definition.instances?.[target.instanceName];
      if (!instance) {
        throw new Error(`Unknown instance '${target.instanceName}' targeted by bind '${bind.path}'`);
      }
      if (instance.readonly !== false) {
        throw new Error(`Calculate bind cannot target readonly instance '${target.instanceName}'`);
      }
    }
  }
  registerItems(items, prefix = "") {
    var _a, _b, _c, _d, _e;
    for (const item of items) {
      const path = prefix ? `${prefix}.${item.key}` : item.key;
      this._groupItems.set(path, item);
      (_a = this.relevantSignals)[path] ?? (_a[path] = this._rx.signal(true));
      (_b = this.requiredSignals)[path] ?? (_b[path] = this._rx.signal(false));
      (_c = this.readonlySignals)[path] ?? (_c[path] = this._rx.signal(false));
      (_d = this.validationResults)[path] ?? (_d[path] = this._rx.signal([]));
      (_e = this.errorSignals)[path] ?? (_e[path] = this._rx.signal(null));
      if (item.type === "field") {
        this._fieldItems.set(path, item);
        this.initializeFieldSignal(path, item);
        this._createFieldVM(path, item);
        if (item.children) {
          this.registerItemChildren(item.children, path);
        }
        continue;
      }
      if (item.type === "display") {
        this._displaySignalPaths.add(path);
        if (this._bindConfigs[path]?.calculate) {
          this.signals[path] = this._rx.signal(null);
        }
        continue;
      }
      if (item.repeatable) {
        const count = item.minRepeat ?? 1;
        this.repeats[path] = this._rx.signal(count);
        for (let index = 0; index < count; index += 1) {
          this.registerItemChildren(item.children ?? [], `${path}[${index}]`);
        }
      } else {
        this.registerItemChildren(item.children ?? [], path);
      }
    }
  }
  registerItemChildren(items, prefix) {
    var _a, _b, _c, _d, _e, _f;
    for (const item of items) {
      const path = `${prefix}.${item.key}`;
      this._groupItems.set(path, item);
      (_a = this.relevantSignals)[path] ?? (_a[path] = this._rx.signal(true));
      (_b = this.requiredSignals)[path] ?? (_b[path] = this._rx.signal(false));
      (_c = this.readonlySignals)[path] ?? (_c[path] = this._rx.signal(false));
      (_d = this.validationResults)[path] ?? (_d[path] = this._rx.signal([]));
      (_e = this.errorSignals)[path] ?? (_e[path] = this._rx.signal(null));
      if (item.type === "field") {
        this._fieldItems.set(toBasePath(path), item);
        this.initializeFieldSignal(path, item);
        this._createFieldVM(path, item);
        if (item.children) {
          this.registerItemChildren(item.children, path);
        }
        continue;
      }
      if (item.type === "display") {
        this._displaySignalPaths.add(path);
        if (this._bindConfigs[toBasePath(path)]?.calculate) {
          (_f = this.signals)[path] ?? (_f[path] = this._rx.signal(null));
        }
        continue;
      }
      if (item.repeatable) {
        const count = item.minRepeat ?? 1;
        this.repeats[path] = this._rx.signal(count);
        for (let index = 0; index < count; index += 1) {
          this.registerItemChildren(item.children ?? [], `${path}[${index}]`);
        }
      } else {
        this.registerItemChildren(item.children ?? [], path);
      }
    }
  }
  initializeFieldSignal(path, item) {
    if (this.signals[path]) {
      return;
    }
    const hasExpressionInitial = typeof item.initialValue === "string" && item.initialValue.startsWith("=");
    const initial = this.resolveInitialFieldValue(path, item);
    this.signals[path] = this._rx.signal(cloneValue(initial));
    if (!hasExpressionInitial) {
      this._data[path] = cloneValue(initial);
    }
  }
  resolveInitialFieldValue(path, item) {
    const prePopulate = item.prePopulate;
    if (prePopulate) {
      const value = this.getInstanceData(prePopulate.instance, prePopulate.path);
      if (value !== void 0) {
        if (prePopulate.editable === false) {
          this._prePopulateReadonly.add(path);
        }
        return cloneValue(value);
      }
      if (prePopulate.editable === false) {
        this._prePopulateReadonly.add(path);
      }
    }
    if (typeof item.initialValue === "string" && item.initialValue.startsWith("=")) {
      return emptyValueForItem(item);
    }
    if (item.initialValue !== void 0) {
      return coerceInitialValue(item, item.initialValue);
    }
    return emptyValueForItem(item);
  }
  initializeRemoteOptions() {
    for (const bind of Object.values(this._bindConfigs)) {
      if (!bind.remoteOptions) {
        continue;
      }
      const path = toBasePath(bind.path);
      const state = this.optionStateSignals[path] ?? this._rx.signal({ loading: false, error: null });
      this.optionStateSignals[path] = state;
      state.value = { loading: true, error: null };
      const task = fetch(bind.remoteOptions).then((response) => {
        if (!response.ok) {
          throw new Error(`Remote options fetch failed (${response.status})`);
        }
        return response.json();
      }).then((payload) => {
        const options = normalizeRemoteOptions(payload);
        this.optionSignals[path] = this.optionSignals[path] ?? this._rx.signal([]);
        this.optionSignals[path].value = options;
        state.value = { loading: false, error: null };
      }).catch((error) => {
        state.value = {
          loading: false,
          error: error instanceof Error ? error.message : String(error)
        };
      });
      this._remoteOptionsTasks.push(task);
    }
  }
  writeInstanceValue(instanceName, path, value, options) {
    const instance = this.definition.instances?.[instanceName];
    if (!instance) {
      throw new Error(`Unknown instance '${instanceName}'`);
    }
    if (!options?.bypassReadonly && instance.readonly !== false) {
      throw new Error(`Instance '${instanceName}' is readonly`);
    }
    let nextValue;
    if (!path) {
      nextValue = cloneValue(value);
    } else {
      nextValue = cloneValue(this.instanceData[instanceName] ?? {});
      setNestedPathValue(nextValue, path, cloneValue(value));
    }
    this.validateInstanceSchema(instanceName, nextValue);
    if (deepEqual(this.instanceData[instanceName], nextValue)) {
      return;
    }
    this.instanceData[instanceName] = nextValue;
    this.instanceVersion.value += 1;
  }
  validateInstanceSchema(instanceName, data) {
    const schema = this.definition.instances?.[instanceName]?.schema;
    validateInstanceDataAgainstSchema(instanceName, data, schema && typeof schema === "object" ? schema : void 0);
  }
  evaluateExpression(expression, currentItemPath = "", dataOverride, resultOverride, scopedVariableOverrides, replaceSelfRef = false) {
    return safeEvaluateExpression(this.normalizeExpressionForWasm(expression, currentItemPath, replaceSelfRef), buildWasmFelExpressionContext({
      currentItemPath,
      data: this._data,
      fullResult: this._fullResult,
      resultOverride,
      dataOverride,
      scopedVariableOverrides,
      fieldSignals: this.signals,
      validationResults: this.validationResults,
      relevantSignals: this.relevantSignals,
      readonlySignals: this.readonlySignals,
      requiredSignals: this.requiredSignals,
      repeats: this.repeats,
      bindConfigs: this._bindConfigs,
      variableDefs: this._variableDefs,
      variableSignals: this.variableSignals,
      instanceData: this.instanceData,
      nowIso: this.nowISO(),
      locale: this._runtimeContext.locale,
      meta: this._runtimeContext.meta
    }));
  }
  repeatCountsSnapshot() {
    return Object.fromEntries(Object.entries(this.repeats).map(([path, repeatSignal]) => [path, repeatSignal.value]));
  }
  shapedEvalResult(base) {
    return mergeWasmEvalWithExternalValidations(base, {
      externalValidations: this._externalValidation
    });
  }
  _evaluate() {
    const baseResult = wasmEvaluateDefinition(this.definition, this._data, wasmEvaluateDefinitionPayload({
      nowIso: this.nowISO(),
      previousResult: this._fullResult,
      instances: this.instanceData,
      registryDocuments: this._registryDocuments,
      repeatCounts: this.repeatCountsSnapshot()
    }));
    const evalResult = this.shapedEvalResult(baseResult);
    this.applyInstanceCalculates(evalResult);
    const delta = diffEvalResults(this._previousEvalResult, evalResult);
    this._rx.batch(() => {
      patchValueSignalsFromWasm({
        values: evalResult.values,
        signals: this.signals,
        data: this._data,
        fieldItems: this._fieldItems,
        bindConfigs: this._bindConfigs,
        calculatedFields: this._calculatedFields
      });
      patchDeltaSignalsFromWasm(this._rx, delta, {
        relevantSignals: this.relevantSignals,
        requiredSignals: this.requiredSignals,
        readonlySignals: this.readonlySignals,
        validationResults: this.validationResults,
        shapeResults: this.shapeResults,
        variableSignals: this.variableSignals,
        variableSignalKeys: this._variableSignalKeys,
        prePopulateReadonly: this._prePopulateReadonly
      });
      this.syncInstanceCalculateSignals();
      patchErrorSignalsFromWasm(this._rx, {
        validationResults: this.validationResults,
        errorSignals: this.errorSignals
      });
      this._evaluationVersion.value += 1;
    });
    this._previousEvalResult = evalResult;
    this._fullResult = evalResult;
  }
  evaluateResultForTrigger(trigger) {
    return this.shapedEvalResult(wasmEvaluateDefinition(this.definition, this._data, wasmEvaluateDefinitionPayload({
      nowIso: this.nowISO(),
      trigger,
      previousResult: this._fullResult,
      instances: this.instanceData,
      registryDocuments: this._registryDocuments,
      repeatCounts: this.repeatCountsSnapshot()
    })));
  }
  applyInstanceCalculates(result) {
    let changed = false;
    for (const bind of this._instanceCalculateBinds) {
      const target = parseInstanceTarget(bind.path);
      if (!target || !bind.calculate) {
        continue;
      }
      const value = this.evaluateExpression(bind.calculate, "", this._data, result);
      const before = cloneValue(this.getInstanceData(target.instanceName, target.instancePath));
      this.writeInstanceValue(target.instanceName, target.instancePath, value, { bypassReadonly: true });
      if (!deepEqual(before, this.getInstanceData(target.instanceName, target.instancePath))) {
        changed = true;
      }
    }
    return changed;
  }
  syncInstanceCalculateSignals() {
    for (const bind of this._instanceCalculateBinds) {
      const target = parseInstanceTarget(bind.path);
      if (!target || !bind.calculate) {
        continue;
      }
      const nextValue = this.evaluateExpression(bind.calculate);
      if ((nextValue === null || nextValue === void 0) && this.getInstanceData(target.instanceName, target.instancePath) !== void 0) {
        continue;
      }
      this.writeInstanceValue(target.instanceName, target.instancePath, nextValue, { bypassReadonly: true });
    }
  }
  normalizeExpressionForWasm(expression, currentItemPath = "", replaceSelfRef = false) {
    return normalizeExpressionForWasmEvaluation({
      expression,
      currentItemPath,
      replaceSelfRef,
      repeats: this.repeats,
      fieldSignals: this.signals
    });
  }
  resolveRepeatPath(itemName) {
    return this.repeats[itemName] ? itemName : toBasePath(itemName);
  }
  clearRepeatSubtree(rootRepeatPath) {
    const repeatPrefix = `${rootRepeatPath}[`;
    for (const path of Object.keys(this._fieldViewModels)) {
      if (path.startsWith(repeatPrefix)) {
        delete this._fieldViewModels[path];
      }
    }
    clearRepeatIndexedSubtree({
      rootRepeatPath,
      signals: this.signals,
      relevantSignals: this.relevantSignals,
      requiredSignals: this.requiredSignals,
      readonlySignals: this.readonlySignals,
      errorSignals: this.errorSignals,
      validationResults: this.validationResults,
      optionSignals: this.optionSignals,
      optionStateSignals: this.optionStateSignals,
      repeats: this.repeats,
      data: this._data
    });
  }
  _createFieldVM(path, item) {
    const basePath = toBasePath(path);
    const vm = createFieldViewModel({
      rx: this._rx,
      localeStore: this._localeStore,
      templatePath: basePath,
      instancePath: path,
      id: `field-${path.replace(/[\.\[\]]/g, "-")}`,
      itemKey: item.key,
      dataType: item.dataType ?? "string",
      getItemLabel: () => item.label,
      getItemHint: () => item.hint ?? null,
      getItemDescription: () => item.description ?? null,
      getItemLabels: () => item.labels,
      getLabelContext: () => this._labelContextSignal.value,
      getFieldValue: () => this.signals[path] ?? this._rx.signal(null),
      getRequired: () => this.requiredSignals[path] ?? this._rx.signal(false),
      getVisible: () => this.relevantSignals[path] ?? this._rx.signal(true),
      getReadonly: () => this.readonlySignals[path] ?? this._rx.signal(false),
      getDisabledDisplay: () => this.getDisabledDisplay(path),
      getErrors: () => this.validationResults[basePath] ?? this._rx.signal([]),
      getOptions: () => this.optionSignals[basePath] ?? this._rx.signal([]),
      getOptionsState: () => this.optionStateSignals[basePath] ?? this._rx.signal({ loading: false, error: null }),
      getOptionSetName: () => {
        const bindConfig = this._bindConfigs[basePath];
        return bindConfig?.optionSet ?? void 0;
      },
      setFieldValue: (value) => this.setValue(path, value),
      evalFEL: (expr) => wasmEvalFELWithContext(expr, this._buildLocaleFELContext(path))
    });
    this._fieldViewModels[path] = vm;
  }
  _buildLocaleFELContext(currentItemPath = "") {
    return buildWasmFelExpressionContext({
      currentItemPath,
      data: this._data,
      fullResult: this._fullResult,
      fieldSignals: this.signals,
      validationResults: this.validationResults,
      relevantSignals: this.relevantSignals,
      readonlySignals: this.readonlySignals,
      requiredSignals: this.requiredSignals,
      repeats: this.repeats,
      bindConfigs: this._bindConfigs,
      variableDefs: this._variableDefs,
      variableSignals: this.variableSignals,
      instanceData: this.instanceData,
      nowIso: this.nowISO(),
      locale: this._runtimeContext.locale,
      meta: this._runtimeContext.meta
    });
  }
};
FormEngine.instanceSourceCache = /* @__PURE__ */ new Map();

// node_modules/@formspec-org/engine/dist/engine/init.js
function createFormEngine(definition, context, registryEntries, reactiveRuntime = preactReactiveRuntime) {
  return new FormEngine(definition, context, registryEntries, reactiveRuntime);
}

// node_modules/@formspec-org/webcomponent/dist/default-theme.json
var default_theme_default = {
  $formspecTheme: "1.0",
  version: "1.0.0",
  name: "formspec-default",
  title: "Formspec Default Theme",
  description: "Structural default theme providing sensible baseline presentation for all item types.",
  targetDefinition: {
    url: "urn:formspec:any",
    compatibleVersions: ">=1.0.0"
  },
  tokens: {
    "spacing.xs": "0.25rem",
    "spacing.sm": "0.5rem",
    "spacing.md": "1rem",
    "spacing.lg": "1.5rem",
    "spacing.xl": "2rem",
    "radius.sm": "0.25rem",
    "radius.md": "0.5rem"
  },
  defaults: {
    labelPosition: "top",
    accessibility: {
      liveRegion: "off"
    }
  },
  selectors: [
    {
      match: { type: "group" },
      apply: {
        cssClass: "formspec-themed-group",
        accessibility: {
          role: "group"
        }
      }
    },
    {
      match: { type: "display" },
      apply: {
        cssClass: "formspec-themed-display"
      }
    },
    {
      match: { type: "field" },
      apply: {
        cssClass: "formspec-themed-field"
      }
    },
    {
      match: { dataType: "boolean" },
      apply: {
        labelPosition: "start"
      }
    }
  ]
};

// node_modules/@formspec-org/webcomponent/dist/rendering/screener.js
function screenerAnswersSatisfyRequired(screener, answers) {
  const binds = screener.binds || [];
  const requiredPaths = new Set(binds.filter((b2) => b2.required === "true" || b2.required === true).map((b2) => b2.path));
  if (requiredPaths.size > 0) {
    for (const item of screener.items) {
      if (!requiredPaths.has(item.key))
        continue;
      const val = answers[item.key];
      if (val == null || val === "")
        return false;
    }
    return true;
  }
  return screener.items.some((it) => {
    const val = answers[it.key];
    return val != null && val !== "";
  });
}
function normalizeMoneySeed(raw, defaultCurrency) {
  if (raw == null)
    return null;
  if (typeof raw === "number" && !Number.isNaN(raw)) {
    return { amount: raw, currency: defaultCurrency };
  }
  if (typeof raw === "object" && raw.amount != null) {
    const n2 = typeof raw.amount === "string" ? parseFloat(raw.amount) : Number(raw.amount);
    if (Number.isNaN(n2))
      return null;
    return {
      amount: n2,
      currency: typeof raw.currency === "string" ? raw.currency : defaultCurrency
    };
  }
  return null;
}
function normalizeScreenerSeedForItem(item, raw, defaultCurrency) {
  if (raw === void 0)
    return void 0;
  if (item.dataType === "boolean")
    return !!raw;
  if (item.dataType === "money")
    return normalizeMoneySeed(raw, defaultCurrency);
  if (item.dataType === "integer") {
    if (raw === null || raw === "")
      return null;
    const n2 = typeof raw === "string" ? parseInt(raw, 10) : Number(raw);
    return Number.isNaN(n2) ? null : n2;
  }
  if (item.dataType === "decimal") {
    if (raw === null || raw === "")
      return null;
    const n2 = typeof raw === "string" ? parseFloat(raw) : Number(raw);
    return Number.isNaN(n2) ? null : n2;
  }
  return raw === null ? null : raw;
}
function buildInitialScreenerAnswers(screener, seed, defaultCurrency) {
  const answers = {};
  for (const item of screener.items) {
    if (item.dataType === "boolean") {
      answers[item.key] = seed && Object.prototype.hasOwnProperty.call(seed, item.key) ? !!seed[item.key] : false;
      continue;
    }
    if (seed && Object.prototype.hasOwnProperty.call(seed, item.key)) {
      const norm = normalizeScreenerSeedForItem(item, seed[item.key], defaultCurrency);
      if (norm !== void 0)
        answers[item.key] = norm;
    }
  }
  return answers;
}
function extractScreenerSeedFromData(definition, data) {
  const items = definition?.screener?.items;
  if (!Array.isArray(items) || !items.length || !data || typeof data !== "object") {
    return null;
  }
  const seed = {};
  for (const item of items) {
    const k = item?.key;
    if (k && Object.prototype.hasOwnProperty.call(data, k)) {
      seed[k] = data[k];
    }
  }
  return Object.keys(seed).length ? seed : null;
}
function omitScreenerKeysFromData(definition, data) {
  const items = definition?.screener?.items;
  if (!Array.isArray(items) || !items.length) {
    return { ...data };
  }
  const drop = new Set(items.map((i2) => i2?.key).filter(Boolean));
  const out = {};
  for (const [k, v2] of Object.entries(data)) {
    if (!drop.has(k)) {
      out[k] = v2;
    }
  }
  return out;
}
function hasActiveScreener(definition) {
  const screener = definition?.screener;
  return screener?.enabled !== false && Array.isArray(screener?.items) && screener.items.length > 0;
}
function renderScreener(host, container) {
  if (!hasActiveScreener(host._definition))
    return;
  const screener = host._definition.screener;
  const panel = document.createElement("div");
  panel.className = "formspec-screener";
  const heading = document.createElement("h2");
  heading.className = "formspec-screener-heading";
  heading.textContent = host._definition.title || "Screening Questions";
  panel.appendChild(heading);
  if (host._definition.description) {
    const intro = document.createElement("p");
    intro.className = "formspec-screener-intro";
    intro.textContent = host._definition.description;
    panel.appendChild(intro);
  }
  const fieldsContainer = document.createElement("div");
  fieldsContainer.className = "formspec-screener-fields";
  panel.appendChild(fieldsContainer);
  const defaultCurrency = host._definition.formPresentation?.defaultCurrency || "USD";
  const answers = buildInitialScreenerAnswers(screener, host.screenerSeedAnswers, defaultCurrency);
  for (const item of screener.items) {
    const fieldWrapper = document.createElement("div");
    fieldWrapper.className = "formspec-field formspec-screener-field";
    fieldWrapper.dataset.name = item.key;
    const fieldId = `screener-${item.key}`;
    const label = document.createElement("label");
    label.textContent = host.engine.getLabel(item);
    label.htmlFor = fieldId;
    fieldWrapper.appendChild(label);
    const hintId = `${fieldId}-hint`;
    if (item.hint) {
      const hint = document.createElement("span");
      hint.className = "formspec-hint";
      hint.id = hintId;
      hint.textContent = item.hint;
      fieldWrapper.appendChild(hint);
    }
    const clearFieldError = () => {
      fieldWrapper.querySelector(".formspec-error")?.remove();
    };
    if (item.dataType === "choice" && item.options) {
      const select = document.createElement("select");
      select.className = "formspec-input";
      select.id = fieldId;
      if (item.hint)
        select.setAttribute("aria-describedby", hintId);
      const emptyOpt = document.createElement("option");
      emptyOpt.value = "";
      emptyOpt.textContent = "-- Select --";
      select.appendChild(emptyOpt);
      for (const opt of item.options) {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label || opt.value;
        select.appendChild(option);
      }
      const seededChoice = answers[item.key];
      if (seededChoice != null && seededChoice !== "") {
        select.value = String(seededChoice);
      }
      select.addEventListener("change", () => {
        answers[item.key] = select.value || null;
        clearFieldError();
      });
      fieldWrapper.appendChild(select);
    } else if (item.dataType === "boolean") {
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.className = "formspec-input";
      checkbox.id = fieldId;
      if (item.hint)
        checkbox.setAttribute("aria-describedby", hintId);
      checkbox.checked = !!answers[item.key];
      checkbox.addEventListener("change", () => {
        answers[item.key] = checkbox.checked;
        clearFieldError();
      });
      fieldWrapper.appendChild(checkbox);
    } else if (item.dataType === "money") {
      const input = document.createElement("input");
      input.type = "number";
      input.className = "formspec-input";
      input.id = fieldId;
      input.placeholder = "Amount";
      if (item.hint)
        input.setAttribute("aria-describedby", hintId);
      const moneySeed = answers[item.key];
      if (moneySeed && typeof moneySeed.amount === "number" && !Number.isNaN(moneySeed.amount)) {
        input.value = String(moneySeed.amount);
      }
      input.addEventListener("input", () => {
        const val = parseFloat(input.value);
        answers[item.key] = isNaN(val) ? null : { amount: val, currency: host._definition.formPresentation?.defaultCurrency || "USD" };
        clearFieldError();
      });
      fieldWrapper.appendChild(input);
    } else {
      const input = document.createElement("input");
      input.type = item.dataType === "integer" || item.dataType === "decimal" ? "number" : "text";
      input.className = "formspec-input";
      input.id = fieldId;
      if (item.hint)
        input.setAttribute("aria-describedby", hintId);
      const v2 = answers[item.key];
      if (v2 != null && v2 !== "") {
        input.value = String(v2);
      }
      input.addEventListener("input", () => {
        const val = input.value;
        if (item.dataType === "integer") {
          answers[item.key] = val ? parseInt(val, 10) : null;
        } else if (item.dataType === "decimal") {
          answers[item.key] = val ? parseFloat(val) : null;
        } else {
          answers[item.key] = val || null;
        }
        clearFieldError();
      });
      fieldWrapper.appendChild(input);
    }
    fieldsContainer.appendChild(fieldWrapper);
  }
  const continueBtn = document.createElement("button");
  continueBtn.type = "button";
  continueBtn.className = "formspec-screener-continue";
  continueBtn.textContent = "Continue";
  continueBtn.addEventListener("click", () => {
    for (const err of fieldsContainer.querySelectorAll(".formspec-error")) {
      err.remove();
    }
    const binds = screener.binds || [];
    const requiredPaths = new Set(binds.filter((b2) => b2.required === "true" || b2.required === true).map((b2) => b2.path));
    let valid = true;
    if (requiredPaths.size > 0) {
      for (const item of screener.items) {
        if (!requiredPaths.has(item.key))
          continue;
        const val = answers[item.key];
        if (val == null || val === "") {
          valid = false;
          const wrapper = fieldsContainer.querySelector(`[data-name="${item.key}"]`);
          if (wrapper) {
            const err = document.createElement("div");
            err.className = "formspec-error";
            err.setAttribute("role", "alert");
            err.setAttribute("aria-live", "assertive");
            err.textContent = "Required";
            wrapper.appendChild(err);
          }
        }
      }
    } else {
      const hasAny = screener.items.some((it) => {
        const val = answers[it.key];
        return val != null && val !== "";
      });
      if (!hasAny) {
        valid = false;
        for (const item of screener.items) {
          const val = answers[item.key];
          if (val == null || val === "") {
            const wrapper = fieldsContainer.querySelector(`[data-name="${item.key}"]`);
            if (wrapper) {
              const err = document.createElement("div");
              err.className = "formspec-error";
              err.setAttribute("role", "alert");
              err.setAttribute("aria-live", "assertive");
              err.textContent = "Required";
              wrapper.appendChild(err);
            }
          }
        }
      }
    }
    if (!valid)
      return;
    const route = host.engine.evaluateScreener(answers);
    host._screenerRoute = route;
    const routeType = host.classifyScreenerRoute(route);
    const isInternal = routeType === "internal";
    host.dispatchEvent(new CustomEvent("formspec-screener-route", {
      detail: { route, answers, routeType, isInternal },
      bubbles: true,
      composed: true
    }));
    if (isInternal) {
      host._screenerCompleted = true;
      host.emitScreenerStateChange("route-internal", answers);
      host.render();
      return;
    }
    host.emitScreenerStateChange(route ? "route-external" : "route-none", answers);
    if (route) {
      showExternalRouteResult(host, container, route);
    }
  });
  panel.appendChild(continueBtn);
  container.appendChild(panel);
}
function showExternalRouteResult(host, container, route) {
  container.innerHTML = "";
  const panel = document.createElement("div");
  panel.className = "formspec-screener-routed";
  const heading = document.createElement("h2");
  heading.className = "formspec-screener-heading";
  heading.textContent = route.label || "Routed to another form";
  panel.appendChild(heading);
  const target = document.createElement("p");
  target.className = "formspec-screener-routed-target";
  target.textContent = route.target;
  panel.appendChild(target);
  const backBtn = document.createElement("button");
  backBtn.type = "button";
  backBtn.className = "formspec-screener-continue";
  backBtn.textContent = "Back to screening";
  backBtn.addEventListener("click", () => {
    host._screenerRoute = null;
    host.emitScreenerStateChange("restart", void 0);
    host.render();
  });
  panel.appendChild(backBtn);
  container.appendChild(panel);
}

// node_modules/@formspec-org/webcomponent/dist/hydrate-response-data.js
function applyResponseDataToEngine(engine, data, prefix = "") {
  for (const [key, value] of Object.entries(data)) {
    const path = prefix ? `${prefix}.${key}` : key;
    const sig = engine.signals[path];
    if (sig && Object.getOwnPropertyDescriptor(Object.getPrototypeOf(sig), "value")?.set) {
      engine.setValue(path, value);
    } else if (Array.isArray(value)) {
      const currentCount = engine.repeats[path]?.value ?? 0;
      for (let i2 = currentCount; i2 < value.length; i2++) {
        engine.addRepeatInstance(path);
      }
      for (let i2 = 0; i2 < value.length; i2++) {
        if (value[i2] != null && typeof value[i2] === "object") {
          applyResponseDataToEngine(engine, value[i2], `${path}[${i2}]`);
        }
      }
    } else if (value !== null && typeof value === "object") {
      applyResponseDataToEngine(engine, value, path);
    }
  }
}

// node_modules/@formspec-org/webcomponent/dist/rendering/breakpoints.js
function createBreakpointState() {
  return {
    activeBreakpointSignal: y(null),
    cleanups: []
  };
}
function setupBreakpoints(host, state) {
  for (const fn of state.cleanups)
    fn();
  state.cleanups = [];
  state.activeBreakpointSignal.value = null;
  if (!host._componentDocument?.breakpoints)
    return;
  const breakpoints = host._componentDocument.breakpoints;
  const entries = Object.entries(breakpoints).map(([name, val]) => {
    const query = typeof val === "number" ? `(min-width: ${val}px)` : String(val);
    const width = typeof val === "number" ? val : parseInt(String(val).replace(/[^0-9]/g, "")) || 0;
    return { name, query, width };
  }).sort((a2, b2) => a2.width - b2.width);
  for (const { name, query } of entries) {
    const mql = window.matchMedia(query);
    const handler = () => {
      let active = null;
      for (const entry of entries) {
        if (window.matchMedia(entry.query).matches)
          active = entry.name;
      }
      if (active !== state.activeBreakpointSignal.value) {
        state.activeBreakpointSignal.value = active;
        host.scheduleRender();
      }
    };
    mql.addEventListener("change", handler);
    state.cleanups.push(() => mql.removeEventListener("change", handler));
    if (mql.matches)
      state.activeBreakpointSignal.value = name;
  }
}
function cleanupBreakpoints(state) {
  for (const fn of state.cleanups)
    fn();
  state.cleanups = [];
}

// node_modules/@formspec-org/webcomponent/dist/navigation/paths.js
function normalizeFieldPath(path) {
  return typeof path === "string" ? path.trim() : "";
}
function externalPathToInternal(path) {
  return path.replace(/\[(\d+)\]/g, (_match, rawIndex) => {
    const parsed = Number.parseInt(rawIndex, 10);
    if (!Number.isFinite(parsed))
      return `[${rawIndex}]`;
    return `[${Math.max(0, parsed - 1)}]`;
  });
}

// node_modules/@formspec-org/webcomponent/dist/navigation/field-focus.js
function findFieldElement(host, path) {
  if (!path || path === "#")
    return null;
  const candidatePaths = [path, externalPathToInternal(path)];
  for (const p2 of candidatePaths) {
    const escapedPath = typeof CSS !== "undefined" && CSS.escape ? CSS.escape(p2) : p2;
    let fieldEl = host.querySelector(`.formspec-field[data-name="${escapedPath}"]`);
    if (fieldEl)
      return fieldEl;
    const allFields = Array.from(host.querySelectorAll(".formspec-field[data-name]"));
    const found = allFields.find((el2) => {
      const name = el2.getAttribute("data-name");
      return name === p2 || name?.startsWith(`${p2}.`) || name?.startsWith(`${p2}[`);
    });
    if (found)
      return found;
  }
  return null;
}
function revealTabsForField(_host, fieldEl) {
  let tabPanel = fieldEl.closest(".formspec-tab-panel");
  while (tabPanel) {
    const tabsRoot = tabPanel.closest(".formspec-tabs");
    if (tabsRoot instanceof HTMLElement) {
      const panelContainer = tabPanel.parentElement;
      const panels = panelContainer ? Array.from(panelContainer.children).filter((child) => child.classList.contains("formspec-tab-panel")) : [];
      const panelIndex = panels.indexOf(tabPanel);
      if (panelIndex >= 0) {
        tabsRoot.dispatchEvent(new CustomEvent("formspec-tabs-set-active", {
          detail: { index: panelIndex },
          bubbles: false
        }));
      }
    }
    tabPanel = tabPanel.parentElement?.closest(".formspec-tab-panel");
  }
}
function focusField(host, path) {
  const normalizedPath = normalizeFieldPath(path);
  let fieldEl = findFieldElement(host, normalizedPath);
  if (!fieldEl)
    return false;
  const wizardPanel = fieldEl.closest(".formspec-wizard-panel");
  const wizardRoot = wizardPanel?.closest(".formspec-wizard");
  if (wizardPanel instanceof HTMLElement && wizardRoot instanceof HTMLElement) {
    const panelList = Array.from(wizardRoot.querySelectorAll(".formspec-wizard-panel")).filter((panel) => panel.closest(".formspec-wizard") === wizardRoot);
    const panelIndex = panelList.indexOf(wizardPanel);
    if (panelIndex >= 0) {
      wizardRoot.dispatchEvent(new CustomEvent("formspec-wizard-set-step", {
        detail: { index: panelIndex },
        bubbles: false
      }));
      fieldEl = findFieldElement(host, normalizedPath);
      if (!fieldEl)
        return false;
    }
  }
  revealTabsForField(host, fieldEl);
  fieldEl = findFieldElement(host, normalizedPath);
  if (!fieldEl)
    return false;
  let collapsible = fieldEl.closest("details.formspec-collapsible");
  while (collapsible) {
    collapsible.open = true;
    collapsible = collapsible.parentElement?.closest("details.formspec-collapsible");
  }
  const inputEl = fieldEl.querySelector("input, select, textarea, button, [tabindex]");
  const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  fieldEl.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "center" });
  if (inputEl instanceof HTMLElement) {
    inputEl.focus({ preventScroll: true });
  }
  return true;
}

// node_modules/@formspec-org/webcomponent/dist/navigation/wizard.js
function goToWizardStep(host, index) {
  const wizardEl = host.querySelector(".formspec-wizard");
  if (wizardEl && "dispatchEvent" in wizardEl) {
    wizardEl.dispatchEvent(new CustomEvent("formspec-wizard-set-step", {
      detail: { index },
      bubbles: false
    }));
    return true;
  }
  return false;
}

// node_modules/@formspec-org/webcomponent/dist/submit/index.js
function touchFieldsInContainer(container, touchedFields, touchedVersion) {
  const fieldEls = container.querySelectorAll(".formspec-field[data-name]");
  let touchedAny = false;
  for (const fieldEl of fieldEls) {
    const name = fieldEl.dataset.name;
    if (name && !touchedFields.has(name)) {
      touchedFields.add(name);
      touchedAny = true;
    }
  }
  if (touchedAny) {
    touchedVersion.value += 1;
  }
}
function touchAllFields(host) {
  if (!host.engine)
    return;
  let touchedAny = false;
  for (const key of Object.keys(host.engine.errorSignals)) {
    if (host.touchedFields.has(key))
      continue;
    host.touchedFields.add(key);
    touchedAny = true;
  }
  for (const key of Object.keys(host.engine.validationResults)) {
    if (host.touchedFields.has(key))
      continue;
    host.touchedFields.add(key);
    touchedAny = true;
  }
  if (touchedAny) {
    host.touchedVersion.value += 1;
  }
}
function submit(host, options) {
  if (!host.engine)
    return null;
  const mode = options?.mode || "submit";
  const emitEvent = options?.emitEvent !== false;
  touchAllFields(host);
  const response = host.engine.getResponse({ mode });
  const results = Array.isArray(response?.validationResults) ? response.validationResults : [];
  const counts = { error: 0, warning: 0, info: 0 };
  for (const result of results) {
    const severity = result?.severity;
    if (severity === "error" || severity === "warning" || severity === "info") {
      counts[severity] += 1;
    }
  }
  const validationReport = {
    valid: counts.error === 0,
    results,
    counts,
    timestamp: response?.authored || (/* @__PURE__ */ new Date()).toISOString()
  };
  const detail = { response, validationReport };
  host._latestSubmitDetailSignal.value = detail;
  if (emitEvent) {
    host.dispatchEvent(new CustomEvent("formspec-submit", {
      detail,
      bubbles: true,
      composed: true
    }));
  }
  if (!validationReport.valid && host.focusField) {
    const firstError = validationReport.results.find((r2) => r2.severity === "error");
    if (firstError) {
      host.focusField(firstError.path);
    }
  }
  return detail;
}
function setSubmitPending(host, pending) {
  const next = !!pending;
  if (next === host._submitPendingSignal.value)
    return;
  host._submitPendingSignal.value = next;
  host.dispatchEvent(new CustomEvent("formspec-submit-pending-change", {
    detail: { pending: next },
    bubbles: true,
    composed: true
  }));
}
function isSubmitPending(host) {
  return host._submitPendingSignal.value;
}
function resolveValidationTarget(host, resultOrPath) {
  const rawPath = typeof resultOrPath === "string" ? resultOrPath : typeof resultOrPath?.sourceId === "string" ? resultOrPath.sourceId : typeof resultOrPath?.path === "string" ? resultOrPath.path : "";
  const normalizedPath = normalizeFieldPath(rawPath);
  const formLevel = normalizedPath === "" || normalizedPath === "#";
  let path = formLevel ? "" : normalizedPath;
  let fieldElement = null;
  if (!formLevel) {
    const candidatePaths = [normalizedPath, externalPathToInternal(normalizedPath)].filter((candidate, index, all) => candidate && all.indexOf(candidate) === index);
    for (const candidate of candidatePaths) {
      const match = findFieldElement(host, candidate);
      if (!match)
        continue;
      path = candidate;
      fieldElement = match;
      break;
    }
  }
  const keyPath = (path || normalizedPath).replace(/\[\d+\]/g, "");
  const item = keyPath ? host.findItemByKey(keyPath) : null;
  const label = formLevel ? host._definition?.title || "Form" : item?.label || keyPath || normalizedPath || "Field";
  return {
    path,
    label,
    formLevel,
    jumpable: !!fieldElement,
    fieldElement
  };
}

// node_modules/@formspec-org/webcomponent/dist/behaviors/wizard.js
function useWizard(ctx, comp) {
  const children = comp.children || [];
  const currentStep = y(0);
  const setStep = (nextStep) => {
    const bounded = Math.max(0, Math.min(children.length - 1, Math.trunc(nextStep)));
    currentStep.value = bounded;
  };
  const steps = children.map((child, i2) => ({
    id: child.id || `step-${i2}`,
    title: child?.props?.title || `Step ${i2 + 1}`
  }));
  const wizardId = comp.id;
  const compOverrides = {
    cssClass: comp.cssClass,
    style: comp.style,
    accessibility: comp.accessibility
  };
  const showSideNav = comp.sidenav !== false;
  const showProgress = comp.showProgress !== false;
  const allowSkip = !!comp.allowSkip;
  let renderedPanels = [];
  return {
    id: wizardId,
    compOverrides,
    steps,
    showSideNav,
    showProgress,
    allowSkip,
    activeStep() {
      return currentStep.value;
    },
    totalSteps() {
      return children.length;
    },
    canGoNext() {
      return currentStep.value < children.length - 1;
    },
    canGoPrev() {
      return currentStep.value > 0;
    },
    goNext() {
      if (currentStep.value < children.length - 1) {
        const currentPanel = renderedPanels[currentStep.value];
        if (currentPanel) {
          touchFieldsInContainer(currentPanel, ctx.touchedFields, ctx.touchedVersion);
        }
        setStep(currentStep.value + 1);
      }
    },
    goPrev() {
      if (currentStep.value > 0) {
        setStep(currentStep.value - 1);
      }
    },
    goToStep(index) {
      setStep(index);
    },
    renderStep(index, parent) {
      ctx.renderComponent(children[index], parent, ctx.prefix);
      renderedPanels[index] = parent;
    },
    bind(refs) {
      const disposers = [];
      disposers.push(j(() => {
        const step = currentStep.value;
        const total = children.length;
        refs.panels.forEach((p2, idx) => {
          p2.classList.toggle("formspec-hidden", idx !== step);
        });
        if (refs.prevButton) {
          refs.prevButton.disabled = step === 0;
          refs.prevButton.classList.toggle("formspec-hidden", step === 0);
        }
        if (refs.nextButton) {
          refs.nextButton.disabled = total === 0;
          refs.nextButton.textContent = step === total - 1 ? "Submit" : "Next";
        }
        if (refs.skipButton) {
          refs.skipButton.classList.toggle("formspec-hidden", step === total - 1);
        }
        if (refs.sidenavItems) {
          for (let i2 = 0; i2 < refs.sidenavItems.length; i2++) {
            const si = refs.sidenavItems[i2];
            si.item.classList.toggle("formspec-wizard-sidenav-item--active", i2 === step);
            si.item.classList.toggle("formspec-wizard-sidenav-item--completed", i2 < step);
            si.button.setAttribute("aria-current", i2 === step ? "step" : "false");
            si.circle.textContent = i2 < step ? "\u2713" : String(i2 + 1);
          }
        }
        if (refs.progressItems) {
          for (let i2 = 0; i2 < refs.progressItems.length; i2++) {
            const pi = refs.progressItems[i2];
            pi.indicator.classList.toggle("formspec-wizard-step--active", i2 === step);
            pi.indicator.classList.toggle("formspec-wizard-step--completed", i2 < step);
            if (pi.label) {
              pi.label.classList.toggle("formspec-wizard-step-label--active", i2 === step);
            }
          }
        }
        refs.root.dispatchEvent(new CustomEvent("formspec-page-change", {
          detail: {
            index: step,
            total,
            title: children[step]?.props?.title || ""
          },
          bubbles: true,
          composed: true
        }));
      }));
      const onSetStep = (event) => {
        const customEvent = event;
        const requestedIndex = Number(customEvent.detail?.index);
        if (!Number.isFinite(requestedIndex))
          return;
        setStep(requestedIndex);
        event.stopPropagation();
      };
      refs.root.addEventListener("formspec-wizard-set-step", onSetStep);
      disposers.push(() => {
        refs.root.removeEventListener("formspec-wizard-set-step", onSetStep);
      });
      if (refs.nextButton) {
        refs.nextButton.addEventListener("click", () => {
          const isLastStep = currentStep.value === children.length - 1;
          if (isLastStep) {
            ctx.submit({ mode: "submit", emitEvent: true });
            return;
          }
          const currentPanel = renderedPanels[currentStep.value];
          if (currentPanel) {
            touchFieldsInContainer(currentPanel, ctx.touchedFields, ctx.touchedVersion);
          }
          setStep(currentStep.value + 1);
        });
      }
      if (refs.prevButton) {
        refs.prevButton.addEventListener("click", () => {
          if (currentStep.value > 0)
            setStep(currentStep.value - 1);
        });
      }
      return () => disposers.forEach((d2) => d2());
    }
  };
}

// node_modules/@formspec-org/webcomponent/dist/rendering/emit-node.js
function emitNode(host, node, parent, prefix, headingLevel = 3) {
  let target = parent;
  if (node.when) {
    const wrapper = document.createElement("div");
    wrapper.className = "formspec-when";
    target.appendChild(wrapper);
    let fallbackEl = null;
    if (node.fallback) {
      fallbackEl = document.createElement("p");
      fallbackEl.className = "formspec-conditional-fallback";
      fallbackEl.textContent = node.fallback;
      target.appendChild(fallbackEl);
    }
    const exprFn = host.engine.compileExpression(node.when, prefix);
    host.cleanupFns.push(j(() => {
      const visible = !!exprFn();
      wrapper.classList.toggle("formspec-hidden", !visible);
      if (fallbackEl)
        fallbackEl.classList.toggle("formspec-hidden", visible);
    }));
    target = wrapper;
  }
  if (node.isRepeatTemplate && node.props.bind) {
    const bindKey = node.props.bind;
    const fullRepeatPath = prefix ? `${prefix}.${bindKey}` : bindKey;
    const container = document.createElement("div");
    container.className = "formspec-repeat";
    container.dataset.bind = bindKey;
    target.appendChild(container);
    const item = host.findItemByKey(bindKey);
    let innerCleanupFns = [];
    const disposeInner = () => {
      for (const cleanup of innerCleanupFns.splice(0)) {
        cleanup();
      }
    };
    host.cleanupFns.push(j(() => {
      const count = host.engine.repeats[fullRepeatPath]?.value || 0;
      disposeInner();
      container.replaceChildren();
      const nextInnerCleanupFns = [];
      const repeatHost = { ...host, cleanupFns: nextInnerCleanupFns };
      for (let idx = 0; idx < count; idx++) {
        const instanceWrapper = document.createElement("div");
        instanceWrapper.className = "formspec-repeat-instance";
        container.appendChild(instanceWrapper);
        const instancePrefix = `${fullRepeatPath}[${idx}]`;
        for (const child of node.children) {
          emitNode(repeatHost, child, instanceWrapper, instancePrefix, headingLevel);
        }
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "formspec-repeat-add";
        removeBtn.textContent = `Remove ${item?.label || bindKey}`;
        const removeIdx = idx;
        removeBtn.addEventListener("click", () => {
          host.engine.removeRepeatInstance(fullRepeatPath, removeIdx);
        });
        instanceWrapper.appendChild(removeBtn);
      }
      innerCleanupFns = nextInnerCleanupFns;
    }));
    host.cleanupFns.push(() => {
      disposeInner();
    });
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.className = "formspec-repeat-add";
    addBtn.textContent = `Add ${item?.label || bindKey}`;
    addBtn.addEventListener("click", () => {
      host.engine.addRepeatInstance(fullRepeatPath);
    });
    target.appendChild(addBtn);
    return;
  }
  if (node.scopeChange && !node.isRepeatTemplate && node.props.bind) {
    const bindKey = node.props.bind;
    const nextPrefix = prefix ? `${prefix}.${bindKey}` : bindKey;
    const el2 = document.createElement("div");
    el2.className = "formspec-group";
    if (node.props.title) {
      const heading = document.createElement(`h${Math.min(headingLevel, 6)}`);
      heading.textContent = node.props.title;
      el2.appendChild(heading);
    }
    const groupFullPath = nextPrefix;
    if (host.engine.relevantSignals[groupFullPath]) {
      host.cleanupFns.push(j(() => {
        const isRelevant = host.engine.relevantSignals[groupFullPath].value;
        el2.classList.toggle("formspec-hidden", !isRelevant);
      }));
    }
    target.appendChild(el2);
    for (const child of node.children) {
      emitNode(host, child, el2, nextPrefix, Math.min(headingLevel + 1, 6));
    }
    return;
  }
  const comp = {
    component: node.component,
    ...node.props
  };
  if (node.style)
    comp.style = node.style;
  if (node.cssClasses.length > 0)
    comp.cssClass = node.cssClasses;
  if (node.accessibility)
    comp.accessibility = node.accessibility;
  comp.children = node.children;
  renderActualComponent(host, comp, target, prefix);
}
function renderComponent(host, comp, parent, prefix = "") {
  if (comp && typeof comp === "object" && "category" in comp && "id" in comp) {
    emitNode(host, comp, parent, prefix);
    return;
  }
  console.warn("renderComponent called with non-LayoutNode comp \u2014 this should not happen after planner integration", comp);
}
function renderActualComponent(host, comp, parent, prefix = "") {
  const componentType = comp.component;
  const plugin = globalRegistry.get(componentType);
  const ctx = {
    engine: host.engine,
    componentDocument: host._componentDocument,
    themeDocument: host._themeDocument,
    prefix,
    submit: (opts) => host.submit(opts),
    resolveValidationTarget: (r2) => host.resolveValidationTarget(r2),
    focusField: (p2) => host.focusField(p2),
    submitPendingSignal: host._submitPendingSignal,
    latestSubmitDetailSignal: host._latestSubmitDetailSignal,
    setSubmitPending: (pending) => host.setSubmitPending(pending),
    isSubmitPending: () => host.isSubmitPending(),
    renderComponent: (comp2, parent2, pfx) => renderComponent(host, comp2, parent2, pfx),
    resolveToken: (val) => host.resolveToken(val),
    applyStyle: (el2, style) => host.applyStyle(el2, style),
    applyCssClass: (el2, comp2) => host.applyCssClass(el2, comp2),
    applyAccessibility: (el2, comp2) => host.applyAccessibility(el2, comp2),
    resolveItemPresentation: (itemDesc) => host.resolveItemPresentation(itemDesc),
    cleanupFns: host.cleanupFns,
    findItemByKey: (key) => host.findItemByKey(key),
    activeBreakpoint: host.activeBreakpoint,
    touchedFields: host.touchedFields,
    touchedVersion: host.touchedVersion,
    behaviorContext: {
      engine: host.engine,
      definition: host._definition,
      prefix,
      cleanupFns: host.cleanupFns,
      touchedFields: host.touchedFields,
      touchedVersion: host.touchedVersion,
      latestSubmitDetailSignal: host._latestSubmitDetailSignal,
      resolveToken: (v2) => host.resolveToken(v2),
      resolveItemPresentation: (item) => host.resolveItemPresentation(item),
      resolveWidgetClassSlots: (p2) => host.resolveWidgetClassSlots(p2),
      findItemByKey: (key) => host.findItemByKey(key),
      renderComponent: (comp2, parent2, pfx) => renderComponent(host, comp2, parent2, pfx),
      submit: (opts) => host.submit(opts),
      registryEntries: host._registryEntries,
      rerender: () => host.render()
    },
    adapterContext: {
      onDispose: (fn) => host.cleanupFns.push(fn),
      applyCssClass: (el2, comp2) => host.applyCssClass(el2, comp2),
      applyStyle: (el2, style) => host.applyStyle(el2, style),
      applyAccessibility: (el2, comp2) => host.applyAccessibility(el2, comp2),
      applyClassValue: (el2, classValue) => host.applyClassValue(el2, classValue)
    }
  };
  if (componentType === "Stack" && isPageModeWizard(host, comp)) {
    renderPageModeWizard(comp, parent, ctx);
    return;
  }
  if (componentType === "Stack" && isPageModeTabs(host, comp)) {
    renderPageModeTabs(comp, parent, ctx);
    return;
  }
  if (plugin) {
    plugin.render(comp, parent, ctx);
  } else {
    console.warn(`Unknown component type: ${componentType} (custom components should be expanded by planner)`);
  }
}
function isPageModeWizard(host, comp) {
  const pageMode = host._definition?.formPresentation?.pageMode;
  if (pageMode !== "wizard")
    return false;
  const children = comp.children;
  if (!Array.isArray(children) || children.length === 0)
    return false;
  return children.some((c2) => c2.component === "Page");
}
function isPageModeTabs(host, comp) {
  const pageMode = host._definition?.formPresentation?.pageMode;
  if (pageMode !== "tabs")
    return false;
  const children = comp.children;
  if (!Array.isArray(children) || children.length === 0)
    return false;
  return children.some((c2) => c2.component === "Page");
}
function renderPageModeWizard(comp, parent, ctx) {
  const allChildren = comp.children || [];
  const orphans = allChildren.filter((c2) => c2.component !== "Page");
  const pageChildren = allChildren.filter((c2) => c2.component === "Page");
  for (const orphan of orphans) {
    ctx.renderComponent(orphan, parent, ctx.prefix);
  }
  const formPres = ctx.behaviorContext.definition?.formPresentation || {};
  const wizardComp = {
    component: "Wizard",
    children: pageChildren,
    showProgress: formPres.showProgress !== false,
    allowSkip: !!formPres.allowSkip,
    sidenav: formPres.sidenav,
    cssClass: comp.cssClass,
    style: comp.style,
    accessibility: comp.accessibility,
    id: comp.id
  };
  const behavior = useWizard(ctx.behaviorContext, wizardComp);
  const adapterFn = globalRegistry.resolveAdapterFn("Wizard");
  if (adapterFn)
    adapterFn(behavior, parent, ctx.adapterContext);
}
function renderPageModeTabs(comp, parent, ctx) {
  const allChildren = comp.children || [];
  const orphans = allChildren.filter((c2) => c2.component !== "Page");
  const pageChildren = allChildren.filter((c2) => c2.component === "Page");
  for (const orphan of orphans) {
    ctx.renderComponent(orphan, parent, ctx.prefix);
  }
  const formPres = ctx.behaviorContext.definition?.formPresentation || {};
  const tabsComp = {
    component: "Tabs",
    children: pageChildren,
    tabLabels: pageChildren.map((p2) => p2.title || p2.props?.title),
    position: formPres.tabPosition || "top",
    defaultTab: formPres.defaultTab ?? 0,
    cssClass: comp.cssClass,
    style: comp.style,
    accessibility: comp.accessibility,
    id: comp.id
  };
  const behavior = useTabs(ctx.behaviorContext, tabsComp);
  const adapterFn = globalRegistry.resolveAdapterFn("Tabs");
  if (adapterFn)
    adapterFn(behavior, parent, ctx.adapterContext);
}

// node_modules/@formspec-org/webcomponent/dist/styling/tokens.js
function resolveToken2(host, val) {
  return resolveToken(val, host._componentDocument?.tokens, host.getEffectiveTheme().tokens);
}
function emitTokenProperties(host, container) {
  const effectiveTheme = host.getEffectiveTheme();
  const tokens = {
    ...effectiveTheme.tokens || {},
    ...host._componentDocument?.tokens || {}
  };
  for (const [key, value] of Object.entries(tokens)) {
    container.style.setProperty(`--formspec-${key.replace(/\./g, "-")}`, String(value));
  }
}

// node_modules/@formspec-org/webcomponent/dist/styling/classes.js
function applyCssClass(host, el2, comp) {
  if (!comp.cssClass)
    return;
  const classes = Array.isArray(comp.cssClass) ? comp.cssClass : [comp.cssClass];
  for (const cls of classes) {
    const resolved = String(resolveToken2(host, cls));
    for (const c2 of resolved.split(/\s+/)) {
      if (c2)
        el2.classList.add(c2);
    }
  }
}
function applyClassValue(host, el2, classValue) {
  if (classValue === void 0 || classValue === null)
    return;
  const values = Array.isArray(classValue) ? classValue : [classValue];
  for (const cls of values) {
    const resolved = String(resolveToken2(host, cls));
    for (const c2 of resolved.split(/\s+/)) {
      if (c2)
        el2.classList.add(c2);
    }
  }
}
function resolveWidgetClassSlots(_host, presentation) {
  const widgetConfig = presentation.widgetConfig;
  if (!widgetConfig || typeof widgetConfig !== "object")
    return {};
  const config = widgetConfig;
  const extensionSlots = config["x-classes"] && typeof config["x-classes"] === "object" && !Array.isArray(config["x-classes"]) ? config["x-classes"] : {};
  return {
    root: config.rootClass ?? extensionSlots.root,
    label: config.labelClass ?? extensionSlots.label,
    control: config.controlClass ?? config.inputClass ?? extensionSlots.control ?? extensionSlots.input,
    hint: config.hintClass ?? extensionSlots.hint,
    error: config.errorClass ?? extensionSlots.error
  };
}

// node_modules/@formspec-org/webcomponent/dist/styling/style.js
function applyStyle(host, el2, style) {
  if (!style)
    return;
  for (const [key, val] of Object.entries(style)) {
    const resolved = resolveToken2(host, val);
    el2.style[key] = resolved;
  }
}

// node_modules/@formspec-org/webcomponent/dist/styling/accessibility.js
var a11yDescIdCounter = 0;
function applyAccessibility(_host, el2, comp) {
  if (!comp.accessibility)
    return;
  const a11y = comp.accessibility;
  if (a11y.role)
    el2.setAttribute("role", a11y.role);
  const description = a11y.description ?? a11y.ariaDescription;
  if (description) {
    el2.setAttribute("aria-description", description);
    const descId = `formspec-a11y-desc-${++a11yDescIdCounter}`;
    const descEl = document.createElement("span");
    descEl.id = descId;
    descEl.className = "formspec-sr-only";
    descEl.textContent = description;
    el2.appendChild(descEl);
    const existing = el2.getAttribute("aria-describedby");
    el2.setAttribute("aria-describedby", existing ? `${existing} ${descId}` : descId);
  }
  if (a11y.liveRegion)
    el2.setAttribute("aria-live", a11y.liveRegion);
}

// node_modules/@formspec-org/webcomponent/dist/styling/stylesheets.js
var stylesheetRefCounts = /* @__PURE__ */ new Map();
function canonicalizeStylesheetHref(href) {
  try {
    return new URL(href, document.baseURI).href;
  } catch {
    return href;
  }
}
function findThemeStylesheet(hrefKey) {
  const links = document.head.querySelectorAll("link[data-formspec-theme-href]");
  for (const link of links) {
    const htmlLink = link;
    if (htmlLink.dataset.formspecThemeHref === hrefKey)
      return htmlLink;
  }
  return null;
}
function loadStylesheets(host) {
  cleanupStylesheets(host);
  if (!host._themeDocument?.stylesheets)
    return;
  const uniqueHrefs = /* @__PURE__ */ new Set();
  for (const rawHref of host._themeDocument.stylesheets) {
    if (!rawHref || typeof rawHref !== "string")
      continue;
    const hrefKey = canonicalizeStylesheetHref(rawHref);
    if (uniqueHrefs.has(hrefKey))
      continue;
    uniqueHrefs.add(hrefKey);
    const existingCount = stylesheetRefCounts.get(hrefKey) ?? 0;
    if (existingCount === 0) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = rawHref;
      link.dataset.formspecTheme = "true";
      link.dataset.formspecThemeHref = hrefKey;
      document.head.appendChild(link);
    }
    stylesheetRefCounts.set(hrefKey, existingCount + 1);
    host.stylesheetHrefs.push(hrefKey);
  }
}
function cleanupStylesheets(host) {
  for (const hrefKey of host.stylesheetHrefs) {
    const count = stylesheetRefCounts.get(hrefKey) ?? 0;
    if (count <= 1) {
      stylesheetRefCounts.delete(hrefKey);
      const link = findThemeStylesheet(hrefKey);
      if (link)
        link.remove();
    } else {
      stylesheetRefCounts.set(hrefKey, count - 1);
    }
  }
  host.stylesheetHrefs = [];
}

// node_modules/@formspec-org/webcomponent/dist/styling/index.js
function resolveItemPresentation(host, itemDesc) {
  const item = host.findItemByKey(itemDesc.key);
  const tier1 = {
    formPresentation: host._definition?.formPresentation,
    itemPresentation: item?.presentation
  };
  const theme = host.getEffectiveTheme();
  return resolvePresentation(theme, itemDesc, tier1);
}

// node_modules/@formspec-org/webcomponent/dist/element.js
var FormspecRender = class extends HTMLElement {
  get activeBreakpoint() {
    return this._breakpoints.activeBreakpointSignal.value ?? null;
  }
  constructor() {
    super();
    this._themeDocument = null;
    this._registryEntries = /* @__PURE__ */ new Map();
    this.engine = null;
    this.cleanupFns = [];
    this._breakpoints = createBreakpointState();
    this.stylesheetHrefs = [];
    this.rootContainer = null;
    this._renderPending = false;
    this._locale = "";
    this._pendingLocaleDocuments = [];
    this.touchedFields = /* @__PURE__ */ new Set();
    this.touchedVersion = y(0);
    this._screenerCompleted = false;
    this._screenerRoute = null;
    this._screenerSeedAnswers = null;
    this._initialData = null;
    this._submitPendingSignal = y(false);
    this._latestSubmitDetailSignal = y(null);
    this.resolveToken = (val) => resolveToken2(this._stylingHost, val);
    this.resolveItemPresentation = (itemDesc) => resolveItemPresentation(this._stylingHost, itemDesc);
    this.applyStyle = (el2, style) => applyStyle(this._stylingHost, el2, style);
    this.applyCssClass = (el2, comp) => applyCssClass(this._stylingHost, el2, comp);
    this.applyClassValue = (el2, classValue) => applyClassValue(this._stylingHost, el2, classValue);
    this.resolveWidgetClassSlots = (presentation) => resolveWidgetClassSlots(this._stylingHost, presentation);
    this.applyAccessibility = (el2, comp) => applyAccessibility(this._stylingHost, el2, comp);
    this.findItemByKey = (key, items = this._definition.items) => {
      const dot = key.indexOf(".");
      if (dot !== -1) {
        const head = key.slice(0, dot);
        const rest = key.slice(dot + 1);
        for (const item of items) {
          if (item.key === head && item.children) {
            return this.findItemByKey(rest, item.children);
          }
        }
        return null;
      }
      for (const item of items) {
        if (item.key === key)
          return item;
        if (item.children) {
          const found = this.findItemByKey(key, item.children);
          if (found)
            return found;
        }
      }
      return null;
    };
    const shadow = this.attachShadow({ mode: "open" });
    shadow.appendChild(document.createElement("slot"));
  }
  // ── Styling delegators ────────────────────────────────────────────
  get _stylingHost() {
    return this;
  }
  // ── Navigation delegators ─────────────────────────────────────────
  get _navHost() {
    return this;
  }
  // ── Screener helpers ──────────────────────────────────────────────
  isInternalScreenerTarget(target) {
    const defUrl = this._definition?.url;
    if (!defUrl || !target)
      return false;
    return target === defUrl || target.startsWith(defUrl + "/") || target.split("|")[0] === defUrl;
  }
  /** @internal */
  classifyScreenerRoute(route) {
    if (!route?.target)
      return "none";
    return this.isInternalScreenerTarget(route.target) ? "internal" : "external";
  }
  /** Returns the current screener completion + routing state. */
  getScreenerState() {
    const hasScreener = hasActiveScreener(this._definition);
    return {
      hasScreener,
      completed: hasScreener ? this._screenerCompleted : true,
      routeType: this.classifyScreenerRoute(this._screenerRoute),
      route: this._screenerRoute
    };
  }
  /** @internal */
  emitScreenerStateChange(reason, answers) {
    this.dispatchEvent(new CustomEvent("formspec-screener-state-change", {
      detail: {
        ...this.getScreenerState(),
        reason,
        ...answers ? { answers } : {}
      },
      bubbles: true,
      composed: true
    }));
  }
  /**
   * Optional: only screener keys when you have no full `data` blob. Prefer {@link initialData}
   * with the same shape as `response.data` so screener + main form hydrate in one step.
   */
  set screenerSeedAnswers(val) {
    if (val != null && typeof val === "object" && !Array.isArray(val)) {
      this._screenerSeedAnswers = { ...val };
    } else {
      this._screenerSeedAnswers = null;
    }
  }
  get screenerSeedAnswers() {
    return this._screenerSeedAnswers;
  }
  /**
   * Full Formspec response `data` (same object you would pass to engine hydration). Set **before**
   * {@link definition} on a new element. On engine boot, screener fields are split out for the gate;
   * the rest is applied to the engine so one assignment replaces manual `extractScreenerSeedFromData` +
   * `applyResponseDataToEngine` calls.
   */
  set initialData(val) {
    if (val != null && typeof val === "object" && !Array.isArray(val)) {
      this._initialData = { ...val };
    } else {
      this._initialData = null;
    }
  }
  get initialData() {
    return this._initialData;
  }
  tryAutoCompleteScreenerFromSeed() {
    if (!this.engine || !this._screenerSeedAnswers)
      return;
    const screener = this._definition?.screener;
    if (!screener?.items?.length)
      return;
    const defaultCurrency = this._definition.formPresentation?.defaultCurrency || "USD";
    const answers = buildInitialScreenerAnswers(screener, this._screenerSeedAnswers, defaultCurrency);
    if (!screenerAnswersSatisfyRequired(screener, answers))
      return;
    let route;
    try {
      route = this.engine.evaluateScreener(answers);
    } catch {
      return;
    }
    if (this.classifyScreenerRoute(route) === "internal") {
      this._screenerRoute = route;
      this._screenerCompleted = true;
      this._screenerSeedAnswers = null;
      this.emitScreenerStateChange("seed-auto-internal", answers);
    }
  }
  scheduleRender() {
    if (this._renderPending)
      return;
    this._renderPending = true;
    Promise.resolve().then(() => {
      this._renderPending = false;
      this.render();
    });
  }
  /**
   * Set the form definition. Creates a new {@link FormEngine} instance and
   * schedules a re-render. Throws if engine initialization fails.
   */
  set definition(val) {
    this._definition = val;
    this._screenerCompleted = false;
    this._screenerRoute = null;
    this.touchedFields.clear();
    this.touchedVersion.value = 0;
    const bootEngine = () => {
      if (this._definition !== val) {
        return;
      }
      this.engine = createFormEngine(val, void 0, Array.from(this._registryEntries.values()));
      for (const doc of this._pendingLocaleDocuments) {
        this.engine.loadLocale(doc);
      }
      if (this._locale) {
        this.engine.setLocale(this._locale);
        this.setAttribute("dir", this.engine.getLocaleDirection());
      }
      if (this._initialData) {
        const seed = extractScreenerSeedFromData(val, this._initialData);
        if (seed) {
          this._screenerSeedAnswers = seed;
        }
        const rest = omitScreenerKeysFromData(val, this._initialData);
        applyResponseDataToEngine(this.engine, rest);
        this._initialData = null;
      }
      this.emitScreenerStateChange("definition-set");
      this.scheduleRender();
    };
    if (isFormspecEngineInitialized()) {
      try {
        bootEngine();
      } catch (e2) {
        console.error("Engine initialization failed", e2);
        throw e2;
      }
    } else {
      void initFormspecEngine().then(() => {
        try {
          bootEngine();
        } catch (e2) {
          console.error("Engine initialization failed", e2);
        }
      });
    }
  }
  /** The currently loaded form definition object. */
  get definition() {
    return this._definition;
  }
  /**
   * Set the component document (component tree, custom components, tokens,
   * breakpoints). Schedules a re-render.
   */
  set componentDocument(val) {
    this._componentDocument = val;
    this.scheduleRender();
  }
  /** The currently loaded component document. */
  get componentDocument() {
    return this._componentDocument;
  }
  /**
   * Set the theme document. Loads/unloads referenced stylesheets via
   * ref-counting and schedules a re-render.
   */
  set themeDocument(val) {
    this._themeDocument = val;
    loadStylesheets(this._stylingHost);
    this.scheduleRender();
  }
  /** The currently loaded theme document, or `null` if none. */
  get themeDocument() {
    return this._themeDocument;
  }
  /**
   * Set one or more extension registry documents. Builds an internal lookup
   * map from extension name → registry entry so that field renderers can
   * apply constraints and metadata (inputMode, autocomplete, pattern, etc.)
   * generically instead of hardcoding per-extension behaviour.
   */
  set registryDocuments(docs) {
    this._registryEntries.clear();
    const docList = Array.isArray(docs) ? docs : docs ? [docs] : [];
    for (const doc of docList) {
      if (!doc?.entries)
        continue;
      for (const entry of doc.entries) {
        if (entry.name) {
          this._registryEntries.set(entry.name, entry);
        }
      }
    }
    this.scheduleRender();
  }
  /** The current registry entry lookup (extension name → entry). */
  get registryEntries() {
    return this._registryEntries;
  }
  /**
   * Load one or more locale documents into the engine. If the engine
   * hasn't been created yet (no definition set), the documents are
   * buffered and applied when the engine boots.
   *
   * Set **after** `definition` for immediate loading, or before if
   * pre-loading locale bundles before the form definition arrives.
   */
  set localeDocuments(docs) {
    const arr = Array.isArray(docs) ? docs : [docs];
    this._pendingLocaleDocuments = arr;
    if (this.engine) {
      for (const doc of arr) {
        this.engine.loadLocale(doc);
      }
    }
  }
  /**
   * Set the active locale code. Updates the engine locale if available,
   * and sets `lang` and `dir` attributes for accessibility and RTL support.
   *
   * If the engine hasn't been created yet, the locale code is buffered
   * and applied when the engine boots.
   */
  set locale(code) {
    this._locale = code;
    this.setAttribute("lang", code);
    if (this.engine) {
      this.engine.setLocale(code);
      this.setAttribute("dir", this.engine.getLocaleDirection());
    }
  }
  /** The currently active locale code, or empty string if none set. */
  get locale() {
    return this._locale;
  }
  /**
   * Return the underlying {@link FormEngine} instance, or `null` if no
   * definition has been set yet. Useful for direct engine access in tests
   * or advanced integrations.
   */
  getEngine() {
    return this.engine;
  }
  /**
   * Capture a diagnostics snapshot from the engine, including current signal
   * values, validation state, and repeat counts.
   */
  getDiagnosticsSnapshot(options) {
    return this.engine?.getDiagnosticsSnapshot?.(options) || null;
  }
  /**
   * Apply a single replay event (e.g. `setValue`, `addRepeat`) to the engine.
   */
  applyReplayEvent(event) {
    if (!this.engine?.applyReplayEvent) {
      return { ok: false, event, error: "Engine unavailable" };
    }
    return this.engine.applyReplayEvent(event);
  }
  /**
   * Replay a sequence of events against the engine in order.
   */
  replay(events, options) {
    if (!this.engine?.replay) {
      return { applied: 0, results: [], errors: [{ index: 0, event: null, error: "Engine unavailable" }] };
    }
    return this.engine.replay(events, options);
  }
  /**
   * Inject a runtime context (e.g. `now`, user metadata) into the engine.
   */
  setRuntimeContext(context) {
    this.engine?.setRuntimeContext?.(context);
  }
  /**
   * Mark all registered fields as touched so validation errors become visible.
   */
  touchAllFields() {
    touchAllFields(this);
  }
  /**
   * Build a submit payload and validation report from the current form state.
   * Optionally dispatches `formspec-submit` with `{ response, validationReport }`.
   */
  submit(options) {
    return submit(this, options);
  }
  /**
   * Resolve a validation result/path to a navigation target with metadata.
   */
  resolveValidationTarget(resultOrPath) {
    return resolveValidationTarget(this, resultOrPath);
  }
  /**
   * Toggle shared submit pending state and emit `formspec-submit-pending-change`
   * whenever the value changes.
   */
  setSubmitPending(pending) {
    setSubmitPending(this, pending);
  }
  /** Returns the current shared submit pending state. */
  isSubmitPending() {
    return isSubmitPending(this);
  }
  /**
   * Programmatically navigate to a wizard step in the first rendered wizard.
   */
  goToWizardStep(index) {
    return goToWizardStep(this._navHost, index);
  }
  /**
   * Reveal and focus a field by bind path.
   */
  focusField(path) {
    return focusField(this._navHost, path);
  }
  /** @internal */
  getEffectiveTheme() {
    return this._themeDocument || default_theme_default;
  }
  cleanup() {
    for (const fn of this.cleanupFns) {
      fn();
    }
    this.cleanupFns = [];
  }
  /**
   * Perform a full synchronous render of the form.
   */
  render() {
    this.cleanup();
    if (!this.engine || !this._definition)
      return;
    setupBreakpoints(this, this._breakpoints);
    if (this._componentDocument) {
      if (this._componentDocument.$formspecComponent !== "1.0") {
        console.warn(`Unsupported Component Document version: ${this._componentDocument.$formspecComponent}`);
      }
      if (this._componentDocument.targetDefinition) {
        const target = this._componentDocument.targetDefinition;
        if (target.url !== this._definition.url) {
          console.warn(`Component Document target URL (${target.url}) does not match Definition URL (${this._definition.url})`);
        }
      }
    }
    if (!this.rootContainer) {
      this.rootContainer = document.createElement("div");
      this.rootContainer.className = "formspec-container";
      this.appendChild(this.rootContainer);
    }
    const container = this.rootContainer;
    container.className = "formspec-container";
    container.replaceChildren();
    emitTokenProperties(this._stylingHost, container);
    if (hasActiveScreener(this._definition) && !this._screenerCompleted) {
      this.tryAutoCompleteScreenerFromSeed();
    }
    if (hasActiveScreener(this._definition) && !this._screenerCompleted) {
      renderScreener(this, container);
      return;
    }
    const planCtx = {
      items: this._definition.items,
      formPresentation: this._definition.formPresentation,
      componentDocument: this._componentDocument,
      theme: this._themeDocument || this.getEffectiveTheme(),
      activeBreakpoint: this.activeBreakpoint,
      findItem: (key) => this.findItemByKey(key),
      isComponentAvailable: (type) => !!globalRegistry.get(type)
    };
    if (this._componentDocument && this._componentDocument.tree) {
      const plan = planComponentTree(this._componentDocument.tree, planCtx);
      emitNode(this, plan, container, "");
    } else {
      const plans = planDefinitionFallback(this._definition.items, planCtx);
      const pageMode = this._definition.formPresentation?.pageMode;
      const hasPages = (pageMode === "wizard" || pageMode === "tabs") && plans.some((p2) => p2.component === "Page");
      if (hasPages) {
        const wrapperNode = {
          id: "_root-stack",
          component: "Stack",
          category: "layout",
          props: {},
          cssClasses: [],
          children: plans
        };
        emitNode(this, wrapperNode, container, "");
      } else {
        for (const plan of plans) {
          emitNode(this, plan, container, "");
        }
      }
    }
  }
  /** Returns the screener route selected during the screening phase, or null. */
  getScreenerRoute() {
    return this._screenerRoute;
  }
  /** Programmatically skip the screener and proceed to the main form. */
  skipScreener() {
    this._screenerCompleted = true;
    this._screenerRoute = null;
    this.emitScreenerStateChange("skip");
    this.scheduleRender();
  }
  /** Return to the screener from the main form. */
  restartScreener() {
    this._screenerCompleted = false;
    this._screenerRoute = null;
    this.emitScreenerStateChange("restart");
    this.scheduleRender();
  }
  /**
   * Custom element lifecycle callback. Disposes all signal effects,
   * decrements stylesheet ref-counts, tears down breakpoint listeners,
   * and removes the root container.
   */
  disconnectedCallback() {
    this.cleanup();
    cleanupStylesheets(this._stylingHost);
    cleanupBreakpoints(this._breakpoints);
    if (this.rootContainer) {
      this.rootContainer.remove();
      this.rootContainer = null;
    }
  }
};

// node_modules/@formspec-org/webcomponent/dist/index.js
void initFormspecEngine();
registerDefaultComponents();

// node_modules/@formspec-org/adapters/dist/index.js
var dist_exports = {};
__export(dist_exports, {
  tailwindAdapter: () => tailwindAdapter,
  uswdsAdapter: () => uswdsAdapter
});

// node_modules/@formspec-org/adapters/dist/helpers.js
function el(tag, attrs) {
  const element = document.createElement(tag);
  if (attrs) {
    for (const [key, value] of Object.entries(attrs)) {
      if (key === "class") {
        element.className = value;
      } else {
        element.setAttribute(key, value);
      }
    }
  }
  return element;
}
function applyCascadeClasses(root, presentation) {
  if (!presentation.cssClass)
    return;
  const classes = Array.isArray(presentation.cssClass) ? presentation.cssClass : [presentation.cssClass];
  for (const cls of classes) {
    if (cls)
      root.classList.add(...cls.split(/\s+/).filter(Boolean));
  }
}
function applyCascadeAccessibility(root, presentation) {
  if (!presentation.accessibility)
    return;
  const a2 = presentation.accessibility;
  if (a2.role)
    root.setAttribute("role", a2.role);
  if (a2.description)
    root.setAttribute("aria-description", a2.description);
  if (a2.liveRegion)
    root.setAttribute("aria-live", a2.liveRegion);
}

// node_modules/@formspec-org/adapters/dist/uswds/shared.js
function createUSWDSFieldDOM(behavior, options) {
  const p2 = behavior.presentation;
  const labelFor = options?.labelFor ?? true;
  const root = el("div", { class: "usa-form-group", "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const labelAttrs = {
    class: p2.labelPosition === "hidden" ? "usa-label usa-sr-only" : "usa-label"
  };
  if (labelFor)
    labelAttrs.for = behavior.id;
  const label = el("label", labelAttrs);
  label.textContent = behavior.label;
  root.appendChild(label);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("span", { class: "usa-hint", id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createUSWDSError(behavior.id);
  const describedBy = [
    hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  return { root, label, hint, error, describedBy };
}
function createUSWDSError(behaviorId) {
  return el("span", {
    class: "usa-error-message",
    id: `${behaviorId}-error`,
    role: "alert",
    "aria-live": "polite"
  });
}

// node_modules/@formspec-org/adapters/dist/uswds/text-input.js
var renderTextInput2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const isTextarea = behavior.maxLines != null && behavior.maxLines > 1;
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  let control;
  if (isTextarea) {
    const textarea = document.createElement("textarea");
    textarea.className = "usa-textarea";
    textarea.id = behavior.id;
    textarea.name = behavior.fieldPath;
    textarea.rows = behavior.maxLines;
    if (behavior.placeholder)
      textarea.placeholder = behavior.placeholder;
    textarea.setAttribute("aria-describedby", describedBy);
    control = textarea;
  } else {
    const input = document.createElement("input");
    input.className = "usa-input";
    input.id = behavior.id;
    input.name = behavior.fieldPath;
    input.type = behavior.resolvedInputType || "text";
    if (behavior.placeholder)
      input.placeholder = behavior.placeholder;
    if (behavior.inputMode)
      input.inputMode = behavior.inputMode;
    for (const [attr, val] of Object.entries(behavior.extensionAttrs)) {
      if (attr === "inputMode")
        input.inputMode = val;
      else if (attr === "maxLength")
        input.maxLength = Number(val);
      else
        input.setAttribute(attr, val);
    }
    input.setAttribute("aria-describedby", describedBy);
    if (behavior.prefix || behavior.suffix) {
      const group = el("div", { class: "usa-input-group" });
      if (behavior.prefix) {
        const prefixEl = el("div", { class: "usa-input-prefix" });
        prefixEl.textContent = behavior.prefix;
        group.appendChild(prefixEl);
      }
      group.appendChild(input);
      if (behavior.suffix) {
        const suffixEl = el("div", { class: "usa-input-suffix" });
        suffixEl.textContent = behavior.suffix;
        group.appendChild(suffixEl);
      }
      root.appendChild(group);
      control = group;
    } else {
      control = input;
    }
  }
  if (!control.parentElement)
    root.appendChild(control);
  root.appendChild(error);
  parent.appendChild(root);
  const actualInput = control.querySelector("input") || control.querySelector("textarea") || control;
  const dispose = behavior.bind({
    root,
    label,
    control,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      actualInput.classList.toggle(actualInput.classList.contains("usa-textarea") ? "usa-textarea--error" : "usa-input--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/number-input.js
var renderNumberInput2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const input = document.createElement("input");
  input.className = "usa-input";
  input.type = "number";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  input.setAttribute("aria-describedby", describedBy);
  root.appendChild(input);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      input.classList.toggle("usa-input--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/radio-group.js
function buildRadioOptions(behavior, container, options) {
  container.innerHTML = "";
  const controls = /* @__PURE__ */ new Map();
  for (let i2 = 0; i2 < options.length; i2++) {
    const opt = options[i2];
    const optId = `${behavior.id}-${i2}`;
    const wrapper = el("div", { class: "usa-radio" });
    const input = document.createElement("input");
    input.className = "usa-radio__input";
    input.id = optId;
    input.type = "radio";
    input.name = behavior.inputName;
    input.value = opt.value;
    controls.set(opt.value, input);
    const label = el("label", { class: "usa-radio__label", for: optId });
    label.textContent = opt.label;
    wrapper.appendChild(input);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
  }
  return controls;
}
var renderRadioGroup2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const fieldset = el("fieldset", { class: "usa-fieldset" });
  applyCascadeClasses(fieldset, p2);
  applyCascadeAccessibility(fieldset, p2);
  const legendClasses = p2.labelPosition === "hidden" ? "usa-legend usa-sr-only" : "usa-legend";
  const legend = el("legend", { class: legendClasses });
  legend.textContent = behavior.label;
  fieldset.appendChild(legend);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("span", { class: "usa-hint", id: hintId });
    hint.textContent = behavior.hint;
    fieldset.appendChild(hint);
  }
  const optionContainer = el("div", {});
  const initialControls = buildRadioOptions(behavior, optionContainer, behavior.options());
  fieldset.appendChild(optionContainer);
  const error = createUSWDSError(behavior.id);
  fieldset.appendChild(error);
  parent.appendChild(fieldset);
  const dispose = behavior.bind({
    root: fieldset,
    label: legend,
    control: fieldset,
    hint,
    error,
    optionControls: initialControls,
    rebuildOptions: (_container, newOptions) => buildRadioOptions(behavior, optionContainer, newOptions),
    onValidationChange: (hasError) => {
      fieldset.classList.toggle("usa-fieldset--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/checkbox-group.js
function buildCheckboxOptions(behavior, container, options) {
  container.innerHTML = "";
  const controls = /* @__PURE__ */ new Map();
  for (let i2 = 0; i2 < options.length; i2++) {
    const opt = options[i2];
    const optId = `${behavior.id}-${i2}`;
    const wrapper = el("div", { class: "usa-checkbox" });
    const input = document.createElement("input");
    input.className = "usa-checkbox__input";
    input.id = optId;
    input.type = "checkbox";
    input.name = behavior.fieldPath;
    input.value = opt.value;
    controls.set(opt.value, input);
    const label = el("label", { class: "usa-checkbox__label", for: optId });
    label.textContent = opt.label;
    wrapper.appendChild(input);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
  }
  return controls;
}
var renderCheckboxGroup2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const fieldset = el("fieldset", { class: "usa-fieldset" });
  applyCascadeClasses(fieldset, p2);
  applyCascadeAccessibility(fieldset, p2);
  const legendClasses = p2.labelPosition === "hidden" ? "usa-legend usa-sr-only" : "usa-legend";
  const legend = el("legend", { class: legendClasses });
  legend.textContent = behavior.label;
  fieldset.appendChild(legend);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("span", { class: "usa-hint", id: hintId });
    hint.textContent = behavior.hint;
    fieldset.appendChild(hint);
  }
  if (behavior.selectAll && behavior.options().length > 0) {
    const selectAllWrapper = el("div", { class: "usa-checkbox" });
    const selectAllId = `${behavior.id}-select-all`;
    const selectAllCb = document.createElement("input");
    selectAllCb.className = "usa-checkbox__input";
    selectAllCb.id = selectAllId;
    selectAllCb.type = "checkbox";
    selectAllCb.addEventListener("change", () => {
      const checked = [];
      for (const [optVal, cb] of optionControlsRef) {
        cb.checked = selectAllCb.checked;
        if (cb.checked)
          checked.push(optVal);
      }
      behavior.setValue(checked);
    });
    const selectAllLabel = el("label", { class: "usa-checkbox__label", for: selectAllId });
    selectAllLabel.textContent = "Select All";
    selectAllWrapper.appendChild(selectAllCb);
    selectAllWrapper.appendChild(selectAllLabel);
    fieldset.appendChild(selectAllWrapper);
  }
  const optionContainer = el("div", {});
  let optionControlsRef = buildCheckboxOptions(behavior, optionContainer, behavior.options());
  fieldset.appendChild(optionContainer);
  const error = createUSWDSError(behavior.id);
  fieldset.appendChild(error);
  parent.appendChild(fieldset);
  const dispose = behavior.bind({
    root: fieldset,
    label: legend,
    control: fieldset,
    hint,
    error,
    optionControls: optionControlsRef,
    rebuildOptions: (_container, newOptions) => {
      optionControlsRef = buildCheckboxOptions(behavior, optionContainer, newOptions);
      return optionControlsRef;
    },
    onValidationChange: (hasError) => {
      fieldset.classList.toggle("usa-fieldset--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/select.js
var renderSelect2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const select = document.createElement("select");
  select.className = "usa-select";
  select.id = behavior.id;
  select.name = behavior.fieldPath;
  const placeholderOpt = document.createElement("option");
  placeholderOpt.value = "";
  placeholderOpt.textContent = behavior.placeholder || "- Select -";
  if (!behavior.clearable)
    placeholderOpt.disabled = true;
  placeholderOpt.selected = true;
  select.appendChild(placeholderOpt);
  for (const opt of behavior.options()) {
    const option = document.createElement("option");
    option.value = opt.value;
    option.textContent = opt.label;
    select.appendChild(option);
  }
  select.setAttribute("aria-describedby", describedBy);
  root.appendChild(select);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: select,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      select.classList.toggle("usa-select--error", hasError);
    },
    rebuildOptions: (_container, newOptions) => {
      while (select.options.length > 1)
        select.remove(select.options.length - 1);
      const controls = /* @__PURE__ */ new Map();
      for (const opt of newOptions) {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label;
        select.appendChild(option);
      }
      return controls;
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/date-picker.js
var renderDatePicker2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const input = document.createElement("input");
  input.className = "usa-input";
  input.type = behavior.inputType;
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  if (behavior.minDate)
    input.min = behavior.minDate;
  if (behavior.maxDate)
    input.max = behavior.maxDate;
  input.setAttribute("aria-describedby", describedBy);
  root.appendChild(input);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      input.classList.toggle("usa-input--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/checkbox.js
var renderCheckbox2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const root = el("div", { class: "usa-form-group", "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const wrapper = el("div", { class: "usa-checkbox" });
  const input = document.createElement("input");
  input.className = "usa-checkbox__input";
  input.id = behavior.id;
  input.type = "checkbox";
  input.name = behavior.fieldPath;
  const describedBy = [
    behavior.hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  input.setAttribute("aria-describedby", describedBy);
  const label = el("label", { class: "usa-checkbox__label", for: behavior.id });
  label.textContent = behavior.label;
  if (p2.labelPosition === "hidden")
    label.classList.add("usa-sr-only");
  wrapper.appendChild(input);
  wrapper.appendChild(label);
  root.appendChild(wrapper);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("span", { class: "usa-hint", id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createUSWDSError(behavior.id);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/toggle.js
var renderToggle2 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const root = el("div", { class: "usa-form-group", "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const wrapper = el("div", { class: "usa-checkbox" });
  const input = document.createElement("input");
  input.className = "usa-checkbox__input";
  input.id = behavior.id;
  input.type = "checkbox";
  input.name = behavior.fieldPath;
  const describedBy = [
    behavior.hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  input.setAttribute("aria-describedby", describedBy);
  const labelText = behavior.label + (behavior.offLabel ? ` (${behavior.offLabel})` : "");
  const label = el("label", { class: "usa-checkbox__label", for: behavior.id });
  label.textContent = labelText;
  if (p2.labelPosition === "hidden")
    label.classList.add("usa-sr-only");
  wrapper.appendChild(input);
  wrapper.appendChild(label);
  root.appendChild(wrapper);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("span", { class: "usa-hint", id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createUSWDSError(behavior.id);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/money-input.js
var renderMoneyInput2 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior);
  const container = el("div", { class: "usa-input-group" });
  if (behavior.resolvedCurrency) {
    const prefix = el("div", { class: "usa-input-prefix", "aria-hidden": "true" });
    prefix.textContent = behavior.resolvedCurrency;
    container.appendChild(prefix);
  }
  const amountInput = document.createElement("input");
  amountInput.className = "usa-input";
  amountInput.id = behavior.id;
  amountInput.name = `${behavior.fieldPath}__amount`;
  amountInput.type = "number";
  if (behavior.placeholder)
    amountInput.placeholder = behavior.placeholder;
  if (behavior.step != null)
    amountInput.step = String(behavior.step);
  if (behavior.min != null)
    amountInput.min = String(behavior.min);
  if (behavior.max != null)
    amountInput.max = String(behavior.max);
  amountInput.setAttribute("aria-describedby", describedBy);
  container.appendChild(amountInput);
  if (!behavior.resolvedCurrency) {
    const currencyInput = document.createElement("input");
    currencyInput.className = "usa-input formspec-money-currency-input";
    currencyInput.type = "text";
    currencyInput.placeholder = "Currency";
    currencyInput.name = `${behavior.fieldPath}__currency`;
    currencyInput.setAttribute("aria-label", "Currency code");
    container.appendChild(currencyInput);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      amountInput.classList.toggle("usa-input--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/slider.js
var renderSlider2 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy: _describedBy } = createUSWDSFieldDOM(behavior);
  const container = el("div", {});
  const input = document.createElement("input");
  input.className = "usa-range";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  input.type = "range";
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.showTicks && behavior.min != null && behavior.max != null && behavior.step != null) {
    const tickCount = Math.floor((behavior.max - behavior.min) / behavior.step) + 1;
    if (tickCount > 0 && tickCount <= 200) {
      const listId = `usa-ticks-${behavior.fieldPath.replace(/\./g, "-")}`;
      const datalist = document.createElement("datalist");
      datalist.id = listId;
      for (let v2 = behavior.min; v2 <= behavior.max; v2 += behavior.step) {
        const opt = document.createElement("option");
        opt.value = String(v2);
        datalist.appendChild(opt);
      }
      container.appendChild(datalist);
      input.setAttribute("list", listId);
    }
  }
  container.appendChild(input);
  if (behavior.showValue) {
    const valueDisplay = el("span", { class: "formspec-slider-value" });
    container.appendChild(valueDisplay);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
      input.classList.toggle("usa-range--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/rating.js
var renderRating2 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior, { labelFor: false });
  const container = el("div", { class: "formspec-rating-stars", role: "slider" });
  container.setAttribute("tabindex", "0");
  container.setAttribute("aria-valuemin", "0");
  container.setAttribute("aria-valuemax", String(behavior.maxRating));
  container.setAttribute("aria-valuenow", "0");
  container.setAttribute("aria-valuetext", `0 of ${behavior.maxRating}`);
  container.setAttribute("aria-label", behavior.label);
  container.setAttribute("aria-describedby", describedBy);
  const step = behavior.allowHalf ? 0.5 : 1;
  let currentValue = 0;
  const updateValue = (value) => {
    currentValue = Math.max(0, Math.min(value, behavior.maxRating));
    container.setAttribute("aria-valuenow", String(currentValue));
    container.setAttribute("aria-valuetext", `${currentValue} of ${behavior.maxRating}`);
    behavior.setValue(currentValue);
  };
  container.addEventListener("keydown", (e2) => {
    switch (e2.key) {
      case "ArrowRight":
      case "ArrowUp":
        e2.preventDefault();
        updateValue(currentValue + step);
        break;
      case "ArrowLeft":
      case "ArrowDown":
        e2.preventDefault();
        updateValue(currentValue - step);
        break;
      case "Home":
        e2.preventDefault();
        updateValue(0);
        break;
      case "End":
        e2.preventDefault();
        updateValue(behavior.maxRating);
        break;
    }
  });
  for (let i2 = 1; i2 <= behavior.maxRating; i2++) {
    const star = document.createElement("span");
    star.className = "formspec-rating-star";
    star.textContent = behavior.icon;
    star.dataset.value = String(i2);
    star.addEventListener("click", (event) => {
      let value = i2;
      if (behavior.allowHalf) {
        const rect = star.getBoundingClientRect();
        const clickedLeftHalf = rect.width > 0 && event.clientX - rect.left < rect.width / 2;
        value = clickedLeftHalf ? i2 - 0.5 : i2;
      }
      updateValue(value);
    });
    container.appendChild(star);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/file-upload.js
var renderFileUpload2 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy: _describedBy } = createUSWDSFieldDOM(behavior);
  const fileInput = el("div", { class: "usa-file-input" });
  const target = el("div", {
    class: "usa-file-input__target",
    tabindex: "0",
    role: "button",
    "aria-label": "Drop files here or press Enter to browse"
  });
  target.addEventListener("keydown", (e2) => {
    if (e2.key === "Enter" || e2.key === " ") {
      e2.preventDefault();
      input.click();
    }
  });
  const instructions = el("div", { class: "usa-file-input__instructions" });
  const chooseSpan = el("span", { class: "usa-file-input__choose" });
  chooseSpan.textContent = "choose from folder";
  instructions.appendChild(document.createTextNode("Drag file here or "));
  instructions.appendChild(chooseSpan);
  target.appendChild(instructions);
  const input = document.createElement("input");
  input.className = "usa-file-input__input";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  input.type = "file";
  if (behavior.accept)
    input.accept = behavior.accept;
  if (behavior.multiple)
    input.multiple = true;
  target.appendChild(input);
  if (behavior.dragDrop) {
    target.addEventListener("dragover", (e2) => {
      e2.preventDefault();
      target.classList.add("usa-file-input__target--drag");
    });
    target.addEventListener("dragleave", () => {
      target.classList.remove("usa-file-input__target--drag");
    });
    target.addEventListener("drop", (e2) => {
      e2.preventDefault();
      target.classList.remove("usa-file-input__target--drag");
      const files = Array.from(e2.dataTransfer?.files || []);
      const fileData = files.map((f2) => ({ name: f2.name, size: f2.size, type: f2.type }));
      root.dispatchEvent(new CustomEvent("formspec-files-dropped", {
        detail: { fileData, multiple: behavior.multiple },
        bubbles: false
      }));
    });
  }
  fileInput.appendChild(target);
  root.appendChild(fileInput);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/signature.js
var renderSignature2 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createUSWDSFieldDOM(behavior, { labelFor: false });
  const { canvas, clear, dispose: canvasDispose } = createSignatureCanvas({
    height: behavior.height,
    strokeColor: behavior.strokeColor,
    eventTarget: root
  });
  canvas.style.width = "100%";
  canvas.style.border = "1px solid";
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-label", "Signature canvas. Use the Clear button to reset.");
  canvas.setAttribute("aria-describedby", describedBy);
  root.appendChild(canvas);
  actx.onDispose(canvasDispose);
  const clearBtn = document.createElement("button");
  clearBtn.type = "button";
  clearBtn.className = "usa-button usa-button--outline";
  clearBtn.textContent = "Clear";
  clearBtn.addEventListener("click", clear);
  root.appendChild(clearBtn);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: canvas,
    hint,
    error,
    onValidationChange: (hasError) => {
      root.classList.toggle("usa-form-group--error", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/uswds/wizard.js
var renderWizard2 = (behavior, parent, actx) => {
  const root = document.createElement("div");
  if (behavior.id)
    root.id = behavior.id;
  root.className = "formspec-wizard";
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(root, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(root, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(root, behavior.compOverrides.style);
  parent.appendChild(root);
  if (behavior.totalSteps() === 0)
    return;
  let stepIndicator;
  let segmentsList;
  let currentStepSpan;
  let totalStepsSpan;
  let headingText;
  if (behavior.showProgress) {
    stepIndicator = document.createElement("div");
    stepIndicator.className = "usa-step-indicator";
    stepIndicator.setAttribute("aria-label", "progress");
    segmentsList = document.createElement("ol");
    segmentsList.className = "usa-step-indicator__segments";
    stepIndicator.appendChild(segmentsList);
    const header = document.createElement("div");
    header.className = "usa-step-indicator__header";
    const heading = document.createElement("h4");
    heading.className = "usa-step-indicator__heading";
    const counter = document.createElement("span");
    counter.className = "usa-step-indicator__heading-counter";
    const srStep = document.createElement("span");
    srStep.className = "usa-sr-only";
    srStep.textContent = "Step";
    counter.appendChild(srStep);
    currentStepSpan = document.createElement("span");
    currentStepSpan.className = "usa-step-indicator__current-step";
    counter.appendChild(currentStepSpan);
    totalStepsSpan = document.createElement("span");
    totalStepsSpan.className = "usa-step-indicator__total-steps";
    counter.appendChild(totalStepsSpan);
    heading.appendChild(counter);
    headingText = document.createElement("span");
    headingText.className = "usa-step-indicator__heading-text";
    heading.appendChild(headingText);
    header.appendChild(heading);
    stepIndicator.appendChild(header);
    root.appendChild(stepIndicator);
  }
  const panels = [];
  for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-wizard-panel";
    panel.setAttribute("role", "region");
    panel.setAttribute("aria-label", behavior.steps[i2]?.title || `Step ${i2 + 1}`);
    if (i2 !== 0)
      panel.classList.add("formspec-hidden");
    behavior.renderStep(i2, panel);
    root.appendChild(panel);
    panels.push(panel);
  }
  const nav = document.createElement("div");
  nav.className = "formspec-wizard-nav";
  const prevBtn = document.createElement("button");
  prevBtn.type = "button";
  prevBtn.className = "usa-button usa-button--outline";
  prevBtn.textContent = "Previous";
  nav.appendChild(prevBtn);
  if (behavior.allowSkip) {
    const skipBtn = document.createElement("button");
    skipBtn.type = "button";
    skipBtn.className = "usa-button usa-button--unstyled";
    skipBtn.textContent = "Skip";
    skipBtn.addEventListener("click", () => {
      if (behavior.canGoNext())
        behavior.goToStep(behavior.activeStep() + 1);
    });
    nav.appendChild(skipBtn);
  }
  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.className = "usa-button";
  nextBtn.textContent = "Next";
  nav.appendChild(nextBtn);
  root.appendChild(nav);
  if (segmentsList) {
    for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
      const segment = document.createElement("li");
      segment.className = "usa-step-indicator__segment";
      const segLabel = document.createElement("span");
      segLabel.className = "usa-step-indicator__segment-label";
      segLabel.textContent = behavior.steps[i2]?.title || `Step ${i2 + 1}`;
      segment.appendChild(segLabel);
      segmentsList.appendChild(segment);
    }
    if (currentStepSpan)
      currentStepSpan.textContent = "1";
    if (totalStepsSpan)
      totalStepsSpan.textContent = ` of ${behavior.totalSteps()}`;
    if (headingText)
      headingText.textContent = behavior.steps[0]?.title || "Step 1";
  }
  const stepIndicators = segmentsList ? Array.from(segmentsList.children) : void 0;
  const dispose = behavior.bind({
    root,
    panels,
    stepIndicators,
    stepContent: root,
    prevButton: prevBtn,
    nextButton: nextBtn
  });
  actx.onDispose(dispose);
  if (segmentsList && stepIndicators) {
    const updateIndicator = () => {
      const activeIdx = panels.findIndex((p2) => !p2.classList.contains("formspec-hidden"));
      if (activeIdx < 0)
        return;
      for (let i2 = 0; i2 < stepIndicators.length; i2++) {
        const seg = stepIndicators[i2];
        seg.classList.remove("usa-step-indicator__segment--current", "usa-step-indicator__segment--complete");
        if (i2 === activeIdx) {
          seg.classList.add("usa-step-indicator__segment--current");
        } else if (i2 < activeIdx) {
          seg.classList.add("usa-step-indicator__segment--complete");
          const label = seg.querySelector(".usa-step-indicator__segment-label");
          if (label && !label.querySelector(".usa-sr-only")) {
            const sr = document.createElement("span");
            sr.className = "usa-sr-only";
            sr.textContent = "completed";
            label.appendChild(sr);
          }
        } else {
          const sr = seg.querySelector(".usa-sr-only");
          if (sr)
            sr.remove();
        }
      }
      if (currentStepSpan)
        currentStepSpan.textContent = String(activeIdx + 1);
      if (headingText) {
        headingText.textContent = behavior.steps[activeIdx]?.title || `Step ${activeIdx + 1}`;
      }
    };
    const observer = new MutationObserver(updateIndicator);
    for (const panel of panels) {
      observer.observe(panel, { attributes: true, attributeFilter: ["style", "class"] });
    }
    actx.onDispose(() => observer.disconnect());
    updateIndicator();
  }
};

// node_modules/@formspec-org/adapters/dist/uswds/tabs.js
var renderTabs2 = (behavior, parent, actx) => {
  const root = document.createElement("div");
  if (behavior.id)
    root.id = behavior.id;
  root.className = "formspec-tabs";
  if (behavior.position !== "top")
    root.dataset.position = behavior.position;
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(root, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(root, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(root, behavior.compOverrides.style);
  parent.appendChild(root);
  const count = behavior.tabCount;
  const idBase = behavior.id || "tabs";
  const tabBar = document.createElement("ul");
  tabBar.className = "usa-button-group usa-button-group--segmented";
  tabBar.setAttribute("role", "tablist");
  const panelContainer = document.createElement("div");
  panelContainer.className = "formspec-tab-panels";
  const panels = [];
  for (let i2 = 0; i2 < count; i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-tab-panel";
    panel.setAttribute("role", "tabpanel");
    panel.id = `${idBase}-panel-${i2}`;
    panel.setAttribute("aria-labelledby", `${idBase}-tab-${i2}`);
    panel.setAttribute("tabindex", "0");
    if (i2 !== behavior.defaultTab)
      panel.style.display = "none";
    behavior.renderTab(i2, panel);
    panelContainer.appendChild(panel);
    panels.push(panel);
  }
  const buttons = [];
  for (let i2 = 0; i2 < count; i2++) {
    const li = document.createElement("li");
    li.className = "usa-button-group__item";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.setAttribute("role", "tab");
    btn.id = `${idBase}-tab-${i2}`;
    btn.setAttribute("aria-controls", `${idBase}-panel-${i2}`);
    btn.setAttribute("aria-selected", i2 === behavior.defaultTab ? "true" : "false");
    btn.setAttribute("tabindex", i2 === behavior.defaultTab ? "0" : "-1");
    btn.textContent = behavior.tabLabels[i2] || `Tab ${i2 + 1}`;
    btn.className = i2 === behavior.defaultTab ? "usa-button" : "usa-button usa-button--outline";
    li.appendChild(btn);
    tabBar.appendChild(li);
    buttons.push(btn);
  }
  if (behavior.position === "bottom") {
    root.appendChild(panelContainer);
    root.appendChild(tabBar);
  } else {
    root.appendChild(tabBar);
    root.appendChild(panelContainer);
  }
  const dispose = behavior.bind({ root, tabBar, panels, buttons });
  actx.onDispose(dispose);
  const updateButtonStyles = () => {
    for (let i2 = 0; i2 < buttons.length; i2++) {
      const isActive = buttons[i2].getAttribute("aria-selected") === "true";
      buttons[i2].className = isActive ? "usa-button" : "usa-button usa-button--outline";
    }
  };
  const observer = new MutationObserver(updateButtonStyles);
  for (const btn of buttons) {
    observer.observe(btn, { attributes: true, attributeFilter: ["aria-selected"] });
  }
  actx.onDispose(() => observer.disconnect());
};

// node_modules/@formspec-org/adapters/dist/uswds/integration-css.js
var integrationCSS = '.usa-hint,.usa-range__value,.usa-range,.usa-radio__label,.usa-checkbox__label,.usa-fieldset,.usa-select,.usa-textarea,.usa-input{font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1rem;line-height:1.4}.usa-range,.usa-select,.usa-textarea,.usa-input{border-width:1px;border-color:#565c65;border-style:solid;appearance:none;border-radius:0;color:#1b1b1b;display:block;height:2.5rem;margin-top:.5rem;max-width:none;padding:.5rem;width:100%}.usa-form-group{margin-top:1.5rem}.usa-form-group .usa-label:first-child{margin-top:0}.usa-form-group--error{border-left-width:0.25rem;border-left-color:#b50909;border-left-style:solid;padding-left:1rem;position:relative}@media all and (min-width: 64em){.usa-form-group--error{margin-left:-1.25rem}}.usa-label{font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1rem;line-height:1.4;display:block;font-weight:normal;margin-top:1.5rem;max-width:none}.usa-label--error{font-weight:700;margin-top:0}.usa-label--required{color:#b50909}.usa-input:disabled,.usa-input[aria-disabled=true]{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-input:disabled:hover,.usa-input:disabled:active,.usa-input:disabled:focus,.usa-input:disabled.usa-focus,.usa-input[aria-disabled=true]:hover,.usa-input[aria-disabled=true]:active,.usa-input[aria-disabled=true]:focus,.usa-input[aria-disabled=true].usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-input:disabled,.usa-input[aria-disabled=true]{border:0;color:GrayText}.usa-input:disabled:hover,.usa-input:disabled:active,.usa-input:disabled:focus,.usa-input:disabled.usa-focus,.usa-input[aria-disabled=true]:hover,.usa-input[aria-disabled=true]:active,.usa-input[aria-disabled=true]:focus,.usa-input[aria-disabled=true].usa-focus{color:GrayText}}@media(forced-colors: active){.usa-input:disabled,.usa-input[aria-disabled=true]{border:2px solid GrayText}}.usa-input:disabled,.usa-input[aria-disabled=true]{-webkit-text-fill-color:#454545}.usa-input--2xs,.usa-form .usa-input--2xs{max-width:5ex}.usa-input--xs,.usa-form .usa-input--xs{max-width:9ex}.usa-input--sm,.usa-form .usa-input--sm{max-width:13ex}.usa-input--small,.usa-form .usa-input--small{max-width:13ex}.usa-input--md,.usa-form .usa-input--md{max-width:20ex}.usa-input--medium,.usa-form .usa-input--medium{max-width:20ex}.usa-input--lg,.usa-form .usa-input--lg{max-width:30ex}.usa-input--xl,.usa-form .usa-input--xl{max-width:40ex}.usa-input--2xl,.usa-form .usa-input--2xl{max-width:50ex}.usa-input--error{border-width:0.25rem;border-color:#b50909;border-style:solid;padding-top:calc(0.5rem - 0.25rem);padding-bottom:calc(0.5rem - 0.25rem)}.usa-input--success{border-width:0.25rem;border-color:#00a91c;border-style:solid;padding-top:calc(0.5rem - 0.25rem);padding-bottom:calc(0.5rem - 0.25rem)}.usa-textarea:disabled,.usa-textarea[aria-disabled=true]{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-textarea:disabled:hover,.usa-textarea:disabled:active,.usa-textarea:disabled:focus,.usa-textarea:disabled.usa-focus,.usa-textarea[aria-disabled=true]:hover,.usa-textarea[aria-disabled=true]:active,.usa-textarea[aria-disabled=true]:focus,.usa-textarea[aria-disabled=true].usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-textarea:disabled,.usa-textarea[aria-disabled=true]{border:0;color:GrayText}.usa-textarea:disabled:hover,.usa-textarea:disabled:active,.usa-textarea:disabled:focus,.usa-textarea:disabled.usa-focus,.usa-textarea[aria-disabled=true]:hover,.usa-textarea[aria-disabled=true]:active,.usa-textarea[aria-disabled=true]:focus,.usa-textarea[aria-disabled=true].usa-focus{color:GrayText}}@media(forced-colors: active){.usa-textarea:disabled,.usa-textarea[aria-disabled=true]{border:2px solid GrayText}}.usa-textarea{height:10rem}.usa-icon{display:inline-block;fill:currentColor;height:1em;position:relative;width:1em}.usa-icon--size-3{height:1.5rem;width:1.5rem}.usa-icon--size-4{height:2rem;width:2rem}.usa-icon--size-5{height:2.5rem;width:2.5rem}.usa-icon--size-6{height:3rem;width:3rem}.usa-icon--size-7{height:3.5rem;width:3.5rem}.usa-icon--size-8{height:4rem;width:4rem}.usa-icon--size-9{height:4.5rem;width:4.5rem}.usa-select{background-image:url("../img/usa-icons/unfold_more.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat;appearance:none;background-color:#fff;background-position:right .5rem center;background-size:1.25rem;padding-right:2rem}.usa-select::-ms-expand{display:none}.usa-select:-webkit-autofill{appearance:menulist}.usa-select:-moz-focusring{color:rgba(0,0,0,0);text-shadow:0 0 0 #000}.usa-select[multiple]{height:auto;background-image:none;padding-right:0}.usa-select option{overflow:hidden;text-overflow:ellipsis}.usa-select:disabled,.usa-select[aria-disabled=true]{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-select:disabled:hover,.usa-select:disabled:active,.usa-select:disabled:focus,.usa-select:disabled.usa-focus,.usa-select[aria-disabled=true]:hover,.usa-select[aria-disabled=true]:active,.usa-select[aria-disabled=true]:focus,.usa-select[aria-disabled=true].usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-select:disabled,.usa-select[aria-disabled=true]{border:0;color:GrayText}.usa-select:disabled:hover,.usa-select:disabled:active,.usa-select:disabled:focus,.usa-select:disabled.usa-focus,.usa-select[aria-disabled=true]:hover,.usa-select[aria-disabled=true]:active,.usa-select[aria-disabled=true]:focus,.usa-select[aria-disabled=true].usa-focus{color:GrayText}}@media(forced-colors: active){.usa-select:disabled,.usa-select[aria-disabled=true]{border:2px solid GrayText}}@media(forced-colors: active){.usa-select{appearance:listbox;background-image:none;padding-right:0}}.usa-fieldset{border:none;margin:0;padding:0}.usa-legend{font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1rem;line-height:1.4;display:block;font-weight:normal;margin-top:1.5rem;max-width:none}.usa-legend--large{font-size:2rem;font-weight:700;margin-top:1rem}.usa-input-list{margin-bottom:0;margin-top:0;list-style-type:none;padding-left:0}.usa-input-list li{line-height:1.4}.usa-prose .usa-input-list{margin-bottom:0;margin-top:0;list-style-type:none;padding-left:0}.usa-prose .usa-input-list li{line-height:1.4}.usa-checkbox{background:#fff}.usa-checkbox__label{color:#1b1b1b}.usa-checkbox__label::before{background:#fff;box-shadow:0 0 0 2px #1b1b1b}@media(forced-colors: active){.usa-checkbox__label::before{outline:2px solid rgba(0,0,0,0);outline-offset:2px}}.usa-checkbox__input:checked+[class*=__label]::before{background-color:#005ea2;box-shadow:0 0 0 2px #005ea2}.usa-checkbox__input:disabled+[class*=__label],.usa-checkbox__input[aria-disabled=true]+[class*=__label]{color:#757575;cursor:not-allowed}@media(forced-colors: active){.usa-checkbox__input:disabled+[class*=__label],.usa-checkbox__input[aria-disabled=true]+[class*=__label]{color:GrayText}}.usa-checkbox__input:disabled+[class*=__label]::before,.usa-checkbox__input[aria-disabled=true]+[class*=__label]::before{background-color:#fff;box-shadow:0 0 0 2px #757575}.usa-checkbox__input--tile+[class*=__label]{background-color:#fff;border:2px solid #c9c9c9;color:#1b1b1b}.usa-checkbox__input--tile:checked+[class*=__label]{background-color:rgba(0,94,162,.1);border-color:#005ea2}@media(forced-colors: active){.usa-checkbox__input--tile:checked+[class*=__label]{border:ButtonText solid .25rem}}.usa-checkbox__input--tile:disabled+[class*=__label],.usa-checkbox__input--tile[aria-disabled=true]+[class*=__label]{border-color:#e6e6e6}.usa-checkbox__input--tile:disabled:checked+[class*=__label],.usa-checkbox__input--tile:disabled:indeterminate+[class*=__label],.usa-checkbox__input--tile:disabled[data-indeterminate]+[class*=__label],.usa-checkbox__input--tile[aria-disabled=true]:checked+[class*=__label],.usa-checkbox__input--tile[aria-disabled=true]:indeterminate+[class*=__label],.usa-checkbox__input--tile[aria-disabled=true][data-indeterminate]+[class*=__label]{background-color:#fff}.usa-checkbox__input:indeterminate+[class*=__label]::before,.usa-checkbox__input[data-indeterminate]+[class*=__label]::before{background-image:url("../img/checkbox-indeterminate.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat;background-color:#005ea2;box-shadow:0 0 0 2px #005ea2;background-position:center center;background-size:.75rem auto}@media(forced-colors: active){.usa-checkbox__input:indeterminate+[class*=__label]::before,.usa-checkbox__input[data-indeterminate]+[class*=__label]::before{background-image:url("../img/checkbox-indeterminate-alt.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat;background-color:SelectedItem}}.usa-checkbox__input:indeterminate:disabled+[class*=__label]::before,.usa-checkbox__input:indeterminate[aria-disabled=true]+[class*=__label]::before,.usa-checkbox__input[data-indeterminate]:disabled+[class*=__label]::before,.usa-checkbox__input[data-indeterminate][aria-disabled=true]+[class*=__label]::before{box-shadow:0 0 0 2px #757575}.usa-checkbox__input:indeterminate:disabled+[class*=__label],.usa-checkbox__input:indeterminate[aria-disabled=true]+[class*=__label],.usa-checkbox__input[data-indeterminate]:disabled+[class*=__label],.usa-checkbox__input[data-indeterminate][aria-disabled=true]+[class*=__label]{border-color:#e6e6e6}.usa-checkbox__input--tile:indeterminate+[class*=__label],.usa-checkbox__input--tile[data-indeterminate]+[class*=__label]{background-color:rgba(0,94,162,.1);border-color:#005ea2}@media(forced-colors: active){.usa-checkbox__input--tile:indeterminate+[class*=__label],.usa-checkbox__input--tile[data-indeterminate]+[class*=__label]{border:ButtonText solid .25rem}}.usa-checkbox__input:checked+[class*=__label]::before,.usa-checkbox__input:checked:disabled+[class*=__label]::before,.usa-checkbox__input:checked[aria-disabled=true]+[class*=__label]::before{background-image:url("../img/correct8.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-checkbox__input:checked+[class*=__label]::before,.usa-checkbox__input:checked:disabled+[class*=__label]::before,.usa-checkbox__input:checked[aria-disabled=true]+[class*=__label]::before{background-image:url("../img/correct8-alt.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}}.usa-checkbox__input:checked:disabled+[class*=__label]::before,.usa-checkbox__input:checked[aria-disabled=true]+[class*=__label]::before,.usa-checkbox__input:indeterminate:disabled+[class*=__label]::before,.usa-checkbox__input:indeterminate[aria-disabled=true]+[class*=__label]::before,.usa-checkbox__input[data-indeterminate]:disabled+[class*=__label]::before,.usa-checkbox__input[data-indeterminate][aria-disabled=true]+[class*=__label]::before{background-color:#757575}@media(forced-colors: active){.usa-checkbox__input:checked:disabled+[class*=__label]::before,.usa-checkbox__input:checked[aria-disabled=true]+[class*=__label]::before,.usa-checkbox__input:indeterminate:disabled+[class*=__label]::before,.usa-checkbox__input:indeterminate[aria-disabled=true]+[class*=__label]::before,.usa-checkbox__input[data-indeterminate]:disabled+[class*=__label]::before,.usa-checkbox__input[data-indeterminate][aria-disabled=true]+[class*=__label]::before{background-color:GrayText}}.usa-checkbox__input{position:absolute;left:-999em;right:auto}.usa-checkbox__input:focus+[class*=__label]::before{outline:.25rem solid #2491ff;outline-offset:.25rem}.usa-checkbox__input--tile+[class*=__label]{border-radius:.25rem;margin-top:.5rem;padding:.75rem 1rem .75rem 2.5rem;display:inherit}.usa-checkbox__input--tile+[class*=__label]::before{left:.5rem}.usa-checkbox__input:checked+[class*=__label]::before{background-position:center center;background-size:.75rem auto}@media print{.usa-checkbox__input:checked+[class*=__label]::before{background-image:none;background-color:#fff;content:"\u2714";text-align:center}}@media(forced-colors: active){.usa-checkbox__input:checked+[class*=__label]::before{background-color:SelectedItem}}.usa-checkbox__label{cursor:pointer;display:inline-block;font-weight:normal;margin-top:.75rem;padding-left:2rem;position:relative}.usa-checkbox__label::before{content:" ";display:block;left:0;margin-left:2px;margin-top:.075rem;position:absolute}.usa-checkbox__label::before{height:1.25rem;width:1.25rem;border-radius:2px}.usa-checkbox__label-description{display:block;font-size:.88rem;margin-top:.5rem}.usa-radio{background:#fff}.usa-radio__label{color:#1b1b1b}.usa-radio__label::before{background:#fff;box-shadow:0 0 0 2px #1b1b1b}@media(forced-colors: active){.usa-radio__label::before{outline:2px solid rgba(0,0,0,0);outline-offset:2px}}.usa-radio__input:checked+[class*=__label]::before{background-color:#005ea2;box-shadow:0 0 0 2px #005ea2}.usa-radio__input:disabled+[class*=__label],.usa-radio__input[aria-disabled=true]+[class*=__label]{color:#757575;cursor:not-allowed}@media(forced-colors: active){.usa-radio__input:disabled+[class*=__label],.usa-radio__input[aria-disabled=true]+[class*=__label]{color:GrayText}}.usa-radio__input:disabled+[class*=__label]::before,.usa-radio__input[aria-disabled=true]+[class*=__label]::before{background-color:#fff;box-shadow:0 0 0 2px #757575}.usa-radio__input--tile+[class*=__label]{background-color:#fff;border:2px solid #c9c9c9;color:#1b1b1b}.usa-radio__input--tile:checked+[class*=__label]{background-color:rgba(0,94,162,.1);border-color:#005ea2}@media(forced-colors: active){.usa-radio__input--tile:checked+[class*=__label]{border:ButtonText solid .25rem}}.usa-radio__input--tile:disabled+[class*=__label],.usa-radio__input--tile[aria-disabled=true]+[class*=__label]{border-color:#e6e6e6}.usa-radio__input--tile:disabled:checked+[class*=__label],.usa-radio__input--tile:disabled:indeterminate+[class*=__label],.usa-radio__input--tile:disabled[data-indeterminate]+[class*=__label],.usa-radio__input--tile[aria-disabled=true]:checked+[class*=__label],.usa-radio__input--tile[aria-disabled=true]:indeterminate+[class*=__label],.usa-radio__input--tile[aria-disabled=true][data-indeterminate]+[class*=__label]{background-color:#fff}.usa-radio__input:checked+[class*=__label]::before{box-shadow:0 0 0 2px #005ea2,inset 0 0 0 2px #fff}@media(forced-colors: active){.usa-radio__input:checked+[class*=__label]::before{background-color:ButtonText}}.usa-radio__input:checked:disabled+[class*=__label]::before,.usa-radio__input:checked[aria-disabled=true]+[class*=__label]::before{background-color:#757575;box-shadow:0 0 0 2px #757575,inset 0 0 0 2px #fff}@media(forced-colors: active){.usa-radio__input:checked:disabled+[class*=__label]::before,.usa-radio__input:checked[aria-disabled=true]+[class*=__label]::before{background-color:GrayText}}.usa-radio__input{position:absolute;left:-999em;right:auto}.usa-radio__input:focus+[class*=__label]::before{outline:.25rem solid #2491ff;outline-offset:.25rem}.usa-radio__input--tile+[class*=__label]{border-radius:.25rem;margin-top:.5rem;padding:.75rem 1rem .75rem 2.5rem;display:inherit}.usa-radio__input--tile+[class*=__label]::before{left:.5rem}@media print{.usa-radio__input:checked+[class*=__label]::before{box-shadow:inset 0 0 0 2px #fff,inset 0 0 0 1rem #005ea2,0 0 0 2px #005ea2}}.usa-radio__label{cursor:pointer;display:inline-block;font-weight:normal;margin-top:.75rem;padding-left:2rem;position:relative}.usa-radio__label::before{content:" ";display:block;left:0;margin-left:2px;margin-top:.075rem;position:absolute}.usa-radio__label::before{height:1.25rem;border-radius:99rem;width:1.25rem}.usa-radio__label-description{display:block;font-size:.88rem;margin-top:.5rem}.usa-date-picker__wrapper{display:none;position:relative;max-width:none}.usa-date-picker__wrapper:focus{outline:0}.usa-date-picker__external-input[aria-disabled=true]+.usa-date-picker__button,.usa-date-picker__calendar__year:disabled,.usa-date-picker__calendar__previous-year-chunk:disabled,.usa-date-picker__calendar__next-year-chunk:disabled,.usa-date-picker__calendar__month:disabled,.usa-date-picker__calendar__year-selection:disabled,.usa-date-picker__calendar__month-selection:disabled,.usa-date-picker__calendar__date:disabled,.usa-date-picker__calendar__previous-year:disabled,.usa-date-picker__calendar__previous-month:disabled,.usa-date-picker__calendar__next-year:disabled,.usa-date-picker__calendar__next-month:disabled,.usa-date-picker__button:disabled,[aria-disabled=true].usa-date-picker__calendar__year,[aria-disabled=true].usa-date-picker__calendar__previous-year-chunk,[aria-disabled=true].usa-date-picker__calendar__next-year-chunk,[aria-disabled=true].usa-date-picker__calendar__month,[aria-disabled=true].usa-date-picker__calendar__year-selection,[aria-disabled=true].usa-date-picker__calendar__month-selection,[aria-disabled=true].usa-date-picker__calendar__date,[aria-disabled=true].usa-date-picker__calendar__previous-year,[aria-disabled=true].usa-date-picker__calendar__previous-month,[aria-disabled=true].usa-date-picker__calendar__next-year,[aria-disabled=true].usa-date-picker__calendar__next-month,[aria-disabled=true].usa-date-picker__button{cursor:not-allowed;opacity:.6}.usa-date-picker__external-input[aria-disabled=true]+.usa-date-picker__button:hover,.usa-date-picker__calendar__year:hover:disabled,.usa-date-picker__calendar__previous-year-chunk:hover:disabled,.usa-date-picker__calendar__next-year-chunk:hover:disabled,.usa-date-picker__calendar__month:hover:disabled,.usa-date-picker__calendar__year-selection:hover:disabled,.usa-date-picker__calendar__month-selection:hover:disabled,.usa-date-picker__calendar__date:hover:disabled,.usa-date-picker__calendar__previous-year:hover:disabled,.usa-date-picker__calendar__previous-month:hover:disabled,.usa-date-picker__calendar__next-year:hover:disabled,.usa-date-picker__calendar__next-month:hover:disabled,.usa-date-picker__button:hover:disabled,[aria-disabled=true].usa-date-picker__calendar__year:hover,[aria-disabled=true].usa-date-picker__calendar__previous-year-chunk:hover,[aria-disabled=true].usa-date-picker__calendar__next-year-chunk:hover,[aria-disabled=true].usa-date-picker__calendar__month:hover,[aria-disabled=true].usa-date-picker__calendar__year-selection:hover,[aria-disabled=true].usa-date-picker__calendar__month-selection:hover,[aria-disabled=true].usa-date-picker__calendar__date:hover,[aria-disabled=true].usa-date-picker__calendar__previous-year:hover,[aria-disabled=true].usa-date-picker__calendar__previous-month:hover,[aria-disabled=true].usa-date-picker__calendar__next-year:hover,[aria-disabled=true].usa-date-picker__calendar__next-month:hover,[aria-disabled=true].usa-date-picker__button:hover{background-color:initial}@media(forced-colors: active){.usa-date-picker__external-input[aria-disabled=true]+.usa-date-picker__button,.usa-date-picker__calendar__year:disabled,.usa-date-picker__calendar__previous-year-chunk:disabled,.usa-date-picker__calendar__next-year-chunk:disabled,.usa-date-picker__calendar__month:disabled,.usa-date-picker__calendar__year-selection:disabled,.usa-date-picker__calendar__month-selection:disabled,.usa-date-picker__calendar__date:disabled,.usa-date-picker__calendar__previous-year:disabled,.usa-date-picker__calendar__previous-month:disabled,.usa-date-picker__calendar__next-year:disabled,.usa-date-picker__calendar__next-month:disabled,.usa-date-picker__button:disabled,[aria-disabled=true].usa-date-picker__calendar__year,[aria-disabled=true].usa-date-picker__calendar__previous-year-chunk,[aria-disabled=true].usa-date-picker__calendar__next-year-chunk,[aria-disabled=true].usa-date-picker__calendar__month,[aria-disabled=true].usa-date-picker__calendar__year-selection,[aria-disabled=true].usa-date-picker__calendar__month-selection,[aria-disabled=true].usa-date-picker__calendar__date,[aria-disabled=true].usa-date-picker__calendar__previous-year,[aria-disabled=true].usa-date-picker__calendar__previous-month,[aria-disabled=true].usa-date-picker__calendar__next-year,[aria-disabled=true].usa-date-picker__calendar__next-month,[aria-disabled=true].usa-date-picker__button{background-color:GrayText}.usa-date-picker__external-input[aria-disabled=true]+.usa-date-picker__button:hover,.usa-date-picker__calendar__year:hover:disabled,.usa-date-picker__calendar__previous-year-chunk:hover:disabled,.usa-date-picker__calendar__next-year-chunk:hover:disabled,.usa-date-picker__calendar__month:hover:disabled,.usa-date-picker__calendar__year-selection:hover:disabled,.usa-date-picker__calendar__month-selection:hover:disabled,.usa-date-picker__calendar__date:hover:disabled,.usa-date-picker__calendar__previous-year:hover:disabled,.usa-date-picker__calendar__previous-month:hover:disabled,.usa-date-picker__calendar__next-year:hover:disabled,.usa-date-picker__calendar__next-month:hover:disabled,.usa-date-picker__button:hover:disabled,[aria-disabled=true].usa-date-picker__calendar__year:hover,[aria-disabled=true].usa-date-picker__calendar__previous-year-chunk:hover,[aria-disabled=true].usa-date-picker__calendar__next-year-chunk:hover,[aria-disabled=true].usa-date-picker__calendar__month:hover,[aria-disabled=true].usa-date-picker__calendar__year-selection:hover,[aria-disabled=true].usa-date-picker__calendar__month-selection:hover,[aria-disabled=true].usa-date-picker__calendar__date:hover,[aria-disabled=true].usa-date-picker__calendar__previous-year:hover,[aria-disabled=true].usa-date-picker__calendar__previous-month:hover,[aria-disabled=true].usa-date-picker__calendar__next-year:hover,[aria-disabled=true].usa-date-picker__calendar__next-month:hover,[aria-disabled=true].usa-date-picker__button:hover{background-color:GrayText}}.usa-date-picker__calendar__year,.usa-date-picker__calendar__previous-year-chunk,.usa-date-picker__calendar__next-year-chunk,.usa-date-picker__calendar__month,.usa-date-picker__calendar__year-selection,.usa-date-picker__calendar__month-selection,.usa-date-picker__calendar__date,.usa-date-picker__calendar__previous-year,.usa-date-picker__calendar__previous-month,.usa-date-picker__calendar__next-year,.usa-date-picker__calendar__next-month,.usa-date-picker__button{background-color:#f0f0f0;border:0;width:100%}.usa-date-picker__calendar__year:not([disabled]),.usa-date-picker__calendar__previous-year-chunk:not([disabled]),.usa-date-picker__calendar__next-year-chunk:not([disabled]),.usa-date-picker__calendar__month:not([disabled]),.usa-date-picker__calendar__year-selection:not([disabled]),.usa-date-picker__calendar__month-selection:not([disabled]),.usa-date-picker__calendar__date:not([disabled]),.usa-date-picker__calendar__previous-year:not([disabled]),.usa-date-picker__calendar__previous-month:not([disabled]),.usa-date-picker__calendar__next-year:not([disabled]),.usa-date-picker__calendar__next-month:not([disabled]),.usa-date-picker__button:not([disabled]){cursor:pointer}.usa-date-picker__calendar__year:not([disabled]):focus,.usa-date-picker__calendar__previous-year-chunk:not([disabled]):focus,.usa-date-picker__calendar__next-year-chunk:not([disabled]):focus,.usa-date-picker__calendar__month:not([disabled]):focus,.usa-date-picker__calendar__year-selection:not([disabled]):focus,.usa-date-picker__calendar__month-selection:not([disabled]):focus,.usa-date-picker__calendar__date:not([disabled]):focus,.usa-date-picker__calendar__previous-year:not([disabled]):focus,.usa-date-picker__calendar__previous-month:not([disabled]):focus,.usa-date-picker__calendar__next-year:not([disabled]):focus,.usa-date-picker__calendar__next-month:not([disabled]):focus,.usa-date-picker__button:not([disabled]):focus{outline-offset:-4px}.usa-date-picker__calendar__year:not([disabled]):hover,.usa-date-picker__calendar__previous-year-chunk:not([disabled]):hover,.usa-date-picker__calendar__next-year-chunk:not([disabled]):hover,.usa-date-picker__calendar__month:not([disabled]):hover,.usa-date-picker__calendar__year-selection:not([disabled]):hover,.usa-date-picker__calendar__month-selection:not([disabled]):hover,.usa-date-picker__calendar__date:not([disabled]):hover,.usa-date-picker__calendar__previous-year:not([disabled]):hover,.usa-date-picker__calendar__previous-month:not([disabled]):hover,.usa-date-picker__calendar__next-year:not([disabled]):hover,.usa-date-picker__calendar__next-month:not([disabled]):hover,.usa-date-picker__button:not([disabled]):hover{background-color:#dfe1e2}@media(forced-colors: active){.usa-date-picker__calendar__year:not([disabled]):hover,.usa-date-picker__calendar__previous-year-chunk:not([disabled]):hover,.usa-date-picker__calendar__next-year-chunk:not([disabled]):hover,.usa-date-picker__calendar__month:not([disabled]):hover,.usa-date-picker__calendar__year-selection:not([disabled]):hover,.usa-date-picker__calendar__month-selection:not([disabled]):hover,.usa-date-picker__calendar__date:not([disabled]):hover,.usa-date-picker__calendar__previous-year:not([disabled]):hover,.usa-date-picker__calendar__previous-month:not([disabled]):hover,.usa-date-picker__calendar__next-year:not([disabled]):hover,.usa-date-picker__calendar__next-month:not([disabled]):hover,.usa-date-picker__button:not([disabled]):hover{background-color:buttontext}}.usa-date-picker__calendar__year:not([disabled]):active,.usa-date-picker__calendar__previous-year-chunk:not([disabled]):active,.usa-date-picker__calendar__next-year-chunk:not([disabled]):active,.usa-date-picker__calendar__month:not([disabled]):active,.usa-date-picker__calendar__year-selection:not([disabled]):active,.usa-date-picker__calendar__month-selection:not([disabled]):active,.usa-date-picker__calendar__date:not([disabled]):active,.usa-date-picker__calendar__previous-year:not([disabled]):active,.usa-date-picker__calendar__previous-month:not([disabled]):active,.usa-date-picker__calendar__next-year:not([disabled]):active,.usa-date-picker__calendar__next-month:not([disabled]):active,.usa-date-picker__button:not([disabled]):active{background-color:#a9aeb1}@media(forced-colors: active){.usa-date-picker__calendar__year:not([disabled]):active,.usa-date-picker__calendar__previous-year-chunk:not([disabled]):active,.usa-date-picker__calendar__next-year-chunk:not([disabled]):active,.usa-date-picker__calendar__month:not([disabled]):active,.usa-date-picker__calendar__year-selection:not([disabled]):active,.usa-date-picker__calendar__month-selection:not([disabled]):active,.usa-date-picker__calendar__date:not([disabled]):active,.usa-date-picker__calendar__previous-year:not([disabled]):active,.usa-date-picker__calendar__previous-month:not([disabled]):active,.usa-date-picker__calendar__next-year:not([disabled]):active,.usa-date-picker__calendar__next-month:not([disabled]):active,.usa-date-picker__button:not([disabled]):active{background-color:buttontext}}.usa-date-picker--active .usa-date-picker__button{background-color:#f0f0f0}@media(forced-colors: active){.usa-date-picker--active .usa-date-picker__button{background-color:buttontext}}.usa-date-picker--active .usa-date-picker__calendar{z-index:400}.usa-date-picker__button{background-image:url("../img/usa-icons/calendar_today.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat;align-self:stretch;background-color:rgba(0,0,0,0);background-position:center;background-size:1.5rem;margin-top:.5em;width:3em}@media(forced-colors: active){.usa-date-picker__button{background-image:url("../img/usa-icons/calendar_today.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__button{background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/calendar_today.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__button{mask-size:1.5rem !important;position:relative}.usa-date-picker__button:not([disabled]):focus,.usa-date-picker__button:not([disabled]):hover{background-color:Highlight}}.usa-date-picker--initialized .usa-date-picker__wrapper{display:flex}.usa-date-picker__calendar{background-color:#f0f0f0;left:auto;max-width:20rem;position:absolute;right:0;width:100%;z-index:100}.usa-date-picker__calendar__table{border-spacing:0;border-collapse:collapse;table-layout:fixed;text-align:center;width:100%}.usa-date-picker__calendar__table th{font-weight:normal}.usa-date-picker__calendar__table td{padding:0}.usa-date-picker__calendar__row{display:flex;flex-wrap:wrap;text-align:center;width:100%}.usa-date-picker__calendar__cell{background-color:#f0f0f0;flex:1}.usa-date-picker__calendar__cell--center-items{display:flex;justify-content:center;align-items:center}@media(forced-colors: active){.usa-date-picker__calendar__cell--center-items:not([disabled]):hover{outline:2px solid rgba(0,0,0,0);outline-offset:-2px}}.usa-date-picker__calendar__previous-year,.usa-date-picker__calendar__previous-month,.usa-date-picker__calendar__next-year,.usa-date-picker__calendar__next-month{background-position:center;background-size:auto 1.5rem;height:1.5rem;padding:20px 10px}@media(forced-colors: active){.usa-date-picker__calendar__previous-year,.usa-date-picker__calendar__previous-month,.usa-date-picker__calendar__next-year,.usa-date-picker__calendar__next-month{mask-size:1.5rem !important}}.usa-date-picker__calendar__previous-year:not([disabled]){background-image:url("../img/usa-icons/navigate_far_before.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__previous-year:not([disabled]){background-image:url("../img/usa-icons/navigate_far_before.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__previous-year:not([disabled]){background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_far_before.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__previous-year:not([disabled]){background-color:buttonText}}.usa-date-picker__calendar__previous-month:not([disabled]){background-image:url("../img/usa-icons/navigate_before.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__previous-month:not([disabled]){background-image:url("../img/usa-icons/navigate_before.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__previous-month:not([disabled]){background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_before.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__previous-month:not([disabled]){background-color:buttonText}}.usa-date-picker__calendar__next-year:not([disabled]){background-image:url("../img/usa-icons/navigate_far_next.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__next-year:not([disabled]){background-image:url("../img/usa-icons/navigate_far_next.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__next-year:not([disabled]){background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_far_next.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__next-year:not([disabled]){background-color:buttonText}}.usa-date-picker__calendar__next-month:not([disabled]){background-image:url("../img/usa-icons/navigate_next.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__next-month:not([disabled]){background-image:url("../img/usa-icons/navigate_next.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__next-month:not([disabled]){background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_next.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__next-month:not([disabled]){background-color:buttonText}}.usa-date-picker__calendar__day-of-week{padding:6px 0px}.usa-date-picker__calendar__date{padding:10px 0px}.usa-date-picker__calendar__date--focused{outline:2px solid #162e51;outline-offset:-2px;position:relative;z-index:100}.usa-date-picker__calendar__date--next-month:not([disabled]),.usa-date-picker__calendar__date--previous-month:not([disabled]){color:#5d5d52}.usa-date-picker__calendar__date--selected,.usa-date-picker__calendar__date--range-date{background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__date--selected:not([disabled]),.usa-date-picker__calendar__date--range-date:not([disabled]){background-color:#0050d8;color:#f9f9f9}@media(forced-colors: active){.usa-date-picker__calendar__date--selected:not([disabled]),.usa-date-picker__calendar__date--range-date:not([disabled]){border:ActiveText 2px solid}}.usa-date-picker__calendar__date--selected:not([disabled]):hover,.usa-date-picker__calendar__date--range-date:not([disabled]):hover{background-color:#0050d8;color:#e6e6e6}.usa-date-picker__calendar__date--selected:not([disabled]):focus,.usa-date-picker__calendar__date--range-date:not([disabled]):focus{background-color:#0050d8;color:#f9f9f9}@media(forced-colors: active){.usa-date-picker__calendar__date--selected:not([disabled]):focus,.usa-date-picker__calendar__date--range-date:not([disabled]):focus{border:ActiveText 2px solid}}.usa-date-picker__calendar__date--selected:not([disabled]):active,.usa-date-picker__calendar__date--range-date:not([disabled]):active{background-color:#1a4480}@media(forced-colors: active){.usa-date-picker__calendar__date--selected:not([disabled]):active,.usa-date-picker__calendar__date--range-date:not([disabled]):active{background-color:Highlight}}.usa-date-picker__calendar__date--range-date-start{border-top-left-radius:10%;border-bottom-left-radius:10%}.usa-date-picker__calendar__date--range-date-end{border-top-right-radius:10%;border-bottom-right-radius:10%}.usa-date-picker__calendar__date--within-range{background-color:#cfe8ff}.usa-date-picker__calendar__date--within-range:not([disabled]){background-color:#cfe8ff}@media(forced-colors: active){.usa-date-picker__calendar__date--within-range:not([disabled]){border:Highlight 2px solid}}.usa-date-picker__calendar__date--within-range:not([disabled]):hover{background-color:#cfe8ff}@media(forced-colors: active){.usa-date-picker__calendar__date--within-range:not([disabled]):hover{border:Highlight 2px solid}}.usa-date-picker__calendar__date--within-range:not([disabled]):focus{background-color:#cfe8ff}@media(forced-colors: active){.usa-date-picker__calendar__date--within-range:not([disabled]):focus{border:Highlight 2px solid}}.usa-date-picker__calendar__date--within-range:not([disabled]):active{background-color:#cfe8ff}@media(forced-colors: active){.usa-date-picker__calendar__date--within-range:not([disabled]):active{background-color:Highlight}}@media all and (max-width: 19.99em){.usa-date-picker__calendar__month-label{min-width:100%;order:-1}}@media all and (min-width: 20em){.usa-date-picker__calendar__month-label{flex:4;text-align:center}}.usa-date-picker__calendar__year-selection,.usa-date-picker__calendar__month-selection{display:inline-block;height:100%;padding:8px 4px;width:auto}@media all and (max-width: 19.99em){.usa-date-picker__calendar__year-selection,.usa-date-picker__calendar__month-selection{padding-bottom:0;padding-top:12px}}.usa-date-picker__calendar__month-picker{padding:20px 5px}@media all and (max-width: 19.99em){.usa-date-picker__calendar__month-picker{padding-bottom:12px;padding-top:12px}.usa-date-picker__calendar__month-picker tr{display:flex;flex-direction:column}}.usa-date-picker__calendar__month{padding:10px 0}.usa-date-picker__calendar__month--focused{outline:2px solid #162e51;outline-offset:-2px;position:relative;z-index:100}.usa-date-picker__calendar__month--selected{background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__month--selected:not([disabled]){background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__month--selected:not([disabled]):hover{background-color:#0050d8;color:#e6e6e6}.usa-date-picker__calendar__month--selected:not([disabled]):focus{background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__month--selected:not([disabled]):active{background-color:#1a4480}.usa-date-picker__calendar__year-picker{padding:20px 5px}.usa-date-picker__calendar__previous-year-chunk,.usa-date-picker__calendar__next-year-chunk{background-position:center;background-size:auto 2rem;margin:auto;padding:40px 0}@media(forced-colors: active){.usa-date-picker__calendar__previous-year-chunk,.usa-date-picker__calendar__next-year-chunk{mask-size:1.5rem !important}}.usa-date-picker__calendar__previous-year-chunk:not([disabled]){background-image:url("../img/usa-icons/navigate_before.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__previous-year-chunk:not([disabled])::after{background-image:url("../img/usa-icons/navigate_before.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__previous-year-chunk:not([disabled])::after{background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_before.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__previous-year-chunk:not([disabled])::after{content:"";vertical-align:middle;margin-left:auto}.usa-date-picker__calendar__previous-year-chunk:not([disabled]){background-image:none}.usa-date-picker__calendar__previous-year-chunk:not([disabled]):hover{border:2px solid rgba(0,0,0,0);background-color:rgba(0,0,0,0)}}.usa-date-picker__calendar__next-year-chunk:not([disabled]){background-image:url("../img/usa-icons/navigate_next.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}@media(forced-colors: active){.usa-date-picker__calendar__next-year-chunk:not([disabled])::after{background-image:url("../img/usa-icons/navigate_next.svg");background-repeat:no-repeat;background-position:center center;background-size:2.5rem 2.5rem;display:inline-block;height:2.5rem;width:3rem}@supports(mask: url("")){.usa-date-picker__calendar__next-year-chunk:not([disabled])::after{background:none;background-color:ButtonText;mask-image:url("../img/usa-icons/navigate_next.svg"),linear-gradient(transparent, transparent);mask-position:center center;mask-repeat:no-repeat;mask-size:2.5rem 2.5rem}}.usa-date-picker__calendar__next-year-chunk:not([disabled])::after{content:"";vertical-align:middle;margin-left:auto}.usa-date-picker__calendar__next-year-chunk:not([disabled]){background-image:none}.usa-date-picker__calendar__next-year-chunk:not([disabled]):hover{border:2px solid rgba(0,0,0,0);background-color:rgba(0,0,0,0)}}.usa-date-picker__calendar__year{padding:10px 0}.usa-date-picker__calendar__year--focused{outline:2px solid #162e51;outline-offset:-2px;position:relative;z-index:100}.usa-date-picker__calendar__year--selected{background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__year--selected:not([disabled]){background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__year--selected:not([disabled]):hover{background-color:#0050d8;color:#e6e6e6}.usa-date-picker__calendar__year--selected:not([disabled]):focus{background-color:#0050d8;color:#f9f9f9}.usa-date-picker__calendar__year--selected:not([disabled]):active{background-color:#1a4480}[type=file]{border:none;margin-top:.5rem;padding-left:0;padding-top:.2rem}.usa-file-input{display:block;max-width:none;width:100%}.usa-file-input__target{border:1px dashed #a9aeb1;display:block;font-size:.88rem;margin-top:.5rem;position:relative;text-align:center;width:100%}.usa-file-input__target:hover{border-color:#71767a}.usa-file-input__target.has-invalid-file{border-color:#fa9441}.usa-file-input__accepted-files-message{font-weight:bold;margin:-1.5rem 0 1.5rem;pointer-events:none;position:relative;z-index:3}.has-invalid-file .usa-file-input__accepted-files-message{color:#b50909}.usa-file-input__choose{color:#005ea2;text-decoration:underline}.usa-file-input__choose:visited{color:#54278f}.usa-file-input__choose:hover{color:#1a4480}.usa-file-input__choose:active{color:#162e51}.usa-file-input__choose:focus{outline:.25rem solid #2491ff;outline-offset:0rem}.usa-file-input__choose{font-weight:normal}.usa-file-input__instructions{padding:2rem 1rem;pointer-events:none;position:relative;z-index:3}.usa-file-input__box{background:#fff;height:100%;left:0;pointer-events:none;position:absolute;top:0;width:100%;z-index:2}.usa-file-input .usa-file-input__input[type]{cursor:pointer;height:100%;left:0;margin:0;max-width:none;position:absolute;padding:.5rem;text-indent:-999em;top:0;width:100%;z-index:1}.usa-file-input .usa-file-input__input[type]::-webkit-file-upload-button{display:none}.usa-file-input--drag .usa-file-input__target{border-color:#005ea2}.usa-file-input--drag .usa-file-input__box{background-color:#d9e8f6}.usa-file-input--drag .usa-file-input__preview{opacity:.1}.usa-file-input__preview-heading{align-items:center;background:#d9e8f6;display:flex;font-weight:bold;justify-content:space-between;padding:.5rem;pointer-events:none;position:relative;z-index:3}.usa-file-input__preview{align-items:center;background:#d9e8f6;word-wrap:anywhere;display:flex;font-size:.81rem;margin-top:1px;padding:.25rem .5rem;pointer-events:none;position:relative;text-align:left;z-index:3}.usa-file-input__preview:last-child{margin-bottom:-1.5rem}.usa-file-input__preview-image{border:none;display:block;height:2.5rem;margin-right:.5rem;object-fit:contain;width:2.5rem}.usa-file-input__preview-image.is-loading{background-image:url("../img/loader.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat;background-position:center center;background-repeat:no-repeat;background-size:2rem}.usa-file-input__preview-image--generic,.usa-file-input__preview-image--pdf,.usa-file-input__preview-image--word,.usa-file-input__preview-image--excel,.usa-file-input__preview-image--video{background-position:center center;background-repeat:no-repeat;background-size:1.5rem}.usa-file-input__preview-image--pdf{background-image:url("../img/file-pdf.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}.usa-file-input__preview-image--generic{background-image:url("../img/file.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}.usa-file-input__preview-image--word{background-image:url("../img/file-word.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}.usa-file-input__preview-image--excel{background-image:url("../img/file-excel.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}.usa-file-input__preview-image--video{background-image:url("../img/file-video.svg"),linear-gradient(transparent, transparent);background-repeat:no-repeat}.usa-form-group--error .usa-file-input__target{border-color:#b50909;border-width:2px}.usa-file-input--disabled .usa-file-input__instructions,.usa-file-input--disabled .usa-file-input__choose{color:#454545}.usa-file-input--disabled .usa-file-input__box{background-color:#c9c9c9}.usa-file-input--disabled .usa-file-input__input[type]{cursor:not-allowed}.usa-file-input--disabled .usa-file-input__target:hover{border-color:#a9aeb1}.usa-file-input--disabled .usa-file-input--drag .usa-file-input__box{background-color:#c9c9c9}@media(forced-colors: active){.usa-file-input--disabled .usa-file-input__instructions,.usa-file-input--disabled .usa-file-input__choose{color:GrayText}.usa-file-input--disabled .usa-file-input__target,.usa-file-input--disabled .usa-file-input__target:hover{border-color:GrayText}}.usa-range__wrapper{display:flex;flex-direction:row;align-items:center}.usa-range__value{max-inline-size:5%;min-inline-size:5%;padding-top:5px;margin-left:5px}.usa-range{appearance:none;border:none;padding-left:1px;padding-right:1px;width:100%}.usa-range:focus{outline:none}.usa-range:focus::-webkit-slider-thumb{background-color:#fff;box-shadow:0 0 0 2px #2491ff}.usa-range:focus::-moz-range-thumb{background-color:#fff;box-shadow:0 0 0 2px #2491ff}.usa-range:focus::-ms-thumb{background-color:#fff;box-shadow:0 0 0 2px #2491ff}.usa-range::-webkit-slider-runnable-track{background-color:#f0f0f0;border-radius:99rem;border:1px solid #71767a;cursor:pointer;height:1rem;width:100%}.usa-range::-moz-range-track{background-color:#f0f0f0;border-radius:99rem;border:1px solid #71767a;cursor:pointer;height:1rem;width:100%}.usa-range::-ms-track{background-color:#f0f0f0;border-radius:99rem;border:1px solid #71767a;cursor:pointer;height:1rem;width:100%}.usa-range::-webkit-slider-thumb{height:1.25rem;border-radius:99rem;width:1.25rem;background:#f0f0f0;border:none;box-shadow:0 0 0 2px #71767a;cursor:pointer}@media(forced-colors: active){.usa-range::-webkit-slider-thumb{outline:2px solid rgba(0,0,0,0)}}.usa-range::-webkit-slider-thumb{appearance:none;margin-top:-0.19rem}.usa-range::-moz-range-thumb{height:1.25rem;border-radius:99rem;width:1.25rem;background:#f0f0f0;border:none;box-shadow:0 0 0 2px #71767a;cursor:pointer}@media(forced-colors: active){.usa-range::-moz-range-thumb{outline:2px solid rgba(0,0,0,0)}}.usa-range::-ms-thumb{height:1.25rem;border-radius:99rem;width:1.25rem;background:#f0f0f0;border:none;box-shadow:0 0 0 2px #71767a;cursor:pointer}@media(forced-colors: active){.usa-range::-ms-thumb{outline:2px solid rgba(0,0,0,0)}}.usa-range::-ms-fill-lower{background-color:#f0f0f0;border-radius:99rem;border:1px solid #71767a}.usa-range::-ms-fill-upper{background-color:#f0f0f0;border-radius:99rem;border:1px solid #71767a}.usa-range:disabled,.usa-range[aria-disabled=true]{opacity:1}.usa-range:disabled::-webkit-slider-runnable-track,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-webkit-slider-runnable-track:hover,.usa-range:disabled::-webkit-slider-runnable-track:active,.usa-range:disabled::-webkit-slider-runnable-track:focus,.usa-range:disabled::-webkit-slider-runnable-track.usa-focus,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:hover,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:active,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:focus,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-webkit-slider-runnable-track,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track{border:0;color:GrayText}.usa-range:disabled::-webkit-slider-runnable-track:hover,.usa-range:disabled::-webkit-slider-runnable-track:active,.usa-range:disabled::-webkit-slider-runnable-track:focus,.usa-range:disabled::-webkit-slider-runnable-track.usa-focus,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:hover,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:active,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track:focus,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track.usa-focus{color:GrayText}}@media(forced-colors: active){.usa-range:disabled::-webkit-slider-runnable-track,.usa-range[aria-disabled=true]::-webkit-slider-runnable-track{border:2px solid GrayText}}.usa-range:disabled::-moz-range-track,.usa-range[aria-disabled=true]::-moz-range-track{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-moz-range-track:hover,.usa-range:disabled::-moz-range-track:active,.usa-range:disabled::-moz-range-track:focus,.usa-range:disabled::-moz-range-track.usa-focus,.usa-range[aria-disabled=true]::-moz-range-track:hover,.usa-range[aria-disabled=true]::-moz-range-track:active,.usa-range[aria-disabled=true]::-moz-range-track:focus,.usa-range[aria-disabled=true]::-moz-range-track.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-moz-range-track,.usa-range[aria-disabled=true]::-moz-range-track{border:0;color:GrayText}.usa-range:disabled::-moz-range-track:hover,.usa-range:disabled::-moz-range-track:active,.usa-range:disabled::-moz-range-track:focus,.usa-range:disabled::-moz-range-track.usa-focus,.usa-range[aria-disabled=true]::-moz-range-track:hover,.usa-range[aria-disabled=true]::-moz-range-track:active,.usa-range[aria-disabled=true]::-moz-range-track:focus,.usa-range[aria-disabled=true]::-moz-range-track.usa-focus{color:GrayText}}@media(forced-colors: active){.usa-range:disabled::-moz-range-track,.usa-range[aria-disabled=true]::-moz-range-track{border:2px solid GrayText}}.usa-range:disabled::-ms-track,.usa-range[aria-disabled=true]::-ms-track{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-ms-track:hover,.usa-range:disabled::-ms-track:active,.usa-range:disabled::-ms-track:focus,.usa-range:disabled::-ms-track.usa-focus,.usa-range[aria-disabled=true]::-ms-track:hover,.usa-range[aria-disabled=true]::-ms-track:active,.usa-range[aria-disabled=true]::-ms-track:focus,.usa-range[aria-disabled=true]::-ms-track.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-ms-track,.usa-range[aria-disabled=true]::-ms-track{border:0;color:GrayText}.usa-range:disabled::-ms-track:hover,.usa-range:disabled::-ms-track:active,.usa-range:disabled::-ms-track:focus,.usa-range:disabled::-ms-track.usa-focus,.usa-range[aria-disabled=true]::-ms-track:hover,.usa-range[aria-disabled=true]::-ms-track:active,.usa-range[aria-disabled=true]::-ms-track:focus,.usa-range[aria-disabled=true]::-ms-track.usa-focus{color:GrayText}}.usa-range:disabled::-webkit-slider-thumb,.usa-range[aria-disabled=true]::-webkit-slider-thumb{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-webkit-slider-thumb:hover,.usa-range:disabled::-webkit-slider-thumb:active,.usa-range:disabled::-webkit-slider-thumb:focus,.usa-range:disabled::-webkit-slider-thumb.usa-focus,.usa-range[aria-disabled=true]::-webkit-slider-thumb:hover,.usa-range[aria-disabled=true]::-webkit-slider-thumb:active,.usa-range[aria-disabled=true]::-webkit-slider-thumb:focus,.usa-range[aria-disabled=true]::-webkit-slider-thumb.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-webkit-slider-thumb,.usa-range[aria-disabled=true]::-webkit-slider-thumb{border:0;color:GrayText}.usa-range:disabled::-webkit-slider-thumb:hover,.usa-range:disabled::-webkit-slider-thumb:active,.usa-range:disabled::-webkit-slider-thumb:focus,.usa-range:disabled::-webkit-slider-thumb.usa-focus,.usa-range[aria-disabled=true]::-webkit-slider-thumb:hover,.usa-range[aria-disabled=true]::-webkit-slider-thumb:active,.usa-range[aria-disabled=true]::-webkit-slider-thumb:focus,.usa-range[aria-disabled=true]::-webkit-slider-thumb.usa-focus{color:GrayText}}.usa-range:disabled::-moz-range-thumb,.usa-range[aria-disabled=true]::-moz-range-thumb{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-moz-range-thumb:hover,.usa-range:disabled::-moz-range-thumb:active,.usa-range:disabled::-moz-range-thumb:focus,.usa-range:disabled::-moz-range-thumb.usa-focus,.usa-range[aria-disabled=true]::-moz-range-thumb:hover,.usa-range[aria-disabled=true]::-moz-range-thumb:active,.usa-range[aria-disabled=true]::-moz-range-thumb:focus,.usa-range[aria-disabled=true]::-moz-range-thumb.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-moz-range-thumb,.usa-range[aria-disabled=true]::-moz-range-thumb{border:0;color:GrayText}.usa-range:disabled::-moz-range-thumb:hover,.usa-range:disabled::-moz-range-thumb:active,.usa-range:disabled::-moz-range-thumb:focus,.usa-range:disabled::-moz-range-thumb.usa-focus,.usa-range[aria-disabled=true]::-moz-range-thumb:hover,.usa-range[aria-disabled=true]::-moz-range-thumb:active,.usa-range[aria-disabled=true]::-moz-range-thumb:focus,.usa-range[aria-disabled=true]::-moz-range-thumb.usa-focus{color:GrayText}}.usa-range:disabled::-ms-thumb,.usa-range[aria-disabled=true]::-ms-thumb{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-ms-thumb:hover,.usa-range:disabled::-ms-thumb:active,.usa-range:disabled::-ms-thumb:focus,.usa-range:disabled::-ms-thumb.usa-focus,.usa-range[aria-disabled=true]::-ms-thumb:hover,.usa-range[aria-disabled=true]::-ms-thumb:active,.usa-range[aria-disabled=true]::-ms-thumb:focus,.usa-range[aria-disabled=true]::-ms-thumb.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-ms-thumb,.usa-range[aria-disabled=true]::-ms-thumb{border:0;color:GrayText}.usa-range:disabled::-ms-thumb:hover,.usa-range:disabled::-ms-thumb:active,.usa-range:disabled::-ms-thumb:focus,.usa-range:disabled::-ms-thumb.usa-focus,.usa-range[aria-disabled=true]::-ms-thumb:hover,.usa-range[aria-disabled=true]::-ms-thumb:active,.usa-range[aria-disabled=true]::-ms-thumb:focus,.usa-range[aria-disabled=true]::-ms-thumb.usa-focus{color:GrayText}}.usa-range:disabled::-ms-fill-lower,.usa-range[aria-disabled=true]::-ms-fill-lower{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-ms-fill-lower:hover,.usa-range:disabled::-ms-fill-lower:active,.usa-range:disabled::-ms-fill-lower:focus,.usa-range:disabled::-ms-fill-lower.usa-focus,.usa-range[aria-disabled=true]::-ms-fill-lower:hover,.usa-range[aria-disabled=true]::-ms-fill-lower:active,.usa-range[aria-disabled=true]::-ms-fill-lower:focus,.usa-range[aria-disabled=true]::-ms-fill-lower.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-ms-fill-lower,.usa-range[aria-disabled=true]::-ms-fill-lower{border:0;color:GrayText}.usa-range:disabled::-ms-fill-lower:hover,.usa-range:disabled::-ms-fill-lower:active,.usa-range:disabled::-ms-fill-lower:focus,.usa-range:disabled::-ms-fill-lower.usa-focus,.usa-range[aria-disabled=true]::-ms-fill-lower:hover,.usa-range[aria-disabled=true]::-ms-fill-lower:active,.usa-range[aria-disabled=true]::-ms-fill-lower:focus,.usa-range[aria-disabled=true]::-ms-fill-lower.usa-focus{color:GrayText}}.usa-range:disabled::-ms-fill-upper,.usa-range[aria-disabled=true]::-ms-fill-upper{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-range:disabled::-ms-fill-upper:hover,.usa-range:disabled::-ms-fill-upper:active,.usa-range:disabled::-ms-fill-upper:focus,.usa-range:disabled::-ms-fill-upper.usa-focus,.usa-range[aria-disabled=true]::-ms-fill-upper:hover,.usa-range[aria-disabled=true]::-ms-fill-upper:active,.usa-range[aria-disabled=true]::-ms-fill-upper:focus,.usa-range[aria-disabled=true]::-ms-fill-upper.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-range:disabled::-ms-fill-upper,.usa-range[aria-disabled=true]::-ms-fill-upper{border:0;color:GrayText}.usa-range:disabled::-ms-fill-upper:hover,.usa-range:disabled::-ms-fill-upper:active,.usa-range:disabled::-ms-fill-upper:focus,.usa-range:disabled::-ms-fill-upper.usa-focus,.usa-range[aria-disabled=true]::-ms-fill-upper:hover,.usa-range[aria-disabled=true]::-ms-fill-upper:active,.usa-range[aria-disabled=true]::-ms-fill-upper:focus,.usa-range[aria-disabled=true]::-ms-fill-upper.usa-focus{color:GrayText}}.usa-hint{color:#71767a}.usa-hint--required{color:#b50909}.usa-error-message{padding-bottom:.25rem;padding-top:.25rem;color:#b50909;display:block;font-weight:700}.usa-button{font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1rem;line-height:1;color:#fff;background-color:#005ea2;appearance:none;align-items:center;border:0;border-radius:.25rem;cursor:pointer;column-gap:.5rem;display:inline-flex;font-weight:700;justify-content:center;margin-right:.5rem;padding:.75rem 1.25rem;text-align:center;text-decoration:none;width:100%}@media all and (min-width: 30em){.usa-button{width:auto}}.usa-button:visited{color:#fff}.usa-button:hover,.usa-button.usa-button--hover{color:#fff;background-color:#1a4480;border-bottom:0;text-decoration:none}.usa-button:active,.usa-button.usa-button--active{color:#fff;background-color:#162e51}.usa-button:not([disabled]):focus,.usa-button:not([disabled]).usa-focus{outline-offset:.25rem}.usa-button:disabled,.usa-button[aria-disabled=true]{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-button:disabled:hover,.usa-button:disabled:active,.usa-button:disabled:focus,.usa-button:disabled.usa-focus,.usa-button[aria-disabled=true]:hover,.usa-button[aria-disabled=true]:active,.usa-button[aria-disabled=true]:focus,.usa-button[aria-disabled=true].usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-button:disabled,.usa-button[aria-disabled=true]{border:0;color:GrayText}.usa-button:disabled:hover,.usa-button:disabled:active,.usa-button:disabled:focus,.usa-button:disabled.usa-focus,.usa-button[aria-disabled=true]:hover,.usa-button[aria-disabled=true]:active,.usa-button[aria-disabled=true]:focus,.usa-button[aria-disabled=true].usa-focus{color:GrayText}}.usa-button:disabled.usa-button--hover,.usa-button:disabled.usa-button--active,.usa-button[aria-disabled=true].usa-button--hover,.usa-button[aria-disabled=true].usa-button--active{color:#454545;background-color:#c9c9c9;cursor:not-allowed;opacity:1}.usa-button:disabled.usa-button--hover:hover,.usa-button:disabled.usa-button--hover:active,.usa-button:disabled.usa-button--hover:focus,.usa-button:disabled.usa-button--hover.usa-focus,.usa-button:disabled.usa-button--active:hover,.usa-button:disabled.usa-button--active:active,.usa-button:disabled.usa-button--active:focus,.usa-button:disabled.usa-button--active.usa-focus,.usa-button[aria-disabled=true].usa-button--hover:hover,.usa-button[aria-disabled=true].usa-button--hover:active,.usa-button[aria-disabled=true].usa-button--hover:focus,.usa-button[aria-disabled=true].usa-button--hover.usa-focus,.usa-button[aria-disabled=true].usa-button--active:hover,.usa-button[aria-disabled=true].usa-button--active:active,.usa-button[aria-disabled=true].usa-button--active:focus,.usa-button[aria-disabled=true].usa-button--active.usa-focus{color:#454545;background-color:#c9c9c9}@media(forced-colors: active){.usa-button:disabled.usa-button--hover,.usa-button:disabled.usa-button--active,.usa-button[aria-disabled=true].usa-button--hover,.usa-button[aria-disabled=true].usa-button--active{border:0;color:GrayText}.usa-button:disabled.usa-button--hover:hover,.usa-button:disabled.usa-button--hover:active,.usa-button:disabled.usa-button--hover:focus,.usa-button:disabled.usa-button--hover.usa-focus,.usa-button:disabled.usa-button--active:hover,.usa-button:disabled.usa-button--active:active,.usa-button:disabled.usa-button--active:focus,.usa-button:disabled.usa-button--active.usa-focus,.usa-button[aria-disabled=true].usa-button--hover:hover,.usa-button[aria-disabled=true].usa-button--hover:active,.usa-button[aria-disabled=true].usa-button--hover:focus,.usa-button[aria-disabled=true].usa-button--hover.usa-focus,.usa-button[aria-disabled=true].usa-button--active:hover,.usa-button[aria-disabled=true].usa-button--active:active,.usa-button[aria-disabled=true].usa-button--active:focus,.usa-button[aria-disabled=true].usa-button--active.usa-focus{color:GrayText}}@media(forced-colors: active){.usa-button:disabled:not(.usa-button--unstyled),.usa-button[aria-disabled=true]:not(.usa-button--unstyled){border:2px solid GrayText}}.usa-button .usa-icon{flex-shrink:0}@media(forced-colors: active){.usa-button:not(.usa-button--unstyled){border:2px solid rgba(0,0,0,0)}}.usa-button--accent-cool{color:#1b1b1b;background-color:#00bde3}.usa-button--accent-cool:visited{color:#1b1b1b;background-color:#00bde3}.usa-button--accent-cool:hover,.usa-button--accent-cool.usa-button--hover{color:#1b1b1b;background-color:#28a0cb}.usa-button--accent-cool:active,.usa-button--accent-cool.usa-button--active{color:#fff;background-color:#07648d}.usa-button--accent-warm{color:#1b1b1b;background-color:#fa9441}.usa-button--accent-warm:visited{color:#1b1b1b;background-color:#fa9441}.usa-button--accent-warm:hover,.usa-button--accent-warm.usa-button--hover{color:#fff;background-color:#c05600}.usa-button--accent-warm:active,.usa-button--accent-warm.usa-button--active{color:#fff;background-color:#775540}.usa-button--outline{background-color:rgba(0,0,0,0);box-shadow:inset 0 0 0 2px #005ea2;color:#005ea2}.usa-button--outline:visited{color:#005ea2}.usa-button--outline:hover,.usa-button--outline.usa-button--hover{background-color:rgba(0,0,0,0);box-shadow:inset 0 0 0 2px #1a4480;color:#1a4480}.usa-button--outline:active,.usa-button--outline.usa-button--active{background-color:rgba(0,0,0,0);box-shadow:inset 0 0 0 2px #162e51;color:#162e51}.usa-button--outline.usa-button--inverse{box-shadow:inset 0 0 0 2px #dfe1e2;color:#dfe1e2}.usa-button--outline.usa-button--inverse:visited{color:#dfe1e2}.usa-button--outline.usa-button--inverse:hover,.usa-button--outline.usa-button--inverse.usa-button--hover{box-shadow:inset 0 0 0 2px #f0f0f0;color:#f0f0f0}.usa-button--outline.usa-button--inverse:active,.usa-button--outline.usa-button--inverse.usa-button--active{background-color:rgba(0,0,0,0);box-shadow:inset 0 0 0 2px #fff;color:#fff}.usa-button--outline.usa-button--inverse.usa-button--unstyled{color:#005ea2;text-decoration:underline}.usa-button--outline.usa-button--inverse.usa-button--unstyled:visited{color:#54278f}.usa-button--outline.usa-button--inverse.usa-button--unstyled:hover{color:#1a4480}.usa-button--outline.usa-button--inverse.usa-button--unstyled:active{color:#162e51}.usa-button--outline.usa-button--inverse.usa-button--unstyled:focus{outline:.25rem solid #2491ff;outline-offset:0rem}.usa-button--outline.usa-button--inverse.usa-button--unstyled{background-color:rgba(0,0,0,0);border:0;border-radius:0;box-shadow:none;font-weight:normal;justify-content:normal;text-align:left;margin:0;padding:0;width:auto}.usa-button--outline.usa-button--inverse.usa-button--unstyled:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled.usa-button--hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true].usa-button--hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled:active,.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--active,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled:active,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:active,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled.usa-button--active,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true].usa-button--active,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled:focus,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:focus,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled.usa-focus,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true].usa-focus,.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true],.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--disabled{background-color:rgba(0,0,0,0);box-shadow:none;text-decoration:underline}.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--hover{color:#1a4480}.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--active{color:#162e51}.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true],.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:focus{color:#757575}@media(forced-colors: active){.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true],.usa-button--outline.usa-button--inverse.usa-button--unstyled:disabled:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled[aria-disabled=true]:focus{color:GrayText}}.usa-button--outline.usa-button--inverse.usa-button--unstyled{color:#dfe1e2}.usa-button--outline.usa-button--inverse.usa-button--unstyled:visited{color:#dfe1e2}.usa-button--outline.usa-button--inverse.usa-button--unstyled:hover,.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--hover{color:#f0f0f0}.usa-button--outline.usa-button--inverse.usa-button--unstyled:active,.usa-button--outline.usa-button--inverse.usa-button--unstyled.usa-button--active{color:#fff}.usa-button--base{color:#fff;background-color:#71767a}.usa-button--base:hover,.usa-button--base.usa-button--hover{color:#fff;background-color:#565c65}.usa-button--base:active,.usa-button--base.usa-button--active{color:#fff;background-color:#3d4551}.usa-button--secondary{color:#fff;background-color:#d83933}.usa-button--secondary:hover,.usa-button--secondary.usa-button--hover{color:#fff;background-color:#b50909}.usa-button--secondary:active,.usa-button--secondary.usa-button--active{color:#fff;background-color:#8b0a03}.usa-button--big{border-radius:.25rem;font-size:1.38rem;padding:1rem 1.5rem}.usa-button--outline:disabled,.usa-button--outline:disabled:hover,.usa-button--outline:disabled:active,.usa-button--outline:disabled:focus,.usa-button--outline[aria-disabled=true],.usa-button--outline[aria-disabled=true]:hover,.usa-button--outline[aria-disabled=true]:active,.usa-button--outline[aria-disabled=true]:focus,.usa-button--outline-inverse:disabled,.usa-button--outline-inverse:disabled:hover,.usa-button--outline-inverse:disabled:active,.usa-button--outline-inverse:disabled:focus,.usa-button--outline-inverse[aria-disabled=true],.usa-button--outline-inverse[aria-disabled=true]:hover,.usa-button--outline-inverse[aria-disabled=true]:active,.usa-button--outline-inverse[aria-disabled=true]:focus{background-color:rgba(0,0,0,0);color:#757575}.usa-button--outline:disabled,.usa-button--outline[aria-disabled=true]{box-shadow:inset 0 0 0 2px #c9c9c9}.usa-button--outline:disabled.usa-button--inverse,.usa-button--outline[aria-disabled=true].usa-button--inverse{box-shadow:inset 0 0 0 2px #919191;color:#919191}@media(forced-colors: active){.usa-button--outline:disabled.usa-button--inverse,.usa-button--outline[aria-disabled=true].usa-button--inverse{color:GrayText}}.usa-button--unstyled{color:#005ea2;text-decoration:underline}.usa-button--unstyled:visited{color:#54278f}.usa-button--unstyled:hover{color:#1a4480}.usa-button--unstyled:active{color:#162e51}.usa-button--unstyled:focus{outline:.25rem solid #2491ff;outline-offset:0rem}.usa-button--unstyled{background-color:rgba(0,0,0,0);border:0;border-radius:0;box-shadow:none;font-weight:normal;justify-content:normal;text-align:left;margin:0;padding:0;width:auto}.usa-button--unstyled:hover,.usa-button--unstyled.usa-button--hover,.usa-button--unstyled:disabled:hover,.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--unstyled:disabled.usa-button--hover,.usa-button--unstyled[aria-disabled=true].usa-button--hover,.usa-button--unstyled:active,.usa-button--unstyled.usa-button--active,.usa-button--unstyled:disabled:active,.usa-button--unstyled[aria-disabled=true]:active,.usa-button--unstyled:disabled.usa-button--active,.usa-button--unstyled[aria-disabled=true].usa-button--active,.usa-button--unstyled:disabled:focus,.usa-button--unstyled[aria-disabled=true]:focus,.usa-button--unstyled:disabled.usa-focus,.usa-button--unstyled[aria-disabled=true].usa-focus,.usa-button--unstyled:disabled,.usa-button--unstyled[aria-disabled=true],.usa-button--unstyled.usa-button--disabled{background-color:rgba(0,0,0,0);box-shadow:none;text-decoration:underline}.usa-button--unstyled.usa-button--hover{color:#1a4480}.usa-button--unstyled.usa-button--active{color:#162e51}.usa-button--unstyled:disabled,.usa-button--unstyled[aria-disabled=true],.usa-button--unstyled:disabled:hover,.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--unstyled[aria-disabled=true]:focus{color:#757575}@media(forced-colors: active){.usa-button--unstyled:disabled,.usa-button--unstyled[aria-disabled=true],.usa-button--unstyled:disabled:hover,.usa-button--unstyled[aria-disabled=true]:hover,.usa-button--unstyled[aria-disabled=true]:focus{color:GrayText}}.usa-button-group{margin-bottom:0;margin-top:0;display:flex;flex-direction:column;flex-wrap:wrap;list-style-type:none;margin-left:-0.25rem;margin-right:-0.25rem;padding-left:0}@media all and (min-width: 30em){.usa-button-group{flex-wrap:nowrap;align-items:stretch;flex-direction:row}}.usa-button-group .usa-button-group{height:100%}@media all and (min-width: 30em){.usa-button-group .usa-button-group .usa-button-group__item{margin-top:0;margin-bottom:0}}.usa-button-group .usa-button-group--segmented .usa-button-group__item{margin-top:0;margin-bottom:0}.usa-button-group__item{margin:.25rem}@media all and (min-width: 30em){.usa-button-group__item:last-child{margin-right:0}}.usa-button-group__item .usa-button{height:100%;margin-left:0;margin-right:0}.usa-button-group--segmented{flex-direction:row;flex-wrap:nowrap;justify-content:space-between;margin-left:0;margin-right:0}@media all and (min-width: 30em){.usa-button-group--segmented{justify-content:flex-start}}.usa-button-group--segmented .usa-button{position:relative;width:calc(100% + 2px)}@media all and (min-width: 30em){.usa-button-group--segmented .usa-button{width:auto}}.usa-button-group--segmented .usa-button:hover,.usa-button-group--segmented .usa-button:active{z-index:2}.usa-button-group--segmented .usa-button:focus{z-index:3}.usa-button-group--segmented .usa-button-group__item{margin-left:0;margin-right:0;width:100%}@media all and (min-width: 30em){.usa-button-group--segmented .usa-button-group__item{width:auto}}.usa-button-group--segmented .usa-button-group__item:first-child>.usa-button{border-top-right-radius:0;border-bottom-right-radius:0;margin-right:-1px}.usa-button-group--segmented .usa-button-group__item:last-child>.usa-button{border-top-left-radius:0;border-bottom-left-radius:0;margin-right:0;margin-left:-2px;width:calc(100% + 2px)}@media all and (min-width: 30em){.usa-button-group--segmented .usa-button-group__item:last-child>.usa-button{margin-left:-1px;width:auto}}.usa-button-group--segmented .usa-button-group__item:where(:not(:first-child):not(:last-child))>.usa-button{border-radius:0;margin-right:-1px;margin-left:-1px}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button::before{border-right:1px solid #1a4480;bottom:0;content:"";display:block;height:100%;position:absolute;right:1px;top:0;width:1px;z-index:3}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button--secondary::before{border-right-color:#b50909}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button--accent-cool::before{border-right-color:#28a0cb}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button--base::before{border-right-color:#565c65}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) [class*=usa-button]:disabled::before,.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) [class*=usa-button][aria-disabled=true]::before{border-right-color:#fff}.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button:active::before,.usa-button-group--segmented .usa-button-group__item:where(:not(:last-child)) .usa-button--outline::before{display:none}.usa-focus{outline:.25rem solid #2491ff;outline-offset:0rem}.usa-sr-only{position:absolute;left:-999em;right:auto}.usa-step-indicator{font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1rem;line-height:1.2;background-color:#fff;margin-bottom:2rem;margin-left:-1px;margin-right:-1px}@media all and (min-width: 40em){.usa-step-indicator{margin-left:0;margin-right:0}}.usa-step-indicator__segments{counter-reset:usa-step-indicator;display:flex;list-style:none;margin:0;padding:0}.usa-step-indicator__segment{flex:1 1 0%;counter-increment:usa-step-indicator;margin-left:1px;margin-right:1px;max-width:15rem;min-height:.5rem;position:relative}.usa-step-indicator__segment:after{background-color:#919191;content:"";display:block;height:.5rem;left:0;position:absolute;right:0;top:0}@media all and (min-width: 40em){.usa-step-indicator__segment:after{height:.5rem}}.usa-step-indicator__segment--complete::after{background-color:#162e51}.usa-step-indicator__segment--complete .usa-step-indicator__segment-label{color:#162e51}.usa-step-indicator__segment--current::after{background-color:#005ea2}.usa-step-indicator__segment--current .usa-step-indicator__segment-label{color:#005ea2;font-weight:700}.usa-step-indicator__segment-label{display:none}@media all and (min-width: 40em){.usa-step-indicator__segment-label{color:#565c65;display:block;font-size:1rem;margin-top:calc(0.5rem + 0.5rem);padding-right:2rem;text-align:left}}.usa-step-indicator__header{align-items:baseline;display:flex}.usa-step-indicator__heading{color:#1b1b1b;font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;font-size:1.06rem;font-weight:700;margin:1rem 0 0}@media all and (min-width: 40em){.usa-step-indicator__heading{font-size:1.38rem;margin-top:2rem}}.usa-step-indicator__current-step{height:2.5rem;border-radius:99rem;width:2.5rem;font-weight:normal;font-feature-settings:"tnum" 1, "kern" 1;background-color:#005ea2;color:#fff;display:inline-block;padding:calc((2.5rem - 2ex*1.2)*.5);text-align:center}.usa-step-indicator__total-steps{font-weight:normal;font-feature-settings:"tnum" 1, "kern" 1;color:#005ea2;margin-right:.5rem}@media all and (min-width: 40em){.usa-step-indicator--counters .usa-step-indicator__segment,.usa-step-indicator--counters-sm .usa-step-indicator__segment{margin-left:0;margin-right:0;margin-top:calc((2.5rem - 0.5rem)/2 + 0.25rem)}.usa-step-indicator--counters .usa-step-indicator__segment:before,.usa-step-indicator--counters-sm .usa-step-indicator__segment:before{height:2.5rem;border-radius:99rem;width:2.5rem;font-feature-settings:"tnum" 1, "kern" 1;background-color:#fff;box-shadow:inset 0 0 0 .25rem #919191,0 0 0 .25rem #fff;color:#565c65;content:counter(usa-step-indicator);display:block;font-weight:700;left:0;line-height:1;padding:calc((2.5rem - 2ex*1)*.5);position:absolute;text-align:center;top:calc((2.5rem - 0.5rem)/-2);z-index:100}.usa-step-indicator--counters .usa-step-indicator__segment:last-child:after,.usa-step-indicator--counters-sm .usa-step-indicator__segment:last-child:after{display:none}}.usa-step-indicator--counters .usa-step-indicator__segment--complete::before,.usa-step-indicator--counters-sm .usa-step-indicator__segment--complete::before{background-color:#162e51;box-shadow:0 0 0 .25rem #fff;color:#fff}.usa-step-indicator--counters .usa-step-indicator__segment--current::before,.usa-step-indicator--counters-sm .usa-step-indicator__segment--current::before{background-color:#005ea2;box-shadow:0 0 0 .25rem #fff;color:#fff}@media all and (min-width: 40em){.usa-step-indicator--counters .usa-step-indicator__segment-label,.usa-step-indicator--counters-sm .usa-step-indicator__segment-label{margin-top:calc((2.5rem + 0.5rem)/2 + 0.5rem)}}@media all and (min-width: 40em){.usa-step-indicator--counters.usa-step-indicator--center .usa-step-indicator__segment:first-child:after,.usa-step-indicator--counters-sm.usa-step-indicator--center .usa-step-indicator__segment:first-child:after{left:50%;right:0;width:auto}.usa-step-indicator--counters.usa-step-indicator--center .usa-step-indicator__segment:last-child:after,.usa-step-indicator--counters-sm.usa-step-indicator--center .usa-step-indicator__segment:last-child:after{display:block;left:0;right:50%;width:auto}}@media all and (min-width: 40em){.usa-step-indicator--counters-sm .usa-step-indicator__segment{margin-top:calc((1.5rem - 0.5rem)/2 + 0.25rem)}.usa-step-indicator--counters-sm .usa-step-indicator__segment:before{height:1.5rem;border-radius:99rem;width:1.5rem;font-size:.88rem;padding:calc(0.25rem + 1px);top:calc((1.5rem - 0.5rem)/-2)}.usa-step-indicator--counters-sm .usa-step-indicator__segment:last-child:after{display:none}}@media all and (min-width: 40em){.usa-step-indicator--counters-sm .usa-step-indicator__segment-label{margin-top:calc((1.5rem + 0.5rem)/2 + 0.5rem)}}.usa-step-indicator--no-labels{margin-left:-1px;margin-right:-1px}.usa-step-indicator--no-labels .usa-step-indicator__segment{margin-top:0;margin-left:1px;margin-right:1px}.usa-step-indicator--no-labels .usa-step-indicator__segment:before{display:none}.usa-step-indicator--no-labels .usa-step-indicator__segment:last-child:after{display:block}.usa-step-indicator--no-labels .usa-step-indicator__heading{margin-top:1rem}.usa-step-indicator--no-labels .usa-step-indicator__segment-label{display:none}.usa-step-indicator--center{margin-left:-1px;margin-right:-1px}.usa-step-indicator--center .usa-step-indicator__segment{margin-left:1px;margin-right:1px}.usa-step-indicator--center .usa-step-indicator__segment:before{left:calc(50% - (2.5rem + 0.25rem)/2)}.usa-step-indicator--center .usa-step-indicator__segment-label{padding-left:.5rem;padding-right:.5rem;text-align:center}.usa-step-indicator--center.usa-step-indicator--no-labels .usa-step-indicator__segment:first-child:after{left:0}.usa-step-indicator--center.usa-step-indicator--no-labels .usa-step-indicator__segment:last-child:after{right:0}.usa-step-indicator--center.usa-step-indicator--counters-sm .usa-step-indicator__segment:before{left:calc(50% - (1.5rem + 0.25rem)/2)}.formspec-grid .usa-form-group,.formspec-stack .usa-form-group{margin-top:0}.formspec-container .usa-fieldset{border:0;padding:0;margin:0}.formspec-container .usa-label{margin-top:0}.formspec-container .usa-hint{margin-top:0}.formspec-wizard .usa-step-indicator__heading{font-size:1rem}.formspec-wizard .usa-step-indicator__current-step{width:2rem;height:2rem;padding:0;font-size:.875rem;line-height:2rem}.formspec-wizard .usa-step-indicator__heading-text{font-weight:600}/*# sourceMappingURL=uswds-formspec.css.map */';

// node_modules/@formspec-org/adapters/dist/uswds/index.js
var uswdsAdapter = {
  name: "uswds",
  integrationCSS,
  components: {
    TextInput: renderTextInput2,
    NumberInput: renderNumberInput2,
    RadioGroup: renderRadioGroup2,
    CheckboxGroup: renderCheckboxGroup2,
    Select: renderSelect2,
    DatePicker: renderDatePicker2,
    Checkbox: renderCheckbox2,
    Toggle: renderToggle2,
    MoneyInput: renderMoneyInput2,
    Slider: renderSlider2,
    Rating: renderRating2,
    FileUpload: renderFileUpload2,
    Signature: renderSignature2,
    Wizard: renderWizard2,
    Tabs: renderTabs2
  }
};

// node_modules/@formspec-org/adapters/dist/tailwind/shared.js
var TW = {
  // Typography
  label: "mb-1.5 block text-sm font-semibold text-[var(--formspec-tw-text)]",
  labelHidden: "sr-only",
  hint: "mt-1 text-xs leading-relaxed text-[var(--formspec-tw-muted)]",
  error: "mt-1.5 text-sm font-medium text-[var(--formspec-tw-danger)]",
  legend: "mb-2 text-sm font-semibold text-[var(--formspec-tw-text)]",
  // Form inputs
  input: "block w-full rounded-xl border border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-field-bg)] px-3.5 py-2.5 text-sm text-[var(--formspec-tw-text)] shadow-[var(--formspec-tw-shadow-sm)] transition placeholder:text-[var(--formspec-tw-placeholder)] focus:border-[color:var(--formspec-tw-accent)] focus:outline-none focus:ring-4 focus:ring-[var(--formspec-tw-accent-ring)]",
  inputError: "border-[color:var(--formspec-tw-danger)] focus:border-[color:var(--formspec-tw-danger)] focus:ring-[var(--formspec-tw-danger-ring)]",
  inputNormal: "border-[color:var(--formspec-tw-border)]",
  // Layout
  group: "mb-5",
  fieldset: "mb-6 space-y-1 border-0 p-0",
  // Controls
  controlSm: "peer size-[1.125rem] shrink-0 cursor-pointer rounded-md border-[color:var(--formspec-tw-border-strong)] bg-[var(--formspec-tw-surface)] text-[var(--formspec-tw-accent)] transition focus:ring-2 focus:ring-[var(--formspec-tw-accent-ring)] focus:ring-offset-0",
  radioSm: "peer size-[1.125rem] shrink-0 cursor-pointer border-[color:var(--formspec-tw-border-strong)] bg-[var(--formspec-tw-surface)] text-[var(--formspec-tw-accent)] transition focus:ring-2 focus:ring-[var(--formspec-tw-accent-ring)] focus:ring-offset-0",
  optionLabelText: "text-sm font-medium leading-snug text-[var(--formspec-tw-text)]",
  optionLabel: "text-sm font-medium leading-snug text-[var(--formspec-tw-text)]",
  optionWrapper: "flex items-start gap-3",
  // Buttons
  button: "inline-flex items-center justify-center rounded-xl bg-[var(--formspec-tw-accent)] px-5 py-2.5 text-sm font-semibold text-[var(--formspec-tw-accent-fg)] shadow-[var(--formspec-tw-shadow-md)] transition hover:brightness-110 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--formspec-tw-accent-ring)]",
  buttonOutline: "inline-flex items-center justify-center rounded-xl border border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface)] px-5 py-2.5 text-sm font-semibold text-[var(--formspec-tw-text)] shadow-[var(--formspec-tw-shadow-sm)] transition hover:border-[color:var(--formspec-tw-border-strong)] hover:bg-[var(--formspec-tw-surface-muted)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--formspec-tw-accent-ring)]",
  buttonUnstyled: "text-sm font-semibold underline-offset-2 hover:underline",
  // Container for form controls (Toggle, Rating, Slider, etc.)
  controlContainer: "flex min-h-[56px] items-center gap-4 rounded-2xl border border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-5 py-3 shadow-[var(--formspec-tw-shadow-sm)] transition-colors"
};
var TW_CARD_OPTION = "relative group flex cursor-pointer items-center gap-3 rounded-lg border border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface)] px-4 py-3 shadow-[var(--formspec-tw-shadow-sm)] transition-all duration-200 hover:border-[color:var(--formspec-tw-border-strong)] hover:bg-[var(--formspec-tw-surface-muted)] has-[:checked]:border-[color:var(--formspec-tw-accent)] has-[:checked]:bg-[var(--formspec-tw-accent-soft)] has-[:checked]:shadow-[var(--formspec-tw-shadow-md)] has-[:checked]:ring-1 has-[:checked]:ring-[var(--formspec-tw-accent-ring)]";
function createTailwindFieldDOM(behavior, options) {
  const p2 = behavior.presentation;
  const labelFor = options?.labelFor ?? true;
  const root = el("div", { class: TW.group, "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const labelAttrs = {
    class: p2.labelPosition === "hidden" ? TW.labelHidden : TW.label
  };
  if (labelFor)
    labelAttrs.for = behavior.id;
  const label = el("label", labelAttrs);
  label.textContent = behavior.label;
  root.appendChild(label);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("p", { class: TW.hint, id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createTailwindError(behavior.id);
  const describedBy = [
    hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  return { root, label, hint, error, describedBy };
}
function createTailwindError(behaviorId) {
  return el("p", {
    class: TW.error,
    id: `${behaviorId}-error`,
    role: "alert",
    "aria-live": "polite"
  });
}
function toggleInputError(input, hasError) {
  if (hasError) {
    input.classList.add(...TW.inputError.split(/\s+/));
    input.classList.remove(...TW.inputNormal.split(/\s+/));
  } else {
    input.classList.remove(...TW.inputError.split(/\s+/));
    input.classList.add(...TW.inputNormal.split(/\s+/));
  }
}
function createCardOption(id, labelText) {
  const card = el("label", { class: TW_CARD_OPTION, for: id });
  const input = document.createElement("input");
  input.id = id;
  input.type = "checkbox";
  input.className = TW.controlSm;
  const text = el("span", { class: TW.optionLabelText });
  text.textContent = labelText;
  card.appendChild(input);
  card.appendChild(text);
  return { card, input, label: text };
}
function applyErrorStyling(el2, hasError) {
  el2.classList.toggle("ring-2", hasError);
  el2.classList.toggle("ring-[var(--formspec-tw-danger-ring)]", hasError);
  el2.classList.toggle("rounded-xl", hasError);
}

// node_modules/@formspec-org/adapters/dist/tailwind/text-input.js
var renderTextInput3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const isTextarea = behavior.maxLines != null && behavior.maxLines > 1;
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  let control;
  if (isTextarea) {
    const textarea = document.createElement("textarea");
    textarea.className = TW.input;
    textarea.id = behavior.id;
    textarea.name = behavior.fieldPath;
    textarea.rows = behavior.maxLines;
    if (behavior.placeholder)
      textarea.placeholder = behavior.placeholder;
    textarea.setAttribute("aria-describedby", describedBy);
    control = textarea;
  } else {
    const input = document.createElement("input");
    input.className = TW.input;
    input.id = behavior.id;
    input.name = behavior.fieldPath;
    input.type = behavior.resolvedInputType || "text";
    if (behavior.placeholder)
      input.placeholder = behavior.placeholder;
    if (behavior.inputMode)
      input.inputMode = behavior.inputMode;
    for (const [attr, val] of Object.entries(behavior.extensionAttrs)) {
      if (attr === "inputMode")
        input.inputMode = val;
      else if (attr === "maxLength")
        input.maxLength = Number(val);
      else
        input.setAttribute(attr, val);
    }
    input.setAttribute("aria-describedby", describedBy);
    if (behavior.prefix || behavior.suffix) {
      const group = el("div", { class: "flex rounded-xl shadow-sm" });
      if (behavior.prefix) {
        const prefixEl = el("span", {
          class: "inline-flex items-center rounded-l-xl border border-r-0 border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-3 text-sm text-[var(--formspec-tw-muted)]"
        });
        prefixEl.textContent = behavior.prefix;
        group.appendChild(prefixEl);
        input.classList.remove("rounded-xl");
        input.classList.add("rounded-none", "rounded-r-xl");
      }
      group.appendChild(input);
      if (behavior.suffix) {
        const suffixEl = el("span", {
          class: "inline-flex items-center rounded-r-xl border border-l-0 border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-3 text-sm text-[var(--formspec-tw-muted)]"
        });
        suffixEl.textContent = behavior.suffix;
        group.appendChild(suffixEl);
        if (!behavior.prefix) {
          input.classList.remove("rounded-xl");
          input.classList.add("rounded-none", "rounded-l-xl");
        } else {
          input.classList.remove("rounded-r-xl");
          input.classList.add("rounded-none");
        }
      }
      root.appendChild(group);
      control = group;
    } else {
      control = input;
    }
  }
  if (!control.parentElement)
    root.appendChild(control);
  root.appendChild(error);
  parent.appendChild(root);
  const actualInput = control.querySelector("input") || control.querySelector("textarea") || control;
  const dispose = behavior.bind({
    root,
    label,
    control,
    hint,
    error,
    onValidationChange: (hasError) => {
      toggleInputError(actualInput, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/number-input.js
var renderNumberInput3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const input = document.createElement("input");
  input.className = TW.input;
  input.type = "number";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  input.setAttribute("aria-describedby", describedBy);
  root.appendChild(input);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      toggleInputError(input, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/radio-group.js
function buildRadioOptions2(behavior, container, options) {
  container.innerHTML = "";
  const controls = /* @__PURE__ */ new Map();
  for (let i2 = 0; i2 < options.length; i2++) {
    const opt = options[i2];
    const optId = `${behavior.id}-${i2}`;
    const card = el("label", { class: TW_CARD_OPTION, for: optId });
    const input = document.createElement("input");
    input.className = `${TW.radioSm} rounded-full`;
    input.id = optId;
    input.type = "radio";
    input.name = behavior.inputName;
    input.value = opt.value;
    controls.set(opt.value, input);
    const text = el("span", { class: TW.optionLabelText });
    text.textContent = opt.label;
    card.appendChild(input);
    card.appendChild(text);
    container.appendChild(card);
  }
  return controls;
}
var renderRadioGroup3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const fieldset = el("fieldset", { class: TW.fieldset });
  applyCascadeClasses(fieldset, p2);
  applyCascadeAccessibility(fieldset, p2);
  const legend = el("legend", {
    class: p2.labelPosition === "hidden" ? TW.labelHidden : TW.legend
  });
  legend.textContent = behavior.label;
  fieldset.appendChild(legend);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("p", { class: TW.hint, id: hintId });
    hint.textContent = behavior.hint;
    fieldset.appendChild(hint);
  }
  const optionContainer = el("div", { class: "grid gap-3 mt-3 sm:grid-cols-2" });
  const initialControls = buildRadioOptions2(behavior, optionContainer, behavior.options());
  fieldset.appendChild(optionContainer);
  const error = createTailwindError(behavior.id);
  fieldset.appendChild(error);
  parent.appendChild(fieldset);
  const dispose = behavior.bind({
    root: fieldset,
    label: legend,
    control: fieldset,
    hint,
    error,
    optionControls: initialControls,
    rebuildOptions: (_container, newOptions) => buildRadioOptions2(behavior, optionContainer, newOptions),
    onValidationChange: (hasError) => {
      applyErrorStyling(fieldset, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/checkbox-group.js
function optionGridClass(columns) {
  if (columns === 3)
    return "grid gap-3 mt-3 sm:grid-cols-2 lg:grid-cols-3";
  if (columns === 2)
    return "grid gap-3 mt-3 sm:grid-cols-2";
  return "grid gap-3 mt-3";
}
function buildCheckboxOptions2(behavior, container, options) {
  container.innerHTML = "";
  const controls = /* @__PURE__ */ new Map();
  for (let i2 = 0; i2 < options.length; i2++) {
    const opt = options[i2];
    const optId = `${behavior.id}-${i2}`;
    const { card, input } = createCardOption(optId, opt.label);
    input.name = behavior.fieldPath;
    input.value = opt.value;
    controls.set(opt.value, input);
    container.appendChild(card);
  }
  return controls;
}
var renderCheckboxGroup3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const fieldset = el("fieldset", { class: TW.fieldset });
  applyCascadeClasses(fieldset, p2);
  applyCascadeAccessibility(fieldset, p2);
  const legend = el("legend", {
    class: p2.labelPosition === "hidden" ? TW.labelHidden : TW.legend
  });
  legend.textContent = behavior.label;
  fieldset.appendChild(legend);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("p", { class: TW.hint, id: hintId });
    hint.textContent = behavior.hint;
    fieldset.appendChild(hint);
  }
  if (behavior.selectAll && behavior.options().length > 0) {
    const selectAllRow = el("div", {
      class: "mt-2 flex items-center gap-3 rounded-lg border border-dashed border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-3 py-2.5"
    });
    const selectAllId = `${behavior.id}-select-all`;
    const selectAllCb = document.createElement("input");
    selectAllCb.className = TW.controlSm;
    selectAllCb.id = selectAllId;
    selectAllCb.type = "checkbox";
    selectAllCb.addEventListener("change", () => {
      const checked = [];
      for (const [optVal, cb] of optionControlsRef) {
        cb.checked = selectAllCb.checked;
        if (cb.checked)
          checked.push(optVal);
      }
      behavior.setValue(checked);
    });
    const selectAllLabel = el("label", {
      class: "cursor-pointer text-sm font-semibold text-[var(--formspec-tw-text)]",
      for: selectAllId
    });
    selectAllLabel.textContent = "Select all";
    selectAllRow.appendChild(selectAllCb);
    selectAllRow.appendChild(selectAllLabel);
    fieldset.appendChild(selectAllRow);
  }
  const optionContainer = el("div", { class: optionGridClass(behavior.columns) });
  let optionControlsRef = buildCheckboxOptions2(behavior, optionContainer, behavior.options());
  fieldset.appendChild(optionContainer);
  const error = createTailwindError(behavior.id);
  fieldset.appendChild(error);
  parent.appendChild(fieldset);
  const dispose = behavior.bind({
    root: fieldset,
    label: legend,
    control: fieldset,
    hint,
    error,
    optionControls: optionControlsRef,
    rebuildOptions: (_container, newOptions) => {
      optionControlsRef = buildCheckboxOptions2(behavior, optionContainer, newOptions);
      return optionControlsRef;
    },
    onValidationChange: (hasError) => {
      applyErrorStyling(fieldset, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/select.js
var renderSelect3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const select = document.createElement("select");
  select.className = TW.input;
  select.id = behavior.id;
  select.name = behavior.fieldPath;
  const placeholderOpt = document.createElement("option");
  placeholderOpt.value = "";
  placeholderOpt.textContent = behavior.placeholder || "- Select -";
  if (!behavior.clearable)
    placeholderOpt.disabled = true;
  placeholderOpt.selected = true;
  select.appendChild(placeholderOpt);
  for (const opt of behavior.options()) {
    const option = document.createElement("option");
    option.value = opt.value;
    option.textContent = opt.label;
    select.appendChild(option);
  }
  select.setAttribute("aria-describedby", describedBy);
  root.appendChild(select);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: select,
    hint,
    error,
    onValidationChange: (hasError) => {
      toggleInputError(select, hasError);
    },
    rebuildOptions: (_container, newOptions) => {
      while (select.options.length > 1)
        select.remove(select.options.length - 1);
      const controls = /* @__PURE__ */ new Map();
      for (const opt of newOptions) {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label;
        select.appendChild(option);
      }
      return controls;
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/date-picker.js
var renderDatePicker3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior);
  if (p2.labelPosition === "start")
    root.style.display = "flex";
  const input = document.createElement("input");
  input.className = TW.input;
  input.type = behavior.inputType;
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  if (behavior.minDate)
    input.min = behavior.minDate;
  if (behavior.maxDate)
    input.max = behavior.maxDate;
  input.setAttribute("aria-describedby", describedBy);
  root.appendChild(input);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      toggleInputError(input, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/checkbox.js
var renderCheckbox3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const root = el("div", { class: TW.group, "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const { card, input } = createCardOption(behavior.id, behavior.label);
  input.name = behavior.fieldPath;
  input.type = "checkbox";
  const describedBy = [
    behavior.hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  input.setAttribute("aria-describedby", describedBy);
  root.appendChild(card);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("p", { class: TW.hint, id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createTailwindError(behavior.id);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label: card,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      applyErrorStyling(card, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/toggle.js
var renderToggle3 = (behavior, parent, actx) => {
  const p2 = behavior.presentation;
  const root = el("div", { class: TW.group, "data-name": behavior.fieldPath });
  applyCascadeClasses(root, p2);
  applyCascadeAccessibility(root, p2);
  const row = el("div", {
    class: TW.controlContainer
  });
  const copy = el("div", { class: "min-w-0 flex-1" });
  const title = el("span", {
    class: p2.labelPosition === "hidden" ? "sr-only" : "block text-sm font-semibold text-[var(--formspec-tw-text)]"
  });
  title.textContent = behavior.label;
  copy.appendChild(title);
  const track = el("span", {
    class: "relative inline-flex h-8 w-14 shrink-0 cursor-pointer items-center rounded-full bg-[var(--formspec-tw-track)] p-1 transition-colors duration-200 has-[:checked]:bg-[var(--formspec-tw-accent)] has-[:checked]:shadow-inner"
  });
  const input = document.createElement("input");
  input.type = "checkbox";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  input.setAttribute("role", "switch");
  input.className = "peer absolute inset-0 z-10 h-full w-full cursor-pointer opacity-0";
  const knob = el("span", {
    class: "pointer-events-none inline-block h-6 w-6 rounded-full bg-[var(--formspec-tw-surface)] shadow-[var(--formspec-tw-shadow-md)] ring-1 ring-[color:var(--formspec-tw-knob-ring)] transition-transform duration-200 ease-out translate-x-0 peer-checked:translate-x-6",
    "aria-hidden": "true"
  });
  const describedBy = [
    behavior.hint ? `${behavior.id}-hint` : "",
    `${behavior.id}-error`
  ].filter(Boolean).join(" ");
  input.setAttribute("aria-describedby", describedBy);
  track.appendChild(input);
  track.appendChild(knob);
  row.appendChild(copy);
  row.appendChild(track);
  root.appendChild(row);
  let hint;
  if (behavior.hint) {
    const hintId = `${behavior.id}-hint`;
    hint = el("p", { class: TW.hint, id: hintId });
    hint.textContent = behavior.hint;
    root.appendChild(hint);
  }
  const error = createTailwindError(behavior.id);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label: title,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      applyErrorStyling(row, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/money-input.js
var renderMoneyInput3 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior);
  const container = el("div", { class: "flex rounded-xl shadow-sm" });
  if (behavior.resolvedCurrency) {
    const prefix = el("span", {
      class: "inline-flex items-center rounded-l-xl border border-r-0 border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-3 text-sm text-[var(--formspec-tw-muted)]",
      "aria-hidden": "true"
    });
    prefix.textContent = behavior.resolvedCurrency;
    container.appendChild(prefix);
  }
  const amountInput = document.createElement("input");
  amountInput.className = TW.input;
  amountInput.id = behavior.id;
  amountInput.name = `${behavior.fieldPath}__amount`;
  amountInput.type = "number";
  if (behavior.placeholder)
    amountInput.placeholder = behavior.placeholder;
  if (behavior.step != null)
    amountInput.step = String(behavior.step);
  if (behavior.min != null)
    amountInput.min = String(behavior.min);
  if (behavior.max != null)
    amountInput.max = String(behavior.max);
  amountInput.setAttribute("aria-describedby", describedBy);
  if (behavior.resolvedCurrency) {
    amountInput.classList.remove("rounded-xl");
    amountInput.classList.add("rounded-none", "rounded-r-xl");
  }
  container.appendChild(amountInput);
  if (!behavior.resolvedCurrency) {
    const currencyInput = document.createElement("input");
    currencyInput.className = "block w-20 rounded-r-xl border border-[color:var(--formspec-tw-border)] bg-[var(--formspec-tw-surface-muted)] px-2 py-2.5 text-sm text-[var(--formspec-tw-text)] shadow-sm focus:border-[color:var(--formspec-tw-accent)] focus:outline-none focus:ring-4 focus:ring-[var(--formspec-tw-accent-ring)]";
    currencyInput.type = "text";
    currencyInput.placeholder = "Currency";
    currencyInput.name = `${behavior.fieldPath}__currency`;
    currencyInput.setAttribute("aria-label", "Currency code");
    amountInput.classList.remove("rounded-xl");
    amountInput.classList.add("rounded-none", "rounded-l-xl");
    container.appendChild(currencyInput);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      toggleInputError(amountInput, hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/slider.js
var renderSlider3 = (behavior, parent, actx) => {
  const { root, label, hint, error } = createTailwindFieldDOM(behavior);
  const container = el("div", { class: "flex flex-wrap items-center gap-2" });
  const input = document.createElement("input");
  input.className = "formspec-tw-range min-w-[10rem] flex-1 h-2 cursor-pointer rounded-full bg-[var(--formspec-tw-surface-muted)] accent-[var(--formspec-tw-accent)] appearance-none";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  input.type = "range";
  if (behavior.min != null)
    input.min = String(behavior.min);
  if (behavior.max != null)
    input.max = String(behavior.max);
  if (behavior.step != null)
    input.step = String(behavior.step);
  if (behavior.showTicks && behavior.min != null && behavior.max != null && behavior.step != null) {
    const tickCount = Math.floor((behavior.max - behavior.min) / behavior.step) + 1;
    if (tickCount > 0 && tickCount <= 200) {
      const listId = `tw-ticks-${behavior.fieldPath.replace(/\./g, "-")}`;
      const datalist = document.createElement("datalist");
      datalist.id = listId;
      for (let v2 = behavior.min; v2 <= behavior.max; v2 += behavior.step) {
        const opt = document.createElement("option");
        opt.value = String(v2);
        datalist.appendChild(opt);
      }
      container.appendChild(datalist);
      input.setAttribute("list", listId);
    }
  }
  container.appendChild(input);
  if (behavior.showValue) {
    const valueDisplay = el("span", {
      class: "inline-flex min-w-[2.25rem] shrink-0 items-center justify-center rounded-lg px-2 py-0.5 text-sm font-semibold tabular-nums ring-1 ring-[var(--formspec-tw-accent-ring)] formspec-slider-value"
    });
    valueDisplay.style.backgroundColor = "color-mix(in srgb, var(--formspec-tw-accent) 15%, var(--formspec-tw-surface-muted))";
    valueDisplay.style.color = "var(--formspec-tw-accent)";
    container.appendChild(valueDisplay);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      input.classList.toggle("accent-[var(--formspec-tw-danger)]", hasError);
      input.classList.toggle("accent-[var(--formspec-tw-accent)]", !hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/rating.js
var renderRating3 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior, { labelFor: false });
  const container = el("div", {
    class: `${TW.controlContainer} formspec-rating-stars flex items-center gap-1`,
    role: "slider"
  });
  container.setAttribute("tabindex", "0");
  container.setAttribute("aria-valuemin", "0");
  container.setAttribute("aria-valuemax", String(behavior.maxRating));
  container.setAttribute("aria-valuenow", "0");
  container.setAttribute("aria-valuetext", `0 of ${behavior.maxRating}`);
  container.setAttribute("aria-label", behavior.label);
  container.setAttribute("aria-describedby", describedBy);
  const step = behavior.allowHalf ? 0.5 : 1;
  let currentValue = 0;
  const updateValue = (value) => {
    currentValue = Math.max(0, Math.min(value, behavior.maxRating));
    container.setAttribute("aria-valuenow", String(currentValue));
    container.setAttribute("aria-valuetext", `${currentValue} of ${behavior.maxRating}`);
    behavior.setValue(currentValue);
  };
  container.addEventListener("keydown", (e2) => {
    switch (e2.key) {
      case "ArrowRight":
      case "ArrowUp":
        e2.preventDefault();
        updateValue(currentValue + step);
        break;
      case "ArrowLeft":
      case "ArrowDown":
        e2.preventDefault();
        updateValue(currentValue - step);
        break;
      case "Home":
        e2.preventDefault();
        updateValue(0);
        break;
      case "End":
        e2.preventDefault();
        updateValue(behavior.maxRating);
        break;
    }
  });
  for (let i2 = 1; i2 <= behavior.maxRating; i2++) {
    const star = document.createElement("span");
    star.className = "formspec-rating-star cursor-pointer select-none text-3xl text-[var(--formspec-tw-muted)] transition-colors hover:scale-110 hover:text-[var(--formspec-tw-accent)]";
    star.textContent = behavior.icon;
    star.dataset.value = String(i2);
    star.addEventListener("click", (event) => {
      let value = i2;
      if (behavior.allowHalf) {
        const rect = star.getBoundingClientRect();
        const clickedLeftHalf = rect.width > 0 && event.clientX - rect.left < rect.width / 2;
        value = clickedLeftHalf ? i2 - 0.5 : i2;
      }
      updateValue(value);
    });
    container.appendChild(star);
  }
  root.appendChild(container);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: container,
    hint,
    error,
    onValidationChange: (hasError) => {
      container.classList.toggle("ring-2", hasError);
      container.classList.toggle("ring-[var(--formspec-tw-danger-ring)]", hasError);
      container.classList.toggle("rounded", hasError);
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/file-upload.js
var renderFileUpload3 = (behavior, parent, actx) => {
  const { root, label, hint, error } = createTailwindFieldDOM(behavior);
  const dropZone = el("div", {
    class: "flex justify-center rounded-lg border-2 border-dashed border-[color:var(--formspec-tw-border)] px-6 py-10 transition-colors",
    tabindex: "0",
    role: "button",
    "aria-label": "Drop files here or press Enter to browse"
  });
  dropZone.addEventListener("keydown", (e2) => {
    if (e2.key === "Enter" || e2.key === " ") {
      e2.preventDefault();
      input.click();
    }
  });
  const inner = el("div", { class: "text-center" });
  const iconWrapper = el("div", { class: "mx-auto h-12 w-12 text-[var(--formspec-tw-muted)]" });
  iconWrapper.innerHTML = '<svg class="h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true"><path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /></svg>';
  inner.appendChild(iconWrapper);
  const textRow = el("div", { class: "mt-4 flex text-sm text-[var(--formspec-tw-muted)]" });
  const browseLabel = el("span", {
    class: "relative cursor-pointer rounded-md font-medium text-[var(--formspec-tw-accent)] hover:text-[var(--formspec-tw-accent)]"
  });
  browseLabel.textContent = "Upload a file";
  textRow.appendChild(browseLabel);
  textRow.appendChild(document.createTextNode("\xA0or drag and drop"));
  inner.appendChild(textRow);
  const sizeHint = el("p", { class: "text-xs text-[var(--formspec-tw-muted)] mt-1" });
  sizeHint.textContent = behavior.accept || "Any file type";
  inner.appendChild(sizeHint);
  dropZone.appendChild(inner);
  const input = document.createElement("input");
  input.className = "sr-only";
  input.id = behavior.id;
  input.name = behavior.fieldPath;
  input.type = "file";
  if (behavior.accept)
    input.accept = behavior.accept;
  if (behavior.multiple)
    input.multiple = true;
  dropZone.appendChild(input);
  if (behavior.dragDrop) {
    dropZone.addEventListener("dragover", (e2) => {
      e2.preventDefault();
      dropZone.style.borderColor = "var(--formspec-tw-accent)";
      dropZone.style.backgroundColor = "var(--formspec-tw-accent-soft)";
    });
    dropZone.addEventListener("dragleave", () => {
      dropZone.style.borderColor = "";
      dropZone.style.backgroundColor = "";
    });
    dropZone.addEventListener("drop", (e2) => {
      e2.preventDefault();
      dropZone.style.borderColor = "";
      dropZone.style.backgroundColor = "";
      const files = Array.from(e2.dataTransfer?.files || []);
      const fileData = files.map((f2) => ({ name: f2.name, size: f2.size, type: f2.type }));
      root.dispatchEvent(new CustomEvent("formspec-files-dropped", {
        detail: { fileData, multiple: behavior.multiple },
        bubbles: false
      }));
    });
  }
  root.appendChild(dropZone);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: input,
    hint,
    error,
    onValidationChange: (hasError) => {
      dropZone.style.borderColor = hasError ? "var(--formspec-tw-danger)" : "";
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/signature.js
var renderSignature3 = (behavior, parent, actx) => {
  const { root, label, hint, error, describedBy } = createTailwindFieldDOM(behavior, { labelFor: false });
  const { canvas, clear, dispose: canvasDispose } = createSignatureCanvas({
    height: behavior.height,
    strokeColor: behavior.strokeColor,
    eventTarget: root
  });
  canvas.style.width = "100%";
  canvas.classList.add("rounded-md", "border", "border-[color:var(--formspec-tw-border)]");
  canvas.setAttribute("tabindex", "0");
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-label", "Signature canvas. Use the Clear button to reset.");
  canvas.setAttribute("aria-describedby", describedBy);
  root.appendChild(canvas);
  actx.onDispose(canvasDispose);
  const clearBtn = document.createElement("button");
  clearBtn.type = "button";
  clearBtn.className = TW.buttonOutline + " mt-2";
  clearBtn.textContent = "Clear";
  clearBtn.addEventListener("click", clear);
  root.appendChild(clearBtn);
  root.appendChild(error);
  parent.appendChild(root);
  const dispose = behavior.bind({
    root,
    label,
    control: canvas,
    hint,
    error,
    onValidationChange: (hasError) => {
      canvas.style.borderColor = hasError ? "var(--formspec-tw-danger)" : "";
    }
  });
  actx.onDispose(dispose);
};

// node_modules/@formspec-org/adapters/dist/tailwind/wizard.js
var renderWizard3 = (behavior, parent, actx) => {
  const root = document.createElement("div");
  if (behavior.id)
    root.id = behavior.id;
  root.className = "formspec-wizard";
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(root, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(root, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(root, behavior.compOverrides.style);
  parent.appendChild(root);
  if (behavior.totalSteps() === 0)
    return;
  let stepIndicator;
  let stepElements;
  if (behavior.showProgress) {
    stepIndicator = document.createElement("nav");
    stepIndicator.className = "mb-8";
    stepIndicator.setAttribute("aria-label", "progress");
    const stepList = document.createElement("ol");
    stepList.className = "flex items-center";
    stepElements = [];
    for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
      const li = document.createElement("li");
      li.className = i2 < behavior.totalSteps() - 1 ? "relative flex-1 pr-8" : "relative";
      const stepContent = document.createElement("div");
      stepContent.className = "flex items-center";
      const circle = document.createElement("span");
      circle.className = "flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium";
      if (i2 === 0) {
        circle.style.backgroundColor = "var(--formspec-tw-accent)";
        circle.style.color = "var(--formspec-tw-accent-fg)";
      } else {
        circle.style.borderWidth = "2px";
        circle.style.borderStyle = "solid";
        circle.style.borderColor = "var(--formspec-tw-border)";
        circle.style.color = "var(--formspec-tw-muted)";
      }
      circle.textContent = String(i2 + 1);
      stepContent.appendChild(circle);
      const stepLabel = document.createElement("span");
      stepLabel.className = "ml-2 text-sm font-medium text-[var(--formspec-tw-text)]";
      stepLabel.textContent = behavior.steps[i2]?.title || `Step ${i2 + 1}`;
      stepContent.appendChild(stepLabel);
      li.appendChild(stepContent);
      if (i2 < behavior.totalSteps() - 1) {
        const connector = document.createElement("div");
        connector.className = "absolute right-0 top-4 h-0.5 w-full bg-[var(--formspec-tw-border)]";
        connector.style.left = "2rem";
        connector.style.right = "0";
        li.appendChild(connector);
      }
      stepList.appendChild(li);
      stepElements.push(li);
    }
    stepIndicator.appendChild(stepList);
    root.appendChild(stepIndicator);
  }
  const panels = [];
  for (let i2 = 0; i2 < behavior.totalSteps(); i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-wizard-panel";
    panel.setAttribute("role", "region");
    panel.setAttribute("aria-label", behavior.steps[i2]?.title || `Step ${i2 + 1}`);
    if (i2 !== 0)
      panel.classList.add("formspec-hidden");
    behavior.renderStep(i2, panel);
    root.appendChild(panel);
    panels.push(panel);
  }
  const nav = document.createElement("div");
  nav.className = "formspec-wizard-nav flex justify-between mt-6";
  const prevBtn = document.createElement("button");
  prevBtn.type = "button";
  prevBtn.className = TW.buttonOutline;
  prevBtn.textContent = "Previous";
  nav.appendChild(prevBtn);
  if (behavior.allowSkip) {
    const skipBtn = document.createElement("button");
    skipBtn.type = "button";
    skipBtn.className = TW.buttonUnstyled;
    skipBtn.textContent = "Skip";
    skipBtn.addEventListener("click", () => {
      if (behavior.canGoNext())
        behavior.goToStep(behavior.activeStep() + 1);
    });
    nav.appendChild(skipBtn);
  }
  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.className = TW.button;
  nextBtn.textContent = "Next";
  nav.appendChild(nextBtn);
  root.appendChild(nav);
  const dispose = behavior.bind({
    root,
    panels,
    stepIndicators: stepElements,
    stepContent: root,
    prevButton: prevBtn,
    nextButton: nextBtn
  });
  actx.onDispose(dispose);
  if (stepElements) {
    const updateIndicator = () => {
      const activeIdx = panels.findIndex((p2) => !p2.classList.contains("formspec-hidden"));
      if (activeIdx < 0)
        return;
      for (let i2 = 0; i2 < stepElements.length; i2++) {
        const circle = stepElements[i2].querySelector("span");
        circle.className = "flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium";
        circle.style.backgroundColor = "";
        circle.style.color = "";
        circle.style.borderWidth = "";
        circle.style.borderStyle = "";
        circle.style.borderColor = "";
        if (i2 === activeIdx) {
          circle.style.backgroundColor = "var(--formspec-tw-accent)";
          circle.style.color = "var(--formspec-tw-accent-fg)";
        } else if (i2 < activeIdx) {
          circle.style.backgroundColor = "var(--formspec-tw-success)";
          circle.style.color = "var(--formspec-tw-accent-fg)";
        } else {
          circle.style.borderWidth = "2px";
          circle.style.borderStyle = "solid";
          circle.style.borderColor = "var(--formspec-tw-border)";
          circle.style.color = "var(--formspec-tw-muted)";
        }
      }
    };
    const observer = new MutationObserver(updateIndicator);
    for (const panel of panels) {
      observer.observe(panel, { attributes: true, attributeFilter: ["style", "class"] });
    }
    actx.onDispose(() => observer.disconnect());
    updateIndicator();
  }
};

// node_modules/@formspec-org/adapters/dist/tailwind/tabs.js
var renderTabs3 = (behavior, parent, actx) => {
  const root = document.createElement("div");
  if (behavior.id)
    root.id = behavior.id;
  root.className = "formspec-tabs";
  if (behavior.position !== "top")
    root.dataset.position = behavior.position;
  if (behavior.compOverrides.cssClass)
    actx.applyCssClass(root, behavior.compOverrides);
  if (behavior.compOverrides.accessibility)
    actx.applyAccessibility(root, behavior.compOverrides);
  if (behavior.compOverrides.style)
    actx.applyStyle(root, behavior.compOverrides.style);
  parent.appendChild(root);
  const count = behavior.tabCount;
  const idBase = behavior.id || "tabs";
  const tabBar = document.createElement("div");
  tabBar.className = "border-b border-[color:var(--formspec-tw-border)]";
  const tabList = document.createElement("nav");
  tabList.className = "flex -mb-px space-x-4";
  tabList.setAttribute("role", "tablist");
  tabBar.appendChild(tabList);
  const panelContainer = document.createElement("div");
  panelContainer.className = "formspec-tab-panels mt-4";
  const panels = [];
  for (let i2 = 0; i2 < count; i2++) {
    const panel = document.createElement("div");
    panel.className = "formspec-tab-panel";
    panel.setAttribute("role", "tabpanel");
    panel.id = `${idBase}-panel-${i2}`;
    panel.setAttribute("aria-labelledby", `${idBase}-tab-${i2}`);
    panel.setAttribute("tabindex", "0");
    if (i2 !== behavior.defaultTab)
      panel.style.display = "none";
    behavior.renderTab(i2, panel);
    panelContainer.appendChild(panel);
    panels.push(panel);
  }
  const buttons = [];
  for (let i2 = 0; i2 < count; i2++) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.setAttribute("role", "tab");
    btn.id = `${idBase}-tab-${i2}`;
    btn.setAttribute("aria-controls", `${idBase}-panel-${i2}`);
    btn.setAttribute("aria-selected", i2 === behavior.defaultTab ? "true" : "false");
    btn.setAttribute("tabindex", i2 === behavior.defaultTab ? "0" : "-1");
    btn.textContent = behavior.tabLabels[i2] || `Tab ${i2 + 1}`;
    btn.className = i2 === behavior.defaultTab ? "border-b-2 border-[color:var(--formspec-tw-accent)] px-3 py-2 text-sm font-medium text-[var(--formspec-tw-accent)]" : "border-b-2 border-transparent px-3 py-2 text-sm font-medium text-[var(--formspec-tw-muted)] hover:border-[color:var(--formspec-tw-border)] hover:text-[var(--formspec-tw-text)]";
    tabList.appendChild(btn);
    buttons.push(btn);
  }
  if (behavior.position === "bottom") {
    root.appendChild(panelContainer);
    root.appendChild(tabBar);
  } else {
    root.appendChild(tabBar);
    root.appendChild(panelContainer);
  }
  const dispose = behavior.bind({ root, tabBar: tabList, panels, buttons });
  actx.onDispose(dispose);
  const updateButtonStyles = () => {
    for (let i2 = 0; i2 < buttons.length; i2++) {
      const isActive = buttons[i2].getAttribute("aria-selected") === "true";
      buttons[i2].className = isActive ? "border-b-2 border-[color:var(--formspec-tw-accent)] px-3 py-2 text-sm font-medium text-[var(--formspec-tw-accent)]" : "border-b-2 border-transparent px-3 py-2 text-sm font-medium text-[var(--formspec-tw-muted)] hover:border-[color:var(--formspec-tw-border)] hover:text-[var(--formspec-tw-text)]";
    }
  };
  const observer = new MutationObserver(updateButtonStyles);
  for (const btn of buttons) {
    observer.observe(btn, { attributes: true, attributeFilter: ["aria-selected"] });
  }
  actx.onDispose(() => observer.disconnect());
};

// node_modules/@formspec-org/adapters/dist/tailwind/index.js
var tailwindAdapter = {
  name: "tailwind",
  components: {
    TextInput: renderTextInput3,
    NumberInput: renderNumberInput3,
    RadioGroup: renderRadioGroup3,
    CheckboxGroup: renderCheckboxGroup3,
    Select: renderSelect3,
    DatePicker: renderDatePicker3,
    Checkbox: renderCheckbox3,
    Toggle: renderToggle3,
    MoneyInput: renderMoneyInput3,
    Slider: renderSlider3,
    Rating: renderRating3,
    FileUpload: renderFileUpload3,
    Signature: renderSignature3,
    Wizard: renderWizard3,
    Tabs: renderTabs3
  }
};

// node_modules/@formspec-org/engine/dist/fel/fel-api-runtime.js
init_wasm_bridge_runtime();

// node_modules/@formspec-org/engine/dist/fel/fel-api-tools.js
init_wasm_bridge_tools();

// node_modules/@formspec-org/engine/dist/mapping/RuntimeMappingEngine.js
init_wasm_bridge_tools();

// node_modules/@formspec-org/engine/dist/index.js
init_wasm_bridge_runtime();
init_wasm_bridge_tools();

// node_modules/@formspec-org/engine/dist/assembly/assembleDefinition.js
init_wasm_bridge_tools();
export {
  ComponentRegistry,
  FormspecRender,
  dist_exports as adapters,
  applyResponseDataToEngine,
  buildInitialScreenerAnswers,
  createSignatureCanvas,
  default_theme_default as defaultTheme,
  extractScreenerSeedFromData,
  formatMoney,
  getDefaultComponent,
  globalRegistry,
  initFormspecEngine,
  interpolateParams,
  normalizeScreenerSeedForItem,
  omitScreenerKeysFromData,
  resolvePresentation,
  resolveResponsiveProps,
  resolveToken,
  resolveWidget,
  screenerAnswersSatisfyRequired
};
