// compteurs-fr.ts — le nom français des compteurs posés sur les cartes.
//
// Le moteur nomme ses compteurs en anglais (`c_steel`, `c_charge`...) et le
// plateau écrivait ce nom tel quel : « 2 Steel » sur Colossus dans une partie
// en français. La liste est celle de `CardFace.COUNTER` (card_face.py) ; un
// nom absent reste en anglais, lisible, plutôt que d'inventer.

import { langueActuelle } from './langue'

const COMPTEURS_FR: Readonly<Record<string, string>> = {
  counter: 'compteur',
  attack: 'attaque',
  web: 'toile',
  glory: 'gloire',
  damage: 'dégâts',
  acceleration: 'accélération',
  infamy: 'infamie',
  madness: 'folie',
  arrow: 'flèche',
  snoop: 'enquête',
  medical: 'soin',
  pym: 'Pym',
  size: 'taille',
  mystic: 'mystique',
  psionic: 'psionique',
  warrior: 'guerrier',
  time: 'temps',
  test: 'test',
  active: 'actif',
  energy: 'énergie',
  lightning: 'éclair',
  glider: 'planeur',
  bomb: 'bombe',
  mental: 'mental',
  vengeance: 'vengeance',
  physical: 'physique',
  ammo: 'munition',
  charge: 'charge',
  toon: 'toon',
  training: 'entraînement',
  chime: 'carillon',
  rage: 'rage',
  delay: 'délai',
  steel: 'acier',
  reflection: 'reflet',
  command: 'commandement',
  growth: 'croissance',
  poison: 'poison',
  barrage: 'barrage',
  evasion: 'évasion',
  fury: 'furie',
  sand: 'sable',
  flame: 'flamme',
  flare: 'fusée',
  calm: 'calme',
  illusion: 'illusion',
  menace: 'menace',
  evidence: 'preuve',
  adrenaline: 'adrénaline',
  reactor: 'réacteur',
  metal: 'métal',
  sense: 'sens',
  article: 'article',
  wound: 'blessure',
  hate: 'haine',
  shell: 'carapace',
  unworthy: 'indigne',
  pheromone: 'phéromone',
  limb: 'membre',
  squirrel: 'écureuil',
  block: 'blocage',
  tactic: 'tactique',
  diversion: 'diversion',
  stimulant: 'stimulant',
  spider: 'araignée',
  replay: 'rejeu',
  ball: 'balle',
  configuration: 'configuration',
  deploy: 'déploiement',
  labor: 'travail',
  shift: 'décalage',
  pursuit: 'poursuite',
  chi: 'chi',
  ratings: 'audience',
  clue: 'indice',
  stake: 'pieu',
  // ⚠ CLEF A DEUX MOTS, la seule de la table. Le compteur du pack
  // spider_woman_kajislav s'appelle « psionic web » et non « psionic » : ce
  // dernier existait deja et etait PRIS (`mw002`, `35013`), or Madame Web est
  // justement une alliee de ce pack-ci. La recherche se fait sur la clef
  // BRUTE, espace compris ; sans cette entree le plateau ecrivait
  // « 5 psionic web » en pleine partie francaise.
  'psionic web': 'toile psionique',
  aegis: 'égide',
  fire: 'feu',
  // Pack red_sonja (23/09/2026) : Crimson Shadow (rs011, « stealth ») et
  // She-Devil Shackled! (rs018, « fetter ») — trouve en ecrivant le test de
  // rendu de l'etape 8 bis, avant meme d'avoir ete joue.
  stealth: 'discrétion',
  fetter: 'entrave',
  // Pack conan (25/09/2026) : compteurs de The Cimmerian (cn012a/b) et de
  // The Coils of Doom (cn013). « Crom » est un nom propre (le dieu cimmérien).
  crom: 'Crom',
  serpent: 'serpent',
}

/** « steel » → « acier » en français, « steel » en anglais ; « tic_tac_toe_1_1 »
 *  garde ses mots séparés. */
export function nomDeCompteur(cle: string): string {
  const lisible = cle.replace(/_/g, ' ')
  if (langueActuelle() !== 'fr') return lisible
  return COMPTEURS_FR[cle] ?? lisible
}
