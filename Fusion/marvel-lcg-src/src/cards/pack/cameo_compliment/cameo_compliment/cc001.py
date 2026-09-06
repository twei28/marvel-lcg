from . import *

# Lock It Down — SOUTIEN d'aspect JUSTICE. Aucun cout, aucune icone de
#   ressource. Setup. Max 1 per deck.
# Setup: Search your collection for an identity-specific LOCATION support from
#   an identity not in this game. Shuffle that card into your deck. Discard 2
#   cards from your hand and remove this card from the game.
#
# CARTE DE REFERENCE
#  - `58031` Cameo (Meneur, officielle, pack wonder_man) : MOT POUR MOT le meme
#    texte a un mot pres (« for » au lieu de « from »), le meme montage, le
#    meme ordre. Seul le filtre change : un ALLIE la-bas, un soutien LOCATION
#    ici. Tout le montage vit dans `CapaciteCameo`, dans le `__init__.py` du
#    set, pour que les trois cartes ne divergent jamais entre elles.
#
# TEXTE CONTRE CODE
#  ⚠ « an identity-specific LOCATION SUPPORT » -> type `Support` ET trait
#    LOCATION ET `Class: "Hero"`. Le troisieme test est un ECART DELIBERE avec
#    `58031`, documente dans `EstSpecifiqueAUneIdentite` : sans lui, quatre
#    soutiens LOCATION seraient offerts a tort, dont `lj030` * Central Park,
#    qui est une carte BASIQUE que n'importe quel deck peut deja inclure.
#  ⚠ « from an identity NOT IN THIS GAME » -> on retire les sets des identites
#    presentes, TOUTES FACES CONFONDUES.
#  « Setup » -> base automatique, `desc.Setup = "1"` : le moteur met la carte
#    en jeu tout seul a la mise en place. La capacite, elle, est branchee sur
#    `AfterGameSetup`.
#  « Max 1 per deck » -> base automatique, `desc.MaxPerDeck = "1"`. AUCUN
#    SCRIPT.
#  ⚠ AUCUN COUT ET AUCUNE ICONE DE RESSOURCE sur le scan : les deux coins sont
#    vides, verifie par DECOUPE D'IMAGE (lecon Lockjaw). Le `desc` n'a donc ni
#    `Cost` ni `RES`, exactement comme `58031`.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        CapaciteCameo('Support', 'LOCATION'),
    ]
