from . import *

# Underworld Impact — traitrise NEMESIS. Boost 1.
# When Revealed: Choose to either take 1 damage or place 1 threat on the main
#   scheme for each support you control. If you do not control any supports,
#   this card gains surge.
# [star] Boost: This card gets +1 boost icon ([boost]) for each support you
#   control.
#
# Cartes de reference :
#  - `50134` / `ho015` pour `this.PlaceThreatOnSchemes("MainScheme", n,
#    effect)`, et `08013` / `16155` pour le choix entre deux effets
#    (`ChooseAbilities` + `ForChoiceAbility`).
#  - `ag013` Hallucination (pack agent_13) pour `ThisCardGainSurge(effect)`.
#  - **`27082`** Biting Retort : le SEUL montage du depot qui modifie le
#    nombre d'icones de boost — `RegisterTemp(WhenBoostIconsWouldBeCount(
#    Temp0, ... UpdateBoostIcon(...)))`. Ici l'enregistrement se fait depuis
#    `WhenCardBecomeBoost`, qui est envoye a l'etape (b) de
#    `can_boost.py:79`, donc AVANT le `CountBoostIconsInternal()` de l'etape
#    (c) — l'ordre est verifie dans le moteur, pas suppose.
#    `WhenCardBecomeBoost.against_player` (sender_card.py:676) donne le
#    joueur vise, ce qu'aucun autre message de la chaine ne fournit.
#
# ⚠ PORTEE ARBITREE PAR L'UTILISATEUR (03/09/2026). « take 1 damage or place
# 1 threat on the main scheme **for each support you control** » : le « for
# each » porte sur LES DEUX options. Avec 3 soutiens, c'est 3 degats OU
# 3 menaces. La clause « If you do not control any supports, this card gains
# surge » le confirme : si « take 1 damage » valait 1 degat fixe, la carte
# resterait utile a 0 soutien et le Surge n'aurait pas lieu d'etre.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Choose** to either ... or ... » : un vrai choix offert au JOUEUR
#    vise, pas au premier joueur, et pas une resolution automatique.
#  - « **you** control » : les soutiens du joueur a qui la traitrise est
#    revelee. Les soutiens des autres joueurs ne comptent pas.
#  - « take 1 damage » : les degats vont a l'IDENTITE du joueur, pas a un
#    personnage au choix.
#  - « [star] Boost » sans « In expert mode » : capacite TOUJOURS active,
#    convention moteur (cf. 04125).
#  - ⚠ La carte est une machine a punir `as019` The Daily Bugle et `as022`
#    Spider-Verse, les deux soutiens du pack, et plus generalement les decks
#    de Protection charges en lieux. Plus on en pose, plus elle frappe fort,
#    des le boost.


def GetAbilities() -> Sequence['Ability']:

    def compter_soutiens(joueur: 'Player|None') -> int:
        if joueur is None:
            return 0
        return len(list(joueur.supports.Get()))

    def underworld_impact(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        combien = compter_soutiens(joueur)
        if joueur is None or combien <= 0:
            ThisCardGainSurge(effect)
            return

        identite = joueur.GetIdentity()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Take {combien} damage",
                lambda targets:
                    this.DealDamage([identite], combien, effect)
                    if identite is not None else None,
            ),
            AbilityFactory.ForChoiceAbility(
                f"Place {combien} threat on the main scheme",
                lambda targets:
                    this.PlaceThreatOnSchemes("MainScheme", combien, effect),
            ),
        )

    def underworld_impact_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        combien = compter_soutiens(message.against_player)
        if combien <= 0:
            return

        this.effect.RegisterTemp(
            AbilityFactory.WhenBoostIconsWouldBeCount(
                AbilityType.Temp0,
                lambda boost_effect, boost_message:
                    boost_message.UpdateBoostIcon(combien, boost_effect),
                conditions=[
                    lambda boost_effect, boost_message:
                        boost_effect.this is boost_message.trigger,
                ],
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            underworld_impact,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            underworld_impact_boost,
        ),
    ]
