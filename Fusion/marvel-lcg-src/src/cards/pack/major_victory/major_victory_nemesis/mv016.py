from . import *

# Accept Perfection — TRAHISON nemesis. Peril. Boost 2.
# When Revealed: Choose:
#  • Find Michael Korvac and reveal him. Place 4 threat on Korvac's Future.
#  • Discard the highest cost card you control.
#
# CARTES DE REFERENCE
#  - `21177` / `21188` : `Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` pour « find ».
#  - `07042` Oversized Hands : `player.DiscardControlCards(effect, .., highest_cost=True)` pour « discard the highest cost ».
#  - `mw013` : `ChooseAbilities(.., ForChoiceAbility(..), ForChoiceAbility(..))`.
#
# TEXTE CONTRE CODE
#  « Peril » -> `desc.Peril` (base automatique). « Choose: » -> le joueur choisit une des DEUX puces.
#  1re puce : Korvac est cherche (encounter deck, defausse, mis de cote) et REVELE ; ENSUITE 4 menaces sur Korvac's Future
#    (qui entre en jeu a la revelation de Korvac, d'ou l'ordre). Si Korvac est deja en jeu / introuvable, la menace est
#    quand meme posee si la Future est en jeu.
#  2e puce : « the highest cost card you control » = alliee, amelioration, soutien (`control=True`). Egalite : le joueur choisit.
#  Chiffres : 4 menaces.


def GetAbilities() -> Sequence['Ability']:

    def accept_perfection(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def trouver_korvac(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            face = Search.EncounterCard(
                effect,
                joueur,
                include_discard_pile=True,
                include_set_aside=True,
                name=NOM_KORVAC,
                card_type=Minion,
            )
            if face:
                face.Reveal(joueur, effect)
            future = FutureEnJeu(effect)
            if future is not None:
                this.PlaceThreatOnSchemes([future], 4, effect)

        def defausser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            joueur.DiscardControlCards(effect, control=True, highest_cost=True)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Find Michael Korvac and reveal him. Place 4 threat on Korvac's Future", trouver_korvac),
            AbilityFactory.ForChoiceAbility("Discard the highest cost card you control", defausser),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            accept_perfection,
        ),
    ]
