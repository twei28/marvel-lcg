from . import *

# Shape Alteration — TRAITRISE x2 (Skrull Elite - Skymax). 1 icone de boost + etoile.
# When Revealed: Remove each stunned and confused status card from each SKRULL enemy and give each SKRULL
#   enemy a tough status card. If there are no SKRULL enemies in play, this card gains surge.
# [star] Boost: Give 1 SKRULL enemy a tough status card.
#
# Cartes de reference :
#  - Retrait de statuts : `unit.DiscardStunned(effect, rule="All")` / `DiscardConfused` (can_status.py) ;
#    pose : **`sk128`** Mt'nox (`Faces.GiveStatus([unit], "Tough", effect)`).
#  - « If there are no ... this card gains surge » : **`01188`** Caught Off Guard (`ThisCardGainSurge(effect)`).
#  - Boost qui choisit un ennemi : **`24045`** Shocker (`Filter.One`) ; choix du joueur : `ForChoiceAbility(...)
#    .SetTarget(Enemy, trait="SKRULL", canbe_tough=True)` (modele sk150 `AuChoixDuJoueur`).
#
# ⚠ Mots-pieges : « EACH SKRULL ENEMY » (sbires ET mechant porteurs du trait) ; « stunned AND confused »
# (les deux statuts, chacun enleve) ; « AND give each ... a tough » (meme les ennemis qui n'avaient aucun statut) ;
# « NO SKRULL enemies in play » (aucun du tout : surge) ; Boost : UN SEUL ennemi SKRULL, au choix du joueur
# qui retourne la carte.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        ennemis = EnnemisSkrull(effect)
        if not ennemis:
            ThisCardGainSurge(effect)
            return
        for ennemi in ennemis:
            unite = ennemi.CastTo(Unit2)
            unite.DiscardStunned(effect, rule="All")
            unite.DiscardConfused(effect, rule="All")
        Faces.GiveStatus(ennemis, "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Give 1 Skrull enemy a tough status card",
                lambda cibles: Faces.GiveStatus(list(cibles), "Tough", effect),
            ).SetTarget(Enemy, trait="SKRULL", canbe_tough=True),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
