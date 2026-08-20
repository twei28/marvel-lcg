from . import *

# Skies Above New York

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Discard each other SETTING environment in play. »
        this = effect.this.CastTo(Environment)
        autres = [x for x in Worlds.GetOnFieldEnvironment(effect)
                  if x != this and x.HasTrait("SETTING")]
        if autres:
            Faces.DiscardAll(autres, effect)

    def prendre_de_lattitude(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action: Exhaust an AERIAL card you control OR spend an [energy]
        # resource → a friendly character you control gains the AERIAL trait
        # until the end of the round. »
        #
        # C'est la carte qui rend Vulture jouable au sol : elle donne le trait
        # que le vilain exige, un personnage a la fois.
        for cible in effect.targets:
            cible.GainUntilRoundEnd(effect, trait=["AERIAL"])

    def a_une_carte_aerienne(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # ⚠ SANS CETTE CONDITION LA PARTIE BLOQUE, mesure sur 8 parties sur 8 :
        # le moteur propose une action de heros meme quand son cout n'a AUCUNE
        # cible, l'action echoue, il la repropose a l'identique. C'est le meme
        # defaut que sur Tenacity (`01093`, carte officielle) — mais ici la
        # carte peut s'en garder elle-meme.
        joueur = effect.GetInitiator()
        return joueur.GetControlCards(
            CardFinder(trait="AERIAL", canbe_exhaust=True)) != []

    def une_cible_a_convaincre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # ⚠ LE BLOCAGE DU SCENARIO UNDERLING EST ICI, et il a resiste a trois
        # hypotheses (payeur du pilote, empreinte de progres, desistement).
        # Mesure : le journal repete
        #   « [wd165] (Hero Action) WhenPlayerInTurn failed »
        # jusqu'a l'abandon, et le verdict dit « le plateau n'a pas bouge ».
        #
        # La cause : donner AERIAL a un personnage QUI L'A DEJA ne change rien.
        # Quand le seul personnage amical restant est deja aerien — ce qui
        # arrive des que l'allie meurt et que le heros a ete servi une fois —
        # l'action reste proposee, ne fait rien, et la partie tourne en rond.
        #
        # Meme remede que la garde ci-dessus : la carte se garde elle-meme.
        joueur = effect.GetInitiator()
        return any(
            not cible.HasTrait("AERIAL")
            for cible in joueur.GetControlCards(CardFinder(card_type=Friend))
        )

    def action(conditions=[]) -> 'Ability':
        return AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            prendre_de_lattitude,
            conditions=conditions,
        ).SetTarget(CardFinder(card_type=Friend))

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        # Le « OU » du texte est DEUX abilites, pas un cout a deux visages.
        action([a_une_carte_aerienne, une_cible_a_convaincre])
        # ⚠ MEME DEFAUT QUE wd090, ET IL ETAIT LA DEPUIS LE LOT UNDERLING :
        # « an AERIAL card YOU CONTROL ». Sans `from_where`, le cout pouvait
        # epuiser le VILAIN. Aucun outil ne le voyait ; c'est le journal
        # d'autoplay qui l'a dit.
        .SetCostFunc(CostFunc.Exhaust(trait="AERIAL", from_where=["YouControlCards"]))
        .SetCondition(only_if_you_control_trait="AERIAL"),
        action([une_cible_a_convaincre]).SetCost(Cost("Y")),
    ]
