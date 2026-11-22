// narration-fr.ts — ce que la narration du moteur laisse EN ANGLAIS dans une partie en français (journal, titres de fenêtre).
//
// Demande de l'utilisateur (16/11/2026, suite du rapport n°134 « encore quelques infos en anglais ») : tout ce qui est en
// anglais et pas en français, pour tous les héros. Le relevé vient de vraies parties jouées par le pilote automatique
// (Spider-Man, Dazzler, Blade, Captain Marvel) : les ~250 lignes distinctes du journal, triées à la main. Restaient :
//   - les ÉTAPES de mise en place (« Set Up », « Draw Cards », « Resolve Mulligans »...) et les noms de phase (« Player ») ;
//   - les NOMS DE PILES (« Dazzler's PlayerDeck<39> », « EncounterDiscardPile<0> ») ;
//   - les STATUTS bruts (« Stunned », « Confused », « Tough ») et les mots-clés (« overkill », « piercing ») ;
//   - les NOMS D'ÉVÉNEMENTS du moteur (« "WhenEffectWouldResolve" ») et les types d'effet entre parenthèses.
// Le texte arrive déjà en français pour tout le reste (data/translate_fr.json) : on ne touche qu'à ces restes, mot pour mot,
// et seulement quand la partie est en français.
import { MOTEUR_FR, traduireMoteur } from './vocabulaire-moteur'

/** Les titres d'étape que le moteur écrit entre « --- » : le texte EXACT, sans les tirets. */
const ETAPES: Readonly<Record<string, string>> = {
  'Game Start': 'Début de la partie',
  'Select Hero and Villain': 'Choix du héros et du méchant',
  'Set Up': 'Mise en place',
  'Scenario Setup': 'Mise en place du scénario',
  'Draw Cards': 'Pioche des cartes',
  'Resolve Mulligans': 'Résolution des mulligans',
  'Resolve Character Setup Abilities': 'Capacités de mise en place des personnages',
  'Encounter Cards Phase': 'Phase des cartes rencontre',
  'Additional turn': 'Tour supplémentaire',
  'Phase : Villain (skipped)': 'Phase : Méchant (passée)',
  'Init Finished': 'Fin de la mise en place',
}

/** Le nom de phase dans « Phase : Player » / « Fin de phase : Villain ». */
const PHASES: Readonly<Record<string, string>> = { Player: 'Joueurs', Villain: 'Méchant' }

const STATUTS: Readonly<Record<string, string>> = { Stunned: 'Sonné', Confused: 'Désorienté', Tough: 'Tenace' }

/** Les mots-clés écrits entre parenthèses (« gagne (piercing) de... »). */
const MOTS_CLES: Readonly<Record<string, string>> = { overkill: 'Déferlement', piercing: 'Perçant', ranged: 'À Distance' }

/** Le type d'effet que le moteur cite entre parenthèses à la fin d'une ligne. */
const EFFETS: Readonly<Record<string, string>> = {
  'Main Scheme Phase Place Threat': 'étape de la manigance principale',
  'Game Rule': 'règle du jeu',
  rule: 'règle du jeu',
  Scheme: 'manigance',
  'When Revealed': 'une fois révélée',
}

/** « WhenPlayerLikeInTurn » -> « Considéré comme son tour » : par le vocabulaire du plateau, ou à défaut sans le « When ». */
function evenement(nom: string): string {
  const espace = nom.replace(/([a-z])([A-Z])/g, '$1 $2').replace(/^(?:When|After|Before) /, '')
  return MOTEUR_FR[espace] ?? espace
}

