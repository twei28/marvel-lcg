from . import *

# * Karai — SBIRE nemesis, x1 (2/5). FOOT CLAN. NINJA. MNG 1 / ATQ 1 / PV 2.
# When Revealed: Cloak Karai.
# When Defeated: Cloak the villain.
# (Leonardo's nemesis minion.)
# [star] Boost: Deal this card to the first player as a facedown encounter card.
#
# Cartes de reference :
#  - `bw021` Imperius Rex : le MEME ★ Boost « deal this card to yourself as a
#    facedown encounter card » — on detourne le rangement a venir par
#    `WhenCardWouldDiscard` -> `message.SetToArea(joueur.dealt_encounter_cards)`
#    (deplacer la carte dans le corps du boost est ecrase par le moteur) ;
#  - `WhenUnitBeDefeated(WhenDefeated, "This", op)` pour le When Defeated
#    (§3.1 du guide) ; `WhenThisRevealed(None, op)` pour le When Revealed ;
#  - `Worlds.GetFirstPlayer(effect)` pour « the first player ».
#
# « CLOAK X » = poser la carte d'etat Cloaked sur X (fiches
# docs/reference/mots-cles/cloak.md et cloaked.md). `Cloak(...)` vit dans
# `leonardo_nemesis/__init__.py` ; les TROIS appels du pack (tl015 x2, tl016)
# y passent et posent `Faces.GiveStatus([carte], "Cloaked", effect)`.
#
# ⚠ Pas de `desc.Boost` : seule l'ETOILE est imprimee (aucune icone chiffree).
# `desc.Nemesis = "Leonardo"` (nom du heros, comme ls014/ls015).
#
# Mots-pieges :
#  - « Cloak THE VILLAIN » (When Defeated) : le vilain, pas Karai ;
#  - « to the FIRST player » : ≠ bw021 (qui donne a celui qui a revele) ;
#  - nom unique : `CardFinder(name="Karai")` SANS l'etoile.


def GetAbilities() -> Sequence['Ability']:

    def karai_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Cloak(effect, this)

    def karai_vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        Cloak(effect, vilain)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        premier = Worlds.GetFirstPlayer(effect)
        if premier is None:
            return

        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            message2.SetToArea(premier.dealt_encounter_cards)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                rediriger,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            karai_revelee,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            karai_vaincue,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
