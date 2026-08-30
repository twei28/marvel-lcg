from . import *

# Teleport (1/2) — custom « CptScorp »
# Cout 1, [energy], classe Hero, traits SPELL / SUPERPOWER.
# Action: Choose a player -> ready that player's identity. That player may
#   change their form. If the top card of the encounter deck has 2 or more
#   boost icons, that player gets +1 to a basic power of their choice until
#   the end of the round.
#
# Exemplaire physique 1 de 2 (wc011, wc012). Commentaire complet ici,
# pointeur bref sur wc012.
#
# « Action: » nu sur une carte JOUEUR (ni « Hero Action » ni « Alter-Ego
# Action ») -> `AbilityType.Action`, jouable dans les deux formes. Modele :
# Helicarrier (`core/01092.py`), meme type et meme `.SetTarget("Players")`
# pour le « choose a player ». Comme Helicarrier, on remonte au joueur par
# `target.GetControlByPlayer()`.
#
# « ready that player's identity » -> `Faces.ReadyAll([identite], effect)`
# (modele il015 / ok014 / hd001a).
#
# « That player may change their form » -> `YouMayChangeForm(joueur, effect)`,
# l'aide partagee de `cards/pack/__init__.py`, qui pose un
# `MayChooseOneText` sur les autres faces d'identite et appelle
# `ChangeToFace`. C'est bien un « may » (optionnel), et il concerne LE JOUEUR
# CHOISI, pas celui qui joue la carte — piege `that <nom>` de PROCESSUS-CARTE.
# Le pilote de test decline les choix optionnels : le cas dedie emploie
# `accepter_choix: True`.
#
# « +1 to a basic power of their choice until the end of the round » -> quatre
# branches `ChooseAbilities` (ATQ, CTR, DEF, REC), les quatre pouvoirs de base
# d'une identite.
# CHOIX TECHNIQUE ASSUME : `identite.TemporaryGain(effect, None,
# Message.WhenRoundEnd, <pouvoir>=1, ignore_flip=True, render_ui=True)` plutot
# que `GainUntilRoundEnd`. Les deux font strictement la meme chose — c'est le
# corps litteral de `GainUntilRoundEnd` (game/card/face/model/face_action.py:
# 410-437) — mais la version courte n'expose PAS `recover`, alors que
# `TemporaryGain` l'accepte (ligne 49). Passer par la version longue est le
# seul moyen d'offrir les QUATRE pouvoirs de base. Patriot (29016), qui n'en
# donne que trois, s'en tient a `GainUntilRoundEnd` : il vise un personnage
# quelconque, allie compris, qui n'a pas de REC.
#
# `ignore_flip=True` : le bonus survit au changement de forme, ce qui compte
# ici puisque la carte propose justement de changer de forme juste avant.
# L'identite est donc RELUE apres le changement de forme.

def GetAbilities() -> Sequence['Ability']:

    def teleport(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        icones = IconesBoostDuDessus(effect, effect.GetInitiator())

        for target in effect.targets:
            joueur = target.GetControlByPlayer()
            if joueur is None:
                continue

            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

            YouMayChangeForm(joueur, effect)

            if icones < 2:
                continue

            identite = joueur.GetIdentity()
            if identite is None:
                continue

            def bonus(pouvoir: str, face: 'CardFace'):
                def appliquer(targets: Sequence['CardFace']) -> None:
                    Unused(targets)
                    face.TemporaryGain(
                        effect,
                        None,
                        Message.WhenRoundEnd,
                        ignore_flip=True,
                        render_ui=True,
                        **{pouvoir: 1},
                    )
                return appliquer

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "+1 ATK until the end of the round",
                    bonus("attack", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 THW until the end of the round",
                    bonus("thwart", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 DEF until the end of the round",
                    bonus("defense", identite),
                ),
                AbilityFactory.ForChoiceAbility(
                    "+1 REC until the end of the round",
                    bonus("recover", identite),
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            teleport,
        ).SetPlay()
        .SetTarget("Players"),
    ]
