#!/usr/bin/env node
import 'dotenv/config';
import { runPipeline } from './pipeline.js';

const args = process.argv.slice(2);

if (args.includes('--help') || args.length === 0) {
  console.log(`
UWorld Elementor Pipeline
=========================
Usage:
  node src/index.js --gdoc <google-doc-url> --figma <figma-url> [options]

Options:
  --gdoc    <url>   Google Docs URL (must be shared publicly or via your account)
  --figma   <url>   Figma file or design URL
  --skip-qa         Skip the QA stage (faster for drafts)
  --verbose         Show detailed progress logs
  --help            Show this help

Examples:
  node src/index.js \\
    --gdoc "https://docs.google.com/document/d/YOUR_DOC_ID/edit" \\
    --figma "https://www.figma.com/design/YOUR_FILE_KEY/Page-Name" \\
    --verbose

Environment:
  Copy .env.example → .env and fill in your API keys before running.

Output:
  Files are written to OUTPUT_DIR (default: ./output/{date}-{slug}/)
    page_spec.json          — merged content + design spec
    {slug}-elementor.html   — Elementor preview HTML
    elementor-checklist.txt — step-by-step widget build guide
    developer-handoff.txt   — CSS tokens, fonts, missing assets
    qa-report.txt           — pre-flight QA results
    manifest.json           — build summary
`);
  process.exit(0);
}

function getArg(flag) {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] : null;
}

const gdocUrl = getArg('--gdoc');
const figmaUrl = getArg('--figma');
const skipQa = args.includes('--skip-qa');
const verbose = args.includes('--verbose');

if (!gdocUrl) {
  console.error('Error: --gdoc <url> is required');
  process.exit(1);
}
if (!figmaUrl) {
  console.error('Error: --figma <url> is required');
  process.exit(1);
}
if (!process.env.ANTHROPIC_API_KEY) {
  console.error('Error: ANTHROPIC_API_KEY is not set. Copy .env.example → .env and add your key.');
  process.exit(1);
}

try {
  const result = await runPipeline({ gdocUrl, figmaUrl, skipQa, verbose });

  console.log('\n✅ Build complete!');
  console.log(`📁 Output folder: ${result.outputPaths.dir}`);
  console.log(`🌐 HTML preview:  ${result.outputPaths.html ?? 'N/A'}`);
  console.log(`📋 Checklist:     ${result.outputPaths.checklist ?? 'N/A'}`);
  console.log(`📝 Handoff notes: ${result.outputPaths.handoff ?? 'N/A'}`);
  if (!skipQa) {
    console.log(`🔍 QA report:     ${result.outputPaths.qa ?? 'N/A'}`);
  }
} catch (err) {
  console.error('\n❌ Pipeline failed:', err.message);
  if (verbose) console.error(err.stack);
  process.exit(1);
}
