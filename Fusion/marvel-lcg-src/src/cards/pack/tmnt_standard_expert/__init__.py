from cards.pack import *

# ===========================================================================
# Helpers partages des ensembles TMNT Standard / Expert (Inkwire, prefixe `te`),
# utilisables par TOUS les vilains TMNT. Les cartes « habillees » (te021-te027,
# te121-te123) n'ont aucun script : `ability_link` les branche sur le core
# 01186-01193.
#
# ⚠ « daze your identity » : la carte d'etat DAZED est livree par le pack du
# vilain Baxter Stockman (autre agent, encart « Dazed Rules Insert ») ; ce pack
# ne la definit pas, il la POSE par `Faces.GiveStatus(..., "Dazed", ...)`.
# ⚠ « Cloak » : meme definition que le pack `shredder` (cloak.md, cloaked.md).
# ===========================================================================


def Cloak(effect: 'Effect', face: 'CardFace|None') -> bool:
    if face is None:
        return False
    return Faces.GiveStatus([face], "Cloaked", effect) > 0


def Daze(effect: 'Effect', face: 'CardFace|None') -> bool:
    if face is None:
        return False
    return Faces.GiveStatus([face], "Dazed", effect) > 0


def FaceCacheeAuPremierJoueur(effect: 'Effect', this: 'CardFace') -> None:
    """« Deal this card to the first player as a facedown encounter card » (boost) :
    detourne le rangement de la carte de boost (modele tl015 / bw021)."""
    premier = Worlds.GetFirstPlayer(effect)
    if premier is None:
        return

    def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
        message2.SetToArea(premier.dealt_encounter_cards)

    this.effect.RegisterTemp(
        AbilityFactory.WhenCardWouldDiscard(AbilityType.Temp0, "This", rediriger),
        unregister_after_exec=False,
        until_round_end=True,
    )
