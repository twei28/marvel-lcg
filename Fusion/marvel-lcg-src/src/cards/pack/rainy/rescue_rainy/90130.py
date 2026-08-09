from . import *

# Catastrophic Collision

def GetAbilities() -> Sequence['Ability']:

    def collision(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()

        def degats(targets: Sequence['CardFace']) -> None:
            def action(pl: 'Player') -> None:
                # « 2 par joueur ». NOTE : le piercing des degats indirects
                # n'est pas modelisable ici (DealIndirectDamage n'accepte pas de
                # propriete d'attaque) ; un statut tough absorbera donc 1 point
                # au lieu d'etre ignore.
                nombre = 2 * Worlds.GetPlayerNum(effect)
                this.DealIndirectDamage(pl.GetIdentity(), nombre, effect)
            Players.ForEachPlayer(effect, action)

        def carte_face_cachee(targets: Sequence['CardFace']) -> None:
            def action(pl: 'Player') -> None:
                # Methode du joueur ; les cartes distribuees le sont face cachee.
                pl.DealEncounterCards(1, effect)
            Players.ForEachPlayer(effect, action)

        def defausser_la_plus_chere(targets: Sequence['CardFace']) -> None:
            def action(pl: 'Player') -> None:
                main = list(pl.hand_cards.Get())
                if not main:
                    return
                chere = max(main, key=lambda f: f.cost if f.cost != None else 0)
                Faces.DiscardAll([chere], effect)
            Players.ForEachPlayer(effect, action)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 2 indirect damage per player (piercing)", degats),
            AbilityFactory.ForChoiceAbility(
                "Deal each player 1 facedown encounter card", carte_face_cachee),
            AbilityFactory.ForChoiceAbility(
                "Each player discards the highest-cost card from their hand",
                defausser_la_plus_chere),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            collision
        ),
    ]
