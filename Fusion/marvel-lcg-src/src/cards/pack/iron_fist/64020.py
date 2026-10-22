from . import *

# 22/10/2026 : carte OFFICIELLE du pack Iron Fist (MC64, n° de collection 20), ex-`up039` (aspects TMNT d'Inkwire, meme texte). `up039` n'existe plus : c'est maintenant
# l'art alternatif « tmnt » de `64020` (data/arts_alternatifs.json). Script, cas et gabarit PROCESSUS-CARTE repris tels quels.
# Tonfa — AMELIORATION 1 [physical], aspect Protection (TMNT Aspects, Inkwire). ITEM. WEAPON.
# Restricted.
# Hero Interrupt: When calculating damage during an attack against you, exhaust this card -> give your hero
#   either +1 DEF or retaliate 1 for this attack.
#
# NOUVELLE. MOTS-CLES (fiches lues AVANT le code) : Restricted (restricted.md, `desc`, aucun code),
# Retaliate (retaliate.md : « retaliate 1 for this attack » = mot-cle temporaire, resolu apres l'attaque).
#
# EXTENSION MOTEUR (16/10/2026) : le moteur n'avait AUCUNE fenetre de joueur au moment du calcul des degats
# (`WhenRecalculateAttackDamage` est un message de calcul : constantes et interruptions forcees seulement).
# Ajout de `Message.WhenCalculatingAttackDamage` (sender_damage.py), envoye par `can_attack.py` apres le
# calcul de la valeur d'attaque (boosts compris) et avant le retrait de la DEF du defenseur ;
# `GainDefenseForThisAttack(1)` ajoute a cette DEF.
#
# CARTES DE REFERENCE
#  - `42004` Aerial Agility (Archangel) : « gain retaliate 1 for this attack » =
#    `hero.TemporaryGain(effect, would_atk_message, retaliate=+1)`.
#  - `38014` Judoka Skill : un bonus « for this attack » porte par le message d'attaque.
#  - `tl005` / `tl006` : un choix « either ... or » = `ChooseAbilities(ForChoiceAbility, ForChoiceAbility)`.
#
# TEXTE CONTRE CODE
#  ⚠ « an attack AGAINST YOU » : la cible des degats est votre identite (defendue par elle ou non
#    defendue) ; si un allie defend, il recoit l'attaque : la fenetre ne vous concerne plus.
#  ⚠ « exhaust this card -> » : cout ; « either +1 DEF OR retaliate 1 » : UN des deux, au choix.
#  ⚠ « +1 DEF » : ne change les degats que si votre heros DEFEND (la DEF ne compte qu'en defense) ;
#    affiche aussi sur le heros (`TemporaryGain`).
#  ⚠ « Hero Interrupt » : forme heros (la cible doit etre votre HEROS).


def GetAbilities() -> Sequence['Ability']:

    def contre_vous(effect: 'Effect', message: 'Message.WhenCalculatingAttackDamage') -> bool:
        joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return False
        heros = joueur.GetIdentity()
        return Hero.IsType(heros) and message.target is heros

    def tonfa(effect: 'Effect', message: 'Message.WhenCalculatingAttackDamage') -> None:
        joueur = effect.GetInitiator()
        heros = joueur.GetIdentity()
        atk = message.would_atk_message

        def plus_def(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            heros.TemporaryGain(effect, atk, defense=+1)
            message.GainDefenseForThisAttack(1, effect)

        def riposte(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            heros.TemporaryGain(effect, atk, retaliate=+1)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Your hero gets +1 DEF for this attack", plus_def),
            AbilityFactory.ForChoiceAbility("Your hero gains retaliate 1 for this attack", riposte),
        )

    return [
        Ability(
            AbilityType.HeroInterrupt,
            Message.WhenCalculatingAttackDamage,
            [contre_vous],
            tonfa,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
