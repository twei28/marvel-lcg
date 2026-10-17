from . import *

# Mizuki — EVENEMENT DUAL Kuji-Kiri/Ninjutsu, cout 2, [mental]. PSIONIC. THWART.
# Classe : « Kuji-Kiri;Ninjutsu ».
# Hero Action (thwart): Remove 2 threat from a scheme. If this removes the last threat on that scheme, choose:
#   • Cloak a friendly character.
#   • Return an event from your discard pile to your hand.
#
# Mots-cles (fiches lues AVANT le code) : Cloak (cloak.md, cloaked.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « Remove 2 threat from a scheme. If this removes the last threat on that scheme » : `bt006` (pack beast) et `04049` Clear
#    the Area (`SetTarget(Scheme2)` + `RemoveThreatFromSchemes`, test du reste sur la manigance CIBLEE) ;
#  - « Choose: » a deux branches ciblees : `tmnt_aspect_aggression/ua002` Apex Predator (`ChooseAbilities` de
#    `ForChoiceAbility(...).SetTarget(...)` : une branche sans cible legale n'est pas offerte) ;
#  - « cloak a friendly character » : `td005` Improvised Tactics (`Faces.GiveStatus(..., "Cloaked", effect)`) ;
#  - « return an event from your discard pile to your hand » : `tmnt_shinobi_paths/se004` (`Faces.AddToHand`).
#
# TEXTE CONTRE CODE
#  ⚠ « If this removes THE LAST threat ON THAT SCHEME » : la manigance CIBLEE avait au moins 1 menace avant et en a 0 apres ; un
#    complot qui n'est pas vide (3 menaces -> 1) ne declenche rien ; 2 menaces exactement -> vide -> le choix part.
#  ⚠ « choose: » : UNE seule branche. « a FRIENDLY character » : identite ou allie de n'importe quel joueur, pas un ennemi ;
#    aucun filtre de plus (comme td005 : un personnage deja camoufle peut etre designe, `GiveStatus` n'empile pas un 2e Cloaked).
#    « an EVENT from YOUR discard pile » : sa propre defausse, un evenement (pas une amelioration) ; Mizuki elle-meme n'y est
#    pas encore pendant sa resolution.
#  ⚠ « Hero Action (thwart) » : forme heros, libelle `thwart`.


def GetAbilities() -> Sequence['Ability']:

    def mizuki(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None or not effect.targets:
            return
        manigance = effect.targets[0].CastTo(Scheme2)
        avant = manigance.threat
        this.RemoveThreatFromSchemes([manigance], 2, effect)
        if not (avant > 0 and manigance.threat == 0):
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Cloak a friendly character",
                lambda cibles: ShinobiCloak(effect, cibles),
            ).SetTarget(Friend),
            AbilityFactory.ForChoiceAbility(
                "Return an event from your discard pile to your hand",
                lambda cibles: Faces.AddToHand(list(cibles), joueur, effect),
            ).SetTarget(Event, from_where=["YourDiscardPile"]),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mizuki,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
