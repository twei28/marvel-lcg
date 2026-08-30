from . import *

# Mother's Protection — SOUTIEN signature, custom « CptScorp »
# Cout 1, [mental], classe Hero, trait FAMILY.
# Interrupt: When your identity would take any amount of damage, shuffle
#   Mother's Protection back into your deck -> prevent 3 of that damage.
#
# `AbilityFactory.CanPlayThisSupportCard()` est declaree explicitement : le
# moteur exige EXACTEMENT une capacite « Play » sur une carte joueur
# (game/card/factory.py:88-121). `Support.GetAbilities` en ajoute une d'office
# quand la carte n'en declare aucune (support.py:17-23), la declarer ici ne
# change donc rien au comportement — c'est le meme objet, pose a la main pour
# que le fichier dise tout ce que la carte fait.
#
# Declencheur -> `AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.Interrupt,
# "YourIdentity", ...)`, la fabrique standard des preventions de degats
# (guide §3.1). « your identity » et non « your hero » : la protection joue
# aussi en forme civile, d'ou la cible `"YourIdentity"` et non `"YourHero"`.
# « any amount of damage » : aucun filtre `is_from_attack`, donc les degats
# de trahison et les degats indirects sont couverts aussi.
#
# Prevention -> `message.PreventDamage(3, effect)`. Modele du couple
# « payer un cout -> prevenir » : Mockingbird (`bkw/04004.py`), meme forme
# `.SetCostFunc(...)` + `PreventDamage` dans le handler. Mockingbird previent
# « all », Mother's Protection previent EXACTEMENT 3 : valeur imprimee, pas
# "All".
#
# Cout « shuffle Mother's Protection back into your deck » -> aucune
# `CostFunc` du moteur ne fait ce trajet (la liste complete est
# game/ability/cost_func.py:106-1156 : ReturnToHand, Discard, RemoveFromGame,
# Exhaust... mais pas de « ShuffleIntoDeck »). On passe donc par
# `CostFunc.Custom(None, ...)`, le point d'extension prevu pour ca (8 cartes
# du depot l'emploient deja, ex. dt098, 16172, 29038), qui appelle
# `Faces.ShuffleAllTo([this], joueur.player_deck, effect)` (faces.py:48).
# `CostFunc.Custom(None, ...)` cible « This » par defaut : le cout ne peut
# porter que sur la carte elle-meme, exactement ce que le texte dit.
# Le cout est REEL, pas cosmetique : il est paye par le moteur AVANT le
# handler (`Effect.ProcessSelfCost`), donc la carte a bien quitte le jeu quand
# la prevention s'applique.

def GetAbilities() -> Sequence['Ability']:

    def remelanger_dans_le_deck(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        this = effect.this
        joueur = this.GetOwnerPlayer()
        if joueur is None:
            return False
        Faces.ShuffleAllTo([this], joueur.player_deck, effect)
        return True

    def mothers_protection(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        message.PreventDamage(3, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "YourIdentity",
            mothers_protection,
        ).SetCostFunc(CostFunc.Custom(None, remelanger_dans_le_deck)),
    ]
