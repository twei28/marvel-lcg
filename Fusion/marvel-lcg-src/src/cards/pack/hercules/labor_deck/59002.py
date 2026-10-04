from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        player = message.GetToPlayer()
        def has_6hp(effect2: 'Effect', face: 'CardFace') -> bool:
            try:
                return (int(str(face.paper.desc.get('HP', '0')).rstrip('*')) >= 6)
            except ValueError:
                return False
        minion = Worlds.FindCardOnField(effect, finder=CardFinder(non_trait='ELITE', card_type=Minion, check_effect_fn=has_6hp))
        if not minion:
            # ⚠ include_set_aside : LA CIBLE DE CETTE CARTE Y VIT (17/09/2026).
            # « Find » fouille TOUTES les zones ou la carte peut se trouver
            # (Rules Reference p.19 : « play area, set-aside area, player deck,
            # discard pile, encounter deck, etc. »). Le set NEMESIS d'Hercules
            # est mis de cote, et il contient 59037 Lernean Hydra : minion,
            # 6 PV, non-ELITE — c'est-a-dire la cible evidente d'une carte qui
            # s'appelle « Defeat the Hydra ». Sans ce drapeau, le Travail se
            # revelait et se defaussait sans rien faire. Signale en partie :
            # « le travail de sbire d'Hercules trigger dans le vide ».
            minion = Search.EncounterCard(effect, player, include_discard_pile=True, include_set_aside=True, finder=CardFinder(non_trait='ELITE', card_type=Minion, check_effect_fn=has_6hp))
            if minion:
                minion.Reveal(player, effect)
        if minion:
            minion.CastTo(CanHealth).HealHealth('All', effect)
            this.AttachTo2(minion, effect)
    def check_not_hercules(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        source = message.source
        if source and (source.paper.name == 'Hercules'):
            return False
        return True
    def after_leave(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Attachment)
        # Attache a un sbire, le Travail n'a ni controleur ni proprietaire
        # « joueur » (les deux rendent le vilain) : on retrouve Hercules par son
        # identite. 59003, sur un complot, obtient lui le joueur.
        player = None
        for candidat in Worlds.GetPlayers(effect):
            identite = candidat.GetIdentity()
            if identite and identite.IsName('Hercules'):
                player = candidat
        if Player.IsType(player):
            Atonement(effect, player)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(with_attach=True), health=6, trait='ELITE'),
            AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, None, conditions=[check_not_hercules]),
            AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, 'This', after_leave).LimitOncePerPhase()]
