from . import *

# Break Through — EVENEMENT signature, custom « jakxin »
# Cout 2, [energy], traits ATTACK + SUPERPOWER + THWART. Deux exemplaires
# physiques : ma015 et ma016, meme texte, meme code.
#
# Hero Action (attack/thwart): Deal 4 damage to an enemy. Remove 3 threat
#   from a scheme. If this defeats an enemy or scheme, stun or confuse an
#   enemy.
#
# ---------------------------------------------------------------------------
# LE DOUBLE LIBELLE
#
# La carte imprime « (attack/thwart) » et porte les DEUX traits ATTACK et
# THWART. `Ability.SetLabel` est variadique (ability.py:375-382) : on ecrit
# `.SetLabel('attack', 'thwart')`. Modeles : `dt028` Pay It Forward, `dt095`,
# `dt115`, `60050` In Harm's Way, `60055`. Ce n'est pas cosmetique : le
# libelle est ce qui range la carte parmi les reponses d'attaque ET de
# contre, et c'est par lui que le harnais l'atteint.
#
# ⚠ `.SetPlay()` AVANT `.SetLabel()`, et les deux avant tout `.SetTarget` :
# `SetLabel` porte `assert self.selectors == []` (ability.py:379).
#
# ---------------------------------------------------------------------------
# TROIS EFFETS, LE TROISIEME CONDITIONNEL
#
# Les deux premieres phrases sont deux CONSEQUENCES separees par un point :
# aucune fleche, les deux se resolvent toujours, meme si l'une ne trouve pas
# de cible.
#
# « If this DEFEATS an enemy OR SCHEME » : deux declencheurs distincts, et le
# moteur a une brique pour chacun —
#   `DealDamage(..., if_this_attack_defeats=fn)` (card_face.py:558-563),
#     modeles `ag006`, `ab004`, `50037` ;
#   `RemoveThreatFromSchemes(..., if_this_remove_last_threat=fn)`
#     (card_face.py:692), modeles `56009` Feline Senses, `37009`, `56039`.
# Mot-piege `defeated` vs `damaged` (PROCESSUS-CARTE §5) : c'est bien la
# DEFAITE, pas le fait d'infliger des degats.
#
# Un DRAPEAU local garantit que le bonus ne part QU'UNE FOIS meme si les deux
# defaites arrivent : le texte dit « stun or confuse AN enemy », au singulier,
# une seule fois. Deux resolutions seraient plus permissives.
#
# « STUN OR CONFUSE » : choix du joueur entre deux `ForChoiceAbility`
# (`canbe_stunned=True` / `canbe_confused=True` filtrent les cibles
# eligibles). Modele `56009` pour la forme.
#
# ⚠ Le pilote du harnais prend TOUJOURS la premiere option d'un
# `ChooseAbilities` : la branche « confuse » n'est atteignable qu'avec la cle
# `preferer_option` du banc.


DEGATS = 4
MENACE = 3


def GetAbilities() -> Sequence['Ability']:

    def break_through(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        une_defaite = [False]

        def noter(*args):
            Unused(args)
            une_defaite[0] = True

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: deal 4 damage to an enemy",
                lambda targets:
                    this.DealDamage(list(targets), DEGATS, effect,
                                    if_this_attack_defeats=noter),
            ).SetTarget(Enemy),
        )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: remove 3 threat from a scheme",
                lambda targets:
                    this.RemoveThreatFromSchemes(list(targets), MENACE, effect,
                                                 if_this_remove_last_threat=noter),
            ).SetTarget(Scheme2),
        )

        if not une_defaite[0]:
            return

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: stun an enemy",
                lambda targets:
                    Faces.GiveStatus(list(targets), "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Break Through: confuse an enemy",
                lambda targets:
                    Faces.GiveStatus(list(targets), "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            break_through,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
