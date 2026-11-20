from . import *

# * Luke Cage — ALLIE 4 [physical], aspect Basic (Iron Fist 22). DEFENDER. HERO FOR HIRE. PV 3, THW 1*, ATK 2*.
# Toughness.
# If your hero shares a TRAIT with Luke Cage, your hero gets +1 DEF.
#
# MOTS-CLES (fiche lue) : toughness.md (`desc.Toughness`, lu par le moteur, aucun code).
#
# CARTES DE REFERENCE
#  - `40204` Hope Summers + `sk003`/`hulkling_kajislav` : un bonus conditionne a un TRAIT de l'identite =
#    `GiveKeywordToInPlayWhenApplyThis(..., condition=..., change_on_event=[Form/Faceup/Trait de l'identite])` ; le
#    recalcul a chaque changement de forme/trait est ce qui rend la condition « vivante ».
#  - `an002` Sera / `up015` : « your hero gets +1 X » = `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", ...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « your HERO » : le heros du joueur (forme heros) ; en alter-ego il n'y a pas de heros, donc pas de bonus.
#  ⚠ « shares a trait WITH LUKE CAGE » : au moins un trait en commun entre l'identite heros et les traits COURANTS de
#    Luke Cage (DEFENDER, HERO FOR HIRE) ; le bonus est recalcule au changement de forme et de trait.
#  ⚠ « +1 DEF » : defense, pas ATK ; la valeur n'est pas cumulee par les deux conditions (une seule source).


RECALCUL_IDENTITE = [OnEvent.Form("YourIdentity"), OnEvent.Faceup("YourIdentity"), OnEvent.Trait("YourIdentity")]


def HeroPartageUnTrait(effect: 'Effect') -> bool:
    joueur = effect.this.GetControlByOrOwner()
    if joueur is None or not Player.IsType(joueur):
        return False
    identite = joueur.GetIdentity()
    if not Hero.IsType(identite):
        return False
    return any(identite.HasTrait(t) for t in effect.this.traits)


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            defense=1,
            condition=HeroPartageUnTrait,
            change_on_event=Condition.AddEvent(Condition.AddEvent(RECALCUL_IDENTITE[0], RECALCUL_IDENTITE[1]), RECALCUL_IDENTITE[2]),
        ),
    ]
