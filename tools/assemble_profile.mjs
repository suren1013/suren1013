// Build both GitHub profile variants from preserved, selectable source copy.
import {readFileSync,writeFileSync,existsSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
process.chdir(root);
const contentPath='profile/content.json';
let content;
if(existsSync(contentPath)) content=JSON.parse(readFileSync(contentPath,'utf8'));
else {
  const old=readFileSync('README.md','utf8');
  const details=[...old.matchAll(/<details>\s*<summary>(.*?)<\/summary>([\s\S]*?)<\/details>/g)].map(([,title,body])=>({title,body:body.trim()}));
  const get=title=>{const item=details.find(x=>x.title.startsWith(title));if(!item)throw Error('Missing preserved section '+title);return item.body;};
  const projects=details.filter(x=>x.title==='Open project file — problem & implementation');
  if(projects.length!==3)throw Error('Expected three complete project descriptions');
  content={
    intro:get('01 / From physics'),status:get('Workshop status'),disciplines:get('What I work on'),current:get('02 / Current work'),
    palette:get('04 / Working palette'),principles:get('05 / Build principles'),workflow:get('Engineering workflow'),research:get('Research directions'),collaboration:get('Collaboration starting points'),
    projects:projects.map(x=>x.body)
  };
  mkdirSync('profile',{recursive:true});writeFileSync(contentPath,JSON.stringify(content,null,2)+'\n');
}
const image=(name,alt,motion=true)=>`<picture>\n  <source media="(max-width: 600px)" srcset="./assets/${name}-mobile.png" />\n  <img src="./assets/${name}.${motion?'gif':'png'}" alt="${alt}" width="100%" />\n</picture>`;
const detail=(title,body)=>`<details>\n<summary>${title}</summary>\n\n${body}\n\n</details>`;
const projects=[
  {name:'casting',title:'Casting Assistant',url:'https://github.com/suren1013/Casting-Assistant',alt:'Genuine Casting Assistant interface with its default example, 6 alloys, 3D riser schematic, modulus, yield, feeding and risk.',caption:'Casting and riser design: modulus, feeding distance, yield, and risk across six alloys.'},
  {name:'clv',title:'Customer CLV Dashboard',url:'https://github.com/suren1013/customer-clv-dashboard',alt:'Genuine Customer CLV interface using bundled public demo data. 10 cleaning steps, 12 customer metrics, 7 RFM segments.',caption:'From validated transactions to customer metrics, segmentation, CLV, and export.'},
  {name:'election',title:'TN Election Live Dashboard',url:'https://github.com/suren1013/TN-Election-Live-Dashboard',alt:'Genuine deployed election dashboard snapshot. 234 constituencies, 60-second refresh, majority tracking.',caption:'Seat movement, constituency status, and the majority threshold in one place.'}
];
const sections=[
  '<img src="./assets/control-cover.png" alt="Surendher — mechanical engineering and computation. Original brutalist architecture, suspended blocks and a fractured hedron under vermilion light." width="100%" />',
  '**I turn physical problems into models, simulations, and tools that people can actually use.**\n\n[Still version — no motion](./STILL.md) &nbsp; / &nbsp; [Selected projects](#selected-work) &nbsp; / &nbsp; [Repository archive](https://github.com/suren1013?tab=repositories) &nbsp; / &nbsp; [LinkedIn](https://www.linkedin.com/in/surendher-r/) &nbsp; / &nbsp; [Email](mailto:rsurendher35@gmail.com)',
  '## 01 / Personal dossier\n\n'+image('dossier','SURENDHER_R — mechanical engineering and computation. Original concrete SR emblem; current study: forced-air cooling for avionics heat sinks; learning OpenFOAM and numerical methods; open to internships and collaborations.')+'\n\n**Mechanical Engineering student · Thermal engineering & CFD · Engineering software**\n\n'+detail('Open the dossier — profile, workshop status & disciplines',content.intro+'\n\n### Workshop status\n\n'+content.status+'\n\n### What I work on\n\n'+content.disciplines),
  '<a id="selected-work"></a>\n\n## 02 / Project evidence\n\n<sub>REAL INTERFACES / ENGINEERING, ANALYTICS & LIVE SYSTEMS</sub>',
  ...projects.map((p,i)=>`<a href="${p.url}">${image(p.name+'-evidence',p.alt)}</a>\n\n**[${p.title} →](${p.url})** — ${p.caption}\n\n[Inspect the full interface capture](./assets/${p.name}-interface.png)\n\n`+detail('Open project file — problem & implementation',content.projects[i])+(p.name==='election'?'\n\n[Live application →](https://tn-election-dashboard-2026-1096783328687.us-west1.run.app)':'')),
  '## 03 / Research spotlight\n\n'+image('research-spotlight','Original conceptual 3D heat-sink geometry for the avionics forced-air cooling research spotlight. Heat transfer and OpenFOAM-based CFD. No simulation results are shown.')+'\n\n**Current focus:** OpenFOAM-based forced-air cooling for avionics heat sinks.\n\n<sub>The image is a conceptual geometry study; its lighting does not represent temperatures or simulation results.</sub>\n\n'+detail('Research file — current work & future directions',content.current+'\n\n'+content.research),
  '<img src="./assets/hedron-study.gif" alt="Order from complexity — original 3D hedron and suspended concrete blocks in a smooth twelve-second loop." width="100%" />',
  '## 04 / Method & tools\n\n'+image('method-board','Question, model, simulate, validate, build. Engineering: OpenFOAM, ANSYS, SolidWorks, CFD, FEA, Heat Transfer. Code: Python, TypeScript, JavaScript, React, Next.js, Java. Tools: Git, GitHub, VS Code, LangChain.')+'\n\n**Question → Model → Simulate → Validate → Build → Refine**\n\n'+detail('Working method, complete tool palette & build principles',content.workflow+'\n\n### Working palette\n\n'+content.palette+'\n\n### Build principles\n\n'+content.principles),
  '## 05 / Public activity\n\n'+image('activity-landscape','An isometric concrete-column contribution calendar based on validated public GitHub data. One column per day; height and colour represent GitHub intensity levels. Actual contribution total, active days, date range and refresh date appear in the artwork.',false)+'\n\n[Readable activity summary](./assets/activity-summary.md) &nbsp; / &nbsp; [Underlying calendar data](./assets/activity-data.json) &nbsp; / &nbsp; [Public source](https://github.com/users/suren1013/contributions)\n\n<sub>Scheduled refresh: daily at 07:30 IST. Artwork retains its last successful refresh date if an update fails.</sub>',
  '## 06 / Let’s build something useful\n\n'+image('contact-board',"Open to internships and collaborations in thermal engineering, CFD, engineering software, and applied AI. Let's build something useful.")+'\n\nI am open to **internships and collaborations** in thermal engineering, CFD, engineering software, and applied AI.\n\n'+detail('Collaboration starting points',content.collaboration)+'\n\n[Connect on LinkedIn →](https://www.linkedin.com/in/surendher-r/) &nbsp; / &nbsp; [Send me an email →](mailto:rsurendher35@gmail.com)',
  '[Explore the repository archive →](https://github.com/suren1013?tab=repositories)\n\n<sub>Mechanical engineering, computation, and a lot of building.</sub>\n\n[View the complete still version →](./STILL.md)'
];
const main=sections.join('\n\n<br />\n\n')+'\n';
writeFileSync('README.md',main);
const still=main.replace(/\.\/assets\/([\w-]+)\.gif/g,(_,name)=>`./assets/${name==='hedron-study'?'hedron-study-still':name}.png`)
  .replace('[Still version — no motion](./STILL.md)','[View the motion version](./README.md)')
  .replace('[View the complete still version →](./STILL.md)','[Return to the motion version →](./README.md)');
writeFileSync('STILL.md',still);
console.log('Assembled six visual sections and synchronized the still version.');
