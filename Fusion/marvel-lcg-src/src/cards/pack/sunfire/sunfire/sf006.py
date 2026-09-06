from . import *

# * Atomic Samurai — AMELIORATION, cout 2, [mental]. FIRE. TITLE. UNIQUE.
# Interrupt: When an enemy would take damage from the triggered ability of
#   Burning, they take 1 additional damage.
#
# CARTES DE REFERENCE
#  - `dt094` Diversion Skill : `WhenUnitWouldTakeDamage` +
#    `message.IncreaseDamage(n, effect)`, la fenetre et la primitive qui
#    alourdissent des degats deja en route. ⚠ `UpdateDamage` existe aussi
#    mais sur un AUTRE message (sender_damage.py:932), et ne compte que les
#    degats EXCEDENTAIRES : l'employer ici n'aurait rien fait.
#  - `sf009` Burning : la carte dont on lit la capacite declenchee.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « from the TRIGGERED ABILITY of Burning » — PAS « from Burning ». La
#    distinction est imprimee et elle est reelle : Burning inflige 1 degat par
#    sa Reponse forcee de fin de phase, et c'est le SEUL moment ou elle en
#    inflige. Le filtre porte donc sur la SOURCE des degats
#    (`message.by_effect.this`), qui vaut la brulure elle-meme.
#  ⚠ « an ENEMY » -> le sujet est l'ennemi brule, pas le heros. Un degat que
#    Sunfire subirait ne serait jamais concerne, mais la condition est ecrite.
#  ⚠ « they take 1 ADDITIONAL damage » -> on AJOUTE, on ne remplace pas : de 1
#    a 2 par brulure et par phase. Avec six brulures en jeu, l'ecart est de
#    six degats par tour.
#  « INTERRUPT » -> avant que les degats ne tombent, seule fenetre ou l'on
#    peut encore changer le nombre.
#  ⚠ UNIQUE (etoile devant le nom, verifiee par decoupe d'image), et une seule
#    copie dans les 15 : `desc` n'a donc pas besoin de `MaxPerDeck`, c'est
#    l'unicite native qui borne le terrain.


def GetAbilities() -> Sequence['Ability']:

    def degats_dune_brulure(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(effect)
        source = getattr(getattr(message, "by_effect", None), "this", None)
        return (source is not None and source.IsName(NOM_BRULURE)
                and message.trigger is not None and Enemy.IsType(message.trigger))

    def samourai_atomique(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.IncreaseDamage(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            None,
            samourai_atomique,
            conditions=[degats_dune_brulure],
        ),
    ]
