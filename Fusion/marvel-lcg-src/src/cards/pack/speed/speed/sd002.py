from . import *

# * Quicksilver — ALLIE signature, custom « CptScorp »
# Cout 4, PV 3, ATQ 2*, CTR 2*, [wild], classe Hero, trait AVENGER.
# Interrupt: When Quicksilver attacks or thwarts an enemy or scheme with an
#   explosive counter on it, he suffers no consequential damage for that use.
#
# `ATK "2*"` / `THW "2*"` : l'etoile sur la stat d'un ALLIE est lue
# nativement par le moteur comme des DEGATS CONSECUTIFS
# (`can_attack.py:48-52` : `consequential_damage = value.count('*')`). Rien a
# coder pour ca — et c'est justement ce que la capacite imprimee annule.
#
# DECLENCHEUR -> modele EXACT : `* Cosmo` (`stld/17020.py`), le seul allie du
# depot qui annule ses degats consecutifs sous condition, meme couple
# `AbilityFactory.WhenUnitWouldAttackOrThwart(AbilityType.Interrupt, "This",
# ...)` (factory/do_attack.py:1225) + `message.DoesNotTakeConsequentialDamage(
# effect)` (sender_damage.py:178 pour l'attaque, sender_friend.py:61 pour le
# contre). Une seule fabrique couvre les deux verbes imprimes : elle ecoute
# `Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart`.
#
# LA CONDITION est portee par `UneCibleDeCeMessagePorteUnCompteur`
# (speed/speed/__init__.py), qui lit `attacked_targets` sur une attaque et
# `schemes` sur un contre. « an enemy OR scheme with an explosive counter on
# it » : il suffit qu'UNE des cibles porte un compteur.
#
# « for that use » -> rien a poser d'autre : le drapeau vit sur le message de
# CETTE attaque / de CE contre, il disparait avec lui.
#
# ⚠ AUCUNE recherche par nom dans ce fichier. Le catalogue contient DEJA le
# HEROS OFFICIEL `14001a` « * Quicksilver » et l'allie `15002` « * Quicksilver »
# (pack scw) : un `CardFinder(name="Quicksilver")` non borne les toucherait a
# une table partagee. La capacite ne vise que « This ».
# (La collision preexiste et n'est PAS corrigee cote `qsv` : ecart documente
# dans docs/speed_cartes.md.)


def GetAbilities() -> Sequence['Ability']:

    def cible_marquee(effect: 'Effect',
                      message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> bool:
        Unused(effect)
        return UneCibleDeCeMessagePorteUnCompteur(message)

    def quicksilver(effect: 'Effect',
                    message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.DoesNotTakeConsequentialDamage(effect)

    return [
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.Interrupt,
            "This",
            quicksilver,
            conditions=[cible_marquee],
        ),
    ]
