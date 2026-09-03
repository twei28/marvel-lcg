from . import *

# Love Concoction — ATTACHEMENT nemesis (N 5/5). ITEM. TEMPTATION.
# Aucune icone de boost chiffree, une icone [star].
# Attach to your identity.
# Forced Action: Exhaust this card and give the villain a facedown boost card
#   -> ready your identity.
# Alter-Ego Action: Exhaust this card and give the villain a facedown boost
#   card -> discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - `02048` All Tied Up pour `AttachToFaceWhenPutIntoPlay("YourIdentity")` et
#    `PlayerActionToDiscardThis` ;
#  - **`02035` Intimidation** pour « give the villain a facedown boost card » :
#    `Faces.GiveFacedownBoostCards(<vilains>, 1, effect)` ;
#  - `27078` "Now We're Angry!" / `ho017` pour `WhenCardBecomeBoost("This",
#    RevealThisCard)` — le helper existe deja dans `cards/pack/__init__.py`.
#
# ⚠ HOMONYME : `55014` Love Concoction (set Enchantress) est une AUTRE carte
# du meme personnage source. Deux cartes distinctes de meme nom.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Le cout est DOUBLE des deux cotes : incliner la carte ET donner une carte
#    de boost au vilain. Oublier la seconde moitie rendrait la carte gratuite
#    (piege `wd005`).
#  - « ready your identity » n'est PAS « discard this card » : la premiere
#    capacite laisse l'attachement en place, tour apres tour. C'est une
#    tentation, d'ou le trait : on peut rejouer chaque round au prix d'une
#    carte de boost donnee au vilain, ou payer pour s'en debarrasser.
#  - `Forced Action` : la phase du joueur ne peut pas se terminer tant qu'elle
#    est possible. Elle ne l'est plus une fois la carte inclinee, ce qui la
#    borne a une fois par round.
#  - « [star] Boost: Reveal this card » : la carte SORT du paquet de boost
#    pour entrer en jeu attachee. C'est ce qui la met en jeu sans qu'elle soit
#    revelee normalement — le meme montage que `ho017`.
#  - Aucune icone de boost chiffree (`desc.Boost = "0"`) : la carte n'ajoute
#    rien a la puissance de l'activation, elle se revele, point.


def GetAbilities() -> Sequence['Ability']:

    def donner_une_carte_de_boost(effect: 'Effect') -> None:
        vilains = Worlds.GetVillains(effect)
        if vilains:
            Faces.GiveFacedownBoostCards(list(vilains), 1, effect)

    def love_concoction(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        donner_une_carte_de_boost(effect)

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    def cout_boost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        donner_une_carte_de_boost(effect)
        return True

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.ForcedAction,
            love_concoction,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_boost)),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
