// Usage: node scripts/build-models.mjs /path/to/precogly/frontend
// Calls the actual pinned tool's serializer rather than inventing an interchange schema.
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
if(!process.argv[2])throw Error('Supply the pinned Precogly frontend directory.');
const frontend=resolve(process.argv[2]);
const {build}=await import(pathToFileURL(frontend+'/node_modules/esbuild/lib/main.js'));
await build({entryPoints:[frontend+'/src/features/guest-editor/lib/cyclonedx-guest.ts'],bundle:true,platform:'node',format:'esm',outfile:'/tmp/threat-talk-serializer.mjs'});
const {serializeGuestToCycloneDx,deserializeCycloneDxToGuest}=await import('file:///tmp/threat-talk-serializer.mjs');
const results=[];
for(const name of ['shop-app']) {
 const s=JSON.parse(readFileSync(`threat-model/${name}.source.json`,'utf8'));
 const output=serializeGuestToCycloneDx(s.title,s.nodes,s.edges,s.threats,s.countermeasures,s.notationStyle,s.systemContext);
 writeFileSync(`threat-model/${name}.cdx.json`,output+'\n');
 const re=deserializeCycloneDxToGuest(output);
 for(const key of ['nodes','edges','threats','countermeasures']) if(re[key].length!==s[key].length) throw Error(name+' lost '+key);
 for(const t of s.threats) if(!re.threats.some(x=>x.name===t.name && x.targetId===t.targetId && x.description===t.description)) throw Error('Threat linkage mismatch '+t.name);
 results.push({name,nodes:re.nodes.length,flows:re.edges.length,threats:re.threats.length,controls:re.countermeasures.length,status:'serializer/deserializer roundtrip passed'});
}
writeFileSync('threat-model/model-roundtrip.json',JSON.stringify({checkedAt:new Date().toISOString(),results},null,2)+'\n');
console.log(results);
