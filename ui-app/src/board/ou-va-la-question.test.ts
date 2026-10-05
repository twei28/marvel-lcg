// LA GATE DE LA QUESTION : le moteur n'attend JAMAIS sans que l'écran le dise.
//
// ⚠ POURQUOI CETTE GATE EXISTE. Défaut signalé en partie le 14/09/2026 :
// « en mode détaillé il n'indique même plus quand on peut défendre, il fait
// cliquer sur la carte sans rien indiquer. C'est une putain de régression. »
//
// Mesuré en jeu (Rhino / Spider-Man, mode Détaillé, serveur de chantier) : à
// chaque attaque qui suit un dégât, le cartouche se repliait sur « tu peux
// défendre ou répondre » SANS UN SEUL BOUTON, pendant que l'animation de
// l'effet précédent finissait. Relevé du rendu à cet instant précis :
//   effets = 1, afficherDemandeCentrale = false, questionEnScene = false.
//
// ⚠ ET LE DÉFAUT EST SILENCIEUX, comme celui du rythme : rien ne plante, rien
// ne rougit. Il ne se voit qu'en jouant, à la seconde où l'on cherche le
// bouton « Défendre » et où il n'y en a pas.
import { describe, expect, it } from 'vitest'
import {
  narrationAuCentre,
  questionDansLaScene,
  questionDansLePanneau,
  type EtatDeLaQuestion,
} from './ou-va-la-question'

/** Le moteur demande « Défendre / Passer », en mode Détaillé, phase du méchant. */
const defense = (sur: Partial<EtatDeLaQuestion> = {}): EtatDeLaQuestion => ({
  moteurAttendLeJoueur: true,
  demandePresente: true,
  effetEnCours: false,
  ciblage: false,
  menuCarte: false,
  sceneCentrale: true,
  phaseMechantEnCours: true,
  questionDeLaManigance: false,
  ...sur,
})

describe('⚠ la fenêtre de défense s’annonce TOUJOURS quelque part', () => {
  it('la question se joue dans la scène du mode Détaillé', () => {
    expect(questionDansLaScene(defense())).toBe(true)
    expect(questionDansLePanneau(defense())).toBe(false)
  })

  it('⚠ UNE ANIMATION EN COURS NE LA FAIT PAS DISPARAÎTRE — le défaut du 14/09', () => {
    // LE CAS QUI COMPTE. Shocker attaque juste après les dégâts de Rhino :
    // l'animation tourne encore quand la question arrive. La scène est le seul
    // endroit où répondre — elle doit la porter quand même.
    const pendantUneAnimation = defense({ effetEnCours: true })
    expect(questionDansLaScene(pendantUneAnimation)).toBe(true)
    // Et la narration ne vient PAS se poser par-dessus les boutons.
    expect(
      narrationAuCentre(pendantUneAnimation, { connecte: true, evenementImportant: true })
    ).toBe(false)
  })

  it('un ciblage la remplace : c’est la table qui répond, pas la scène', () => {
    expect(questionDansLaScene(defense({ ciblage: true }))).toBe(false)
    expect(questionDansLePanneau(defense({ ciblage: true }))).toBe(false)
  })

  it('le menu d’une carte la remplace : il porte déjà les options', () => {
    expect(questionDansLaScene(defense({ menuCarte: true }))).toBe(false)
    expect(questionDansLePanneau(defense({ menuCarte: true }))).toBe(false)
  })

  it('sans question du moteur, rien ne s’affiche', () => {
    expect(questionDansLaScene(defense({ moteurAttendLeJoueur: false }))).toBe(false)
    expect(questionDansLePanneau(defense({ moteurAttendLeJoueur: false }))).toBe(false)
  })

  it('le client ne connaît pas encore la demande : on n’invente rien', () => {
    expect(questionDansLaScene(defense({ demandePresente: false }))).toBe(false)
    expect(questionDansLePanneau(defense({ demandePresente: false }))).toBe(false)
  })
})

describe('les deux panneaux ne s’affichent jamais ensemble', () => {
  it('la scène prend la question, le panneau central se tait', () => {
    const e = defense()
    expect(questionDansLaScene(e) && questionDansLePanneau(e)).toBe(false)
  })

  it('hors de la scène (mode « Sur la table », ou hors phase du méchant), le panneau prend la question', () => {
    expect(questionDansLePanneau(defense({ sceneCentrale: false }))).toBe(true)
    expect(questionDansLePanneau(defense({ phaseMechantEnCours: false }))).toBe(true)
  })

  it('hors de la scène, une animation garde sa priorité : la barre du bas reste pour répondre', () => {
    const horsScene = defense({ sceneCentrale: false, effetEnCours: true })
    expect(questionDansLePanneau(horsScene)).toBe(false)
    expect(narrationAuCentre(horsScene, { connecte: true, evenementImportant: false })).toBe(true)
  })
})

describe('la narration centrale', () => {
  it('se tait devant le panneau de question', () => {
    const e = defense({ sceneCentrale: false })
    expect(questionDansLePanneau(e)).toBe(true)
    expect(narrationAuCentre(e, { connecte: true, evenementImportant: true })).toBe(false)
  })

  it('ne dit rien quand il n’y a ni effet ni moment important', () => {
    expect(
      narrationAuCentre(defense({ moteurAttendLeJoueur: false }), {
        connecte: true,
        evenementImportant: false,
      })
    ).toBe(false)
  })

  it('ne dit rien hors connexion', () => {
    expect(
      narrationAuCentre(defense({ moteurAttendLeJoueur: false, effetEnCours: true }), {
        connecte: false,
        evenementImportant: true,
      })
    ).toBe(false)
  })
})

