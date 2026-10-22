// compteurs-fr.ts — le nom français des compteurs posés sur les cartes.
//
// Le moteur nomme ses compteurs en anglais (`c_steel`, `c_charge`...) et le
// plateau écrivait ce nom tel quel : « 2 Steel » sur Colossus dans une partie
// en français. La liste est celle de `CardFace.COUNTER` (card_face.py) ; un
// nom absent reste en anglais, lisible, plutôt que d'inventer.

import { langueActuelle } from './langue'

const COMPTEURS_FR: Readonly<Record<string, string>> = {
  counter: 'compteur',
  revelation: 'révélation',
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
  hunter: 'chasseur',
  pep: 'pep', // ub037 Pepperoni (aspect TMNT Basic, Inkwire) : « pep counters », mot laissé tel quel
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
  // Pack skrull_menace, scenario Paibok (15/10/2026) : les jetons de MAITRISE poses sur
  // Paibok (compteur maison, insert p.12) et les jetons d'ABSORPTION d'Asti the
  // All-Seeing (sk163, set New Revengers).
  mastery: 'maîtrise',
  absorption: 'absorption',
  suspicion: 'soupçon',
  // Pack skrull_menace, scenario Skrull Pantheon (15/10/2026) : les jetons de FOI poses sur le
  // mechant Kly'bn / Sl'gur't (insert p.14).
  faith: 'foi',
  // Pack hunting_season (09/10/2026) : Reptilian Rage (hs060) pose de la « honte » sur Curtis.
  shame: 'honte',
  // Packs TMNT (16/10/2026) : essaims de Donatello (td016/td017, PV = compteurs) et
  // Mutagen Bomb de Raphael (tr014).
  swarm: 'essaim',
  // Galactic Storm, scenario 5 (20/10/2026) : « Uses (7[per_hero] integrity counters) » de gs200 Holding Tank.
  integrity: 'intégrité',
  knucklehead: 'andouille',
  // Aspects TMNT Dual-Aspect (16/10/2026) : ud003 Heavy Metal entre en jeu avec 2 « amp counters ».
  amp: 'ampli',
  timer: 'minuteur',
  // Aspect TMNT Protection (16/10/2026) : Lindsey Baker (up022), Grotto (up014), Road Rage (up031).
  healing: 'guérison',
  brute: 'brute',
  fuel: 'carburant',
  // Galactic Storm, heros Quasar (20/10/2026) : « Uses (3 duty counters) » de gs065 Protector of the Universe.
  duty: 'devoir',
  // Punisher MC×DC 2026, set Hobgoblin (21/10/2026) : Rabble (pu076) entre en jeu avec 2 « drone counters ».
  drone: 'drone',
  // SWAT Team (21/10/2026) : les « wanted counters » de la manigance SWAT (pu119).
  wanted: 'recherché',
  // Campagne Punisher (22/10/2026) : S.H.I.E.L.D. Support Team (pu145).
  intelligence: 'renseignement',
  // Pack TMNT Venus (16/10/2026) : compteurs de dragage poses sur l'identite (tv001a, tv001b, tv003-tv013).
  dredge: 'dragage',
  // Pack Jennika (16/10/2026) : les compteurs de Fearless Resolve (tj006).
  samurai: 'samouraï',
  // TMNT Shinobi Ninjutsu (17/10/2026) : Hamato Clan (sa007) pose des « shadow counters », Smoke Bombs
  // (sa008) entre en jeu avec 2 « smoke counters ».
  shadow: 'ombre',
  smoke: 'fumée',
  // Pack TMNT Shinobi Taijutsu (17/10/2026) : « Uses (3 cudgel counters) » de sh016 Jō.
  cudgel: 'bâton',
  // Scenario Baxter Stockman (16/10/2026) : sbires SWARM a compteur nomme (Roadkill Rodneys,
  // Auto Defense Bots, Superfly).
  cable: 'câble',
  shield: 'bouclier',
  ooze: 'mutagène',
  // Aspect TMNT Justice (16/10/2026) : Ram-Shell uj026 (momentum, aussi Juggernaut), Zebulon uj039,
  // Turtle Line uj034 (Uses 3 rope).
  momentum: 'élan',
  scorch: 'brûlure',
  rope: 'corde',
}

/** « steel » → « acier » en français, « steel » en anglais ; « tic_tac_toe_1_1 »
 *  garde ses mots séparés. */
export function nomDeCompteur(cle: string): string {
  const lisible = cle.replace(/_/g, ' ')
  if (langueActuelle() !== 'fr') return lisible
  return COMPTEURS_FR[cle] ?? lisible
}
