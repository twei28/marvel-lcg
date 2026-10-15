from . import *

# Impostor — ATTACHEMENT (Skrull Empire ; meme carte dans Secret Invasion). CONDITION.
# Treat attached ally as a SKRULL minion with a blank text box. Attached
#   minion's SCH is equal to its printed THW and it does not take consequential
#   damage.
# When Revealed: Attach to the non-SKRULL ally with the most remaining hit
#   points without Impostor attached. Attached ally engages its controller.
#   Otherwise, the villain schemes.
#
# Cartes de reference : **`36038`** Possessed (MEME premier paragraphe :
# `TreatAttachedCardAsMinion(Ally, "Controlled Minion")` + `AttachTo2`), avec la
# carte technique `skrull_minion` « Skrull Minion » (comme controlled_minion) ;
# `Filter.One(..., most_remaining_hp=True)` (operate/filter.py).
#
# ⚠ Mots-pieges : « NON-SKRULL ally » ; « most REMAINING hit points » ; « without
# Impostor attached » ; « engages its CONTROLLER » (natif dans TreatAsMinion) ;
# « Otherwise, the villain SCHEMES » contre le joueur qui revele (pas de surge,
# contrairement a Possessed).


def GetAbilities() -> Sequence['Ability']:

    def imposteur(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        allies = [a for a in Worlds.GetOnFieldAllies(effect, CardFinder(not_with_attach=CardFinder(name="Impostor")))
                  if not a.HasTrait("SKRULL")]
        allie = Filter.One(allies, effect, most_remaining_hp=True) if allies else None
        if allie:
            this.AttachTo2(allie, effect)
            return
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            mechant.DoSchemes(message.GetToPlayer(), effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Skrull Minion"),
        AbilityFactory.WhenThisRevealed(None, imposteur),
    ]
