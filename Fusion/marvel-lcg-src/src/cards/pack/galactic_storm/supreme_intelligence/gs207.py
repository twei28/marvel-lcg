from . import *

# Supremor Seed — COMPLOT ANNEXE (Supreme Intelligence), x2. Menace 4[per_hero], icone de DANGER (Hazard),
# 2 icones de boost.
# When Defeated: The defeating player may place 1 KREE minion from the victory display in the encounter
#   discard pile.
#
# Cartes de reference :
#  - **`skrull_menace_campaign/sk271`** : `WhenSchemeBeDefeated(WhenDefeated, "This", op,
#    has_defeating_player=True)` + `message.GetDefeatingPlayer()` + `MayChooseOneAbility` pour « the
#    defeating player MAY ... ».
#  - **`aos/50127`** : `Worlds.VictoryDisplay(effect)` (pile de victoire) ; `Faces.MoveAllTo(faces,
#    Worlds.GetEncounterDiscardPile(effect), effect)` pour poser une carte dans la defausse rencontre.
#  - Hazard : base AUTOMATIQUE (`desc.Hazard`, fiche hazard.md).
#
# ⚠ Mots-pieges : « The DEFEATING player » (celui qui a retire la derniere menace, pas le premier joueur) ;
# « MAY » (refus possible : option « Cancel ») ; « 1 KREE MINION » (un seul, sbire au trait KREE : Starforce,
# Kree Infantry, Ren-Varr, Supremor...) ; « FROM the victory display IN the encounter discard pile » (un
# deplacement, la carte quitte la pile de victoire : Supremor perd 1 PV, le bonus Starforce tombe).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        vainqueur = message.GetDefeatingPlayer()
        if vainqueur is None:
            return
        sbires = [f for f in Worlds.VictoryDisplay(effect).GetAll()
                  if Minion.IsType(f) and f.HasTrait("KREE")]
        choix = []
        vus = set()
        for sbire in sbires:
            if sbire.paper.card_id in vus:
                continue
            vus.add(sbire.paper.card_id)

            def deplacer(targets: Sequence['CardFace'], sbire: 'CardFace' = sbire) -> None:
                Unused(targets)
                Faces.MoveAllTo([sbire], Worlds.GetEncounterDiscardPile(effect), effect)

            choix.append(AbilityFactory.ForChoiceAbility(
                f"Place {sbire.paper.name.lstrip('* ')} in the encounter discard pile", deplacer))
        if choix:
            vainqueur.MayChooseOneAbility(effect, *choix)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincu,
            has_defeating_player=True,
        ),
    ]
