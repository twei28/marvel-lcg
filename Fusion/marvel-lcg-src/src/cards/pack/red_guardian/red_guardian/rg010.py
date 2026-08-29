from . import *

# Shield Harness
# Red Guardian's Shield does not count toward your hand size.
# Hero Response: After Red Guardian's Shield is discarded from play, exhaust
#   Shield Harness -> return Red Guardian's Shield to your hand.
#
# 1) La taille de main. Le crochet existe : `Message.CheckIfFaceCountHandSize`,
# envoye par le moteur pour CHAQUE carte de la main quand il compte la main
# (player_action.py). Connection to the Worldmind (28007) l'utilise via
# `AbilityFactory.ThisDoesNotCountTowardHandSize()`, mais cette fabrique fixe le
# declencheur sur « This » et ne travaille QUE depuis la main. Ici la capacite
# est portee par une AUTRE carte, en jeu, et vise le bouclier : la capacite est
# donc montee a la main sur le meme message, avec un declencheur nomme.
# Aucun ecart : la clause est bien rendue.
#
# 2) Le retour. Le bouclier vient de quitter le jeu pour la defausse, donc
# `RendreLeBouclier` (qui cherche une carte EN JEU) ne le trouverait plus. On
# recupere directement la carte qui a declenche le message et on l'ajoute a la
# main.
#
# `from_where="PlayerArea"` n'est PAS utilisable : ce filtre teste
# `from_area.play_area != None`, or le bouclier vit attache a un ennemi ou a une
# manigance, dans un `DeckType.UpgradesArea` construit sans joueur associe. Le
# test fidele de « from play » est le drapeau `is_in_play` de la zone d'origine,
# qui est bien arme pour cette zone.


def GetAbilities() -> Sequence['Ability']:

    def _est_le_bouclier_de_ce_joueur(effect: 'Effect',
                                      message: 'Message.CheckIfFaceCountHandSize') -> bool:
        if not message.trigger.IsName(NOM_BOUCLIER):
            return False
        if not message.IsToPlayer():
            return False
        return message.GetToPlayer() is effect.this.GetControlByPlayer()

    def hors_taille_de_main(effect: 'Effect',
                            message: 'Message.CheckIfFaceCountHandSize') -> None:
        message.SetNotCountHandSize(effect)

    def defausse_depuis_le_jeu(effect: 'Effect',
                               message: 'Message.AfterCardDiscard') -> bool:
        return message.from_area.flags.is_in_play

    def recuperer(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = effect.GetInitiator() or effect.this.GetControlByPlayer()
        bouclier = message.trigger
        if joueur is None or bouclier is None:
            return
        Faces.AddToHand([bouclier], joueur, effect)

    return [
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfFaceCountHandSize,
            [_est_le_bouclier_de_ce_joueur],
            hors_taille_de_main,
        ),
        AbilityFactory.AfterCardDiscard(
            AbilityType.HeroResponse,
            CardFinder(name=NOM_BOUCLIER),
            recuperer,
            control_by_player="You",
            conditions=[defausse_depuis_le_jeu],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
