from . import *

# The Other Guy — soutien signature, x1 (n/15 = 12).
# GAMMA. PERSONA. Cout 2, ressource [mental].
# Alter-Ego Response (thwart): After you change form, remove 1 threat from a
#   scheme. (Limit once per phase.)
# Hero Response (attack): After you change form, deal 1 damage to an enemy.
#   (Limit once per phase.)
#
# Cartes de reference :
#  - `aa009` * The Witches' Road pour `AfterUnitChangeForm(..., op)` ;
#  - `aa001a` pour `.LimitOncePerPhase()` ;
#  - `hk001a` / `hk010` du meme pack pour le choix de cible par
#    `ChooseAbilities` + `ForChoiceAbility`.
#
# ⚠ LE POINT DELICAT, ET IL A SON CAS DE TEST : la forme evaluee est celle
# d'APRES la bascule. En partant de l'alter-ego pour passer en heros, c'est
# la branche HERO qui tire, pas l'autre. `to_form` est ecrit en clair a cote
# du type d'abilite pour que les deux disent la meme chose : une relecture
# qui hesiterait sur l'ordre y trouve la reponse.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After YOU change form » : le joueur qui controle le soutien, pas un
#    coequipier — d'ou `"You"` et non `Identity`.
#  - Deux limites SEPAREES : chaque capacite a la sienne, « once per phase »
#    ne se partage pas entre les deux branches. Les formes s'excluant, il
#    faudrait de toute facon deux bascules dans la meme phase pour le voir.
#  - Les libelles `(thwart)` et `(attack)` alimentent Desoriente et Sonne :
#    un heros sonne ne peut pas declencher la branche degats.
#  - Aucun cout : le soutien ne s'epuise pas. Il sert a chaque bascule, une
#    fois par phase, tant qu'il est en jeu.
#  - Cette carte est la moitie de la reponse au CTR 0 de la face heros : le
#    pack force la bascule (hk007 en civil, hk008 en heros, hk003
#    Alter-Ego Action) et la recompense ici.


def GetAbilities() -> Sequence['Ability']:

    def en_civil(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect),
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    def en_heros(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 1, effect),
            ).SetLabel('attack').SetTarget(Enemy),
        )

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.AlterEgoResponse,
            "You",
            en_civil,
            to_form=AlterEgo,
        ).LimitOncePerPhase(),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            en_heros,
            to_form=Hero,
        ).LimitOncePerPhase(),
    ]
