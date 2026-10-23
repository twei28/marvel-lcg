// LA RECHERCHE DANS LES REGLAGES (23/10/2026) : « Chercher un reglage » retrouve une ligne par son nom ou son aide, dans les quatre onglets a la fois.
//
// Le filtre travaille sur le DOM rendu, par onglet : chaque enfant direct d'un onglet est un TITRE de section (`.reglages-groupe`), une
// LIGNE de reglage, ou une note. Une ligne reste si TOUS les mots de la requete se trouvent dans son intitule et son aide (les libelles
// des pastilles « Non / 2 s / 5 s » ne comptent pas : « non » ne doit pas tout garder). Un titre reste si au moins une ligne de sa section
// reste. Les notes (raccourcis, aide du temps par decision) disparaissent pendant la recherche.

/** Minuscules, sans accents ni ponctuation de liaison : « Météo » et « meteo » se trouvent l'un l'autre. */
export function normaliser(texte: string): string {
  return texte
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[’']/g, ' ')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim()
}

/** Tous les mots de la requete figurent dans le texte (ordre libre). Requete vide : tout correspond. */
export function correspond(texte: string, requete: string): boolean {
  const mots = normaliser(requete).split(' ').filter(Boolean)
  if (mots.length === 0) return true
  const cible = normaliser(texte)
  return mots.every((mot) => cible.includes(mot))
}

/** Ce qui se lit d'une ligne : son intitule et son aide, pas ses pastilles de choix. */
function texteDeLaLigne(element: HTMLElement): string {
  const libelle = element.querySelector('.ligne-option-libelle')
  return (libelle ?? element).textContent ?? ''
}

function cacher(element: HTMLElement, cache: boolean): void {
  element.hidden = cache
  element.style.display = cache ? 'none' : ''
}

/**
 * Applique la requete a tous les onglets rendus sous `racine` (un conteneur `[data-onglet]` par onglet). Rend le nombre de lignes qui
 * restent visibles. Requete vide : tout est remontre.
 */
export function filtrerReglages(racine: HTMLElement, requete: string): number {
  const vide = normaliser(requete) === ''
  let visibles = 0
  for (const onglet of racine.querySelectorAll<HTMLElement>('[data-onglet]')) {
    let titre: HTMLElement | undefined
    let lignesDeLaSection = 0
    let derniereLigneGardee = true
    const fermerSection = () => {
      if (titre) cacher(titre, !vide && lignesDeLaSection === 0)
    }
    for (const enfant of Array.from(onglet.children) as HTMLElement[]) {
      if (enfant.classList.contains('reglages-groupe')) {
        fermerSection()
        titre = enfant
        lignesDeLaSection = 0
        continue
      }
      // Les pastilles de l'apercu d'ambiance sont un COMPLEMENT de la ligne qui les precede : elles suivent son sort.
      if (enfant.classList.contains('apercu-pastilles')) {
        cacher(enfant, !vide && !derniereLigneGardee)
        continue
      }
      const estLigne = enfant.classList.contains('ligne-option') || enfant.classList.contains('reglage-teinte')
      if (!estLigne) {
        // Une note : elle n'a de sens que dans son onglet, pas dans une liste de resultats.
        cacher(enfant, !vide)
        continue
      }
      const garde = vide || correspond(texteDeLaLigne(enfant), requete)
      cacher(enfant, !garde)
      derniereLigneGardee = garde
      if (garde) {
        lignesDeLaSection += 1
        visibles += 1
      }
    }
    fermerSection()
  }
  return visibles
}
