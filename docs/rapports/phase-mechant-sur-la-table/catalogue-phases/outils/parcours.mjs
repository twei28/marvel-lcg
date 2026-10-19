import { cmd as cmdGlobal } from './lib.mjs'
let _fait = {}
const SENS = /^Sens d'Araignée$/
const DEF_SM = /^Défendre avec Spider-Man/i
const vil = async (monde) => (await monde()).area_villain[0]
const sch = async (monde) => (await monde()).area_schemes_main[0]
const allies4 = ["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01075', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)"]
export const P = {
  // 1-3, 6, 10
  'klaw-base': { scenario: 'klaw', rafale: true },
  'klaw-defend': { scenario: 'klaw', setup: async ({ cmd }) => { await cmd(["Puzzle.Gain('01003')"]) }, prefere: [SENS, DEF_SM, /^Jouer$/] },
  // 4
  'klaw-allie1': { setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01050', under_control=True)"]) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-allies2': { setup: async ({ cmd }) => { await cmd(allies4.slice(0, 2)) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-allies3': { setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)); await cmd(["Puzzle.Exhaust('01068')", "Puzzle.Tough('01075')"]) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-allies4': { sansPhase: true, setup: async ({ cmd }) => { await cmd(allies4) } },
  'klaw-allies4-old': { setup: async ({ cmd }) => { await cmd(allies4); await cmd(["Puzzle.Exhaust('01068')", "Puzzle.Tough('01076')"]) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-allie-ko': { setup: async ({ cmd }) => { await cmd(allies4.slice(0, 1)); await cmd(["Puzzle.Damage('01050', 4)"]) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-alter': { form: 'alter' },
  'klaw-heros-ko': { setup: async ({ cmd }) => { await cmd(["Puzzle.Damage('01001a', 8)"]) }, deck: ['01118', '01119', '01118', '01119', '01120', '01122'], prefere: [DEF_SM] },
  'klaw-sonne': { setup: async ({ cmd, monde }) => { const v = await vil(monde); await cmd([`Puzzle.Stun(${v.id})`]) } },
  'klaw-desoriente': { setup: async ({ cmd, monde }) => { const v = await vil(monde); await cmd([`Puzzle.Confuse(${v.id})`]) } },
  'klaw-tenace': { setup: async ({ cmd, monde }) => { const v = await vil(monde); await cmd([`Puzzle.Tough(${v.id})`, "Puzzle.Tough('01001a')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.Tough('01050')"]) }, prefere: [/^Défendre avec Hulk/i] },
  'klaw-etoile-planche': { deck: ['01121', '01109', '01110', '01122'] },
  'klaw-boost-trait': { deck: ['01111', '01118', '01112', '01122'] },
  'klaw-boost-crise': { deck: ['01125', '01151', '01112', '01122'] },
  'klaw-stade': { setup: async ({ cmd, monde }) => { const v = await vil(monde); await cmd(["Puzzle.PutIntoPlay('10031', under_control=True)", `Puzzle.Damage(${v.id}, ${v.info.health - 1})`]) }, prefere: [DEF_SM, /^Armure Électrostatique — Réponse/] },
  'klaw-manig-fin': { setup: async ({ cmd, monde }) => { const s = await sch(monde); await cmd([`Puzzle.SetThreat(${s.id}, 5)`]) } },
  'klaw-annexes': { setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('01125')", "Puzzle.PutIntoPlay('01151')"]) } },
  // 7-8
  'rhino-sbire1': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01101')"]) }, rafale: true },
  'rhino-sbires3': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"]) }, deck: ['01121', '01110', '01101', '01118', '01102', '01103'] },
  'rhino-sbires6': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01172')", "Puzzle.PutIntoPlay('01184')", "Puzzle.PutIntoPlay('01167')"]) } },
  'rhino-sbires-alter': { scenario: 'rhino', form: 'alter', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"]) } },
  'rhino-sbire-defendu': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01050', under_control=True)"]) }, prefere: [/^Défendre avec Hulk/i] },
}

const RH = (deck, extra = {}) => ({ scenario: 'rhino', deck: ['01112', ...deck], ...extra })
Object.assign(P, {
  // 8 : révélation
  'rev-sbire': RH(['01102', '01110']),
  'rev-attach-mechant': RH(['01098', '01110']),
  'rev-annexe-crise': RH(['01108', '01110']),
  'rev-annexe-accel': RH(['01109', '01110']),
  'rev-traitrise': RH(['01105', '01110']),
  'rev-traitrise-attaque': RH(['01187', '01110']),
  'rev-obligation': RH(['01165', '01110']),
  'rev-environnement': RH(['01140', '01110']),
  'rev-surge': RH(['01178', '01104', '01110']),
  'rev-deux-fois': RH(['01121', '01121', '01110']),
  'rev-gangup-alter': RH(['01189', '01105', '01110'], { form: 'alter' }),
  'rev-gangup-heros': RH(['01189', '01110'], { setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"]) } }),
  'rev-etoile': RH(['01121', '01110']),
  'rev-sbire-etoile-boost': { scenario: 'rhino', deck: ['01121', '01102', '01110'] },
  // 4-5 : mots-clés
  'rhino-surcharge': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.Damage('01050', 3)"]) }, deck: ['16134', '01110', '01110'], prefere: [/^Défendre avec Hulk/i] },
  'rhino-perforante': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('04101')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.Tough('01050')"]) }, deck: ['01112', '01110'], prefere: [/^Défendre avec Hulk/i] },
  'rhino-garde-defense': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('16117')", "Puzzle.PutIntoPlay('10031', under_control=True)"]) }, deck: ['01112', '01110'], prefere: [DEF_SM, /^Armure Électrostatique — Réponse/] },
  'rhino-retaliation': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01172')", "Puzzle.PutIntoPlay('01184')", "Puzzle.PutIntoPlay('01167')"]) } },
  // scénarios variés
  'ultron-base': { scenario: 'ultron' },
  'shredder-base': { scenario: 'shredder' },
  'baxter-base': { scenario: 'baxter_stockman' },
  'bebop-base': { scenario: 'bebop_rocksteady', choisir: async ({ page }, sig) => {
    if (await page.getByText('Choisir la cible', { exact: false }).count() && await page.getByText('Choisir la cible').first().isVisible().catch(() => false)) {
      const c = page.locator('.plateau-cadre .scan-card[aria-label^="Bebop"]').first()
      await c.click({ timeout: 2000, force: true }).catch(() => {})
      await new Promise((r) => setTimeout(r, 400))
      const ok = page.getByRole('button', { name: /capacités forcées/i }).first()
      if (await ok.isEnabled().catch(() => false)) await ok.click({ timeout: 1500 }).catch(() => {})
      return true
    }
    return false } },
  'crossbones-base': { scenario: 'crossbones' },
  // 12 : variantes d'affichage
  'v-reduit': { scenario: 'klaw', reduit: true, setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)) }, prefere: [/^Défendre avec Hulk/i] },
  'v-paysage': { scenario: 'klaw', w: 1050, h: 480, tactile: true, setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)) }, prefere: [/^Défendre avec Hulk/i] },
  'v-tablette': { scenario: 'klaw', w: 1180, h: 820, tactile: true, setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)) }, prefere: [/^Défendre avec Hulk/i] },
  'v-mobile-portrait': { scenario: 'klaw', w: 390, h: 844, tactile: true, setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)) }, prefere: [/^Défendre avec Hulk/i] },
  'v-mobile-paysage': { scenario: 'klaw', w: 844, h: 390, tactile: true, setup: async ({ cmd }) => { await cmd(allies4.slice(0, 3)) }, prefere: [/^Défendre avec Hulk/i] },
})
Object.assign(P, {
  'klaw-3boosts': { scenario: 'klaw', deck: ['60120', '01112', '01112', '01112', '01110'], prefere: [DEF_SM] },
  'klaw-boost-amplify': { scenario: 'klaw', deck: ['16054', '16069', '01112', '01110'] },
  'klaw-boost-etoile-surge': { scenario: 'klaw', deck: ['01121', '01178', '01112', '01110'] },
})
Object.assign(P, {
  'klaw-defaite': { scenario: 'klaw', setup: async ({ cmd, monde, sleep }) => { await cmd(["Puzzle.AdvanceMainScheme(1)"]); await sleep(1500); const s = await sch(monde); await cmd([`Puzzle.SetThreat(${s.id}, 7)`]) } },
  'klaw-victoire': { scenario: 'klaw', setup: async ({ cmd, monde, sleep }) => { const v = await vil(monde); await cmd([`Puzzle.AdvanceVillain()`]); await sleep(2000); const v2 = await vil(monde); console.log('villain', v2.id, v2.name, v2.info.health); await cmd([`Puzzle.Damage(${v2.id}, ${v2.info.health - 1})`, "Puzzle.PutIntoPlay('10031', under_control=True)"]) }, prefere: [DEF_SM, /^Armure Électrostatique — Réponse/] },
})
Object.assign(P, {
  'rhino-sbires6b': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.Tough('01001a')"]); await cmd(["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01121')", "Puzzle.PutIntoPlay('01182')", "Puzzle.PutIntoPlay('01184')", "Puzzle.PutIntoPlay('01172')"]) }, prefere: [/^Défendre avec (Hulk|Luke Cage|Vision)/i, DEF_SM] },
})
const SB3 = { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')"]) }, deck: ['01112', '01121', '01102', '01110'] }
Object.assign(P, {
  'vt-sbires': { ...SB3, w: 1180, h: 820, tactile: true },
  'vp-sbires': { ...SB3, w: 1050, h: 480, tactile: true },
  'vm-sbires': { ...SB3, w: 844, h: 390, tactile: true },
  'vmp-sbires': { ...SB3, w: 390, h: 844, tactile: true },
  'vr-sbires': { ...SB3, reduit: true },
  'vt-klaw-alter': { scenario: 'klaw', form: 'alter', w: 1180, h: 820, tactile: true, deck: ['01112', '01112', '01189', '01105'] },
  'vp-klaw-ko': { scenario: 'klaw', w: 1050, h: 480, tactile: true, setup: async ({ cmd }) => { await cmd(["Puzzle.Damage('01001a', 8)"]) }, deck: ['01118', '01119', '01118', '01119', '01120', '01122'], prefere: [DEF_SM] },
})
Object.assign(P, {
  'klaw-aucun-defenseur': { scenario: 'klaw', setup: async ({ cmd }) => { await cmd(["Puzzle.Exhaust('01001a')"]) } },
  'klaw-barriere': { scenario: 'klaw', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('05017', under_control=True)"]) }, prefere: [/^Barrière Énergétique — /i] },
  'klaw-allie-sonne': { scenario: 'klaw', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.Stun('01050')", "Puzzle.Confuse('01050')"]) }, prefere: [/^Défendre avec Hulk/i] },
})
Object.assign(P, {
  'rhino-perforante2': { scenario: 'rhino', setup: async ({ cmd }) => { await cmd(["Puzzle.PutIntoPlay('04101')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)", "Puzzle.Tough('01050')", "Puzzle.Tough('01076')"]) }, deck: ['01112', '01110', '01110', '01110'], prefere: [/^Défendre avec Hulk/i, /^Défendre avec Luke Cage/i] },
})
Object.assign(P, {
  'rhino-perforante3': { scenario: 'rhino', setup: async ({ cmd, monde }) => { const v = (await monde()).area_villain[0]; await cmd([`Puzzle.Stun(${v.id})`, "Puzzle.PutIntoPlay('04101')", "Puzzle.Tough('01001a')"]) }, deck: ['01112', '01110', '01110'] },
})

Object.assign(P, {
  'klaw-aucun-defenseur2': { scenario: 'klaw', onState: async (page, info) => { if (info.phase === 'Enemy Activation' && !_fait.a) { _fait.a = true; await cmdGlobal(["Puzzle.Exhaust('01001a')"]) } } },
})
