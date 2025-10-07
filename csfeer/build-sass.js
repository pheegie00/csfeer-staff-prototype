const sass = require("sass");
const fs = require("fs");
const path = require("path");
const chokidar = require("chokidar");

function validateAndNormalizePath(targetPath, basePath = __dirname) {
  if (!targetPath || typeof targetPath !== "string")
    throw new Error("Invalid path: Path must be a non-empty string");

  const normalizedPath = path.normalize(targetPath);

  if (normalizedPath.includes("..") || normalizedPath.includes("\x00"))
    throw new Error(
      `Invalid path specified: Path '${targetPath}' contains forbidden characters or patterns`
    );

  const normalizedBasePath = path.resolve(basePath);
  const normalizedTargetPath = path.resolve(normalizedBasePath, normalizedPath);

  if (
    !normalizedTargetPath.startsWith(normalizedBasePath + path.sep) &&
    normalizedTargetPath !== normalizedBasePath
  )
    throw new Error(
      `Invalid path specified: Path '${targetPath}' is outside the allowed directory '${basePath}'`
    );

  console.log(`🔒 Validated path: ${targetPath} → ${normalizedTargetPath}`);
  return normalizedTargetPath;
}

const inputFile = validateAndNormalizePath(path.join("styles", "styles.scss"));
const outputFile = validateAndNormalizePath(path.join("static", "styles.css"));

function compileSass() {
  try {
    const result = sass.compile(inputFile, {
      style: process.env.NODE_ENV === "production" ? "compressed" : "expanded",
      sourceMap: process.env.NODE_ENV !== "production",
      quietDeps: true,
      loadPaths: [
        validateAndNormalizePath(path.join("node_modules")),
        validateAndNormalizePath(
          path.join("node_modules", "@uswds", "uswds", "packages")
        ),
      ],
    });

    const outputDir = validateAndNormalizePath(path.dirname(outputFile));
    // nosemgrep
    if (!fs.existsSync(outputDir)) {
      // nosemgrep
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // nosemgrep
    fs.writeFileSync(outputFile, result.css);
    console.log(`✅ Compiled: ${inputFile} → ${outputFile}`);
  } catch (error) {
    if (error.message.includes("Invalid path")) {
      console.error("🔒 Security error:", error.message);
    } else {
      console.error("❌ SASS compilation error:", error.message);
    }
    process.exit(1);
  }
}

const isWatchMode = process.argv.includes("--watch");

if (isWatchMode) {
  console.log("👀 Watching for changes...");

  compileSass();

  const watcher = chokidar.watch(
    [
      validateAndNormalizePath(path.join("src", "**", "*.scss")),
      validateAndNormalizePath(path.join("src", "**", "*.sass")),
    ],
    {
      ignoreInitial: true,
    }
  );

  watcher.on("change", (filePath) => {
    console.log(`📝 Changed: ${path.relative(__dirname, filePath)}`);
    compileSass();
  });

  watcher.on("add", (filePath) => {
    console.log(`➕ Added: ${path.relative(__dirname, filePath)}`);
    compileSass();
  });
} else {
  // Single compilation
  compileSass();
}
