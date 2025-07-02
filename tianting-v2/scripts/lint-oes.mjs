import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Simple OES task JSON validator
// Usage: node scripts/lint-oes.mjs [rootDir]
// - Looks for any .json file under "tasks" folders and validates against the JSON Schema
//   embedded in docs/06-oes-spec.md.
// - Exits with code 1 if any validation fails.

const __filename = fileURLToPath(import.meta.url);
const projectRoot = path.resolve(path.dirname(__filename), '..'); // tianting-v2 root
const schemaMarkdownPath = path.join(projectRoot, 'docs', '06-oes-spec.md');

async function extractJsonSchema(markdownFile) {
  const md = await fs.readFile(markdownFile, 'utf8');
  const matches = [...md.matchAll(/```json\s*([\s\S]*?)\s*```/g)];
  if (!matches.length) {
    throw new Error('JSON schema block not found in 06-oes-spec.md');
  }
  const schemaStr = matches[matches.length-1][1];
  try {
    return JSON.parse(schemaStr);
  } catch (err) {
    throw new Error('Failed to parse JSON schema from markdown: ' + err.message);
  }
}

async function collectTaskJsonFiles(startDir) {
  const files = [];
  async function walk(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      // Skip node_modules and dot dirs
      if (entry.name.startsWith('.')) continue;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
      } else if (
        entry.isFile() &&
        entry.name.endsWith('.json') &&
        fullPath.includes(`${path.sep}tasks${path.sep}`)
      ) {
        files.push(fullPath);
      }
    }
  }
  await walk(startDir);
  return files;
}

async function main() {
  // Allow overriding root via CLI
  const rootDir = process.argv[2] ? path.resolve(process.argv[2]) : projectRoot;

  let schema;
  try {
    schema = await extractJsonSchema(schemaMarkdownPath);
  } catch (err) {
    console.error('[lint-oes] Error extracting schema:', err.message);
    process.exit(1);
  }

  const Ajv = (await import('ajv')).default;
  const ajv = new Ajv({ allErrors: true, allowUnionTypes: true });
  const validate = ajv.compile(schema);

  const jsonFiles = await collectTaskJsonFiles(rootDir);
  if (jsonFiles.length === 0) {
    console.log('[lint-oes] No task JSON files found. Nothing to validate.');
    return;
  }

  let hasError = false;
  for (const file of jsonFiles) {
    try {
      const content = await fs.readFile(file, 'utf8');
      const data = JSON.parse(content);
      const valid = validate(data);
      if (!valid) {
        hasError = true;
        console.error(`❌ ${file}`);
        console.error(validate.errors);
      } else {
        console.log(`✅ ${file}`);
      }
    } catch (err) {
      hasError = true;
      console.error(`❌ ${file} – ${err.message}`);
    }
  }

  if (hasError) {
    console.error('\nValidation failed.');
    process.exit(1);
  } else {
    console.log('\nAll task files passed validation.');
  }
}

main().catch((err) => {
  console.error('[lint-oes] Unexpected error:', err);
  process.exit(1);
}); 