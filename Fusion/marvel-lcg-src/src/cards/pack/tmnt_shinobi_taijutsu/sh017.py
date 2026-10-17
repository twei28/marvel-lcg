from . import *

# * Odyn — ALLIE unique 3 [physical], Taijutsu (TMNT Shinobi, Inkwire). MONK. NINJA. TURTLE.
# THW 1 (1 degat consecutif) / ATQ 3 (2 degats consecutifs) / PV 3.
# [star] Response: After Odyn uses a basic power, discard a DEFENSE card from your hand → give Odyn a tough status
#   card.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md ; `ATK = "3**"`, `THW = "1*"` = icones de degats consecutifs).
#
# Cartes de reference :
#  - « After X uses a basic power » (allie) : `14001a` / `tg001a` (`AfterUnitUseBasicPower(type, "This", op)`),
#    RECETTES-MOTEUR §1 ;
#  - « give X a tough status card » : `tmnt_aspect_dual/ud006` Nightwatcher (`Faces.GiveStatus([this], "Tough", effect)`) ;
#  - « discard a <trait> card from your hand → » : `ares/ar010` (`CostFunc.Discard("YourHandCards", trait=..., range=(1, 1))`).
#
# TEXTE CONTRE CODE
#  ⚠ « After ODYN uses a basic power » : lui seul (« This »), attaque OU contre (pas un autre allie, pas le heros).
#  ⚠ « discard a DEFENSE CARD from your hand » : une carte de VOTRE main portant le TRAIT DEFENSE, quel que soit son
#    type (evenement, amelioration...) ; c'est un COUT (avant la fleche) : sans carte DEFENSE en main, la Reponse n'est pas
#    proposee.
#  ⚠ « give Odyn a tough status card » : un seul Tough par personnage ; Odyn peut etre Hebete ou Camoufle en meme temps.
#  ⚠ « Response » nu (le [star] est la marque d'allie unique imprimee), pas « Hero Response ».
#  ⚠ Coquille du scan : citation « behnd » (question Q-T2, carte NON terminee).


def GetAbilities() -> Sequence['Ability']:

    def odyn(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            odyn,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetCostFunc(CostFunc.Discard("YourHandCards", trait="DEFENSE", range=(1, 1))),
    ]
