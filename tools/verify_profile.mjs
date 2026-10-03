// Validate content retention and local images without network requests.
import { readFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';

const current = readFileSync('README.md', 'utf8');
const original = execFileSync('git', ['show', 'HEAD:README.md'], { encoding: 'utf8' });
const paragraphs = original.split(/\r?\n/).filter(line =>
  /^(I am |I use |My present |Alongside |Long term,|\*\*Problem\*\*|\*\*Built\*\*)/.test(line));
for (const paragraph of paragraphs) assert.ok(current.includes(paragraph), `Missing copy: ${paragraph}`);
for (const [, href] of original.matchAll(/\]\((https?:\/\/[^)]+|mailto:[^)]+)\)/g)) {
  assert.ok(current.includes(href), `Missing link: ${href}`);
}
for (const [, src] of current.matchAll(/src="([^"]+)"/g)) {
  assert.ok(existsSync(src), `Missing image: ${src}`);
}
assert.ok(!current.includes('.svg'), 'Retired SVG still used');
assert.equal(readFileSync('assets/hedron-study.gif').subarray(0, 6).toString(), 'GIF89a');
console.log(`Verified ${paragraphs.length} original paragraphs, all original link targets, and local image references.`);
