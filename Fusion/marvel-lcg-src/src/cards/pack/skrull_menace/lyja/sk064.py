from . import *

# Fantastic Four Member — AMELIORATION BASIC, cout 0 [mental]. TITLE.
# Play only if your identity has the FANTASTIC FOUR trait.
# Attach to a friendly character. Max 1 per character.
# Attached character gets +1 hit point and gains the FANTASTIC FOUR trait.
#
# Carte de reference : **`62037`** Black Belt — le MEME texte mot pour mot (« Play only if
# ... Attach to a friendly character. Max 1 per character. Attached character gets +1
# hit point and gains the X trait ») : `CanPlayThisUpgradeCard(Friend, conditions=[...])` +
# `*GiveKeywordToAttached("Character", health=1, trait=...)` ; « Max 1 per character » =
# `desc.MaxPerUnit "1"` (lu par le moteur).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Play only if YOUR IDENTITY has the FF trait » : l'identite du joueur (Lyja heros oui,
#    Laura Green non : SKRULL. SPY.) ; ce n'est pas « un personnage FF ».
#  - « FRIENDLY character » : `Friend` (identite ou allie), pas un ennemi.
#  - « Max 1 PER CHARACTER » : MaxPerUnit 1 (sk064 deux fois sur le meme personnage refusee).


def GetAbilities() -> Sequence['Ability']:

    def identite_ff(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.GetInitiator().GetIdentity().HasTrait("FANTASTIC FOUR")

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Friend,
            conditions=[identite_ff],
        ),
        *AbilityFactory.GiveKeywordToAttached("Character", health=1, trait="FANTASTIC FOUR"),
    ]
