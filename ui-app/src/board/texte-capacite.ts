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

export function extraireCapacite(
  texte: string | undefined,
  nomOption: string,
  typeDemande?: string
): string | undefined {
  if (!texte) return undefined
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
