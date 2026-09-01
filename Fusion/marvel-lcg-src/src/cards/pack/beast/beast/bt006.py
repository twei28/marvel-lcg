from . import *

# In The Heat Of Battle — evenement signature. THWART. Cout 2. RES [mental]
# Action (thwart): Remove 4 threat from a scheme. If this event removed all
#   threat from a scheme -> shuffle 1 discovery card into your hand.
#
# Cartes de reference :
#  - 04049 Clear the Area : « Hero Action (thwart): Remove 2 threat from a
#    scheme. If this removes the last threat on that scheme, draw 1 card. »
#    Structure identique au mot pres — retrait de menace, puis test du
#    resultat sur la MEME manigance — et meme facon de le verifier, en relisant
#    `scheme.threat == 0` APRES le retrait (recette moteur §2 : « from THAT
#    scheme » = meme cible, pas un second choix).
#  - le tirage dans le pool mis de cote : bt001b Dr Hank McCoy, meme
#    `GetDiscoveryDeck` et meme `Faces.ShuffleAllTo`.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : le texte dit « **shuffle** 1
# discovery card into your **hand** » — on ne melange pas dans une main. Le
# VERBE l'emporte : la carte part dans le DECK, comme pour bt001b. Consigne au
# §6 du journal de portage, point 4, pour l'auteur.
#
# ⚠ « Action », pas « Hero Action » : le texte imprime ne dit pas « Hero ».
# L'evenement est donc jouable dans les DEUX formes, contrairement a 04049.
# Un heros a CTR 1 qui retire 4 menaces depuis sa forme alter-ego, c'est
# inhabituel mais c'est ce qui est imprime.
#
# ⚠ « removed ALL threat » se teste sur la manigance CIBLEE, pas sur une
# quelconque : `effect.targets` porte celle que le joueur a choisie.
# Une manigance deja a 0 avant l'evenement ne compte pas : elle n'aurait pas
# ete une cible legale.

def GetAbilities() -> Sequence['Ability']:

    def in_the_heat_of_battle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

        videe = False
        for target in effect.targets:
            scheme = target.CastTo(Scheme2)
            if scheme.threat == 0:
                videe = True

        if not videe:
            return

        faces = GetDiscoveryDeck(effect)
        if not faces:
            return
        face = Rand.RandomChoice(faces, effect)
        Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            in_the_heat_of_battle
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
