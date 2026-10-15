from . import *

# Forming the Revengers — TRAITRISE x2 (New Revengers). 1 boost.
# When Revealed: Discard cards from the top of the encounter deck until a card with the REVENGER trait is
#   discarded. Reveal that card.
#
# Cartes de reference : **`sk102`** A New Skrull Is Born (meme coffret : `Worlds.DiscardEncounterCardsUntil(
# effect, trait=...)` puis `face.Reveal(...)`) ; **`01116b`** Underground Distribution.
#
# ⚠ Mots-pieges : « a card WITH THE REVENGER TRAIT » : TOUT type de carte (sbire, environnement
# O.M.N.I.T.R.O.N.I.C.U.S. compris), pas seulement un sbire ; « REVEAL » (pas « put into play ») : ses
# « When Revealed » partent ; carte « Revenger » absente du deck : la defausse remelangee est native
# (acceleration), pas de boucle infinie.


def GetAbilities() -> Sequence['Ability']:

    def formation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        face = Worlds.DiscardEncounterCardsUntil(effect, trait=TRAIT_REVENGER)
        if face is not None:
            face.Reveal(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, formation),
    ]
