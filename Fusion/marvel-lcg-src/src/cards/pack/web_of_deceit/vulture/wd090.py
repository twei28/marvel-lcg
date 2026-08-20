from . import *

# Wingsuit V2
#
# ⚠ CETTE CARTE N'AVAIT AUCUN MODULE, et c'est la voie de contre-jeu du
# scenario. `NePeutEtreAttaqueQueParLesAeriens` (voir le `__init__.py` du set)
# n'accepte que le trait AERIAL sur l'attaquant ou sur la carte qui porte
# l'attaque ; le Wingsuit distribue a la mise en place (wd077a) est justement ce
# qui donne ce trait. Sans module, il entrait en jeu inerte et aucun heros
# non-AERIAL ne pouvait frapper Vulture.
#
# Le modele est `wd165` (Skies Above New York), qui rend le meme effet pour la
# variante sous-fifre. Trois differences, toutes dans le texte :
#   - le cout est un ET (epuiser ET payer), pas un OU : une seule abilite ;
#   - la ressource est « of any type », donc `Cost("1")` ;
#   - le trait dure jusqu'a la fin de la PHASE, pas du round.

def GetAbilities() -> Sequence['Ability']:

    def prendre_de_lattitude(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action: Exhaust an AERIAL card you control and spend 1 resource
        # of any type -> a friendly character you control gains the AERIAL trait
        # until the end of the phase. »
        for cible in effect.targets:
            cible.GainUntilPhaseEnd(effect, trait=["AERIAL"])

    def a_une_carte_aerienne(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # ⚠ MEME GARDE QUE wd165, ET ELLE N'EST PAS FACULTATIVE : le moteur
        # propose une action de heros meme quand son cout n'a AUCUNE cible,
        # l'action echoue, il la repropose a l'identique, et la partie boucle.
        # Mesure sur 8 parties sur 8 a l'epoque de wd165.
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

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            prendre_de_lattitude,
            conditions=[a_une_carte_aerienne, une_cible_a_convaincre],
        )
        .SetTarget(CardFinder(card_type=Friend))
        # ⚠ `from_where` N'EST PAS FACULTATIF : « an AERIAL card YOU CONTROL ».
        # Sans lui, le selecteur balaie tout ce qui est en jeu, et le journal
        # d'autoplay l'a montre noir sur blanc — le cout epuisait VULTURE, un
        # cadeau au joueur au lieu d'un prix a payer.
        .SetCostFunc(CostFunc.Exhaust(trait="AERIAL", from_where=["YouControlCards"]))
        .SetCost(Cost("1"))
        .SetCondition(only_if_you_control_trait="AERIAL"),
    ]
