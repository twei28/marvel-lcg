from . import *

# Crane Daughter — SBIRE nemesis d'Iron Fist (N 2/5 a 4/5, 3 exemplaires). MYSTIC. MAN 2, ATQ 2, PV 3.
#   2 icones de boost + [star].
# Vulnerable.
# When Defeated: Shuffle Crane Daughter into the encounter deck.
# [star] Boost: After this activation, tuck this card under Davos.
#
# MOTS-CLES : Vulnerable (fiche vulnerable.md : `desc.Vulnerable`, natif, aucun script), boost etoile (boost.md),
#   tuck (tuck.md).
#
# CARTES DE REFERENCE
#  - « When Defeated: shuffle » : `50098` Machete.
#  - « [star] Boost: After this activation » : `ares_nemesis/ar012` (`message.AfterThisActivation(effect, fn)`).
#
# TEXTE CONTRE CODE
#  ⚠ « AFTER this activation » : la carte compte d'abord comme boost (ses 2 icones), puis est glissee au lieu d'etre
#    defaussee.
#  ⚠ « under Davos » : Davos EN JEU. Absent, rien a faire : la carte est defaussee comme toute carte de boost.


def GetAbilities() -> Sequence['Ability']:

    def rejoindre_davos(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this

        def glisser() -> None:
            davos = DavosEnJeu(effect)
            if davos is not None and not this.IsInPlay():
                Glisser(davos, [this], effect)

        message.AfterThisActivation(effect, glisser)

    return [
        MelangerQuandVaincu(),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            rejoindre_davos,
        ),
    ]
