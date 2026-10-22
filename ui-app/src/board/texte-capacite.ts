// Le TEXTE d'une capacite que le moteur propose de declencher.
//
// « I Object! » de Jennifer Walters s'ouvre avant que la menace soit placee ;
// le panneau montrait le nom de la capacite et « Passer », rien de plus. Un
// nouveau joueur ne sait pas ce que fait I Object!, et devait survoler la
// carte pour le lire (signale en jeu le 12/09/2026, et decision : afficher le
// texte, meme en anglais, sous le bouton).
//
// Ce module est PUR. Il recoit le texte imprime (cards.json, anglais, ou
// TEXTES_FR quand le plateau a le francais) et le nom de l'option du moteur
// (« "I_Object!" », « Spider-Sense », « Interrupt »...), et rend la phrase de
// la capacite : le paragraphe qui porte ce nom, sinon celui qui commence par
// le mot-cle du type (Interrupt, Response, Action...), sinon tout le texte.

/** Un paragraphe par capacite : cards.json separe les capacites par un saut de ligne. */
function paragraphes(texte: string): string[] {
  return texte
    .split(/\n+/)
    .map((p) => p.trim())
    .filter(Boolean)
}

/** Le texte tel qu'on le lit : sans balises, avec les fleches et les traits. */
export function nettoyerTexteCarte(texte: string): string {
  return texte
    .replace(/<[^>]+>/g, '')
    .replace(/&#8594;|&rarr;/g, '→')
    .replace(/&quot;/g, '"')
    .replace(/\[star\]\s*/g, '★ ')
    // Les jetons de ressource survivent, sous leur forme a un crochet : ils sont
    // dessines en icones plus loin (`marquerRessources`).
    .replace(/\[\[(physical|mental|energy|wild|lightning)\]\]/g, '[$1]')
    .replace(/\[\[([^\]]+)\]\]/g, '$1')
    .replace(/\s+/g, ' ')
    .trim()
}

