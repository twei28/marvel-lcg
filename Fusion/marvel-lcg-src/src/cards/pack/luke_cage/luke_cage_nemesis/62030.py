from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        # « discards cards from the top of the ENCOUNTER deck » : c'est bien le
        # deck rencontre, pas celui du joueur. La borne evite la boucle infinie
        # si aucun sbire [[Serpent Society]] ne reste a trouver.
        trouve = None
        for _ in range(60):
            faces = Worlds.DiscardEncounterCards(1, effect)
            if not faces:
                break
            face = faces[0]
            if Minion.IsType(face) and face.HasTrait('SERPENT SOCIETY'):
                trouve = face
                break
        if trouve:
            trouve.Reveal(player, effect)
    def boost_ability(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        # « You are confused » : le joueur vise est celui contre qui l'ennemi
        # s'active, que le message porte deja.
        player = message.GetToPlayer()
        if player:
            Faces.GiveStatus([player.GetIdentity()], "Confused", effect)
    return [
        *AbilityFactory.UnitCannotAttackTarget(None, cannot_attack=CardFinder(trait='SERPENT SOCIETY')),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True),
        AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost_ability),
    ]
