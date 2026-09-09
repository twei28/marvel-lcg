from . import *

# Stronger Together — EVENEMENT, cout 1, RES [wild]. TACTIC.
# Max 1 per round.
# Hero Action: Ready 2 friendly characters that share a TRAIT.
#
# ⚠⚠ HOMONYME, PAS UN JUMEAU. L'officielle `58019` (Protection, pack
# wonder_man) s'appelle aussi « Stronger Together » et n'a RIEN a voir : elle
# reduit les degats subis par un personnage qui partage un trait avec votre
# heros. Celle-ci en REDRESSE deux. Ne pas recopier son module — c'est le
# piege exact que le nom tend.
#
# CARTES DE REFERENCE
#  - `03015` Team Training (« Max 1 per round », meme forme de limite) et
#    `32009` Bulletproof Protector (« Ready your hero » par `Faces.ReadyAll`).
#
# TEXTE CONTRE CODE
#  ⚠ « 2 friendly characters THAT SHARE A TRAIT » : les deux doivent partager
#    un trait ENTRE EUX, pas avec votre heros. Le moteur n'a pas de selecteur
#    pour « une paire coherente » : on choisit le premier librement, puis on
#    restreint le second a ceux qui partagent un trait avec lui.
#  ⚠ « friendly characters » : identites ET allies, de TOUS les joueurs — le
#    texte ne dit pas « you control ». `Friend` couvre exactement cela.
#  ⚠ « READY » : un personnage deja redresse n'est pas une cible valable
#    (`canbe_ready=True`), sinon la carte se gaspillerait.
#  ⚠ « Max 1 per round » -> `LimitOncePerRound()`, limite IMPRIMEE, temoin
#    d'epuisement exige (PROCESSUS-CARTE 7 bis).
def GetAbilities() -> Sequence['Ability']:

    def stronger_together(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        premiers = [c for c in effect.targets if c is not None]
        if not premiers:
            return
        premier = premiers[0]
        Faces.ReadyAll([premier], effect)

        # ⚠ `share_trait=<face>` est le parametre PREVU du CardFinder
        # (`finder.py:135`) : il dit « partage un trait avec CETTE carte ». Un
        # predicat maison par `check_face_fn` faisait le meme travail en
        # apparence et ne rendait aucune cible — mesure du 09/09/2026.
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready a second character that shares a TRAIT with the first",
                lambda cibles: Faces.ReadyAll(list(cibles), effect)
            ).SetTarget(CardFinder(share_trait=premier, non_face=premier),
                        canbe_ready=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stronger_together
        ).SetPlay()
        .SetTarget(Friend, canbe_ready=True)
        .LimitOncePerRound(),
    ]
