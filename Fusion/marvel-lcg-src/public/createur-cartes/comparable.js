// « Voir une vraie carte comparable » : cherche dans le catalogue une carte OFFICIELLE ANGLAISE du meme type, au nombre de mots et de
// declencheurs proches, et montre son scan a cote de la carte en cours, a la meme echelle : on juge la longueur et la taille du texte.
// L'index (donnees/comparables.json, fait par extraire-comparables.py) ne contient aucune image ; les scans viennent de
// /api/createur/scan/<code>, qui demande une session (donc : sur le site, pas en mode local).
import { dialogue, el, S } from './commun.js'

const BASE = '/createur-cartes/'
// type du createur -> type du catalogue
const TYPE_CATALOGUE = {
  ally: 'Ally', event: 'Event', upgrade: 'Upgrade', support: 'Support', resource: 'Resource', 'alter-ego': 'AlterEgo', identity: 'Hero',
  obligation: 'Obligation', playersidescheme: 'PlayerSideScheme', villain: 'Villain', minion: 'Minion', treachery: 'Treachery',
  environment: 'Environment', attachment: 'Attachment', sidescheme: 'SideScheme', main_scheme_a: 'MainScheme', main_scheme_b: 'MainScheme',
  'obligation-villain': 'Obligation', 'generic-promo': 'Ally', 'generic-promo-vert': 'Ally', 'alter-ego-promo': 'AlterEgo', 'identity-promo': 'Hero',
}
let index = null
async function chargerIndex() {
  if (!index) index = await (await fetch(BASE + 'donnees/comparables.json')).json()
  return index
}

/** Mots et declencheurs du texte de regles d'une carte (balises et icones [energy] ignorees). */
export function mesurerTexte(html) {
  const brut = String(html ?? '')
  return { mots: brut.replace(/<[^>]*>|\[[a-z_]+\]/gi, ' ').split(/\s+/).filter(Boolean).length, declencheurs: (brut.match(/<b>/gi) ?? []).length }
}

/** Les cartes officielles les plus proches : meme type, peu d'ecart de mots (les declencheurs comptent plus). */
export function plusProches(liste, type, mesure, n = 12) {
  const t = TYPE_CATALOGUE[type] ?? 'Ally'
  return liste.filter((x) => x[2] === t)
    .map((x) => ({ code: x[0], nom: x[1], mots: x[3], declencheurs: x[4], ecart: Math.abs(x[3] - mesure.mots) + 4 * Math.abs(x[4] - mesure.declencheurs) }))
    .sort((a, b) => a.ecart - b.ecart || a.code.localeCompare(b.code))
    .slice(0, n)
}

/** `rendre(carte)` -> canvas de la carte en cours. */
export async function ouvrirComparable(rendre) {
  const c = S.carte()
  const mesure = mesurerTexte(c.contenu.regles)
  let candidates
  try {
    candidates = plusProches(await chargerIndex(), c.type, mesure)
  } catch {
    return S.message('Index des cartes officielles introuvable.')
  }
  if (!candidates.length) return S.message('Aucune carte officielle de ce type à comparer.')
  const toile = await rendre(c)
  const miennes = el('img', { alt: '', class: 'comp-carte', src: toile.toDataURL('image/png') })
  const officielle = el('img', { alt: '', class: 'comp-carte' })
  const legende = el('div', { class: 'aide', 'aria-live': 'polite' })
  const erreur = el('div', { class: 'aide' })
  let i = 0
  const montrer = () => {
    const x = candidates[i]
    erreur.textContent = ''
    officielle.onerror = () => { erreur.textContent = 'Scan indisponible.' }
    officielle.src = `/api/createur/scan/${encodeURIComponent(x.code)}`
    legende.textContent = `${x.nom} (${x.code}) · ${x.mots} mots, ${x.declencheurs} déclencheur(s) · ${i + 1}/${candidates.length}`
  }
  montrer()
  const d = dialogue('Voir une vraie carte comparable',
    el('div', {},
      el('div', { class: 'aide' }, `Ta carte : ${mesure.mots} mots, ${mesure.declencheurs} déclencheur(s). À droite, une carte officielle anglaise du même type, au texte de longueur proche, à la même taille.`),
      el('div', { class: 'comp-paire' }, el('figure', {}, miennes, el('figcaption', {}, 'Ta carte')), el('figure', {}, officielle, el('figcaption', {}, 'Carte officielle'))),
      legende, erreur,
      el('div', { class: 'rang', style: 'justify-content:center' },
        el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { i = (i + candidates.length - 1) % candidates.length; montrer() } }, '← Précédente'),
        el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { i = (i + 1) % candidates.length; montrer() } }, 'Suivante →'))),
    [{ texte: 'Fermer' }])
  d.querySelector('.panneau').style.minWidth = 'min(760px,94vw)'
}
