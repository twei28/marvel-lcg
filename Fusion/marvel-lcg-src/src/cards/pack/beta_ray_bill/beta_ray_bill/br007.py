from . import *

# * Skuttlebutt — SOUTIEN, cout 3, [mental]. AERIAL. PERSONA. VEHICLE. UNIQUE.
# Skuttlebutt does not ready at the end of the player phase. While Skuttlebutt
#   is ready, you get +1 hand size.
# Hero Action: Exhaust Skuttlebutt -> choose one:
#   • Deal 2 damage to each enemy.
#   • Remove 2 threat from each scheme.
#
# ⚠ LE VAISSEAU EST UNE RESSOURCE A UN COUP PAR PARTIE, sauf si on le
# redresse : br005 Star Jump est la SEULE carte qui le fait, et c'est tout
# l'interet de sa premiere branche.
#
# TEXTE CONTRE CODE
#  « does NOT ready at the end of the player phase » -> une carte inclinee le
#    reste. C'est la moitie la plus importante du texte, et celle qu'on oublie.
#  « While Skuttlebutt is READY, you get +1 hand size » -> le bonus s'eteint
#    des qu'on utilise l'Action. Le joueur choisit donc entre une main plus
#    large et un effet. ⚠ `condition=` + `change_on_event` sont OBLIGATOIRES :
#    sans `change_on_event`, la valeur est calculee une fois et ne bouge plus
#    (leçon `get_new_value` du pack doctor_druid).
#  « DEAL 2 DAMAGE TO EACH ENEMY » -> TOUS les ennemis, vilain compris, et
#    ceux des autres joueurs. Aucun filtre de controle dans le texte.
#  « choose one » -> `ChooseAbilities` avec deux `ForChoiceAbility`.


def GetAbilities() -> Sequence['Ability']:

    def c_est_la_fin_de_phase(effect: 'Effect', message: 'Message.WhenCardWouldReady') -> bool:
        """« does NOT ready at the end of the player phase », et RIEN D'AUTRE.

        ⚠ AUCUNE FABRIQUE `ThisNotReadyInReadyStep` N'EXISTE : c'etait une API
        inventee, sortie par `test_cards`. Et aucune carte du depot ne porte ce
        texte, il n'y a donc pas de modele a copier.
        Le moteur redresse tout en fin de phase par `Faces.ReadyAll(faces,
        EndPhase(player))` (player_phase.py:100). On bloque donc le
        redressement UNIQUEMENT quand l'effet qui redresse est cette regle-la :
        `CardCannotReady` sans condition interdirait aussi br005 Star Jump, qui
        existe precisement pour redresser le vaisseau, et Skuttlebutt serait
        alors mort au premier usage.
        """
        Unused(effect)
        par = getattr(message, "by_effect", None)
        return par is not None and type(par).__name__ == "EndPhase"

    def est_pret(effect: 'Effect') -> bool:
        this = getattr(effect, "this", None)
        return this is not None and not this.IsExhaust()

    def piloter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def frapper(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
            if ennemis:
                this.DealDamage(ennemis, 2, effect)

        def deblayer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            manigances = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                          if s.threat > 0]
            if manigances:
                this.RemoveThreatFromSchemes(manigances, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 2 damage to each enemy", frapper),
            AbilityFactory.ForChoiceAbility("Remove 2 threat from each scheme", deblayer),
        )

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        *AbilityFactory.CardCannotReady(
            "This",
            conditions=[c_est_la_fin_de_phase],
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            hand_size=1,
            # ⚠ IL N'EXISTE AUCUN `OnEvent` POUR L'INCLINAISON. La liste
            # (on_event.py) va de `CardInPlay` a `Faceup`, `Form`, `Counter`,
            # `Threat`, `Status`... rien sur pret/incline. `OnEvent.Exhaust`
            # etait invente, et `test_cards` l'a sorti.
            # On se repose donc sur `condition=`, que la fabrique evalue A
            # CHAQUE LECTURE de la valeur (leçon `EstEnMain`, pack
            # doctor_druid) : la taille de main suit bien l'etat du vaisseau.
            condition=est_pret,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            piloter,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
