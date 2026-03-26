#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const packageRoot = path.resolve(__dirname, "..");
const ignoredDirectoryNames = new Set(["__pycache__"]);
const payloadRoots = [
  "AGENTS.md",
  ".agents",
  ".codex",
  ".github",
  "docs",
  "plans",
  "runbooks",
  "scripts",
];
const gitignoreFragmentPath = path.join(packageRoot, "installer", "gitignore.fragment");

function printUsage() {
  console.log(`create-codexkit

Usage:
  npm create codexkit@latest <directory>
  npx create-codexkit@latest init .
  npx create-codexkit@latest new <directory>

Commands:
  new <directory>     Create a new directory and install CodexKit into it
  init [directory]    Install CodexKit into an existing directory (default: .)
  help                Show this help message

Options:
  --force             Overwrite conflicting files in the target directory

Notes:
  - \`npm create codexkit@latest my-repo\` is equivalent to \`create-codexkit new my-repo\`
  - After install, run \`python3 scripts/bootstrap-codexkit.py --apply\`
  - In Codex, \`/ck:new-project\` is supported as an alias of \`/ck:project\`
`);
}

function fail(message, code = 1) {
  console.error(`[create-codexkit] ${message}`);
  process.exit(code);
}

function parseArgs(argv) {
  const args = [...argv];
  let force = false;
  const positional = [];

  for (const arg of args) {
    if (arg === "--force") {
      force = true;
    } else {
      positional.push(arg);
    }
  }

  if (positional.length === 0) {
    return { command: "help", target: null, force };
  }

  const [first, second] = positional;
  if (first === "help" || first === "--help" || first === "-h") {
    return { command: "help", target: null, force };
  }
  if (first === "init") {
    return { command: "init", target: second || ".", force };
  }
  if (first === "new") {
    return { command: "new", target: second, force };
  }

  return { command: "new", target: first, force };
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function walkFiles(rootPath) {
  const entries = [];
  const stat = fs.statSync(rootPath);
  if (stat.isFile()) {
    if (rootPath.endsWith(".pyc")) {
      return [];
    }
    return [rootPath];
  }

  for (const entry of fs.readdirSync(rootPath, { withFileTypes: true })) {
    if (entry.isDirectory() && ignoredDirectoryNames.has(entry.name)) {
      continue;
    }
    const childPath = path.join(rootPath, entry.name);
    if (entry.isDirectory()) {
      entries.push(...walkFiles(childPath));
    } else if (entry.isFile()) {
      if (entry.name.endsWith(".pyc")) {
        continue;
      }
      entries.push(childPath);
    }
  }
  return entries;
}

function collectPayloadFiles() {
  return payloadRoots.flatMap((relativePath) => {
    const absolutePath = path.join(packageRoot, relativePath);
    if (!fs.existsSync(absolutePath)) {
      fail(`installer payload is missing: ${relativePath}`);
    }
    return walkFiles(absolutePath);
  });
}

function fileContentsEqual(a, b) {
  const aBuffer = fs.readFileSync(a);
  const bBuffer = fs.readFileSync(b);
  return Buffer.compare(aBuffer, bBuffer) === 0;
}

function relativeToPackageRoot(filePath) {
  return path.relative(packageRoot, filePath);
}

function detectConflicts(targetRoot, files, force) {
  const conflicts = [];
  for (const sourceFile of files) {
    const relativePath = relativeToPackageRoot(sourceFile);
    const targetFile = path.join(targetRoot, relativePath);
    if (!fs.existsSync(targetFile)) {
      continue;
    }
    if (fileContentsEqual(sourceFile, targetFile)) {
      continue;
    }
    if (!force) {
      conflicts.push(relativePath);
    }
  }
  return conflicts;
}

function copyFile(sourceFile, targetRoot, stats, force) {
  const relativePath = relativeToPackageRoot(sourceFile);
  const targetFile = path.join(targetRoot, relativePath);

  ensureDir(path.dirname(targetFile));

  if (fs.existsSync(targetFile)) {
    if (fileContentsEqual(sourceFile, targetFile)) {
      stats.unchanged += 1;
      return;
    }
    if (!force) {
      return;
    }
    stats.updated += 1;
  } else {
    stats.copied += 1;
  }

  fs.copyFileSync(sourceFile, targetFile);
  const sourceMode = fs.statSync(sourceFile).mode;
  fs.chmodSync(targetFile, sourceMode);
}

function mergeGitignore(targetRoot) {
  const targetFile = path.join(targetRoot, ".gitignore");
  const fragment = fs.readFileSync(gitignoreFragmentPath, "utf8").trimEnd();
  const start = "# >>> codexkit >>>";
  const end = "# <<< codexkit <<<";
  const block = `${start}\n${fragment}\n${end}\n`;

  if (!fs.existsSync(targetFile)) {
    fs.writeFileSync(targetFile, `${block}`, "utf8");
    return "created";
  }

  const current = fs.readFileSync(targetFile, "utf8");
  const startIndex = current.indexOf(start);
  const endIndex = current.indexOf(end);

  if (startIndex !== -1 && endIndex !== -1 && endIndex > startIndex) {
    const before = current.slice(0, startIndex);
    const after = current.slice(endIndex + end.length).replace(/^\n+/, "");
    const merged = `${before}${block}${after ? `\n${after}` : ""}`.replace(/\n{3,}/g, "\n\n");
    fs.writeFileSync(targetFile, merged.endsWith("\n") ? merged : `${merged}\n`, "utf8");
    return "updated";
  }

  const separator = current.endsWith("\n") ? "\n" : "\n\n";
  fs.writeFileSync(targetFile, `${current}${separator}${block}`, "utf8");
  return "appended";
}

function installInto(targetRoot, force) {
  const payloadFiles = collectPayloadFiles();
  const conflicts = detectConflicts(targetRoot, payloadFiles, force);

  if (conflicts.length > 0) {
    console.error("[create-codexkit] install aborted because these files already exist and differ:");
    for (const conflict of conflicts) {
      console.error(`  - ${conflict}`);
    }
    console.error("[create-codexkit] re-run with --force if you want to overwrite those files deliberately.");
    process.exit(1);
  }

  const stats = { copied: 0, updated: 0, unchanged: 0 };
  ensureDir(targetRoot);

  for (const sourceFile of payloadFiles) {
    copyFile(sourceFile, targetRoot, stats, force);
  }

  const gitignoreStatus = mergeGitignore(targetRoot);
  return { ...stats, gitignoreStatus };
}

function printNextSteps(targetRoot, mode) {
  console.log(`[create-codexkit] ${mode === "new" ? "created" : "updated"} ${targetRoot}`);
  console.log("[create-codexkit] next steps:");
  console.log(`  1. cd ${targetRoot}`);
  console.log("  2. python3 scripts/bootstrap-codexkit.py --apply");
  console.log("  3. scripts/check-kit.sh");
  console.log("  4. In Codex, try /ck:new-project billing-platform or /ck:feature tenant-rate-limits");
}

function main() {
  const { command, target, force } = parseArgs(process.argv.slice(2));
  if (command === "help") {
    printUsage();
    return;
  }
  if (!target) {
    fail("missing target directory. Run with `help` to see examples.");
  }

  const targetRoot = path.resolve(process.cwd(), target);
  if (command === "new" && fs.existsSync(targetRoot) && fs.readdirSync(targetRoot).length > 0) {
    fail(`target directory already exists and is not empty: ${target}`);
  }

  const result = installInto(targetRoot, force);
  console.log(`[create-codexkit] copied ${result.copied} files`);
  console.log(`[create-codexkit] updated ${result.updated} files`);
  console.log(`[create-codexkit] unchanged ${result.unchanged} files`);
  console.log(`[create-codexkit] .gitignore ${result.gitignoreStatus}`);
  printNextSteps(targetRoot, command);
}

main();
