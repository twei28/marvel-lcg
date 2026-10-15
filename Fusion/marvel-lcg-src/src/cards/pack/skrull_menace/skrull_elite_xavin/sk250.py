from . import *

# * Xavin — SBIRE (Skrull Elite - Xavin). ELITE. SKRULL. MNG 2, ATQ 3, PV 5[per_hero], Victory 1, une
# etoile de boost (aucune icone chiffree).
# Victory 1.
# When Revealed: Discard cards from the encounter deck until a treachery is discarded. Reveal that treachery.
# [star] Boost: Put Xavin into play engaged with you.
#
# Cartes de reference :
#  - « Discard cards until X is discarded. Reveal that X » : **`sk144b`** / helper `RevelerPouvoirDuDeck` de
#    paibok (`Worlds.DiscardEncounterCardsUntil` + `Reveal`) ; critere : `CardFinder(check_face_fn=...)`
#    (modele lyja/__init__.py `FinderTraitrise`).
#  - Boost qui met la carte en jeu : **`hs007`** ; helper `MettreEnJeuEngage`.
#
# ⚠ Mots-pieges : « until a TREACHERY is discarded » (type Treachery ou trait TREACHERY, voir `EstTraitrise`) ;
# « Reveal THAT treachery » (la carte defaussee est revelee : elle sort de la defausse) ; aucune traitrise dans le
# deck : tout le deck est defausse, rien n'est revele ; Victory 1 natif.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        traitrise = Worlds.DiscardEncounterCardsUntil(effect, check_face_fn=EstTraitrise)
        if traitrise is not None:
            traitrise.Reveal(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreEnJeuEngage(effect, effect.this, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
