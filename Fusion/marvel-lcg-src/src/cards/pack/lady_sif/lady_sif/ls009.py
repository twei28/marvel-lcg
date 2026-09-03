from . import *

# * Sif's Crest — amelioration signature, x1 (n/15 = 13).
# ARMOR. ASGARD. Cout 3, ressource [mental].
# You get +2 hit points.
# Hero Interrupt: When Lady Sif uses a basic power, draw 1 card.
#   (Limit once per phase.)
#
# Cartes de reference :
#  - `05023` Endurance / `hk011` pour les PV :
#    `GiveKeywordToAttached("You", health=2)` ;
#  - `04032` * Captain Marvel pour la famille « pouvoir de base », ici dans sa
#    version INTERRUPTION (`WhenUnitUseBasicPower`, friend.py:339) et non
#    RESPONSE (`AfterUnitUseBasicPower`, friend.py:373) ;
#  - `aa001a` pour `.LimitOncePerPhase()`.
#
# ⚠ L'ECART AVEC ls001a, ET IL EST IMPRIME. Valiant Warrior dit
# « **Response**: **After** Lady Sif uses a basic power » et n'a AUCUNE
# limite. Sif's Crest dit « **Interrupt**: **When** Lady Sif uses a basic
# power » et plafonne a une fois par phase. Deux cartes du meme pack, presque
# la meme phrase, deux fenetres et deux limites differentes :
#  - l'Interruption resout AVANT le pouvoir (la carte piochee peut donc etre
#    depensee pour l'attaque qui suit) ;
#  - la Response resout APRES.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOU get +2 hit points » : « you » = l'identite, donc les DEUX faces.
#    13 PV -> 15 en heros comme en civil (piege §3 de RECETTES-MOTEUR).
#  - « a basic power » : les trois, `powers=None`.
#  - « Hero Interrupt » : rien en forme civile, alors meme que les +2 PV, eux,
#    valent dans les deux formes.
#  - Aucun cout : la carte ne s'incline pas. C'est la limite par phase qui
#    borne, pas un epuisement.


def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            piocher,
        ).LimitOncePerPhase(),
    ]
