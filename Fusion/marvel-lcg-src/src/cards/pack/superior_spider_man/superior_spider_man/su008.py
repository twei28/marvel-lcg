from . import *

# Mastermind — AMELIORATION, cout 1 [mental]. TITLE.
# Action: Attach a card from your hand to Contingency Plan facedown (to a
#   maximum of 1).
# Hero Response: After you defeat a minion with 2 or more threat on it, look at
#   the top 3 cards of the encounter deck. Discard 1 of them.
#
# CARTES DE REFERENCE
#  - `su001b` / `su001c` : la meme attache face cachee (`PlaceCardHere(...,
#    False, effect)`), sans la pioche.
#  - `an001a`, `vp001a` : `AfterUnitDefeatedUnit(type, "You", Minion, op)`.
#    ⚠⚠ RECETTES §1 : cette fabrique rend une ENVELOPPE `DelayAbility` et la
#    limite « once per » y etait silencieusement inerte jusqu'au correctif du
#    03/09/2026. Ici il n'y a pas de limite imprimee, mais le piege est a
#    connaitre.
#  - `40004` Precognition, `hd024` : regarder N cartes du dessus du deck
#    rencontre et en defausser une.
#
# TEXTE CONTRE CODE
#  ⚠ « a minion WITH 2 OR MORE THREAT ON IT » : la menace posee par `track`.
#    C'est la seule carte qui RECOMPENSE l'accumulation, et le seuil de 2
#    demande donc DEUX tracks sur le meme sbire.
#    ⚠ Le sbire est vaincu quand la Reponse part : on lit sa menace sur le
#    message, pas en jeu — un sbire mort n'y est plus (RECETTES §7).
#  ⚠ « Action » et non « Hero Action » : la premiere capacite vaut dans les
#    DEUX formes, contrairement a celle des alter-egos.
#  ⚠ « TO A MAXIMUM OF 1 » : plafond sur ce qui est deja pose sous Contingency
#    Plan.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def plan_disponible(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        plan = ContingencyPlanDuJoueur(effect)
        if plan is None or len(CartesPoseesSous(plan)) >= 1:
            return False
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and len(list(joueur.hand_cards.Get())) > 0

    def attacher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        plan = ContingencyPlanDuJoueur(effect)
        cartes = [c for c in effect.targets if c is not None]
        if plan is not None and cartes:
            plan.PlaceCardHere(cartes[:1], False, effect)

    def sbire_charge(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        # ⚠ CORRECTIF DU 09/09/2026 — LA CAPACITE NE PARTAIT JAMAIS.
        # Le sbire vaincu est `message.target` (alias `who_took_damage`,
        # sender_damage.py:944 et 953). `defeated_unit` N'EXISTE PAS sur ce
        # message, et le repli `message.trigger` designe... le TUEUR
        # (`super().__init__(trigger=killer)`, ligne 955). La condition lisait
        # donc la menace posee sur le HEROS, toujours nulle, et refusait la
        # capacite a chaque fois. Mesure du 09/09/2026, sonde posee dans la
        # condition : `cond=[('[(01,su001a) Spider-Man]', 0)]` — c'est bien
        # Spider-Man qui etait pese, pas le sbire qu'il venait de tuer.
        # Aucune gate ne pouvait le voir : le seul cas du pack mesurait l'AUTRE
        # capacite de la carte (l'Action d'attache).
        vaincu = getattr(message, "target", None)
        return MenaceSurSbire(vaincu) >= 2

    def fouiller(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        deck = Worlds.GetEncounterDeck(effect)
        if deck is None:
            return
        vues = [f for f in list(deck.Get())[::-1][:3] if f is not None]
        if not vues:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 1 of the top 3 encounter cards",
                lambda cibles: Faces.DiscardAll(
                    [c for c in cibles if c is not None][:1], effect),
            # ⚠ CORRECTIF DU 09/09/2026 — `from_where` MANQUAIT. Sans lui, la
            # selection ne regarde que les cartes EN JEU (`Default`) : les trois
            # du dessus du deck Rencontre n'etaient jamais des cibles legales,
            # le choix partait sans candidat et RIEN n'etait defausse. Mesure du
            # 09/09/2026 : le deck rendait le meme etat avec et sans le module.
            # `EncounterDeckTop` est la zone prevue (selector_where.py:13) ; le
            # `check_face_fn` la reduit aux trois cartes REGARDEES.
            ).SetTarget(CardFinder(check_face_fn=lambda f: f in vues), range=(1, 1),
                        from_where=["EncounterDeckTop"]),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            attacher,
            conditions=[plan_disponible],
        ).SetName("Mastermind")
        .SetTarget(CardFinder(), range=(1, 1), from_where=["YourHandCards"]),

        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Minion,
            fouiller,
            conditions=[sbire_charge],
        ),
    ]
