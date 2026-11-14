from . import *

# Target Lock (6A, FOCUSED) — ATTACHEMENT. Setup. Permanent. SCH +★, ATQ +★ (badges « étoile » : aucune valeur chiffree).
# ★ Forced Interrupt : When Punisher would activate, he attacks the enemy with the fewest remaining hit points instead. If this
#   attack damages an enemy or ally, place threat on the main scheme equal to the number of boost icons on the top card of the
#   encounter discard pile.
#
# Cartes de reference : `AbilityFactory.WhenEnemyWouldActivate` + `would_act_message.SetBeInstead` (enemy.py `DoActivate`),
# brique commune `Enemy.AttackCharacter` (jigsaw/pu059 pour le garde de re-entree), `FacesCounter.CountTotalBoostIcons`
# (agent_13/ag001b.py).
# ⚠ « attacks the ENEMY with the fewest HP INSTEAD » : minions et vilain cible, jamais Punisher ni ceux qu'il ne peut pas attaquer
# (Rachel, Microchip) ; a egalite le premier joueur choisit ; « If this attack damages an ENEMY or ALLY » : au moins un ennemi ou
# allie blesse ; les icones de boost de la carte du dessus de la DEFAUSSE (la carte de boost de cette attaque) ; l'attaque de
# remplacement repasse par la meme interruption : garde de re-entree.

def GetAbilities() -> Sequence['Ability']:
    en_cours = {'oui': False}

    def au_lieu_d_activer(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        if en_cours['oui']:
            return
        punisher = Punisher(effect)
        if punisher is None:
            return
        cible = LePlusFaible(effect, CiblesDePunisher(effect, punisher))
        if cible is None:
            return
        message.SetBeInstead(effect)

        def menace_selon_le_boost(blesses: List['Unit2']) -> None:
            if not any(Enemy.IsType(u) or Ally.IsType(u) for u in blesses):
                return
            defausse = Worlds.GetEncounterDiscardPileCards(effect)
            if not defausse:
                return
            icones = FacesCounter.CountTotalBoostIcons([defausse[0]])
            schemes = Worlds.GetMainSchemes(effect)
            if icones > 0 and schemes:
                effect.this.PlaceThreatOnSchemes(schemes[:1], icones, effect)

        en_cours['oui'] = True
        try:
            PunisherAttaque(effect, punisher, cible, if_characters_damaged_by_this=menace_selon_le_boost)
        finally:
            en_cours['oui'] = False

    return [
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, CardFinder(name="Punisher"), au_lieu_d_activer),
    ]
