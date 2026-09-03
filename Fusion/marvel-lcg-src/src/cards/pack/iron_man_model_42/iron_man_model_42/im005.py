from . import *

# * Stark Tower — soutien signature, x1 (n/15 = 8).
# LOCATION. Cout 3, ressource [wild] (etoile verte, verifiee sur le scan
# contre l'eclair jaune de im004 et la molecule bleue de im003).
# Resource: Exhaust Stark Tower -> generate a [wild] resource for any player.
#
# Cartes de reference : `an007` Asgard's Assassin et `ma005` * Star Light —
# `CanGenerateResources(AbilityType.Resource, Resources("G"))` +
# `CostFunc.Exhaust("This")`.
#
# ⚠ PAS DE `CanPlayThisSupportCard()`. Releve du 03/09/2026 sur tout le
# depot : **212 soutiens sur 257 ne l'appellent pas**, et la mesure faite le
# meme jour sur ls002 a montre qu'un ALLIE entre en jeu sans l'equivalent —
# la fabrique ne sert qu'aux cartes jouees hors de leur tour ou sous
# condition. Le cas de test de cette carte le verifiera.

# ⚠ « Resource » NU, pas « Hero Resource » ni « Alter-Ego Resource » : la
# ressource se genere dans LES DEUX formes. C'est ce qui distingue cette carte
# de hk012 Limitless Strength, qui imprime « Hero Resource ».
#
# ⚠ ECART ASSUME — « for ANY PLAYER ». Le moteur n'expose aucun parametre pour
# offrir une ressource generee a un AUTRE joueur : la signature de
# `CanGenerateResources` (resources.py:277) propose `for_card`, `for_ability`,
# `from_hand`, `for_player_whose_identity_has_trait`, mais rien qui designe un
# joueur destinataire. La ressource va donc au joueur qui paie. En SOLO les
# deux lectures sont identiques ; a plusieurs, la carte perd son cote
# « Commandement ». Signale plutot que masque.
#
# ⚠ CONSEQUENCE DE L'ARBITRAGE SUR im001a : cette carte GENERE un wild, elle
# ne porte donc PAS d'icone energie imprimee au sens de « Reactor Cores ».
# **Stark Tower ne peut pas charger le reacteur.** C'est voulu : sans cette
# lecture, un seul Stark Tower le rechargerait indefiniment.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
