// LA TABLE PAR BRIQUES, le rendu (decisions du 05/10/2026) : de la liste
// d'emplacements que construit `construirePlateau` (zones.ts) et de la
// disposition (table-briques.ts), on tire les ZONES A DESSINER.
//
// Une zone qui reprend exactement un emplacement d'origine le rend TEL QUEL :
// la table d'origine est donc strictement la meme qu'avant. Les autres (une
// brique sortie de sa zone, deux briques d'origines differentes reunies) sont
// ASSEMBLEES : leurs groupes viennent des emplacements d'origine, dans l'ordre
// ou zones.ts les a poses, et leur titre est celui des briques.
//
// Module PUR.

import { t } from './langue'
import { NOMS, ancre, titreDeZone, type CleBrique, type Disposition, type Zone } from './table-briques'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from './zones'

/** L'emplacement d'origine (zones.ts) ou vit chaque brique. */
export const EMPLACEMENT_DE_BRIQUE: Record<CleBrique, CleEmplacement> = {
  'piles-rencontre': 'piles-rencontre',
  mechant: 'rencontre',
  'manigance-principale': 'complot-principal',
  'manigances-annexes': 'complots-secondaires',
  allies: 'terrain-combat',
  sbires: 'terrain-combat',
  environnements: 'terrain-combat',
  heros: 'terrain-soutien',
  soutiens: 'terrain-soutien',
  'piles-joueur': 'piles-joueur',
  annexes: 'annexes',
  main: 'main',
}

/** Les emplacements qui suivent le heros dans sa zone (deck special, reserve, marée montante). */
export const ACCOMPAGNEMENT: readonly CleEmplacement[] = ['deck-special', 'reserve', 'rising-tide']

export type ZoneRendue = {
  /** Le nom de l'aire de grille de la zone : sa premiere brique. */
  aire: CleBrique
  /** La zone de la disposition : sa place et la taille de ses cartes. */
  zone: Zone
  /** Ce qu'elle montre ; `undefined` = rien a montrer, la place reste vide. */
  emplacement?: EmplacementAffiche
  /** Les zones personnelles du heros, a sa gauche : seulement dans la zone qui a la brique Heros. */
  accompagnement: EmplacementAffiche[]
  /** La zone porte la brique Heros. */
  avecHeros: boolean
}

const briqueSeule = (cle: CleEmplacement): CleBrique | undefined =>
  (Object.keys(EMPLACEMENT_DE_BRIQUE) as CleBrique[]).find((b) => EMPLACEMENT_DE_BRIQUE[b] === cle)

export function assemblerZones(plateau: Plateau, disposition: Disposition): ZoneRendue[] {
  const parCle = new Map(plateau.emplacements.map((e) => [e.cle, e] as const))
  return disposition.zones.map((zone): ZoneRendue => {
    const avecHeros = zone.briques.includes('heros')
    const accompagnement = avecHeros
      ? ACCOMPAGNEMENT.map((cle) => parCle.get(cle)).filter((e): e is EmplacementAffiche => e !== undefined)
      : []
    const base = { aire: ancre(zone), zone, accompagnement, avecHeros }

    const origines = [...new Set(zone.briques.map((b) => EMPLACEMENT_DE_BRIQUE[b]))]
    const tout = origines.length === 1 && (Object.keys(EMPLACEMENT_DE_BRIQUE) as CleBrique[])
      .filter((b) => EMPLACEMENT_DE_BRIQUE[b] === origines[0])
      .every((b) => zone.briques.includes(b))
    if (tout) return { ...base, emplacement: parCle.get(origines[0]) }

    const choisis: {
      groupe: UniteAffichee[]
      origine: EmplacementAffiche
      proprietaire?: number
      pile?: string
      brique: CleBrique
    }[] = []
    for (const origine of plateau.emplacements) {
      if (!origines.includes(origine.cle)) continue
      origine.groupes.forEach((groupe, index) => {
        const brique = origine.groupesBriques?.[index] ?? briqueSeule(origine.cle)
        if (!brique || !zone.briques.includes(brique)) return
        choisis.push({
          groupe,
          origine,
          proprietaire: origine.proprietaires?.[index],
          pile: origine.groupesPiles?.[index],
          brique,
        })
      })
    }
    if (choisis.length === 0) return base

    const emplacementsDOrigine = [...new Set(choisis.map((c) => c.origine.cle))]
    return {
      ...base,
      emplacement: {
        cle: emplacementsDOrigine[0],
        titre: titreDeZone(zone.briques, (b) => t(NOMS[b]), t('et')),
        groupes: choisis.map((c) => c.groupe),
        nombreSurLaLigne: choisis.reduce((total, c) => total + c.groupe.length, 0),
        ...(choisis.every((c) => c.proprietaire !== undefined)
          ? { proprietaires: choisis.map((c) => c.proprietaire as number) }
          : {}),
        ...(choisis.some((c) => c.pile !== undefined) ? { groupesPiles: choisis.map((c) => c.pile) } : {}),
        groupesBriques: choisis.map((c) => c.brique),
        emplacementsDOrigine,
        groupesDOrigine: choisis.map((c) => c.origine.cle),
      },
    }
  })
}
