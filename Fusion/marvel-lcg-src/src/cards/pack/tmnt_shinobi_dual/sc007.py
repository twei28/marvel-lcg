from . import *

# Mizuki — EVENEMENT DUAL Kuji-Kiri/Ninjutsu, cout 2, [mental]. PSIONIC. THWART.
# Classe : « Kuji-Kiri;Ninjutsu ».
# Hero Action (thwart): Remove 2 threat from a scheme. Choose:
#   • Cloak a friendly character.
#   • Return an event from your discard pile to your hand.
#   (TEXTE CHANGE LE 17/11/2026, fichier Inkwire du 19/10/2026 : le « If this removes the last threat on that scheme »
#   a DISPARU, le choix part TOUJOURS ; une citation « Take flight. » —Leonardo a ete ajoutee.)
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
#  ⚠ (avant le 17/11/2026 : « If this removes the last threat on that scheme » ; SUPPRIME du texte imprime) : la manigance
#    est CIBLEE, 2 menaces sont retirees, puis le joueur choisit TOUJOURS, qu'elle soit videe ou non.
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
        this.RemoveThreatFromSchemes([manigance], 2, effect)

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
