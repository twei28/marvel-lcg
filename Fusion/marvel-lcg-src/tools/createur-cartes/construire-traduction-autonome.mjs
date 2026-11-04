// Construit public/createur-cartes/traduction-autonome.html : tout le JS des modules de la page « Traduction »
// (commun.js, polices.js, texte.js, effacer-texte.js, detecter-zone.js, zip.js, stockage-traduction.js, traduction.js)
// inline dans un seul <script> classique (import/export retires), les polices necessaires encodees en base64
// (chargerPolices() construit ses FontFace avec des data URL au lieu de fetch(dossier+fichier)), donnees/types.json
// inline en JSON (plus de fetch), style.css + le <style> de traduction.html inline. Resultat : aucune requete
// reseau a l'ouverture, utilisable directement en file:// (double-clic), sans serveur.
//
// A relancer apres toute modification de traduction.js, traduction.html, ou d'un des modules ci-dessus, pour que
// traduction-autonome.html reste synchronise avec la version servie (traduction.html, elle, n'est jamais modifiee
// par ce script).
//
// Usage : node tools/createur-cartes/construire-traduction-autonome.mjs
import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const SRC = path.join(ICI, '..', '..', 'public', 'createur-cartes')
const lire = (f) => readFileSync(path.join(SRC, f), 'utf8')

// ------------------------------------------------------------------ 1. JS des modules, import/export retires
function depouiller(src) {
  return src
    .split('\n')
    .filter((ligne) => !/^import\s.*from\s+['"]\.\//.test(ligne))
    .join('\n')
    .replace(/^export (async function|function|const|let)\b/gm, '$1')
}

// polices.js : remplace le chargement par fetch(dossier+fichier) par une lecture dans FONTS_B64 (data URL). Fait sur
// le texte BRUT (avant depouiller, qui retire les "export " dont ce remplacement a besoin pour retrouver la ligne) —
// l'ordre inverse a deja ete une vraie cause de bug ici (FONTS_MIME is not defined, remplacement sans effet).
const FACES_FICHIERS = [
  'TextbookNewW08-ExtraBold.ttf', 'AvenirNextCondensed-BoldItalic.ttf', 'Avenir Next Condensed Medium.ttf',
  'ElektraMedProMod-BoldItalic-mod.ttf', 'Exo2Mod-Bold.ttf', 'AvenirNextLTPro-It.otf', 'AvenirNextLTPro-Bold.otf',
  'Horrible-Jefe.ttf', 'AvenirNextLTPro-BoldItalic.otf', 'AvenirNextLTPro-Regular.otf', 'AvenirNextLTPro-Demi.otf',
  'ChampionsIcons.ttf', 'KomikaTitle.ttf', 'KOMTXT_.ttf', 'KOMTXTI.ttf', 'figgins-extrabold.otf', 'FUTURAMC.TTF',
  'Futura Extra Bold.otf',
]
const MIME = (f) => (f.toLowerCase().endsWith('.otf') ? 'font/otf' : f.toLowerCase().endsWith('.woff2') ? 'font/woff2' : 'font/ttf')
const fontsB64 = {}
for (const f of FACES_FICHIERS) {
  fontsB64[f] = readFileSync(path.join(SRC, 'polices', f)).toString('base64')
}
let policesSrc = lire('polices.js')
const avantChargerPolices = "export function chargerPolices(dossier = 'polices/') {"
const avantFontFace = "const face = new FontFace(famille, `url(\"${dossier + encodeURI(fichier)}\")`, { weight: d.weight, style: d.style })"
if (!policesSrc.includes(avantChargerPolices) || !policesSrc.includes(avantFontFace)) {
  throw new Error('polices.js a changé : les remplacements de chargerPolices() ne correspondent plus, à reporter à la main.')
}
policesSrc = policesSrc
  .replace(avantChargerPolices, 'const FONTS_MIME = ' + JSON.stringify(Object.fromEntries(FACES_FICHIERS.map((f) => [f, MIME(f)]))) + "\nexport function chargerPolices() {")
  .replace(avantFontFace, 'const face = new FontFace(famille, `url(data:${FONTS_MIME[fichier]};base64,${FONTS_B64[fichier]})`, { weight: d.weight, style: d.style })')
policesSrc = `const FONTS_B64 = ${JSON.stringify(fontsB64)}\n\n` + policesSrc

const ORDRE_SRC = {
  'commun.js': lire('commun.js'), 'polices.js': policesSrc, 'texte.js': lire('texte.js'),
  'effacer-texte.js': lire('effacer-texte.js'), 'detecter-zone.js': lire('detecter-zone.js'),
  'zip.js': lire('zip.js'), 'stockage-traduction.js': lire('stockage-traduction.js'),
}
const jsModules = Object.entries(ORDRE_SRC).map(([f, src]) => `// ====== ${f} ======\n` + depouiller(src)).join('\n\n')

// traduction.js : import/export retires, fetch('donnees/types.json') remplacé par le JSON inline.
let app = depouiller(lire('traduction.js'))
const typesJson = JSON.parse(lire('donnees/types.json'))
const avantFetchTypes = /try \{\s*TYPES = await \(await fetch\('donnees\/types\.json'\)\)\.json\(\)\s*\} catch \{\s*TYPES = \{\}\s*\}/
if (!avantFetchTypes.test(app)) throw new Error("traduction.js a changé : le remplacement du fetch('donnees/types.json') ne correspond plus, à reporter à la main.")
app = app.replace(avantFetchTypes, 'TYPES = TYPES_JSON')
app = `const TYPES_JSON = ${JSON.stringify(typesJson)}\n\n` + app

const scriptFinal = jsModules + '\n\n// ====== traduction.js ======\n' + app

// ------------------------------------------------------------------ 2. CSS : style.css + le <style> de traduction.html
const styleCommun = lire('style.css')
const htmlSource = lire('traduction.html')
const matchStyle = /<style>([\s\S]*?)<\/style>/.exec(htmlSource)
if (!matchStyle) throw new Error('traduction.html a changé : plus de bloc <style>, à reporter à la main.')
const styleSpecifique = matchStyle[1]

// ------------------------------------------------------------------ 3. le reste du HTML (corps), le <script type=module> retiré
const corps = htmlSource
  .replace(/<link rel="stylesheet" href="\/createur-cartes\/style\.css">\n?/, '')
  .replace(/<style>[\s\S]*?<\/style>\n?/, '')
  .replace(/<script type="module" src="\.\/traduction\.js"><\/script>\n?/, '')
  .replace('<title>MC Creator — Traduction</title>', '<title>MC Creator — Traduction (autonome)</title>')
  .replace('<a class="btn petit" href="./">← Retour à MC Creator</a>', '<span class="aide">Fichier autonome — ouvert sans serveur (file://)</span>')

const sortie = corps
  .replace('</head>', `<style>\n${styleCommun}\n${styleSpecifique}\n</style>\n</head>`)
  .replace('</body>', `<script>\n${scriptFinal}\n</script>\n</body>`)

const chemin = path.join(SRC, 'traduction-autonome.html')
writeFileSync(chemin, sortie)
console.log('Écrit :', chemin, '-', (sortie.length / 1024 / 1024).toFixed(2), 'Mio')
