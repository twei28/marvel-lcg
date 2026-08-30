from . import *

# Swift Strikes (exemplaire 1/3) — EVENEMENT signature, custom « CptScorp »
# Cout 2, [physical], classe Hero, traits ATTACK / SUPERPOWER.
# Hero Action (attack): Deal 3 damage to an enemy. Make a basic thwart against
#   a scheme with an explosive counter on it without exhausting.
#
# Exemplaire physique 1 de 3 (sd008, sd009, sd010). Commentaire complet ici,
# pointeur bref sur sd009 et sd010.
#
# ⚠ MIROIR DE BLASTING VELOCITY (sd003/sd004), PAS SA JUMELLE. Ici : DEGATS
# d'abord (3 a un ennemi, cible libre), CONTRE de base ensuite, sur une
# MANIGANCE marquee. La-bas : menace d'abord, ATTAQUE de base ensuite, sur un
# ENNEMI marque. Trois exemplaires ici, deux la-bas. Ressource imprimee
# PHYSIQUE ici, ENERGIE la-bas — ce qui change tout pour Hyperkinetic Fuel :
# Swift Strikes ne pose un compteur que si on la paie AVEC AUTRE CHOSE que sa
# propre icone.
#
# ---------------------------------------------------------------------------
# « Deal 3 damage to AN ENEMY » -> `.SetTarget(Enemy)` + `.SetLabel('attack')`
# + `this.DealDamage(effect.targets, 3, effect)`. Forme standard d'un
# evenement d'attaque du depot (modele 01087 Haymaker, meme structure exacte).
#
# ---------------------------------------------------------------------------
# « Make a basic thwart against a scheme with an explosive counter on it
# without exhausting » :
#
# - `heros.BasicThwart(cibles, effect)` (can_thwart.py:188), le pendant exact
#   de `BasicAttack`. « Without exhausting » : la methode n'incline rien, et
#   `IsCanThwart` (can_thwart.py:201) ne teste pas l'inclinaison — le contre
#   part meme si Speed est deja incline.
#
# - Ciblage restreint par `has_counter=COMPTEUR_EXPLOSIF`
#   (card_finder/checker.py:346). `Scheme2` et non `MainScheme` : « a scheme »,
#   n'importe laquelle.
#
# - Aucune manigance marquee -> rien, sans erreur (garde explicite avant le
#   `ChooseAbilities`, qui poserait sinon une question sans cible legale).
#
# - `ChooseAbilities` imbrique plutot que `.SetTarget2` : lecon hd009, le
#   pilote de `tools/test_capacites.py` n'alimente pas `effect.targets2`.
#
# - Le contre part du HEROS (`joueur.GetHero()`), pas de l'evenement : c'est un
#   CONTRE DE BASE, il doit employer le CTR de Speed.


def GetAbilities() -> Sequence['Ability']:

    def swift_strikes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return

        cibles = [face for face in FacesAvecUnCompteurExplosif(effect)
                  if Scheme2.IsType(face)]
        if not cibles:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Make a basic thwart against a scheme with an explosive counter on it, without exhausting",
                lambda targets:
                    heros.BasicThwart(list(targets), effect),
            ).SetTarget(Scheme2, has_counter=COMPTEUR_EXPLOSIF, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swift_strikes,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
