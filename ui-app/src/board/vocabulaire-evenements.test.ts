// AUCUN NOM D'ÉVÉNEMENT DU MOTEUR NE DOIT RESSORTIR EN ANGLAIS.
//
// ⚠ POURQUOI CETTE GATE EXISTE. Mesure du 15/09/2026, en vraie partie
// française : le surtitre de la narration centrale affichait « Scheme Place
// Threat », « Card Un Apply_Text », « Cards Moved To Revealing Area_Text ».
// Du moteur brut, au milieu d'un écran français. Constat de l'utilisateur :
// « quand je joue en français tout doit être en français ».
//
// ⚠ ET ELLE LIT LE MOTEUR, PAS UNE LISTE RECOPIÉE. Une liste figée ici aurait
// vieilli au premier message ajouté côté Python, et personne ne l'aurait su
// avant qu'un joueur tombe dessus. On relève donc les `Message.<Nom>` dans les
// sources, on leur applique le MÊME découpage que `libelleEvenement`, et on
// exige une traduction pour chacun.
//
// Ce qu'on ne réclame pas : les messages internes du moteur (`CheckIf…`,
// `Getting…`, `Calc…`, `Fake…`, `Text…`). Ce sont des questions que le moteur
// se pose à lui-même, jamais une narration montrée au joueur. Ils sont écartés
// par leur PRÉFIXE, pas un par un : une liste d'exceptions nominatives serait
// la même dette que la liste figée.
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import { traduireMoteur } from './vocabulaire-moteur'

/** La copie vivante du moteur (GUIDE-CREATION-CONTENU §1). */
const MOTEUR = '../Fusion/marvel-lcg-src/src'

/** Les préfixes des messages que le moteur s'envoie à lui-même. */
const INTERNES = /^(Check|Getting|Calc|Fake|Text)/

function fichiersPython(racine: string): string[] {
  const trouves: string[] = []
  for (const entree of readdirSync(racine)) {
    const chemin = join(racine, entree)
    if (statSync(chemin).isDirectory()) trouves.push(...fichiersPython(chemin))
    else if (entree.endsWith('.py')) trouves.push(chemin)
  }
  return trouves
}

/**
 * Le découpage de `libelleEvenement` (DemandeCentrale.tsx), à l'identique.
 *
 * ⚠ IL EST RECOPIÉ ICI, ET C'EST ASSUMÉ : la fonction n'est pas exportée, et
 * l'exporter pour un test donnerait l'impression qu'elle sert ailleurs. Si elle
 * change, cette gate rougit — c'est exactement ce qu'on veut d'une copie.
 */
function libelleEvenement(nom: string): string {
  return nom
    .replace(/^When/, '')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .replace(/^After /, '')
    .trim()
}

describe('les noms d’événement du moteur', () => {
  const noms = new Set<string>()
  for (const fichier of fichiersPython(MOTEUR)) {
    const source = readFileSync(fichier, 'utf-8')
    for (const trouve of source.matchAll(/Message\.([A-Za-z_][A-Za-z0-9_]*)/g)) {
      noms.add(trouve[1])
    }
  }

  it('le moteur en déclare bien une centaine : sinon c’est le chemin qui est faux', () => {
    // Sans cette garde, un chemin cassé rendrait un ensemble VIDE et la gate
    // passerait au vert en ne vérifiant rien. Même piège que le site anglais.
    expect(noms.size).toBeGreaterThan(150)
  })

  it('ont tous leur français : aucun ne peut s’afficher en anglais', () => {
    const sansTraduction = [...noms]
      .filter((nom) => !INTERNES.test(nom))
      .map(libelleEvenement)
      .filter((libelle) => libelle && traduireMoteur(libelle) === libelle)
      .sort()

    expect(
      sansTraduction,
      'ces noms d’événement s’afficheraient tels quels, en anglais, dans le ' +
        'surtitre de la narration centrale. Ajoute-les à MOTEUR_FR ' +
        `(vocabulaire-moteur.ts) :\n  ${sansTraduction.join('\n  ')}`
    ).toEqual([])
  })
})
