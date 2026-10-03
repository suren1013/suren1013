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
for (const [, src] of current.matchAll(/srcset="([^"]+)"/g)) assert.ok(existsSync(src), `Missing compact image: ${src}`);
assert.ok(!current.includes('.svg'), 'Retired SVG still used');
assert.equal(readFileSync('assets/hedron-study.gif').subarray(0, 6).toString(), 'GIF89a');
if (existsSync('STILL.md')) {
  const still = readFileSync('STILL.md', 'utf8');
  assert.ok(!still.includes('.gif'), 'Still profile includes motion');
  for (const paragraph of paragraphs) assert.ok(still.includes(paragraph), `Still profile missing copy: ${paragraph}`);
  for (const [, src] of still.matchAll(/src="([^"]+)"/g)) assert.ok(existsSync(src), `Missing still image: ${src}`);
  const expected = current.replace(/\.\/assets\/([\w-]+)\.gif/g, (_,name) => `./assets/${name==='hedron-study'?'hedron-study-still':name}.png`)
    .replace('[Still version — no motion](./STILL.md)', '[View the motion version](./README.md)')
    .replace('[View the complete still version →](./STILL.md)', '[Return to the motion version →](./README.md)');
  assert.equal(still, expected, 'Still version content is out of sync');
}
for (const tool of ['OpenFOAM','ANSYS','SolidWorks','CFD','FEA','Heat Transfer','Python','TypeScript','JavaScript','React','Next.js','Java','Git','GitHub','VS Code','LangChain']) {
  assert.ok(current.includes(tool), `Missing selectable technology: ${tool}`);
}
const activity=JSON.parse(readFileSync('assets/activity-data.json','utf8'));
assert.equal(activity.total, activity.days.reduce((sum,day)=>sum+day.count,0));
assert.equal(activity.active_days, activity.days.filter(day=>day.count>0).length);
for (const [, href] of current.matchAll(/\]\((\.\/[^)#]+)(?:#[^)]*)?\)/g)) assert.ok(existsSync(href), `Missing local link: ${href}`);
console.log(`Verified ${paragraphs.length} original paragraphs, all original link targets, and local image references.`);
