// LES MOTS-CLÉS DE L'APERÇU, ET SURTOUT L'EXIGENCE.
//
// ⚠ POURQUOI CE FICHIER EXISTE. `Requirement` manquait à `mots-cles.ts` alors
// que 24 cartes du catalogue le portent (relevé dans `data/cards.json` le
// 15/09/2026) : le joueur lisait « Exigence ([mental]) » sur la carte, et
// l'aperçu ne lui disait pas ce que ça veut dire. Signalé dans
// `.planning/todos/2026-09-02-portage-viv-vision.md`.
//
// Le piège de ce mot-clé n'est pas son absence, c'est sa VALEUR : `desc`
// contient des COULEURS (« B », « BB », « YBR »), pas un nombre. Poussé comme
// les autres, il aurait affiché « Exigence YBR ».
import { describe, expect, it } from 'vitest'
import { couleursExigees, motsClesDeCarte } from './mots-cles'

/** Les mots-clés d'une carte qui ne porte QUE ce `desc`. */
const nomsDe = (desc: Record<string, string>) => motsClesDeCarte(desc, '').map((m) => m.nom)

describe('⚠ Exigence : le mot-clé de 24 cartes qui n’avait pas d’infobulle', () => {
  it('nomme le mot-clé par son nom officiel français', () => {
    // 27006 Web Binding : « Exigence ([mental]) » sur la carte FR.
    expect(nomsDe({ Requirement: 'B' })).toEqual(['Exigence (mentale)'])
  })

  it('⚠ n’affiche JAMAIS la chaîne brute du moteur', () => {
    // LE CAS QUI COMPTE. Le suffixe commun (« Entrave 2 ») aurait collé la
    // valeur telle quelle : « Exigence YBR », qui ne veut rien dire.
    const nom = nomsDe({ Requirement: 'YBR' })[0]
    expect(nom).not.toMatch(/YBR/)
    // 27049 * Spider-Man : « Exigence ([energy] [mental] [physical]) ».
    expect(nom).toBe('Exigence (énergie, mentale, physique)')
  })

  it('⚠ garde la RÉPÉTITION : « BB » veut dire DEUX mentales', () => {
    // 29020 R&D Facility. Dédoublonner effacerait la moitié de la règle.
    expect(nomsDe({ Requirement: 'BB' })).toEqual(['Exigence (mentale, mentale)'])
  })

  it('donne une définition, et elle dit le piège', () => {
    const [mot] = motsClesDeCarte({ Requirement: 'B' }, '')
    // « Requirement ([mental]) » sur une carte à 2 se lit « 2, dont au moins 1
    // mentale », et non « 2 + 1 mentale » (docs/reference/mots-cles/requirement.md).
    expect(mot.definition).toMatch(/pas un coût en plus/i)
  })

  it('la ressource libre (wild) est nommée, elle aussi', () => {
    // Deux cartes du catalogue portent `Requirement: "G"`.
    expect(nomsDe({ Requirement: 'G' })).toEqual(['Exigence (libre)'])
  })

  it('une carte sans Exigence n’en montre pas', () => {
    expect(nomsDe({ Guard: '1' })).toEqual(['Garde'])
  })

  it('une valeur inconnue ne fabrique pas de parenthèses vides', () => {
    // Robustesse : si le moteur invente une lettre un jour, on montre le
    // mot-clé seul plutôt qu'un « Exigence () » qui ferait douter le joueur.
    expect(couleursExigees('ZZ')).toBe('')
    expect(nomsDe({ Requirement: 'ZZ' })).toEqual(['Exigence'])
  })
})

describe('les mots-clés déjà en place ne bougent pas', () => {
  it('lit les clés de desc', () => {
    expect(nomsDe({ Patrol: '1', Toughness: '1' })).toEqual(['Patrouille', 'Ténacité'])
  })

  it('garde le suffixe numérique des autres mots-clés', () => {
    expect(nomsDe({ Hinder: '2' })).toEqual(['Entrave 2'])
  })

  it('lit aussi le TEXTE de la carte', () => {
    expect(motsClesDeCarte({}, 'This attack has piercing.').map((m) => m.nom)).toEqual(['Perçant'])
  })
})
