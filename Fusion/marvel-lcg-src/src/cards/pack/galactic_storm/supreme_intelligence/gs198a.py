from . import *
from cards.pack.galactic_storm.campaign import CampaignSetup

# Protectors of the Kree Empire (1A) — COMPLOT PRINCIPAL (Supreme Intelligence).
# Contents: Supreme Intelligence (I) and (II) (... (II) and (III) instead for expert mode). Supreme
#   Intelligence, Starforce, and Standard sets. One modular encounter set (Seeds of Corruption).
# Setup: Set each STARFORCE minion aside and put 1 of them at random into play engaged with the first
#   player. Attach Holding Tank to the villain.
#
# Cartes de reference :
#  - **`next_evol/40139a`** Sinister Intent et **`gmw/16082a`** : `WhenCardSetup("This", op)` +
#    `SetupCards.SetAsideCards(...)` (deck rencontre ET table) pour « set ... aside » a la mise en place.
#  - **`aos/50104b`** Upgrading Adaptoids : `Rand.RandomChoice` parmi les cartes mises de cote, puis
#    `PutIntoPlay("FirstPlayer")` = « put 1 of them at random into play engaged with the first player ».
#  - **`gmw/ronan/16107a`** : `face.AttachTo2(villain, effect)` pour « attach X to the villain » depuis la
#    zone mise de cote.
#
# ⚠ Mots-pieges : « EACH STARFORCE minion » (tout sbire au trait STARFORCE du deck rencontre : les huit du
# set Starforce ET les deux Supremor, lecture retenue en attendant la question Q1) ; « 1 of THEM at random »
# (parmi ceux qu'on vient de mettre de cote) ; « engaged with the FIRST player » ; « Attach Holding Tank to
# the VILLAIN » (Holding Tank est mis de cote par le scenario, `set_aside`). Le « Contents » est un texte de
# preparation (fichiers data/scenarios/gs_supreme_intelligence*.json), aucun code.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        MettreDeCoteLesSbiresStarforce(effect)
        MettreEnJeuUnStarforceAuHasard(effect)
        mechant = LeMechant(effect)
        reservoirs = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_RESERVOIR, card_type=Attachment))
        if mechant is not None and reservoirs:
            reservoirs[0].CastTo(Attachment).AttachTo2(mechant, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(5),
    ]
