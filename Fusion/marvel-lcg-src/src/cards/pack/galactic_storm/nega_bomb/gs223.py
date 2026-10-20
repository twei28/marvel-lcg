from . import *

# Green Interference — TRAITRISE (Nega-Bomb), x2. ★ + 2 icones de boost.
# When Revealed: Remove 1 all-purpose counter from each card in play. If no counter was removed this way, this
#   card gains surge.
# ★ Boost: Remove 1 all-purpose counter from a card in play.
#
# Cartes de reference :
#  - **`aos/50029`** Press Conference : « remove 1 all-purpose counter from each support you control » ;
#    fiche mots-cles/all-purpose-counter.md (FAQ officielle : la carte qui porte le compteur en definit le
#    type : les compteurs « time » de la Nega-Bomb, « integrity » de Holding Tank, les Uses des cartes joueur
#    sont des compteurs polyvalents).
#  - **`27135`** Loose Ends : `ThisCardGainSurge(effect)` pour « this card gains surge ».
#  - Choix d'UNE carte : `ChooseAbilities` avec une option par carte (`gs207`).
#
# ⚠ Mots-pieges : « EACH card in play » (cartes de rencontre ET cartes joueur) ; « 1 » par carte ; « IF NO
# counter was removed this way » -> Renfort ; Boost : « A card in play » (une seule, choisie par le joueur
# active) ; les jetons de degats et de menace ne sont PAS des compteurs. Lecture (question Q5) : une carte
# qui porte deux sortes de compteurs en perd un de la premiere sorte trouvee.


def GetAbilities() -> Sequence['Ability']:

    def cartes_a_compteurs(effect: 'Effect') -> List['CardFace']:
        return [f for f in Worlds.GetOnFieldCards(effect) if f.IsInPlay() and CompteursPolyvalents(f)]

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        retires = 0
        for face in cartes_a_compteurs(effect):
            if RetirerUnCompteur(face, effect):
                retires += 1
        if retires == 0:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer() or Worlds.GetFirstPlayer(effect)
        faces = cartes_a_compteurs(effect)
        if not faces:
            return
        if len(faces) == 1:
            RetirerUnCompteur(faces[0], effect)
            return
        choix = []
        for face in faces:
            def retirer(targets: Sequence['CardFace'], face: 'CardFace' = face) -> None:
                Unused(targets)
                RetirerUnCompteur(face, effect)
            choix.append(AbilityFactory.ForChoiceAbility(
                f"Remove 1 counter from {face.paper.name.lstrip('* ')}", retirer))
        joueur.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
