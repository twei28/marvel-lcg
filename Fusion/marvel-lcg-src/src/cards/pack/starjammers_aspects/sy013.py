from . import *
# Honorary Starjammer (Basic, amelioration 0 [energy]). TITLE.
# Play only if your identity has the STARJAMMER trait.
# Attach to a friendly character. Max 1 per character.
# Attached character gets +1 hit point and gains the STARJAMMER trait.
#
# Carte de reference : sk064 Fantastic Four Member (62037 Black Belt) : le MEME texte mot pour mot a un trait pres
# (`CanPlayThisUpgradeCard(Friend, conditions=[identite a le trait])` + `*GiveKeywordToAttached("Character", health=1, trait=..)` ;
# « Max 1 per character » = `desc.MaxPerUnit "1"`).
# « Play only if YOUR IDENTITY has the trait » : l'identite du joueur, pas un personnage ami.
def GetAbilities() -> Sequence['Ability']:
    def identite_starjammer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return effect.GetInitiator().GetIdentity().HasTrait("STARJAMMER")
    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Friend,
            conditions=[identite_starjammer],
        ),
        *AbilityFactory.GiveKeywordToAttached("Character", health=1, trait="STARJAMMER"),
    ]
