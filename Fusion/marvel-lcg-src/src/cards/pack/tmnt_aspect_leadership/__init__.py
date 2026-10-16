from cards.pack import *


# Allies WEASEL lies a `ul040` Weasel In (ul041 Mushroom, ul042 Zanna, ul043 Zink), cartes joueur a DOS DE
# RENCONTRE. Texte commun :
#   « X does not count against your ally limit. When Revealed: <effet> and put X into play under your
#     control. This card gains surge. This effect cannot be canceled. »
# Modele : `39071` Longshot (meme phrase mot pour mot) et `60139` Shop Proprietor (« your » = le joueur
# qui revele la carte, `message.GetToPlayer()`, mise en jeu `under_control=True`).
def AbilitiesBelette(effet_propre: Callable[['Effect', 'Player'], None]) -> List['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Ally)
        joueur = message.GetToPlayer()
        effet_propre(effect, joueur)
        this.PutIntoPlay(joueur, effect, under_control=True)
        ThisCardGainSurge(effect)

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ).SetCannotBeCancel(),
    ]
