from . import *

# * Wave

def GetAbilities() -> Sequence['Ability']:

    def storm_surge(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player) or message.to_player != joueur:
            return
        if not message.faces:
            return

        # ⚠ CE MOMENT PRECIS : `AfterCardsBeSpendAsResource` part APRES que les
        # cartes ont ete depensees (elles sont dans `area_resources`), mais
        # AVANT `World.DiscardResourcesArea()` qui les envoie en defausse
        # juste apres (`player_action.py`, la meme fonction, deux lignes plus
        # bas). On ne deplace donc PAS la carte ici : on intercepte plutot sa
        # defausse a venir et on la redirige (meme mecanisme que `Reserve`,
        # pack `brawn`, `RecyclerVersLaReserve`).
        choisie = joueur.AskChooseFace(
            message.faces, effect,
            prompt="Place in your Rising Tide area", forced=False,
        )
        if not choisie:
            return

        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            # Garde-fou : ne redirige QUE la defausse issue de la depense en
            # ressource (comme Reserve filtre sur `is_processing`), jamais une
            # AUTRE defausse future de la meme carte physique une fois
            # qu'elle a change de main.
            if not choisie.card.area.flags.is_resources_area:
                return
            message2.SetToArea(joueur.rising_tide)

        def apres_defausse(effet_temp: 'Effect', message2: 'Message.AfterCardDiscard') -> None:
            # `Deck.Insert` (game/deck/deck.py) corrige DEJA `is_face_up` pour
            # toute carte qui entre dans une zone marquee `is_face_up`, sur
            # CE chemin comme sur tous les autres (contrairement a
            # `Card.CheckIfCanMove`, qui lui saute son propre retournement
            # quand `ui_group=True` -- le cas de la defausse redirigee).
            # Verifie le 22/9/2026 par un cas reel (`test_capacites.py`) :
            # la carte arrive DEJA face visible ici. Ce filet ne reste que
            # pour le jour ou ce comportement moteur changerait.
            if choisie.card.area is joueur.rising_tide and not choisie.card.IsFaceUp():
                choisie.card.Flip(effet_temp)

        # ⚠ `until_round_end=True`, PAS `until_resolve_effect=effect` (bug
        # trouve et corrige le 22/9/2026 via un cas reel de test_capacites.py
        # sur la carte : `until_resolve_effect` desarme l'abilite des que la
        # resolution de CETTE reponse se termine, c'est-a-dire AVANT que
        # `World.DiscardResourcesArea()` (player_action.py, deux lignes apres
        # l'envoi du message qui declenche cette reponse) n'envoie la
        # veritable defausse -- la redirection n'avait donc jamais le temps
        # de s'armer. Modele exact de `RecyclerVersLaReserve` (pack brawn) :
        # `until_round_end=True`.
        choisie.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0, "This", rediriger,
            ),
            AbilityFactory.AfterCardDiscardInternal(
                AbilityType.Temp0, "This", apres_defausse,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        Ability(
            AbilityType.Response,
            Message.AfterCardsBeSpendAsResource,
            [],
            storm_surge,
        ).SetName("Storm Surge"),
    ]
