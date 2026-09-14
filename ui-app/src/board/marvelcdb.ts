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

/**
 * Un identifiant de carte reconnu, marvelcdb ou non.
 *
 * `codeMarvelcdb()` répond à une autre question : « cette carte a-t-elle une
 * page sur marvelcdb ? ». Seul l'officiel en a une, et son format à cinq
 * chiffres le dit. Le contenu fan-made porte un préfixe de DEUX LETTRES
 * (voir `.planning/todos/2026-08-12-nommage-contenu-fanmade.md`) précisément
 * pour ne jamais entrer en collision avec la numérotation de FFG.
 *
 * Les deux rôles étaient confondus tant que le fan-made empruntait des numéros :
 * l'aperçu français des cartes fan-made passait par la garde marvelcdb, et il a
 * cessé de s'afficher à la seconde où elles ont pris leur vrai préfixe.
 */
export function codeCarteConnu(codeCarte: string | undefined): string | undefined {
  const correspondance = codeCarte?.match(/^(\d{5}[a-z]?|[a-z]{2}\d{3}[a-z]?)$/)
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
  /**
   * La carte n'a PAS de traduction française sur marvelcdb.
   *
   * ⚠ Le serveur RETIRE alors le texte, et c'est voulu. fr.marvelcdb.com rend
   * l'anglais quand la traduction manque, sans le dire : le joueur français
   * lisait donc de l'anglais sous une carte française (signalé en partie le
   * 14/09/2026). Le proxy le détecte en comparant `text` et `real_text`, qui
   * sont identiques dans ce cas. Ce drapeau reste pour qui voudrait un jour
   * l'afficher autrement ; aujourd'hui, l'absence de texte suffit à ne rien
   * montrer.
   */
  non_traduit?: boolean
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