function normaliser(valeur: string): string {
  return valeur
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/[«»"'’!?.,:;()\[\]]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

/**
 * @param texte     le texte imprime de la carte porteuse (brut, balises comprises)
 * @param nomOption le nom de l'option du moteur (`Option.name`), brut
 * @param typeDemande `Demande.ability_type` (« Interrupt », « Response »...)
 */
const TRADUCTIONS: Readonly<Record<string, string>> = {
  forced: 'forcée',
  interrupt: 'interruption',
  response: 'réponse',
  hero: 'de héros',
  'alter-ego': "d'alter-ego",
  alterego: "d'alter-ego",
}

/** « forced response » -> « réponse forcée », « hero action » -> « action de héros ». */
function traductionsDuType(type: string): string[] {
  const traduits = type.split(' ').map((mot) => TRADUCTIONS[mot] ?? mot)
  // L'anglais met l'adjectif AVANT (« forced response »), le francais APRES
  // (« réponse forcée ») : on essaie les deux ordres.
  return [...new Set([normaliser(traduits.join(' ')), normaliser([...traduits].reverse().join(' '))])]
}

/**
 * La repartition de degats INDIRECTS (`PlayerAction.AssignDamage`, moteur :
 * « Assign 3 damage ») : une question de REGLE, que le moteur rattache a
 * l'identite. Rapport Yarro n92 (16/10/2026) : sous Starshark, le titre
 * affichait le seul paragraphe de Rocket Raccoon, « "Murdered You!" —
 * Response », sans rapport avec la question.
 */
export const REPARTITION_INDIRECTE = /^Assign[ _](\d+)[ _]damage$/

export function extraireCapacite(
  texte: string | undefined,
  nomOption: string,
  typeDemande?: string
): string | undefined {
  if (!texte) return undefined
  if (REPARTITION_INDIRECTE.test(nomOption)) return undefined
  const paras = paragraphes(texte).map(nettoyerTexteCarte).filter(Boolean)
  if (paras.length === 0) return undefined
  if (paras.length === 1) return paras[0]

  const nom = normaliser(nomOption.startsWith('p_') ? nomOption.slice(2) : nomOption)
  if (nom) {
    const nommee = paras.find((p) => normaliser(p).includes(nom))
    if (nommee) return nommee
  }
  // Le type vient du moteur, en anglais (« Interrupt », « Forced Response »,
  // « Alter-Ego Action ») ; le texte peut etre le francais officiel
  // (« Interruption », « Réponse forcée », « Action d'alter-ego »). On cherche
  // le debut du paragraphe avec les deux vocabulaires, le nom de la capacite
  // (« "Objection !" — ») retire.
  const type = normaliser(typeDemande ?? '')
  if (type) {
    const debuts = [type, ...traductionsDuType(type)]
    const parType = paras.find((p) => {
      const debut = normaliser(p.replace(/^.*?—\s*/, ''))
      return debuts.some((d) => debut.startsWith(d))
    })
    if (parType) return parType
  }
  return paras.join(' ')
}

/**
 * LA PHRASE DU BOOST ★ d'une carte rencontre (D10, cartouche du bas) : le
 * paragraphe qui porte « Boost », sans son mot-cle ni l'etoile. Le reste de la
 * carte (son effet « Une fois revelee ») n'a rien a faire sous la rangee de
 * l'attaque. `undefined` sans un tel paragraphe : la vue dit alors seulement
 * que l'effet s'applique.
 */
export function extraireBoost(texte: string | undefined): string | undefined {
  if (!texte) return undefined
  for (const paragraphe of paragraphes(texte)) {
    const lu = nettoyerTexteCarte(paragraphe)
    const trouve = /^(?:★\s*)?Boost\s*:\s*(.+)$/i.exec(lu)
    if (trouve) return trouve[1].trim()
  }
  return undefined
}

/**
 * LE TEXTE IMPRIME d'une carte rencontre revelee, une ligne par paragraphe,
 * sans ce que le cartouche dit deja ailleurs : le Renfort (la fleche) et le
 * Boost ★ (la ligne sous la rangee de l'attaque). Sert quand le moteur n'a
 * publie aucun resume de l'effet : le joueur lit alors la carte telle qu'elle
 * est imprimee, plutot que rien.
 */
export function extraireEffetRevele(texte: string | undefined): string[] {
  if (!texte) return []
  return paragraphes(texte)
    .map(nettoyerTexteCarte)
    .filter((ligne) => ligne !== '')
    .filter((ligne) => !/^(?:★\s*)?Boost\s*:/i.test(ligne))
    .filter((ligne) => !/^(?:Surge|Renfort)\s*\.?(?:\s*\(.*\))?$/i.test(ligne))
}

/**
 * LE NOM D'UNE ACTION quand une carte en offre PLUSIEURS du meme type (demande du 22/10/2026 : plus jamais « Action »
 * et « Action 1 » sans savoir laquelle fait quoi). Le moteur numerote les doublons (« Action », « Action_1 »...) ; les
 * cartes n'ont pas de nom pour leurs actions. On rend donc le RESUME du paragraphe imprime : l'index lu dans le nom de
 * l'option designe le N-ieme paragraphe de ce type dans le texte de la carte.
 *
 * `undefined` quand il n'y a rien a dire : pas une action, une seule action de ce type, texte absent, ou moins de
 * paragraphes de ce type que l'index ne l'exige (on garde alors le nom du moteur).
 */
const LIBELLES_ACTION: Readonly<Record<string, string[]>> = {
  action: ['Action'],
  'hero action': ['Hero Action', 'Action de héros', 'Action de heros'],
  'alter ego action': ['Alter-Ego Action', 'Alter Ego Action', 'Action d’alter-ego', "Action d'alter-ego", 'Action d’alter ego', "Action d'alter ego"],
  'first player action': ['First Player Action', 'Action du premier joueur'],
  'forced action': ['Forced Action', 'Action forcée'],
}

function echapper(valeur: string): string {
  return valeur.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

export function nomActionParlant(nomOption: string, texte: string | undefined): string | undefined {
  if (!texte) return undefined
  const brut = (nomOption.startsWith('p_') ? nomOption.slice(2) : nomOption).replaceAll('_', ' ').trim()
  const trouve = /^(.+?)(?: (\d+))?$/.exec(brut)
  if (!trouve) return undefined
  const base = normaliser(trouve[1]!)
  const libelles = LIBELLES_ACTION[base]
  if (!libelles) return undefined
  const index = trouve[2] ? Number(trouve[2]) : 0
  const motif = new RegExp(`^(?:★\\s*)?(?:[^:—]+—\\s*)?(?:${libelles.map(echapper).join('|')})\\s*:\\s*(.+)$`, 'i')
  const lignes = paragraphes(texte)
    .map(nettoyerTexteCarte)
    .map((p) => motif.exec(p)?.[1])
    .filter((p): p is string => Boolean(p))
  if (lignes.length < 2 || index >= lignes.length) return undefined
  const ligne = lignes[index]!.replace(/\s*\(Limit[^)]*\)\.?$/i, '').trim()
  if (ligne.length <= 64) return ligne
  const coupe = ligne.slice(0, 64)
  return `${coupe.slice(0, Math.max(coupe.lastIndexOf(' '), 32))}…`
}
