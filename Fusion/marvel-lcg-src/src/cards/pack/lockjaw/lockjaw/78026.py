from . import *

# * Ms. Marvel (Kamala Khan) — custom « Nugget » (carte d'aspect BASIC)
# [star] Interrupt: When Ms. Marvel thwarts, she gets +1 THW and takes +1
#   consequential damage for this thwart.
# [star] Interrupt: When Ms. Marvel attacks, she gets +1 ATK and takes +1
#   consequential damage for this attack.


def GetAbilities() -> Sequence['Ability']:

    return [
        # Les deux « Interrupt » etoiles se declenchent a chaque attaque et a
        # chaque contre : le resultat est exactement un bonus permanent de +1
        # avec +1 degat consecutif, seul montage expose par le moteur (meme
        # ecart assume que Fin Fang Foom 68016).
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1,
            attack=1,
            thwart=1,
            attack_consequential_damage=1,
            thwart_consequential_damage=1,
        ),
    ]
