from . import *

# Super-Skrull Enhancement — ATTACHEMENT x3 variantes (Secret Invasion). CONDITION. Badge +3 ATQ (cle desc `ATK+`), ★ + sans icone chiffree.
# Attach to the SKRULL minion with the most remaining hit points without another Super-Skrull Enhancement attached. If you
#   cannot, choose a CAMOUFLAGED ally, flip that ally and attach this card to it. Otherwise, this card gains surge.
# (aucun paragraphe de regle apres l'attache)
# ★ Boost: Reveal this card, after this activation ends.
#
# Cartes de reference :
#  - Attache : **`AttachToFaceWhenPutIntoPlay(CardFinder2("SKRULL", Minion), most_remaining_hp=True, without_another_copy=True,
#    if_cannot_operation=...)`** (attachment.py ; `sk098` pour « most remaining hit points », `gambit 37034` pour « without
#    another copy »). Branche « If you cannot » : le joueur choisit un allie CAMOUFLAGED, `RetournerAllie` (helper du set),
#    puis `AttachTo2` ; sinon la carte gagne Surge (`ThisCardGainSurge`, `sk103`).
#  - Boost « Reveal this card, after this activation ends » : **`sk107`** Skrull Scientist (`RunAt.AfterEnemyActivationEnd`) +
#    `sk115` (`this.Reveal(joueur, effect)`).
#  - `ATK+` : base automatique (`HasModify`), aucun script ; `GiveKeywordToAttached` pour les PV / la riposte (`sk122`).
#
# ⚠ Mots-pieges : « the SKRULL minion » (un SBIRE, pas un allie ni le mechant) ; « WITHOUT ANOTHER Super-Skrull Enhancement »
# (trois cartes de meme nom, les trois variantes comptent) ; « If you cannot, choose a CAMOUFLAGED ally, flip THAT ally and
# attach » : retourner D'ABORD (les attachements de l'allie partent), attacher ENSUITE au sbire ; « Otherwise » = aucun allie
# CAMOUFLAGED non plus ; le Boost est resolu APRES l'activation.


def GetAbilities() -> Sequence['Ability']:

    def sans_sbire(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        allies = AlliesCamoufles(effect)
        if not allies:
            ThisCardGainSurge(effect)
            return
        choisi = Filter.One(list(allies), effect)
        sbire = RetournerAllie(effect, choisi) if choisi is not None else None
        if sbire is not None and sbire.IsInPlay():
            this.AttachTo2(sbire, effect)
        else:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        RunAt.AfterEnemyActivationEnd(effect, message.would_message, lambda: this.Reveal(joueur, effect))

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder2("SKRULL", Minion),
            most_remaining_hp=True,
            without_another_copy=True,
            if_cannot_operation=sans_sbire,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
