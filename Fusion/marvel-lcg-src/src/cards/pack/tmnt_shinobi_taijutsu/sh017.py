from . import *

# * Odyn — ALLIE unique 3 [physical], Taijutsu (TMNT Shinobi, Inkwire). MONK. NINJA. TURTLE.
# THW 1 (1 degat consecutif) / ATQ 3 (2 degats consecutifs) / PV 3.
# [star] Response: After Odyn takes consequential damage ([consequential]), discard a DEFENSE card from your hand → give
#   Odyn a tough status card.
#   (TEXTE CHANGE LE 17/11/2026, fichier Inkwire du 10/11/2026 : avant « After Odyn uses a basic power ».)
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md ; `ATK = "3**"`, `THW = "1*"` = icones de degats consecutifs).
#
# Cartes de reference :
#  - « After X takes consequential damage » (allie) : `sh014` Minarai (`AfterAllyTakeConsequentialDamage(Response,
#    "AttachedAlly"/"This", op)`) ;
#  - « give X a tough status card » : `tmnt_aspect_dual/ud006` Nightwatcher (`Faces.GiveStatus([this], "Tough", effect)`) ;
#  - « discard a <trait> card from your hand → » : `ares/ar010` (`CostFunc.Discard("YourHandCards", trait=..., range=(1, 1))`).
#
# TEXTE CONTRE CODE
#  ⚠ « After ODYN takes consequential damage » : lui seul (« This »), apres les degats consecutifs de SON attaque (2) ou
#    de SON contre (1) ; ils sont DEJA subis quand le Tenace arrive (le Tenace ne les previent plus, il protege des
#    degats suivants) ; pas un autre allie, pas le heros.
#  ⚠ « discard a DEFENSE CARD from your hand » : une carte de VOTRE main portant le TRAIT DEFENSE, quel que soit son
#    type (evenement, amelioration...) ; c'est un COUT (avant la fleche) : sans carte DEFENSE en main, la Reponse n'est pas
#    proposee.
#  ⚠ « give Odyn a tough status card » : un seul Tough par personnage ; Odyn peut etre Hebete ou Camoufle en meme temps.
#  ⚠ « Response » nu (le [star] est la marque d'allie unique imprimee), pas « Hero Response ».
#  ⚠ Coquille du scan : citation « behnd » (Q-T2, reponse du 17/10/2026 : corrigee en « behind » dans cards.json).


def GetAbilities() -> Sequence['Ability']:

    def odyn(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            odyn,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetCostFunc(CostFunc.Discard("YourHandCards", trait="DEFENSE", range=(1, 1))),
    ]
