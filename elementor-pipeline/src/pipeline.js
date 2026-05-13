import { fetchGoogleDoc } from './fetch-gdoc.js';
import { fetchFigmaFile } from './fetch-figma.js';
import {
  extractContentSpec,
  extractDesignSpec,
  mergeSpecs,
  generateElementorPage,
  runQaCheck,
} from './claude-client.js';
import { writeOutput } from './output.js';

export async function runPipeline({ gdocUrl, figmaUrl, skipQa = false, verbose = false }) {
  const results = {};

  log('=== UWorld Elementor Build Pipeline ===\n', verbose);

  // ── STAGE 1: Fetch Google Doc ──────────────────────────────────────────────
  log('▶ Stage 1 — Fetching Google Doc content...', verbose);
  const { text: docText } = await fetchGoogleDoc(gdocUrl);
  log(`  ✓ Doc fetched (${docText.length} chars)`, verbose);

  // ── STAGE 2: Fetch Figma File ──────────────────────────────────────────────
  log('▶ Stage 2 — Fetching Figma design data...', verbose);
  const figmaData = await fetchFigmaFile(figmaUrl, process.env.FIGMA_TOKEN);
  log(`  ✓ Figma file "${figmaData.fileName}" fetched (${figmaData.frames.length} frames)`, verbose);

  // ── STAGE 3: Extract Content Spec via Claude ───────────────────────────────
  log('▶ Stage 3 — Extracting content spec (Claude)...', verbose);
  const contentSpec = await extractContentSpec(docText);
  results.contentSpec = contentSpec;
  log(`  ✓ Content spec: ${contentSpec.sections?.length ?? 0} sections, page type: ${contentSpec.page_meta?.page_type}`, verbose);
  if (contentSpec.missing_content?.length) {
    log(`  ⚠ Missing content: ${contentSpec.missing_content.join(', ')}`, verbose);
  }

  // ── STAGE 4: Extract Design Spec via Claude ────────────────────────────────
  log('▶ Stage 4 — Extracting design spec (Claude)...', verbose);
  const designSpec = await extractDesignSpec(figmaData);
  results.designSpec = designSpec;
  log(`  ✓ Design spec: ${designSpec.sections?.length ?? 0} sections, ${Object.keys(designSpec.design_tokens?.colors ?? {}).length} color tokens`, verbose);

  // ── STAGE 5: Merge Specs ───────────────────────────────────────────────────
  log('▶ Stage 5 — Merging specs (Claude)...', verbose);
  const pageSpec = await mergeSpecs(contentSpec, designSpec);
  results.pageSpec = pageSpec;
  const readySections = pageSpec.sections?.filter(s => s.status === 'ready').length ?? 0;
  const missingDesign = pageSpec.missing_design?.length ?? 0;
  const missingContent = pageSpec.missing_content?.length ?? 0;
  log(`  ✓ Merged: ${readySections} ready, ${missingDesign} design-missing, ${missingContent} content-missing`, verbose);

  // ── STAGE 6: Generate Elementor Page ──────────────────────────────────────
  log('▶ Stage 6 — Generating Elementor page (Claude)...', verbose);
  const { html, checklist, handoff } = await generateElementorPage(pageSpec);
  results.html = html;
  results.checklist = checklist;
  results.handoff = handoff;
  log(`  ✓ HTML generated (${html.length} chars)`, verbose);

  // ── STAGE 7: QA Check ─────────────────────────────────────────────────────
  if (!skipQa) {
    log('▶ Stage 7 — Running QA checks (Claude)...', verbose);
    const qaReport = await runQaCheck(pageSpec, html);
    results.qaReport = qaReport;
    log('  ✓ QA report generated', verbose);
  }

  // ── Write Output Files ─────────────────────────────────────────────────────
  log('▶ Writing output files...', verbose);
  const outputPaths = await writeOutput(results, pageSpec);
  log(`  ✓ Files written to: ${outputPaths.dir}`, verbose);

  log('\n=== Pipeline Complete ===', verbose);
  return { ...results, outputPaths };
}

function log(msg, verbose) {
  if (verbose || msg.startsWith('=') || msg.startsWith('▶')) {
    process.stdout.write(msg + '\n');
  }
}
