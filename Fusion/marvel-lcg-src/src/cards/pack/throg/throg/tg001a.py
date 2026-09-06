from . import *

# * Throg (face heros) — ASGARD. GUARDIAN. PV 12, CTR 1, ATQ 2, DEF 2, main 5.
# [star] Froglike Stamina — Response: After Throg uses a basic power, return
#   Frogjolnir to your hand -> ready Throg. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `14001a` * Quicksilver, « Super Speed — Response: After you use one of
#    Quicksilver's basic powers (THW, ATK, or DEF), ready him. (Limit once per
#    phase.) » : MOT POUR MOT le meme declencheur, le meme effet et la meme
#    limite. Seul le cout change.
#  - `tt001a` * Texas Twister : meme fabrique `AfterUnitUseBasicPower`, et
#    l'endroit ou le projet a note que le `[star]` d'une face heros est une
#    convention d'impression, pas un `AbilityType.NonKeywordStar`.
#  - `53002` / `04004` / `32011` : `CostFunc.ReturnToHand`, le renvoi en main
#    paye en COUT.
#
# TEXTE CONTRE CODE
#  « After Throg USES A BASIC POWER » -> les TROIS pouvoirs de base du heros
#    (`POUVOIRS_DE_BASE`). Pas la RECUPERATION : elle appartient a Puddlegulp,
#    qui est une AUTRE face et ne porte pas cette capacite.
#  « return Frogjolnir to your hand » est devant la FLECHE : c'est un COUT.
#    Sans marteau EN JEU, la Reponse ne se propose pas — le moteur ne montre
#    pas une capacite dont le cout est impayable. C'est ce qui borne la carte.
#  ⚠ « to YOUR hand » -> `to_who="Owner"`, pas `"Initiator"`. Sur une
#    amelioration posee sur sa propre identite les deux coincident, mais
#    « your » designe le proprietaire, et c'est lui qu'on ecrit.
#  « ready THROG » -> la face heros, celle qui vient d'agir. Le nom ne designe
#    QU'ELLE : l'alter-ego s'appelle Puddlegulp. `"YourHero"` (le litteral de
#    14001a) rend exactement ca.
#  « (Limit once per PHASE.) » -> `.LimitOncePerPhase()`, pas par round : deux
#    phases de joueur dans le meme round la rendent deux fois.


def GetAbilities() -> Sequence['Ability']:

    def endurance_de_grenouille(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            endurance_de_grenouille,
            powers=POUVOIRS_DE_BASE,
        ).SetCostFunc(CostFunc.ReturnToHand(
            name=NOM_MARTEAU,
            card_type=Upgrade,
            to_who="Owner",
        ))
        .SetTarget("YourHero")
        .LimitOncePerPhase()
        .SetName("Froglike Stamina"),
    ]
