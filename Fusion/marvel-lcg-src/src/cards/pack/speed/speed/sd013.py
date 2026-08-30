from . import *

# Mother's Protection — SOUTIEN signature, custom « CptScorp »
# Cout 1, [mental], classe Hero, trait FAMILY.
# Interrupt: When your identity would take any amount of damage, shuffle
#   Mother's Protection back into your deck -> prevent 3 of that damage.
#
# ⚠ C'EST EXACTEMENT LA CARTE `wc015` DU PACK WICCAN : meme nom, meme cout,
# meme ressource imprimee, meme type, meme trait, meme texte au caractere
# pres. L'auteur (CptScorp) a reutilise la carte de Billy pour son frere
# jumeau — les deux illustrations montrent d'ailleurs la meme scene de
# famille.
#
# CE MODULE EST UN DUPLICAT VOLONTAIRE de `wiccan/wiccan/wc015.py`, et NON un
# `full_link` dans cards.json : une reimpression `full_link` heriterait du
# `set_name` « Wiccan » de la carte source, ce qui ferait de sd013 une carte
# SIGNATURE DE WICCAN (visible dans son deck, comptee dans son pack, et
# refusee par le controle « jamais une carte signature d'un autre heros dans
# un deck » du §5.2 du guide). Les deux fichiers doivent donc rester
# synchronises a la main : toute correction sur l'un se reporte sur l'autre.
#
# ---------------------------------------------------------------------------
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
# aussi en forme civile, d'ou la cible `"YourIdentity"`. « any amount of
# damage » : aucun filtre `is_from_attack`, donc les degats de trahison et les
# degats indirects sont couverts aussi.
#
# Prevention -> `message.PreventDamage(3, effect)`. Modele du couple « payer un
# cout -> prevenir » : Mockingbird (`bkw/04004.py`). Mockingbird previent
# « All », Mother's Protection previent EXACTEMENT 3 : valeur imprimee.
#
# Cout « shuffle Mother's Protection back into your deck » -> aucune `CostFunc`
# du moteur ne fait ce trajet (game/ability/cost_func.py : ReturnToHand,
# Discard, RemoveFromGame, Exhaust... mais pas de « ShuffleIntoDeck »). On
# passe donc par `CostFunc.Custom(None, ...)`, le point d'extension prevu pour
# ca, qui appelle `Faces.ShuffleAllTo([this], joueur.player_deck, effect)`.
# `CostFunc.Custom(None, ...)` cible « This » par defaut. Le cout est REEL,
# pas cosmetique : il est paye par le moteur AVANT le handler
# (`Effect.ProcessSelfCost`), donc la carte a bien quitte le jeu quand la
# prevention s'applique.


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
