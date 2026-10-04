from . import *


def GetAbilities() -> Sequence['Ability']:

    def reveal_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        player = message.GetToPlayer()
        effect.this.Reveal(player, effect)

    def after_attack(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    def psycho_man_attacked(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        return message.atk_message is not None and message.trigger == effect.this.bind_face

    return [
        # CORRECTIF 4/8/2026 : `WhenThisBoostAttachTo` ne se declenche QUE si
        # la carte sert de carte de boost. Revelee normalement depuis le deck
        # Rencontre, elle n'attachait rien et partait directement a la
        # defausse : l'attachement etait inerte dans le cas le plus courant.
        # Le texte « Attach to Psycho-Man. If you cannot, this card gains
        # surge. » vise la mise en jeu, d'ou `AttachToFaceWhenPutIntoPlay`
        # (modele Genetically Enhanced 01163). La ligne Boost, elle, se
        # contente de reveler la carte : c'est `reveal_boost` ci-dessus.
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Psycho-Man"),
            if_cannot_gain_surge=True,
        ),
        # CORRECTIF 4/8/2026 : le bonus est DEJA rendu nativement par la cle
        # desc `ATK+: 2` de cards.json. Le `GiveKeywordToAttached(attack=2)` qui
        # etait ici le doublait (+4 au lieu de +2). Invisible tant que la
        # carte ne s'attachait jamais, voir le correctif juste au-dessus.
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            Enemy,
            after_attack,
            conditions=[psycho_man_attacked],
        ).SetName("Titanic Terror"),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            reveal_boost,
        ).SetName("Boost"),
    ]
