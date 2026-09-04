from . import *

# * Texas Twister (face heros) — AERIAL. RANGER. PV 10, ATQ 1, CTR 1, DEF 1,
#   main 5.
# Vortex Control — [star] Response: After you use one of Texas Twister's basic
#   powers (THW, ATK, or DEF), he gets +1 to that power until the end of the
#   round.
#
# CARTES DE REFERENCE
#  - `14001a` Quicksilver et `28001a` Nova : `AfterUnitUseBasicPower` avec
#    `powers=["ATK", "THW", "DEF"]`, c'est LA fabrique de ce declencheur.
#  - `12016` Moxie : `GainUntilRoundEnd(...)`, l'idiome du bonus de round.
#
# TEXTE CONTRE CODE
#  « +1 to THAT power » -> le pouvoir est lu sur `message.power`, JAMAIS
#    devine. Donner +1 partout ferait de cette carte un triple de tt003
#    Accelerated Rotation, qui elle donne bien les trois. Mot-piege « that ».
#  « until the end of the ROUND » -> `GainUntilRoundEnd`, pas `for this use` :
#    le bonus vaut aussi pour les usages SUIVANTS du meme round, et c'est tout
#    le moteur du pack (chaque usage rend le suivant meilleur).
#  ⚠ AUCUNE LIMITE IMPRIMEE. Contrairement a Quicksilver (« Limit once per
#    phase »), Texas Twister empile : trois attaques dans le round donnent +3
#    ATQ. Ne PAS ajouter de `LimitOncePerRound()` par reflexe — ici l'absence
#    de limite EST la carte. Verifie sur le scan.
#  « [star] » devant Response -> simple renvoi aux etoiles des trois
#    statistiques imprimees, pas une limite.


def GetAbilities() -> Sequence['Ability']:

    def controle_du_vortex(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        BonusAuPouvoir(this, message.power, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            controle_du_vortex,
            powers=POUVOIRS_DE_BASE,
        ).SetName("Vortex Control"),
    ]
