from . import *

# * Aka — SBIRE, HAND. NINJA. PV 4, ATQ 2, MAN 2. Quickstrike (desc). Sbire nemesis d'Elektra (1/5).
# When Defeated : se melange dans le paquet de rencontre. [star] Boost : Aka est distribue face cachee au joueur Elektra Natchios.
#
# CARTES DE REFERENCE
#  - When Defeated -> paquet de rencontre : `50098` Machete.
#  - Boost « deal THIS card to the X player as a facedown encounter card » : `62029` Cottonmouth.
#
# TEXTE CONTRE CODE
#  ⚠ C'est CETTE carte qui est distribuee (pas une copie cherchee par nom). Sans joueur Elektra Natchios a la table, elle va au
#    joueur vise par l'activation en cours (meme repli que 62029).
#  ⚠ Aucune icone de boost imprimee : l'etoile seule.
#  ⚠ Aka EN JEU ne doit PAS se distribuer quand une AUTRE carte de boost est retournee (il attaque en Quickstrike, Elektra defend
#    avec sa carte de boost) : c'est la fabrique `WhenBoostCardTurnedFaceUp` qui le garantit depuis le correctif du 14/11/2026
#    (boost.py, `check_cette_carte_est_le_boost`). Cas dedie : « 63029 Aka EN JEU : une autre carte de boost est retournee ».


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Minion)
        cible = JoueurElektra(effect) or message.GetToPlayer()
        if cible:
            cible.DealEncounterCard(this, effect)

    return [
        MelangerQuandVaincu(),
        AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost),
    ]
