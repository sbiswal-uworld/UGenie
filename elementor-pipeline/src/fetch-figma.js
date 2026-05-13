import fetch from 'node-fetch';

/**
 * Extract the file key from a Figma URL.
 * Handles /file/{KEY}/... and /design/{KEY}/... forms.
 */
function extractFigmaKey(url) {
  const match = url.match(/\/(file|design)\/([a-zA-Z0-9]+)/);
  if (!match) throw new Error(`Cannot parse Figma file key from URL: ${url}`);
  return match[2];
}

/**
 * Fetch top-level file metadata + first page nodes from Figma REST API.
 * Returns a simplified structure suitable for passing to Claude.
 */
export async function fetchFigmaFile(urlOrKey, figmaToken) {
  if (!figmaToken) {
    throw new Error(
      'FIGMA_TOKEN is required. Get yours at https://www.figma.com/developers/api#access-tokens and add it to .env'
    );
  }

  const fileKey = urlOrKey.includes('figma.com')
    ? extractFigmaKey(urlOrKey)
    : urlOrKey;

  const baseUrl = `https://api.figma.com/v1/files/${fileKey}`;

  const res = await fetch(baseUrl, {
    headers: {
      'X-Figma-Token': figmaToken,
      'Content-Type': 'application/json',
    },
  });

  if (res.status === 403 || res.status === 401) {
    throw new Error('Figma auth error. Check that your FIGMA_TOKEN is valid and has read access to this file.');
  }
  if (!res.ok) {
    throw new Error(`Figma API error: ${res.status} ${res.statusText}`);
  }

  const data = await res.json();

  // Reduce the response to relevant fields only — full Figma JSON can be 10MB+
  return simplifyFigmaResponse(data, fileKey);
}

function simplifyFigmaResponse(data, fileKey) {
  const firstPage = data.document?.children?.[0];
  const frames = (firstPage?.children ?? [])
    .filter(n => n.type === 'FRAME' || n.type === 'COMPONENT')
    .slice(0, 20) // cap at 20 frames to stay within Claude context
    .map(frame => ({
      id: frame.id,
      name: frame.name,
      type: frame.type,
      width: frame.absoluteBoundingBox?.width,
      height: frame.absoluteBoundingBox?.height,
      background: extractFill(frame.background ?? frame.fills),
      children: (frame.children ?? []).slice(0, 30).map(child => ({
        id: child.id,
        name: child.name,
        type: child.type,
        text: child.characters ?? null,
        fills: extractFill(child.fills),
        strokes: extractFill(child.strokes),
        cornerRadius: child.cornerRadius ?? null,
        style: child.style
          ? {
              fontFamily: child.style.fontFamily,
              fontSize: child.style.fontSize,
              fontWeight: child.style.fontWeight,
              lineHeightPx: child.style.lineHeightPx,
            }
          : null,
        effects: (child.effects ?? []).map(e => ({ type: e.type, radius: e.radius })),
      })),
    }));

  return {
    fileKey,
    fileName: data.name,
    lastModified: data.lastModified,
    thumbnailUrl: data.thumbnailUrl,
    frames,
  };
}

function extractFill(fills) {
  if (!fills || !fills.length) return null;
  const solid = fills.find(f => f.type === 'SOLID' && f.visible !== false);
  if (!solid) return null;
  const { r, g, b, a } = solid.color;
  const toHex = v => Math.round(v * 255).toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}
