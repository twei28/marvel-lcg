from . import *

# Phase Up — evenement signature, x2 (n/15 = 4 et 5). DEFENSE. SUPERPOWER.
# Cout 1, ressource [energy], Requirement ([energy]).
# Interrupt (defense): When you would take any amount of damage, prevent all
#   of that damage. You gain stalwart until the end of the round.
#
# Cartes de reference :
#  - 03005 Shield Block (Captain America), src/cards/pack/cap/captain_america/
#    03005.py : meme montage exact
#    `WhenUnitWouldTakeDamage(Interrupt, "You", ...).SetPlay()
#    .SetLabel('defense')` + `message.PreventDamage("All", effect)`. C'est le
#    bon modele et NON 01003 Backflip, qui ajoute `is_from_attack=True` ;
#  - dd001a (pack doctor_doom) pour un mot-cle accorde « until the end of the
#    round » par `GainUntilRoundEnd`, la ou toutes les autres cartes du depot
#    accordent stalwart en permanence par attachement.
#
# ⚠ CORRECTIF MOTEUR REQUIS PAR CETTE CARTE (02/09/2026) : `TemporaryGain` et
# `GainUntilRoundEnd` (game/card/face/model/face_action.py) ne passaient pas
# `stalwart` a `Gain`, qui l'accepte pourtant depuis toujours
# (face_gain.py:23, applique en face_gain.py:141). Troisieme occurrence du
# meme oubli, apres `retaliate` (4/8/2026) et `villainous` (1/9/2026).
# vv004 est le PREMIER stalwart TEMPORAIRE du depot : les ~30 autres cartes
# qui l'accordent le font par attachement permanent, d'ou l'angle mort.
#
# ⚠ AUCUN script pour le `Requirement` : `desc.Requirement` = "Y", base
# automatique (voir mots-cles/requirement.md).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « ANY AMOUNT of damage » et non « damage from an attack » : pas de
#    `is_from_attack=True`. La carte pare aussi les degats d'une traitrise ou
#    d'un effet, pas seulement une attaque. C'est tout l'ecart avec Backflip.
#  - « PREVENT ALL of that damage » : `PreventDamage("All", effect)`, pas une
#    valeur chiffree.
#  - « YOU gain stalwart » : l'IDENTITE, donc les deux faces. On l'accorde a
#    `message.trigger`, l'unite qui allait subir les degats — que le filtre
#    « You » de la fabrique garantit etre l'identite du joueur. Avec
#    `ignore_flip=True` (defaut), le mot-cle survit a un changement de forme.
#  - « until the end of the ROUND » : `GainUntilRoundEnd`, pas la phase.
#  - Ordre imprime : la prevention D'ABORD, le stalwart ENSUITE. Sans
#    consequence mecanique ici, mais respecte.
#  - `stalwart` fait defausser les cartes de statut Sonne et Desoriente deja
#    posees (`GainStalwart`, has_stalwart.py) : c'est le comportement natif du
#    mot-cle, pas un effet supplementaire de la carte.


def GetAbilities() -> Sequence['Ability']:

    def phase_up(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

        identite = message.trigger
        if identite is not None:
            identite.GainUntilRoundEnd(effect, stalwart=1)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            phase_up,
        ).SetPlay().SetLabel('defense'),
    ]
