// LA GATE DU RYTHME : rien ne relâche la trame à la place du joueur.
//
// ⚠ POURQUOI CETTE GATE EXISTE. Le défaut « ça continue tout seul » a été
// signalé TROIS FOIS le 14/09/2026, avec trois causes différentes :
//   1. le réglage « Avance toute seule », grisé hors du mode Détaillé mais dont
//      la valeur s'appliquait quand même (corrigé, `avance-auto-mode.test.ts`) ;
//   2. le mode lui-même, tant qu'il n'existait pas ;
//   3. l'ANNONCE, qui acquitte toute seule en mode Détaillé.
//
// La troisième est celle que ce fichier garde. « Je te l'ai dit mille fois,
// pourquoi est-ce que ça continue tout seul sans que moi je mette suivant ? Ça
// ne devrait pas arriver. »
//
// ⚠ ET LE DÉFAUT EST SILENCIEUX : rien ne plante, rien ne rougit, la phase
// défile simplement sans qu'on ait cliqué. C'est exactement ce qu'un test doit
// garder, parce qu'on ne le verra pas en travaillant.
import { describe, expect, it } from 'vitest'
import { cartoucheEstAJour, type EtatDuCartouche } from './cartouche-a-jour'

/** Une phase ordinaire, en cours, rien de particulier. */
const enCours = (sur: Partial<EtatDuCartouche> = {}): EtatDuCartouche => ({
  termine: false,
  partieFinie: false,
  sansEtape: false,
  questionAuJoueur: false,
  surLaDerniereEtape: true,
  etapeValidee: false,
  etapeEstAnnonce: false,
  surTable: false,
  ...sur,
})

describe('⚠ sur la table, RIEN n’avance sans le clic du joueur', () => {
  it('une étape ordinaire non validée retient la trame', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true }))).toBe(false)
  })

  it('⚠ une ANNONCE non validée la retient AUSSI', () => {
    // LE CAS QUI COMPTE. En Détaillé elle acquitte seule (décision 7 du
    // 07/09/2026) ; ici l'utilisateur a décidé l'inverse : deux clics par
    // attaque, l'annonce portant le premier, « parce que c'est là aussi où on
    // peut choisir de défendre ». Sans cette garde, CHAQUE annonce relâchait la
    // trame et toute la phase défilait sans un clic.
    expect(cartoucheEstAJour(enCours({ surTable: true, etapeEstAnnonce: true }))).toBe(false)
  })

  it('le clic, et lui seul, la relâche', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, etapeValidee: true }))).toBe(true)
  })

  it('aucune combinaison ne relâche une étape non validée', () => {
    // Le balayage : deux booléens indépendants, quatre cas, tous retenus tant
    // que le joueur n'a pas cliqué.
    for (const etapeEstAnnonce of [false, true]) {
      for (const surLaDerniereEtape of [false, true]) {
        expect(
          cartoucheEstAJour(enCours({ surTable: true, etapeEstAnnonce, surLaDerniereEtape })),
          `annonce=${etapeEstAnnonce} derniere=${surLaDerniereEtape}`
        ).toBe(false)
      }
    }
  })
})

describe('une suite différée : l’annonce validée dont la conséquence est déjà inscrite (19/10/2026)', () => {
  it('relâche le moteur pour qu’il résolve l’attaque, sans sauter à la conséquence', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, etapeEstAnnonce: true, etapeValidee: true, surLaDerniereEtape: false, suiteDifferee: true }))).toBe(true)
  })

  it('⚠ TÉMOIN : tant que l’annonce n’est pas validée, le moteur reste retenu', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, etapeEstAnnonce: true, etapeValidee: false, surLaDerniereEtape: false, suiteDifferee: true }))).toBe(false)
  })

  it('⚠ TÉMOIN : sans suite différée, une étape validée qui n’est pas la dernière ne relâche rien', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, etapeValidee: true, surLaDerniereEtape: false }))).toBe(false)
  })
})

describe('le mode « Détaillé » garde son rythme d’origine', () => {
  it('une annonce y acquitte toute seule : c’est la décision 7 du 07/09/2026', () => {
    expect(cartoucheEstAJour(enCours({ etapeEstAnnonce: true }))).toBe(true)
  })

  it('une étape ordinaire y attend le clic, comme ailleurs', () => {
    expect(cartoucheEstAJour(enCours())).toBe(false)
  })
})

describe('ce qui relâche la trame dans TOUS les modes', () => {
  // ⚠ CES QUATRE-LÀ NE SONT PAS DES EXCEPTIONS DE CONFORT : sans eux la partie
  // se bloque jusqu'au filet anti-blocage de 90 secondes.
  it('la phase racontée jusqu’au bout', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, termine: true }))).toBe(true)
  })

  it('la partie finie', () => {
    expect(cartoucheEstAJour(enCours({ surTable: true, partieFinie: true }))).toBe(true)
  })

  it('aucune étape à montrer', () => {
    // Une trame qui ne fabrique aucune étape : la retenir figerait la phase sur
    // le premier micro-événement muet.
    expect(cartoucheEstAJour(enCours({ surTable: true, sansEtape: true }))).toBe(true)
  })

  it('⚠ une question du moteur', () => {
    // Retenir ici ne protège de RIEN : le moteur ne produit plus rien tant
    // qu'on ne lui a pas répondu, et c'est notre accusé qui lui permet
    // d'ARRIVER à sa question. Ne pas acquitter bloquerait la partie.
    expect(cartoucheEstAJour(enCours({ surTable: true, questionAuJoueur: true }))).toBe(true)
  })
})

describe('le cartouche qui n’est pas au bout', () => {
  it('retient tant qu’il lui reste des étapes à montrer', () => {
    expect(cartoucheEstAJour(enCours({ surLaDerniereEtape: false }))).toBe(false)
    expect(cartoucheEstAJour(enCours({ surLaDerniereEtape: false, etapeValidee: true }))).toBe(false)
  })
})