// LA QUESTION DE LA MANIGANCE N'APPARTIENT QU'AU PANNEAU.
//
// Defaut trouve en relecture le 15/09/2026 : `ou-va-la-question.ts` n'avait
// pas ete touche par le chantier de la face A. `DemandeCentrale` et
// `BarreAction` affichaient donc la MEME question sous le voile, avec le
// libelle brut « Reveal Main Scheme », absent de `dico-en.ts`. Pire : pendant
// les 400 ms du retournement, le panneau passe en `pointer-events: none`, le
// bouton ordinaire redevenait cliquable, contournait la garde du panneau et
// pouvait repondre a la question SUIVANTE a la place du joueur.
describe('la question de la manigance (Reveal_Main_Scheme)', () => {
  it('⚠ NE S’AFFICHE NI DANS LE PANNEAU CENTRAL NI DANS LA SCENE : le panneau de la manigance la porte seul', () => {
    const manigance = defense({ questionDeLaManigance: true })
    expect(questionDansLePanneau(manigance)).toBe(false)
    expect(questionDansLaScene(manigance)).toBe(false)
  })

  it('hors de la scene non plus : c’est la meme question, et elle a deja son panneau', () => {
    const manigance = defense({ questionDeLaManigance: true, sceneCentrale: false })
    expect(questionDansLePanneau(manigance)).toBe(false)
    expect(questionDansLaScene(manigance)).toBe(false)
  })

  it('la narration ne vient pas se poser par-dessus la carte montree en grand', () => {
    // La porte ci-dessus retire la question du panneau ET de la scene : sans
    // garde, `narrationAuCentre` en profiterait pour s'afficher AU CENTRE,
    // par-dessus le panneau de la manigance.
    const manigance = defense({ questionDeLaManigance: true, effetEnCours: true })
    expect(narrationAuCentre(manigance, { connecte: true, evenementImportant: true })).toBe(false)
  })

  it('n’enleve rien aux autres questions : sans elle, la regle ne bouge pas', () => {
    expect(questionDansLaScene(defense())).toBe(true)
    expect(questionDansLePanneau(defense({ sceneCentrale: false }))).toBe(true)
  })
})

// LE CARTOUCHE DU BAS (refonte du 04/10/2026, scene PC). Deux champs
// optionnels, faux par defaut : les seize cas ci-dessus ne bougent pas.
//  - `cartoucheEnBas` : pendant la phase, le cartouche colle en bas porte TOUT
//    (la question, et ce que la narration racontait au centre) ;
//  - `coupHorsPhaseEnScene` : hors phase, une attaque annoncee pendant le tour
//    du joueur ouvre le cartouche « Pendant ton tour », qui porte la defense.
describe('le cartouche du bas (scene PC)', () => {
  it('la narration se tait sous le cartouche du bas pendant la phase', () => {
    const sansQuestion = defense({ moteurAttendLeJoueur: false, effetEnCours: true, cartoucheEnBas: true })
    expect(narrationAuCentre(sansQuestion, { connecte: true, evenementImportant: true })).toBe(false)
    // Temoin : sans le cartouche du bas, la meme situation narre au centre.
    const temoin = defense({ moteurAttendLeJoueur: false, effetEnCours: true })
    expect(narrationAuCentre(temoin, { connecte: true, evenementImportant: true })).toBe(true)
    // Hors phase, le cartouche du bas ne dit rien a la narration.
    const horsPhase = defense({ moteurAttendLeJoueur: false, effetEnCours: true, cartoucheEnBas: true, phaseMechantEnCours: false })
    expect(narrationAuCentre(horsPhase, { connecte: true, evenementImportant: true })).toBe(true)
  })

  it('hors phase, une annonce hors phase en scene met la question dans la scene', () => {
    const e = defense({ phaseMechantEnCours: false, coupHorsPhaseEnScene: true })
    expect(questionDansLaScene(e)).toBe(true)
    expect(questionDansLePanneau(e)).toBe(false)
  })

  it('hors phase sans coup : le panneau prend la question', () => {
    const e = defense({ phaseMechantEnCours: false, coupHorsPhaseEnScene: false })
    expect(questionDansLaScene(e)).toBe(false)
    expect(questionDansLePanneau(e)).toBe(true)
  })

  it('mode table hors phase : le panneau, meme avec un coup hors phase', () => {
    const e = defense({ sceneCentrale: false, phaseMechantEnCours: false, coupHorsPhaseEnScene: true })
    expect(questionDansLaScene(e)).toBe(false)
    expect(questionDansLePanneau(e)).toBe(true)
  })

  // LOT 5 (planche, etat 15b) : pendant le tour, « Spider-Man subit 4 dégâts »
  // se posait au centre pendant que le cartouche « Pendant ton tour » montrait
  // la meme attaque. Tant qu'un cartouche du bas est a l'ecran hors phase (ce
  // coup, ou la relecture du journal), il est le seul a raconter.
  it('hors phase, la narration se tait tant qu un cartouche du bas est a l ecran', () => {
    const affiche = defense({
      moteurAttendLeJoueur: false,
      effetEnCours: true,
      cartoucheEnBas: true,
      phaseMechantEnCours: false,
      cartoucheHorsPhaseAffiche: true,
    })
    expect(narrationAuCentre(affiche, { connecte: true, evenementImportant: false })).toBe(false)
    // Temoin : le meme effet sans cartouche a l'ecran narre au centre.
    expect(narrationAuCentre({ ...affiche, cartoucheHorsPhaseAffiche: false }, { connecte: true, evenementImportant: false })).toBe(true)
  })
})
