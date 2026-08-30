from . import *

# Bulletproof Chica — EVENEMENT signature, custom « jakxin »
# Cout 1, [mental], traits DEFENSE + SUPERPOWER. Deux exemplaires physiques :
# ma011 et ma012, meme texte, meme code.
#
# Hero Interrupt (defense): When you would take any amount of damage, prevent
#   all of that damage. Give your identity a tough status card.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# `rg004` Shield Block (pack red_guardian) et son original officiel `03005`
# (Captain America) : meme phrase imprimee « When you would take ANY AMOUNT
# OF DAMAGE, prevent all of that damage », meme montage
# `WhenUnitWouldTakeDamage(<type>, "You", fn).SetPlay().SetLabel('defense')`
# + `message.PreventDamage("All", effect)` (sender_damage.py:808-820).
#
# ⚠ MOT-PIEGE « ANY AMOUNT OF DAMAGE » : AUCUN `is_from_attack=`. Le texte ne
# restreint PAS aux degats d'une attaque, contrairement a Backflip (`01003`)
# et a `dz010` L'Ange, qui disent « when you would take damage FROM AN
# ATTACK » et portent `is_from_attack=True`. Ici une traitrise, un degat
# consecutif ou un degat direct sont prevenus tout autant. C'est la lecture
# litterale, et le commentaire de `rg004` la formule deja mot pour mot.
#
# `is_from_attack=None` (defaut) = aucun filtre (damage.py:26-31).
#
# ---------------------------------------------------------------------------
# « GIVE YOUR IDENTITY A TOUGH STATUS CARD »
#
# Seconde CONSEQUENCE, pas un cout : les deux phrases sont separees par un
# point, il n'y a AUCUNE fleche. Les deux se resolvent toujours ensemble.
#
# `Faces.GiveStatus([identite], "Tough", effect)` (faces.py:168) —
# ⚠ majuscule : `"Tough"`, pas `'tough'` (`CardFace.STATUS`,
# card_face.py:221). Modeles : `hd011` et `38008`.
#
# « YOUR identity » -> `player.GetIdentity()`, pas `"YourHero"` : le mot
# imprime est « identity ». En pratique la carte est une Hero Interrupt, donc
# l'identite est en forme heros — mais on ecrit ce qui est imprime.
#
# ---------------------------------------------------------------------------
# LE LIBELLE `(defense)`
#
# `.SetLabel('defense')` est ici LEGAL : `Ability.Initialize`
# (ability.py:196) autorise 'defense' et 'thwart' sur une interruption. C'est
# `attack` qui fait planter le montage de partie (piege paye sur `pt015`).
# Le libelle classe la carte comme une reponse de defense et permet au
# harnais de l'atteindre via `Puzzle.Attack(<ennemi>, defender=<heros>)`.
#
# `.SetPlay()` AVANT `.SetLabel()` : `SetCondition` contient
# `assert self.selectors == []` (ability.py:486), l'ordre compte.


def GetAbilities() -> Sequence['Ability']:

    def bulletproof_chica(effect: 'Effect',
                          message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

        player = effect.GetInitiator()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            bulletproof_chica,
        ).SetPlay().SetLabel('defense'),
    ]