export function narrationEnFrancais(texte: string): string {
  let sortie = texte

  // 1. Les titres d'étape, avec ou sans leurs tirets.
  sortie = sortie.replace(/^([ \t]*(?:-{3}[ \t]*)?)([^\n-][^\n]*?)([ \t]*(?:-{3})?[ \t]*)$/gm, (tout, avant: string, corps: string, apres: string) => {
    const nom = corps.trim()
    return ETAPES[nom] ? `${avant}${ETAPES[nom]}${apres}` : tout
  })
  // « Phase : Player » / « Fin de phase : Villain »
  sortie = sortie.replace(/\b(Phase|Fin de phase) : (Player|Villain)\b/g, (_, mot: string, phase: string) => `${mot} : ${PHASES[phase]}`)

  // 2. Les noms de piles : « Dazzler's PlayerDeck<39> » -> « Deck de Dazzler ».
  const NOM = "((?:[A-ZÀ-Ý][\\p{L}\\p{N}.\\-]*)(?: [A-ZÀ-Ý][\\p{L}\\p{N}.\\-]*){0,2})"
  sortie = sortie
    .replace(new RegExp(`${NOM}'s PlayerDeck<\\d+>`, 'gu'), 'deck de $1')
    .replace(new RegExp(`${NOM}'s DiscardPile<\\d+>`, 'gu'), 'défausse de $1')
    .replace(new RegExp(`${NOM}'s BoostCardsDeck<\\d+>`, 'gu'), 'pile de boost de $1')
    // « vers Concert en Direct's PlaceCardArea<3> » : le porteur peut avoir des mots en minuscules (« Concert en Direct »).
    .replace(/vers ([^\n()]+?)'s PlaceCardArea<\d+>/g, 'vers la zone à côté de $1')
    .replace(new RegExp(`${NOM}'s PlaceCardArea<\\d+>`, 'gu'), 'zone à côté de $1')
    .replace(/EncounterDiscardPile<\d+>/g, 'défausse de rencontre')
    .replace(/EncounterDeck<\d+>/g, 'deck de rencontre')
    .replace(/BoostCardsDeck<\d+>/g, 'pile de boost')
    .replace(/AsideDeck<\d+> créé/g, 'pile mise de côté créée')
    .replace(/AsideDeck<\d+>/g, 'pile mise de côté')
    // « déplacée(s) vers deck de Dazzler top » : la position dans la pile.
    .replace(/(deck de (?:rencontre|[^\n()]+?)) top(?=\s|$|\()/g, '$1, au-dessus')
    .replace(/(deck de (?:rencontre|[^\n()]+?)) bottom(?=\s|$|\()/g, '$1, en dessous')

  // 3. Statuts et mots-clés bruts.
  sortie = sortie.replace(/\b(Stunned|Confused|Tough)\b/g, (_, s: string) => STATUTS[s]!)
  sortie = sortie.replace(/\((overkill|piercing|ranged)\)/g, (_, k: string) => `(${MOTS_CLES[k]})`)

  // « ((^!2) Bomb Scare (When Revealed) [2] WhenCardRevealed) » : la carte et le moment, sans la plomberie du moteur.
  sortie = sortie.replace(/\(\(\^![^)]*\)\s*([^()]*?)\s*\(When Revealed\)\s*(?:\[\d+\])?\s*(?:When[A-Za-z]*)?\)/g, `($1, ${EFFETS['When Revealed']})`)

  // 4. Les noms d'événements du moteur : « "WhenEffectWouldResolve" », « WhenCardRevealed ».
  sortie = sortie.replace(/"(When[A-Z][A-Za-z]*)"/g, (_, nom: string) => `« ${evenement(nom)} »`)
  sortie = sortie.replace(/ \[\d+\] (When[A-Z][A-Za-z]*)\)/g, ')')

  // 5. Le type d'effet cité entre parenthèses : « (Main Scheme Phase Place Threat) », « (Game Rule) », « (rule) ».
  sortie = sortie.replace(/\(([A-Za-z ]+)\)/g, (tout, effet: string) => (EFFETS[effet] ? `(${EFFETS[effet]})` : tout))

  // 6. Les questions posées par un script (`AskChooseOneText(titre=...)`), reprises telles quelles au journal : « Cosmo: name a
  //    card type », « Jessica Drew: look at the top card of which deck? ». Même traduction que la fenêtre de la question.
  sortie = sortie.replace(
    /^([ \t]*)(.+?: (?:name a card type|name an encounter card type|discard the top card of which deck\?|look at the top card of which deck\?))[ \t]*$/gm,
    (_, avant: string, titre: string) => `${avant}${traduireMoteur(titre)}`
  )
  return sortie
}
