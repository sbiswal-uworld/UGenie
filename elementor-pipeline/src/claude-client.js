import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const MODEL = process.env.CLAUDE_MODEL ?? 'claude-sonnet-4-6';

async function loadPrompt(name) {
  const p = join(__dirname, '..', 'prompts', `${name}.txt`);
  return readFile(p, 'utf8');
}

/**
 * Ask Claude to extract and structure content from a Google Doc.
 * Returns parsed JSON (content_spec).
 */
export async function extractContentSpec(docText) {
  const systemPrompt = await loadPrompt('normalize-content');

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 4096,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Here is the Google Doc content to extract:\n\n---\n${docText}\n---\n\nReturn strict JSON only.`,
      },
    ],
  });

  return parseJsonResponse(response, 'content_spec');
}

/**
 * Ask Claude to extract design tokens and layout from Figma data.
 * Returns parsed JSON (design_spec).
 */
export async function extractDesignSpec(figmaData) {
  const systemPrompt = await loadPrompt('normalize-design');

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 4096,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Here is the Figma file data to extract:\n\n${JSON.stringify(figmaData, null, 2)}\n\nReturn strict JSON only.`,
      },
    ],
  });

  return parseJsonResponse(response, 'design_spec');
}

/**
 * Ask Claude to merge content_spec + design_spec into a single page_spec.
 * Returns parsed JSON (page_spec).
 */
export async function mergeSpecs(contentSpec, designSpec) {
  const systemPrompt = await loadPrompt('normalize-merge');

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 8192,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Merge these two specs into a single page_spec:\n\nCONTENT SPEC:\n${JSON.stringify(contentSpec, null, 2)}\n\nDESIGN SPEC:\n${JSON.stringify(designSpec, null, 2)}\n\nReturn strict JSON only.`,
      },
    ],
  });

  return parseJsonResponse(response, 'page_spec');
}

/**
 * Ask Claude to generate complete Elementor HTML from a page_spec.
 * Returns { html, checklist, handoff } strings.
 */
export async function generateElementorPage(pageSpec) {
  const systemPrompt = await loadPrompt('generate-elementor');

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 16384,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Generate the complete Elementor page package from this page spec:\n\n${JSON.stringify(pageSpec, null, 2)}`,
      },
    ],
  });

  const raw = response.content[0].text;
  return parseElementorResponse(raw);
}

/**
 * Ask Claude to run QA checks against the page spec and generated HTML.
 * Returns a structured QA report.
 */
export async function runQaCheck(pageSpec, generatedHtml) {
  const systemPrompt = await loadPrompt('qa-check');

  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 4096,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: `Run QA on this page.\n\nPAGE SPEC:\n${JSON.stringify(pageSpec, null, 2)}\n\nGENERATED HTML:\n${generatedHtml}`,
      },
    ],
  });

  return response.content[0].text;
}

function parseJsonResponse(response, label) {
  const raw = response.content[0].text.trim();
  // Strip markdown fences if Claude added them despite instructions
  const cleaned = raw.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '');
  try {
    return JSON.parse(cleaned);
  } catch (e) {
    throw new Error(`Claude returned invalid JSON for ${label}:\n${cleaned.slice(0, 500)}`);
  }
}

function parseElementorResponse(raw) {
  // The generate prompt asks Claude to output sections delimited by markers
  const htmlMatch = raw.match(/<!-- ELEMENTOR_HTML_START -->([\s\S]*?)<!-- ELEMENTOR_HTML_END -->/);
  const checklistMatch = raw.match(/<!-- CHECKLIST_START -->([\s\S]*?)<!-- CHECKLIST_END -->/);
  const handoffMatch = raw.match(/<!-- HANDOFF_START -->([\s\S]*?)<!-- HANDOFF_END -->/);

  return {
    html: htmlMatch ? htmlMatch[1].trim() : raw,
    checklist: checklistMatch ? checklistMatch[1].trim() : '',
    handoff: handoffMatch ? handoffMatch[1].trim() : '',
  };
}
