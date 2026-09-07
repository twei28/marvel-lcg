// « Le moteur attend le joueur » vient de l'etat du MOTEUR, jamais de la
// visibilite d'un panneau.
//
// Constate en partie reelle (Bishop contre Ultron, mode Detaille) : pendant le
// CIBLAGE du choix des deux sbires a activer, le panneau central disparaissait
// (le joueur repond alors en cliquant les cartes sur la table, puis
// « Valider ») et le cartouche du deroule se redeployait par-dessus pour
// annoncer « La suite arrive… ». C'etait exactement le mensonge deja corrige
// une fois pour le panneau : le joueur attendait le moteur, qui l'attendait.
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import type { Demande } from './ask'
import { DeroulePhase } from './DeroulePhase'
import { moteurAttendUneReponse } from './DemandeCentrale'
import type { EtapeDeroule } from './deroule-phase'

/** Une question du moteur qui s'affiche au centre (« quel sbire d'abord ? »). */
const question: Demande = {
  options: [],
  prompt_text: 'Minion Activates Order',
  event_name: 'WhenEnemyActivateOrder',
  show_cancel: false,
  ability_type: 'Normal',
}

/** La question de la barre du bas : le tour libre du joueur. */
const tourLibre: Demande = {
  options: [],
  prompt_text: '',
  event_name: 'WhenPlayerInTurn',
  show_cancel: true,
  ability_type: 'Normal',
}

const etatMoteur = {
  aNous: true,
  connecte: true,
  demande: question,
  validationRequise: false,
}

describe('le signal « le moteur attend le joueur »', () => {
  it('reste vrai pendant un ciblage, quand le panneau central a cede la place', () => {
    // Le ciblage est un etat de l'INTERFACE (`interaction.option` dans
    // board.tsx) : il cache le panneau, il ne change rien a ce que le moteur
    // attend. Le signal ne le connait donc pas, et c'est le but.
    expect(moteurAttendUneReponse(etatMoteur)).toBe(true)
    // Le panneau, lui, s'efface : c'est la composition que board.tsx fait
    // par-dessus le signal, reproduite ici a l'identique.
    const ciblageEnCours = true
    expect(moteurAttendUneReponse(etatMoteur) && !ciblageEnCours).toBe(false)
  })

  it('reste faux quand le moteur ne demande rien', () => {
    expect(moteurAttendUneReponse({ ...etatMoteur, demande: undefined })).toBe(false)
    expect(moteurAttendUneReponse({ ...etatMoteur, aNous: false })).toBe(false)
    expect(moteurAttendUneReponse({ ...etatMoteur, connecte: false })).toBe(false)
  })

  // Le cartouche doit garder son bilan DEPLOYE quand la phase est finie et que
  // le moteur rend la main au joueur : cette question-la se repond dans la
  // barre du bas, pas au centre.
  it('reste faux sur la question du tour libre', () => {
    expect(moteurAttendUneReponse({ ...etatMoteur, demande: tourLibre })).toBe(false)
  })

  // LE CAS DE LA BARRE DU BAS. Le moteur pose sa question PENDANT qu'une trame
  // est retenue : « Black Widow is being attacked by Ultron · Defendre /
  // Passer » s'affichait dans la barre du bas et le cartouche continuait
  // d'annoncer « La suite arrive… » par-dessus (doute 1 du rapport A3-fix,
  // doute 3 du rapport A4, releve trois fois en partie reelle).
  //
  // La garde `!validationRequise` avait ete gardee comme filet : un cartouche
  // replie n'a plus de bouton, et le replier pendant qu'une trame est retenue
  // ne laisserait plus personne la relacher. Ce filet est desormais porte la ou
  // il doit l'etre — dans `cartoucheAJour`, ou une question du moteur est une
  // RAISON D'ACQUITTER (voir DeroulePhase.tsx) — et le signal, lui, dit
  // simplement la verite.
  it('reste vrai quand le moteur pose sa question en retenant sa trame', () => {
    // Une variable, et non un litteral passe directement : le champ ne fait
    // meme plus partie de ce que le signal demande, et c'est le fond de la
    // correction.
    const trameRetenue = { ...etatMoteur, validationRequise: true }
    expect(moteurAttendUneReponse(trameRetenue)).toBe(true)
  })

  it('fait dire au cartouche que le moteur attend, jamais que la suite arrive', () => {
    const etape: EtapeDeroule = {
      cle: 'menace:0:9',
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      cibleNom: 'Assault on NORAD',
      montant: 1,
      boosts: [],
    }
    render(
      <DeroulePhase
        etapes={[etape]}
        phaseMechantEnCours
        questionAuJoueur={moteurAttendUneReponse(etatMoteur)}
        onTerminer={() => {}}
      />
    )
    expect(screen.getByText('Le moteur attend ta réponse')).toBeInTheDocument()
    expect(screen.queryByText('La suite arrive…')).not.toBeInTheDocument()
  })
})
