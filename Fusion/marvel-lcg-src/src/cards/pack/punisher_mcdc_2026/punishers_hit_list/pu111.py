from . import *

# Dramatic Entrance — TRAITRISE x2. Boost ★+2.
# When Revealed : Find Punisher and reveal him. He attacks the villain and then attacks you. Resolve his "Punishment"
#   ability.
# ★ Boost : If this attack defeats an ally, add a counter to Punisher's Hit List.
#
# Cartes de reference : pu109/pu110, `Enemy.AttackCharacter` (attaque sur le vilain) puis `DoAttackYou`.
# ⚠ « attacks the VILLAIN and THEN attacks YOU » : deux attaques d'affilee ; la premiere vise le vilain (brique commune,
# aucun joueur ne defend), la seconde est une attaque normale contre le joueur (avec carte de boost).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        punisher = Find.FindAndReveal(effect, joueur, name="Punisher", card_type=Minion)
        if punisher is not None:
            punisher = punisher.CastTo(Enemy)
            vilains = Worlds.GetVillains(effect)
            if vilains:
                punisher.AttackCharacter(vilains[0], effect)
            if joueur is not None and punisher.IsInPlay():
                punisher.DoAttackYou(joueur, effect, property=AttackProperty(against_player=joueur))
        Punishment(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.IfThisAttackDefeats(Ally, lambda cible: AjouterUnCompteurALaListe(effect), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
