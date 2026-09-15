// CHERCHER UN TEXTE QUI N'EST PLUS D'UN SEUL TENANT.
//
// ⚠ POURQUOI CE MODULE EXISTE (15/09/2026). Depuis que les noms de cartes sont
// survolables dans le cartouche du deroule, la phrase « Klaw attaque Colossus »
// s'ecrit `<b>Klaw</b><span> attaque </span><b>Colossus</b>`. Or `getByText` ne
// lit, par defaut, que les noeuds de texte DIRECTS d'un element : la phrase
// devenait introuvable.
//
// Introuvable, ce serait deja genant ; le vrai danger est ailleurs. Chaque
// `queryByText(…)` suivi de `.not.toBeInTheDocument()` se serait mis a PASSER
// alors que la phrase etait bien a l'ecran. Une batterie verte qui ne regarde
// plus rien est pire qu'une batterie rouge.
//
// On ne reecrit donc pas cent assertions : on remplace le comparateur. Il lit
// le `textContent` entier, et ne retient que l'element le PLUS PROFOND qui
// porte le texte — sinon chaque ancetre repondrait aussi, et la requete
// trouverait dix elements la ou elle en attend un.

import { screen as screenBrut, within, type Matcher, type SelectorMatcherOptions } from '@testing-library/react'

const normaliser = (texte: string | null | undefined) => (texte ?? '').replace(/\s+/g, ' ').trim()

/** Le texte DIRECT d'un element : ce que `getByText` lisait avant. */
function texteDirect(element: Element): string {
  return normaliser(
    Array.from(element.childNodes)
      .filter((noeud) => noeud.nodeType === noeud.TEXT_NODE)
      .map((noeud) => noeud.textContent)
      .join('')
  )
}

/**
 * Le meme critere, tolerant a une phrase decoupee en plusieurs elements.
 *
 * Une fonction ou un autre comparateur passe sans etre touche : seuls la chaine
 * et l'expression reguliere, qui lisent le texte, ont besoin de ce detour.
 */
export function texteEclate(attendu: Matcher): Matcher {
  const porte =
    typeof attendu === 'string'
      ? (element: Element) =>
          normaliser(element.textContent) === normaliser(attendu) ||
          texteDirect(element) === normaliser(attendu)
      : attendu instanceof RegExp
        ? (element: Element) =>
            // ⚠ UNE COPIE DE L'EXPRESSION, jamais l'originale : un drapeau `g`
            // garde `lastIndex` d'un appel a l'autre et rend un test sur deux.
            new RegExp(attendu.source, attendu.flags.replace('g', '')).test(
              normaliser(element.textContent)
            )
        : undefined
  if (!porte) return attendu
  return (_contenu: string, element: Element | null) => {
    if (!element || !porte(element)) return false
    // Le plus profond, et lui seul.
    return !Array.from(element.children).some((enfant) => porte(enfant))
  }
}

/** Les requetes de texte de `screen`, avec le comparateur tolerant. */
export const ecran = {
  ...screenBrut,
  getByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
    screenBrut.getByText(texteEclate(texte), options),
  queryByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
    screenBrut.queryByText(texteEclate(texte), options),
  getAllByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
    screenBrut.getAllByText(texteEclate(texte), options),
  queryAllByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
    screenBrut.queryAllByText(texteEclate(texte), options),
}

/** La meme chose, bornee a un element (comme `within`). */
export function dans(element: HTMLElement) {
  const brut = within(element)
  return {
    ...brut,
    getByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
      brut.getByText(texteEclate(texte), options),
    queryByText: (texte: Matcher, options?: SelectorMatcherOptions) =>
      brut.queryByText(texteEclate(texte), options),
  }
}
