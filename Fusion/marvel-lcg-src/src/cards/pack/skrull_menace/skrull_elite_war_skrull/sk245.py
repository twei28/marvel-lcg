from . import *

# * War Skrull — SBIRE (Skrull Elite - War Skrull). ELITE. SKRULL. MNG 2, ATQ 2*, PV 5[per_hero],
# Victory 1, une etoile de boost (aucune icone chiffree).
# Victory 1.
# [star] Forced Response: After War Skrull attacks you, discard the top 2 cards of your deck.
# [star] Boost: Put War Skrull into play engaged with you.
#
# Cartes de reference :
#  - « After <ennemi> attacks you » : **`sk150`** Ice Control (`AfterUnitAttackYou(ForcedResponse, "AttachedEnemy",
#    op)`, ici `"This"`) ; le joueur par `message.GetAgainstPlayer()`.
#  - « discard the top 2 cards of YOUR deck » : **`sk114`** Skrull Soldier (`player.DiscardDeckTopCards(2, effect)`).
#  - Boost qui met la carte en jeu : **`hs007`** ; helper `MettreEnJeuEngage`.
#
# ⚠ Mots-pieges : « ATTACKS YOU » (une attaque contre ce joueur, meme defendue par un allie ; pas une
# attaque contre un autre joueur) ; « the top 2 cards of YOUR deck » (le deck du joueur attaque, pas le deck
# rencontre) ; les etoiles du texte sont des marqueurs (Reponse obligatoire ordinaire) ; l'ATQ « 2* » est un
# renvoi au texte, pas du degat consequent (decision utilisateur 15/10/2026) ; Victory 1 natif.


def GetAbilities() -> Sequence['Ability']:

    def defausse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.DiscardDeckTopCards(2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreEnJeuEngage(effect, effect.this, message.GetToPlayer())

    return [
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", defausse),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
