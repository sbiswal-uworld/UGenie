import fetch from 'node-fetch';

/**
 * Extract the document ID from a Google Docs URL.
 * Handles both /document/d/{ID}/edit and /document/d/{ID} forms.
 */
function extractDocId(url) {
  const match = url.match(/\/document\/d\/([a-zA-Z0-9_-]+)/);
  if (!match) throw new Error(`Cannot parse Google Docs ID from URL: ${url}`);
  return match[1];
}

/**
 * Fetch a Google Doc as plain text using the public export endpoint.
 * Works for documents shared as "Anyone with the link can view".
 */
export async function fetchGoogleDoc(urlOrId) {
  const docId = urlOrId.includes('docs.google.com')
    ? extractDocId(urlOrId)
    : urlOrId;

  const exportUrl = `https://docs.google.com/document/d/${docId}/export?format=txt`;

  const res = await fetch(exportUrl, {
    headers: { 'User-Agent': 'UWorld-Pipeline/1.0' },
    redirect: 'follow',
  });

  if (res.status === 403 || res.status === 401) {
    throw new Error(
      `Google Docs auth error (${res.status}). Make sure the document is shared as "Anyone with the link can view".`
    );
  }
  if (!res.ok) {
    throw new Error(`Google Docs fetch failed: ${res.status} ${res.statusText}`);
  }

  const text = await res.text();
  if (!text || text.trim().length < 50) {
    throw new Error('Google Doc returned empty or very short content. Check sharing permissions.');
  }

  return { docId, text };
}
