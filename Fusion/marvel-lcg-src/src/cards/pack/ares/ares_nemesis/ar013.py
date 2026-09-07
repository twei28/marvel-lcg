from . import *

# * Aegis Breastplate — ATTACHEMENT nemesis. ARMOR. OLYMPUS. 2 boost. UNIQUE.
# Attach to a minion. Otherwise, attach to the villain.
# Forced Interrupt: When attached enemy would take any amount of damage, place
#   it here instead and deal that much damage to the attacker. If there is 5 or
#   more damage here, discard this card.
#
# CARTES DE REFERENCE
#  - `04065` * Crossbones' Armor : LE MODELE de l'eponge — `WhenUnitWouldTakeDamage
#    (ForcedInterrupt, <hote>, op)` + `message.SetBeInstead(effect)` +
#    `Faces.PlaceCountersOn([this], damage, 'damage', effect)` + defausse a 5.
#  - `04029` * Crossfire's Rifle : `AttachToFaceWhenPutIntoPlay(CardFinder(...),
#    if_cannot_attach_to=Villain)`, le repli « Otherwise, attach to the
#    villain ».
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to a MINION. Otherwise, the villain » -> `CardFinder(card_type=
#    Minion)` puis `if_cannot_attach_to=Villain`. Sans sbire en jeu, la
#    cuirasse va sur le vilain.
#  ⚠ « ANY amount of damage » -> toute source, attaque ou non
#    (`is_from_attack` non pose). Un Feint qui inflige 2, une brulure, un
#    evenement : tout est absorbe.
#  ⚠ « place it HERE instead » -> `SetBeInstead` (l'hote ne prend rien) +
#    compteurs `damage` sur la cuirasse, comme 04065.
#  ⚠ « deal that much damage to the ATTACKER » -> ARBITRAGE UTILISATEUR DU
#    07/09/2026 : si la source des degats est un PERSONNAGE (heros, allie,
#    ennemi), c'est lui ; sinon (Feint, evenement, effet de carte), c'est
#    l'IDENTITE du joueur a l'origine de l'effet. Aucune source ne passe
#    gratuitement. Spray and Pray (ar002) est cinq attaques d'Ares : cinq fois
#    1 degat renvoye a Ares.
#  ⚠ « If there is 5 OR MORE damage here » -> `>= 5`, teste APRES la pose,
#    dans la meme operation : une attaque de 6 absorbe 6, renvoie 6 et defausse
#    la cuirasse. Les degats renvoyes le sont AVANT la defausse, pour partir
#    d'une carte encore en jeu.


SEUIL_DEFAUSSE = 5


def GetAbilities() -> Sequence['Ability']:

    def est_mon_hote(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        hote = Hote(effect.this)
        return hote is not None and getattr(message, "trigger", None) is hote

    def attaquant_de(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> 'CardFace|None':
        source = getattr(message, "source", None)
        if source is not None and (Hero.IsType(source) or Ally.IsType(source) or Enemy.IsType(source)):
            return source
        joueur = JoueurALOrigine(effect, message)
        if joueur is None:
            return None
        return joueur.GetIdentity()

    def encaisser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        degats = int(getattr(message, "will_take_damage", 0) or 0)
        message.SetBeInstead(effect)
        if degats <= 0:
            return
        Faces.PlaceCountersOn([this], degats, 'damage', effect)
        attaquant = attaquant_de(effect, message)
        if attaquant is not None and attaquant.card.IsOnField():
            this.DealDamage([attaquant], degats, effect)
        if this.GetCounters('damage') >= SEUIL_DEFAUSSE:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            Enemy,
            encaisser,
            conditions=[est_mon_hote],
        ),
    ]
