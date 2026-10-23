// CALIBRATION DE LA BARRE D'AVANTAGE (23/10/2026) : rejoue `estimerAvantage` sur les photos d'un round prises par
// `tools/autoplay.py` (variable AUTOPLAY_INSTANTANES), puis confronte la valeur au verdict FINAL de la partie.
//
//   AUTOPLAY_INSTANTANES=/tmp/barre python3.10 tools/autoplay.py .game-src --deck spider_man --vilains rhino,klaw --parties 10 ...
//   cd ui-app && npx vite-node outils/calibrer-barre-avantage.ts /tmp/barre
//
// Les fichiers : <dossier>/<deck>_<vilain>_<difficulte>_<profil>_<graine>-r<round>.json ; le verdict est lu dans
// /tmp/autoplay_<etiquette>.log (ligne « RESULTAT: {...} »). Sortie : par tranche de valeur, la part de parties finalement GAGNEES.
// Une barre bien calibree monte avec la part de victoires. Lecture seule : rien n'est modifie.
import { readdirSync, readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import { estimerAvantage } from '../src/board/barre-avantage'
import type { World } from '../src/board/world'

const dossier = process.argv[2]
if (!dossier || !existsSync(dossier)) {
  console.error('usage : npx vite-node outils/calibrer-barre-avantage.ts <dossier des photos>')
  process.exit(1)
}

function verdictDe(etiquette: string): boolean | null {
  const journal = `/tmp/autoplay_${etiquette}.log`
  if (!existsSync(journal)) return null
  const ligne = readFileSync(journal, 'utf8').split('\n').reverse().find((l) => l.startsWith('RESULTAT:'))
  if (!ligne) return null
  try {
    const r = JSON.parse(ligne.slice('RESULTAT:'.length))
    return typeof r.gagne === 'boolean' ? r.gagne : null
  } catch {
    return null
  }
}

const tranches = [0, 0.2, 0.4, 0.6, 0.8, 1.0001]
const comptes = tranches.slice(0, -1).map(() => ({ n: 0, gagnees: 0 }))
const parties = new Map<string, { gagne: boolean | null; points: { round: number; valeur: number }[] }>()
let ignorees = 0

for (const nom of readdirSync(dossier).filter((f) => f.endsWith('.json')).sort()) {
  const m = /^(.*)-r(\d+)\.json$/.exec(nom)
  if (!m) continue
  const etiquette = m[1]!
  const ronde = Number(m[2])
  const monde = JSON.parse(readFileSync(join(dossier, nom), 'utf8')) as World
  const avantage = estimerAvantage(monde)
  if (avantage.etat !== 'ok') {
    ignorees++
    continue
  }
  const partie = parties.get(etiquette) ?? { gagne: verdictDe(etiquette), points: [] }
  partie.points.push({ round: ronde, valeur: avantage.valeur })
  parties.set(etiquette, partie)
}

let sansVerdict = 0
for (const p of parties.values()) {
  if (p.gagne === null) {
    sansVerdict++
    continue
  }
  for (const { valeur } of p.points) {
    const i = Math.min(comptes.length - 1, tranches.findIndex((t, k) => valeur >= t && valeur < tranches[k + 1]!))
    comptes[i]!.n++
    if (p.gagne) comptes[i]!.gagnees++
  }
}

console.log(`${parties.size} parties (${sansVerdict} sans verdict), ${ignorees} photos sans estimation (indisponible/masque)\n`)
console.log('valeur de la barre   photos   part des parties finalement GAGNEES')
comptes.forEach((c, k) => {
  const part = c.n ? `${Math.round((100 * c.gagnees) / c.n)} %` : '-'
  console.log(`${tranches[k]!.toFixed(1)} - ${Math.min(1, tranches[k + 1]!).toFixed(1)}`.padEnd(21) + String(c.n).padStart(6) + '   ' + part)
})

// Pente simple : si la barre « predit », la part gagnee doit croitre de la tranche basse a la haute.
const parts = comptes.filter((c) => c.n >= 5).map((c) => c.gagnees / c.n)
const croissante = parts.every((x, i) => i === 0 || x >= parts[i - 1]! - 0.05)
console.log(`\nMonte avec la part de victoires : ${parts.length >= 2 ? (croissante ? 'OUI' : 'NON') : 'trop peu de donnees'}`)
