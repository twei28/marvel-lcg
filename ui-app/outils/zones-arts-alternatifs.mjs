// Zones de texte des ARTS ALTERNATIFS de héros (séries cb, rog, rog2, m3t), pour
// la traduction posée : leur mise en page n'est pas celle des cartes officielles,
// le repérage à la volée y échoue. Chaque image reçoit la zone proposée par le
// détecteur du plateau, puis la correction manuelle relevée à l'œil
// (src/board/zones-arts-alternatifs.corrections.json), qui l'emporte.
//
// Lancé par outils/zones_arts_alternatifs.py (point d'entrée), qui lui passe le
// dossier des pixels décodés. Écrit src/board/zones-arts-alternatifs.ts.
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { transpiler } from './generer-traduction-public.mjs'

const ICI = dirname(fileURLToPath(import.meta.url))
const BOARD = resolve(ICI, '../src/board')
const SERIES = /^(.+_(cb|rog|rog2|m3t))\.(jpg|jpeg|png|webp)$/
const L = 300
const H = 420
const LIGNES = 40

const temporaire = mkdtempSync(join(tmpdir(), 'zones-arts-'))
for (const nom of ['traduction-posee', 'traits-fr']) {
  writeFileSync(join(temporaire, `${nom}.mjs`), transpiler(nom).replace(/from '\.\/([\w-]+)\.js'/g, "from './$1.mjs'"))
}
const { detecterZoneTexte, couleurDuFond } = await import(pathToFileURL(join(temporaire, 'traduction-posee.mjs')).href)

// Les pixels viennent de zones_arts_alternatifs.py (Python décode les scans ;
// le Node de ce poste est le binaire Windows, il ne peut pas lancer Python WSL).
const entree = process.argv[2]
const fichiers = JSON.parse(readFileSync(join(entree, 'fichiers.json'), 'utf8'))
const tout = readFileSync(join(entree, 'pixels.bin'))
const propositions = JSON.parse(readFileSync(join(entree, 'propositions.json'), 'utf8'))
const corrections = JSON.parse(readFileSync(join(BOARD, 'zones-arts-alternatifs.corrections.json'), 'utf8'))

const r3 = (v) => Math.round(v * 1000) / 1000
const zones = {}
const proposees = {}
fichiers.forEach((f, i) => {
  const cle = f.match(SERIES)[1]
  const pixels = tout.subarray(i * L * H * 4, (i + 1) * L * H * 4)
  const detectee = detecterZoneTexte(pixels, L, H)
  proposees[cle] = detectee
  // Le détecteur du plateau ne connaît que la mise en page FFG ; à défaut, la
  // tache blanche proposée par le script Python (encadré des arts « Comic »).
  const correction = corrections[cle] ?? (detectee || !propositions[cle] ? undefined : { rect: propositions[cle] })
  let zone = detectee
  if (correction === 'encadre') zone = null
  else if (correction) {
    const [x0, y0, x1, y1] = correction.rect
    const fond = correction.fond ?? couleurDuFond(pixels, L, H, [x0 + 0.02, y0 + 0.02, x1 - 0.02, y1 - 0.02]) ?? [240, 240, 240]
    zone = { x0, y0, x1, y1, fond, bords: [[x0, x1]] }
  }
  if (!zone) {
    zones[cle] = null
    return
  }
  // Les bords sont échantillonnés sur LIGNES lignes régulières : la forme du
  // cache n'en demande pas plus, et la table reste légère.
  const n = zone.bords.length
  const bords = []
  for (let j = 0; j < Math.min(LIGNES, n); j += 1) {
    const b = zone.bords[Math.floor((j * n) / Math.min(LIGNES, n))]
    bords.push([r3(b[0]), r3(b[1])])
  }
  zones[cle] = { x0: r3(zone.x0), y0: r3(zone.y0), x1: r3(zone.x1), y1: r3(zone.y1), fond: zone.fond, bords }
})

const corps = Object.entries(zones)
  .map(([cle, z]) => `  '${cle}': ${JSON.stringify(z)},`)
  .join('\n')
writeFileSync(
  join(BOARD, 'zones-arts-alternatifs.ts'),
  `// GÉNÉRÉ par ui-app/outils/zones-arts-alternatifs.mjs — NE PAS ÉDITER.
// Corriger une zone : src/board/zones-arts-alternatifs.corrections.json, puis relancer l'outil.
// null = la traduction reste dans l'encadré sous la carte.
import type { ZoneTexte } from './traduction-posee'

export const ZONES_ARTS_ALTERNATIFS: Readonly<Record<string, ZoneTexte | null>> = {
${corps}
}
`
)

writeFileSync(join(entree, 'zones.json'), JSON.stringify({ fichiers, zones, proposees }))
rmSync(temporaire, { recursive: true, force: true })
const sans = Object.entries(zones).filter(([, z]) => !z).map(([c]) => c)
console.log(`${fichiers.length} images, ${fichiers.length - sans.length} zones, ${sans.length} sans zone`)
if (sans.length) console.log('sans zone : ' + sans.join(' '))
