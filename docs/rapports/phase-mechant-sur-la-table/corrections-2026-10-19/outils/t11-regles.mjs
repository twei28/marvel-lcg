// T11 : les regles cachees. Usage : OUT=<dossier> node t11-regles.mjs <accel|etoile|desoriente|perforant>
// Monte le cas, joue jusqu'a l'etape concernee et releve le texte de la ligne `.tsm-regles` (+ capture PNG).
import * as L from '../../catalogue-phases/outils/lib.mjs'
const cas = process.argv[2] ?? 'accel'
const CAS = {
  accel: { scenario: 'klaw', cmds: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01109')"], deck: null, attend: /gagne \d+ menaces?/ },
  etoile: { scenario: 'klaw', cmds: ["Puzzle.ChangeForm('01001b')"], deck: ['04116', '01110', '01110', '01122'], attend: /Klaw attaque/ },
  desoriente: { scenario: 'klaw', cmds: ["Puzzle.ChangeForm('01001b')"], deck: null, confus: true, attend: /Klaw attaque/ },
  perforant: { scenario: 'rhino', cmds: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('04101')", "Puzzle.Tough('01001a')"], deck: ['01112', '01110', '01110'], attend: /attaque Spider-Man/ },
}
const c = CAS[cas]
await L.nouvellePartie({ scenario: c.scenario })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(c.cmds)
if (c.deck) await L.cmd(['Puzzle.EmptyEncounterDeck()', `Puzzle.CreateEncounterDeck(${[...c.deck].reverse().map((x) => `'${x}'`).join(',')})`])
if (c.confus) { const v = (await L.monde()).area_villain[0]; await L.cmd([`Puzzle.Confuse(${v.id})`]) }
await L.sleep(600)
for (let essai = 0; essai < 30; essai++) {
  if (!/^Player(?: \d+)? Turn$/.test((await L.monde()).phase)) break
  if (essai % 4 === 0) { try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { /* reessai */ } } else await L.prepa(page, false)
  await L.sleep(700)
}
let trouve = false
for (let i = 0; i < 700 && !trouve; i++) {
  const sig = await L.signature(page)
  const regles = await page.evaluate(() => document.querySelector('.tsm-regles')?.textContent ?? '')
  const phrase = await page.evaluate(() => document.querySelector('.tsm-phrase')?.textContent ?? '')
  if (cas === 'accel' && c.attend.test(phrase) && !regles && !globalThis.vu) { globalThis.vu = true; const w = await L.monde(); console.log('menace : phrase', phrase, '| faits :', JSON.stringify((w.faits_mechant ?? []).filter((f) => f.genre === 'menace').map((f) => ({ montant: f.montant, escalade: f.escalade, acceleration: f.acceleration, joueurs: f.joueurs })))); await L.sleep(1500); continue }
  if (c.attend.test(phrase + ' ' + sig.bandeau) && regles) {
    console.log(cas, '| bandeau :', sig.bandeau.slice(0, 160), '| REGLES :', regles)
    await page.screenshot({ path: `${L.OUT}/t11-${cas}.png` })
    trouve = true
    break
  }
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
  else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(150)
}
if (!trouve) console.log(cas, 'AUCUNE LIGNE DE REGLE TROUVEE')
await browser.close()
