from . import *

# Quick Adaptation — AMELIORATION signature, custom « CptScorp »
# Cout 2, [wild], classe Hero, trait SUPERPOWER.
# Hero Interrupt: When you basic attack or basic thwart against an enemy or
#   scheme with an explosive counter on it, you get +1 ATK and +1 THW for that
#   use.
#
# ⚠ NE PAS FUSIONNER AVEC sd014 Explosive Touch : l'une est une RESPONSE
# (apres) qui s'incline pour redresser Speed, l'autre — celle-ci — est un
# INTERRUPT (quand) qui ne s'incline pas et donne un bonus de stats. Voir le
# commentaire de sd014.
#
# ---------------------------------------------------------------------------
# DECLENCHEUR -> `AbilityFactory.WhenUnitWouldAttackOrThwart(AbilityType
# .HeroInterrupt, "YourIdentity", ..., is_basic_power=True)`
# (factory/do_attack.py:1225), la meme fabrique que sd002 Quicksilver : elle
# ecoute `Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart` et couvre
# donc les deux verbes imprimes en une seule capacite.
#
# ⚠ « YourIdentity » ET SURTOUT PAS « You ». `check_trigger` de cette fabrique
# appelle `Condition.CheckWhichCard(attacker, ...)` DIRECTEMENT, sans passer par
# `Condition.GetYouRule` — contrairement a `AfterUnitAttackUnitInternal`
# (do_attack.py:374), qui, lui, traduit « You ». La chaine « You » n'a donc
# aucune branche dans `CheckWhichCard` (card_type.py:127-190, qui connait
# « YouPlayer », « YourIdentity », « YourHero »... mais pas « You ») : la
# condition etait TOUJOURS FAUSSE et la carte n'a jamais rien fait. Constate
# le 30/08/2026 par le cas de test, qui lisait 1 degat au lieu de 2 ; corrige
# ici, pas dans le moteur (une carte n'a pas a deviner quelles fabriques
# traduisent « You »).
#
# `is_basic_power=True` rend le mot « BASIC » : un evenement d'attaque ne
# declenche rien, seuls les pouvoirs de base du heros comptent. C'est aussi ce
# que reclament `GainATKForThisAttack` (sender_damage.py:114) et
# `GainTHWForThisThwart` (sender_friend.py:69), qui commencent tous deux par un
# `assert self.IsBasicAttack()` / `IsBasicThwart()`.
#
# `AbilityType.HeroInterrupt` et non `Interrupt` nu : le texte dit « Hero
# Interrupt ».
#
# ---------------------------------------------------------------------------
# « YOU GET +1 ATK AND +1 THW FOR THAT USE » -> `this_unit.GainForThisActive(
# effect, message, attack=1, thwart=1)`.
#
# La formule imprimee donne LES DEUX stats, pas « la stat employee » : on la
# rend a la lettre. `GainForThisActive` est exactement le canal du « for that
# use » — c'est celui qu'emploient `GainATKForThisAttack` et
# `GainTHWForThisThwart` sous le capot, avec le message courant comme borne de
# duree. Le passer une seule fois avec les deux stats evite d'avoir a savoir
# lequel des deux messages on tient, et donne le meme resultat en jeu : sur une
# attaque de base seul l'ATQ est lu, sur un contre de base seul le CTR l'est.
#
# ⚠ Le bonus s'applique a `message.trigger`, l'unite qui va employer son
# pouvoir de base — l'identite du joueur, puisque la fabrique est bornee a
# « You ». Pas de recherche par nom : voir le piege « * Speed » decrit dans
# speed/speed/__init__.py.
#
# LA CONDITION « against an enemy or scheme WITH an explosive counter on it »
# est portee par `UneCibleDeCeMessagePorteUnCompteur`. Ici le compteur est lu
# AVANT le pouvoir de base (c'est un Interrupt) : un compteur pose par cette
# meme attaque n'y serait pas encore, ce qui est bien la lecture du texte.


def GetAbilities() -> Sequence['Ability']:

    def cible_marquee(effect: 'Effect',
                      message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> bool:
        Unused(effect)
        return UneCibleDeCeMessagePorteUnCompteur(message)

    def quick_adaptation(effect: 'Effect',
                         message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        unite = message.trigger.CastTo(Unit2)
        unite.GainForThisActive(effect, message, attack=1, thwart=1)

    return [
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.HeroInterrupt,
            "YourIdentity",
            quick_adaptation,
            is_basic_power=True,
            conditions=[cible_marquee],
        ),
    ]
