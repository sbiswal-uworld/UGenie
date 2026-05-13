import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

export async function writeOutput(results, pageSpec) {
  const outputDir = process.env.OUTPUT_DIR ?? './output';
  const slug = slugify(pageSpec.page_meta?.page_title ?? 'page');
  const timestamp = new Date().toISOString().slice(0, 10);
  const dir = join(outputDir, `${timestamp}-${slug}`);

  await mkdir(dir, { recursive: true });

  const paths = { dir };

  // page_spec.json
  if (results.pageSpec) {
    paths.spec = join(dir, 'page_spec.json');
    await writeFile(paths.spec, JSON.stringify(results.pageSpec, null, 2), 'utf8');
  }

  // Elementor preview HTML
  if (results.html) {
    paths.html = join(dir, `${slug}-elementor.html`);
    await writeFile(paths.html, results.html, 'utf8');
  }

  // Elementor build checklist
  if (results.checklist) {
    paths.checklist = join(dir, 'elementor-checklist.txt');
    await writeFile(paths.checklist, results.checklist, 'utf8');
  }

  // Developer handoff notes
  if (results.handoff) {
    paths.handoff = join(dir, 'developer-handoff.txt');
    await writeFile(paths.handoff, results.handoff, 'utf8');
  }

  // QA report
  if (results.qaReport) {
    paths.qa = join(dir, 'qa-report.txt');
    await writeFile(paths.qa, results.qaReport, 'utf8');
  }

  // Raw content spec
  if (results.contentSpec) {
    paths.contentSpec = join(dir, 'content_spec.json');
    await writeFile(paths.contentSpec, JSON.stringify(results.contentSpec, null, 2), 'utf8');
  }

  // Raw design spec
  if (results.designSpec) {
    paths.designSpec = join(dir, 'design_spec.json');
    await writeFile(paths.designSpec, JSON.stringify(results.designSpec, null, 2), 'utf8');
  }

  // Summary manifest
  const manifest = {
    built_at: new Date().toISOString(),
    page_title: pageSpec.page_meta?.page_title,
    page_type: pageSpec.page_meta?.page_type,
    target_keyword: pageSpec.page_meta?.target_keyword,
    sections_built: results.pageSpec?.sections?.length ?? 0,
    files: Object.fromEntries(
      Object.entries(paths)
        .filter(([k]) => k !== 'dir')
        .map(([k, v]) => [k, v.replace(dir + '/', '')])
    ),
  };
  paths.manifest = join(dir, 'manifest.json');
  await writeFile(paths.manifest, JSON.stringify(manifest, null, 2), 'utf8');

  return paths;
}

function slugify(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 50);
}
