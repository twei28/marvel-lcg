// marvelcdb.ts — pont OPTIONNEL vers fr.marvelcdb.com.
//
// Deux usages, tous deux désactivables :
//  - lien « Voir sur marvelcdb » dans le menu d'une carte (aucun réseau tant
//    qu'on ne clique pas) ;
//  - texte officiel français de la carte dans l'aperçu, via le proxy serveur
//    /marvelcdb_card?<code> (AUCUNE requête si l'option est coupée, qui est
//    le défaut : le jeu doit marcher hors ligne).
export const CLE_TEXTES_CDB = 'marvel-board-marvelcdb'

export function lireTextesCdb(): boolean {
  try {
    return window.localStorage.getItem(CLE_TEXTES_CDB) === 'on'
  } catch {
    return false
  }
}

/** Code marvelcdb d'une carte du catalogue : l'API et les pages gardent le
    suffixe de face (01001a). Sinon undefined (cartes custom hors format). */
export function codeMarvelcdb(codeCarte: string | undefined): string | undefined {
  const correspondance = codeCarte?.match(/^(\d{5}[a-z]?)$/)
  return correspondance?.[1]
}

export function urlMarvelcdb(code: string): string {
  return `https://fr.marvelcdb.com/card/${code}`
}

export type TexteCdb = {
  name?: string
  text?: string
  flavor?: string
  traits?: string
}

const cache = new Map<string, TexteCdb | null>()

/** Texte de la carte via le proxy serveur ; null = introuvable (mémorisé). */
export async function texteMarvelcdb(code: string): Promise<TexteCdb | null> {
  const connu = cache.get(code)
  if (connu !== undefined) return connu
  try {
    const reponse = await fetch(`/marvelcdb_card?${code}`)
    if (!reponse.ok) {
      cache.set(code, null)
      return null
    }
    const donnees = (await reponse.json()) as TexteCdb
    const resultat = donnees && (donnees.text || donnees.name) ? donnees : null
    cache.set(code, resultat)
    return resultat
  } catch {
    cache.set(code, null)
    return null
  }
}
