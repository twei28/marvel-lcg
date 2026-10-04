from . import *

@final
class SearchInternal:

    @staticmethod
    def SearchForCardsInternal(by_effect: 'Effect',
                                player: 'Player',
                                all_faces: Sequence['CardFace'],
                                process_choose: Callable[[TC], Any]|None,
                                process_other: Callable[['CardFace'], Any]|None,
                                finder: 'CardFinder|None',
                                may: bool,
                                not_move: bool=False, # will not shuffle
                                range: 'SELECT.RANGE_TYPE'=(1,1),
                                ) -> List[TC]:

        from game.card.face.card_face import CardFace

        legal_faces: List[CardFace] = []
        if finder:
            legal_faces = finder.Checks(all_faces)
        else:
            legal_faces = list(all_faces)

        # if by_find and not legal_faces:
        #     return []

        skip_choose = True
        if range == "All":
            skip_choose = True
        else:
            check_faces_deck: Dict[str, Deck] = {}
            for face in legal_faces:
                face_name = face.name
                if face_name in check_faces_deck:
                    if check_faces_deck[face_name] != face.card.area:
                        skip_choose = False
                        break
                else:
                    check_faces_deck[face_name] = face.card.area
                    if len(check_faces_deck.keys()) > 1:
                        skip_choose = False
                        break

        if skip_choose and legal_faces != []:
            select_face = legal_faces
        else:
            select_face = all_faces

        return_face: List[Any] = []

        if may:
            # Hack
            assert isinstance(range, Tuple)
            x = range[1]
            assert not isinstance(x, str)
            range = (0, x)

        # ⚠ LE SAS DE RECHERCHE COMMENCE ICI (correctif du 21/09/2026,
        # signalement Aghenatak). On releve la zone de CHAQUE candidate AVANT
        # la selection : la selection va sortir la carte choisie de son deck
        # pour la poser dans la zone de traitement, et plus rien ne dira
        # ensuite d'ou elle venait. Voir `EffectInvoker.CloseSearchTransit`.
        zones_avant = {id(face): face.card.area for face in all_faces}

        # We use this to do shuffle
        selector = Select.From(faces=select_face,
                                finder=finder,
                                not_move=not_move,
                                not_shuffle=False,
                                by_search=True,
                                range=range)
        if skip_choose and not may:
            faces = selector.GetAllLegalTargets(by_effect)
            min = selector.selector_range.GetTargetMin(by_effect, faces)
            max = selector.selector_range.GetTargetMax(by_effect, faces)
            faces = faces[:max]
            if not selector.AfterSelectTargets(by_effect, faces, (min, max)):
                # selector.peek = True
                selector.IfSelectTargetFailure(by_effect)
                faces = []
        else:
            faces = player.AskChooseSelect(selector, by_effect)

        # ⚠ ON NOTE LE SAS SUR `by_effect`, L'EFFET DE LA CARTE QUI CHERCHE, et
        # SURTOUT PAS sur l'effet que `AskChooseSelect` vient de fabriquer pour
        # poser la question : celui-la est deja fini, et refermer le sas a SA
        # fin reprendrait la carte AVANT que l'operation appelante ait pu la
        # consommer. Mesure du 21/09/2026 sur `ze014` The Mother of Night, qui
        # enchaine DEUX `Search.PlayerCard` : la premiere carte etait rendue au
        # deck entre les deux, la seconde recherche la retrouvait, et une seule
        # carte finissait posee sous la manigance au lieu de deux.
        for face in faces:
            zone = face.card.area
            if not zone.flags.is_processing or zone.flags.is_revealing:
                continue
            origine = zones_avant.get(id(face))
            if origine is not None and origine.flags.is_deck:
                by_effect.context.search_transit.append((face, origine))

        # FOUILLE FACULTATIVE REFUSEE (correctif du 04/10/2026). Le joueur a vu
        # le contenu du deck puis n'a rien pris : le deck a ete fouille et doit
        # etre melange (Rules Reference v1.8, Search : « If any portion of a
        # deck is searched … shuffle that entire deck »), sinon il connait
        # l'ordre de ses prochaines pioches. `SelectorEnd.DoShuffle` ne melange
        # que le deck d'ou une carte SORT, donc rien ici. Choix de
        # l'utilisateur : « tu as vu le deck ». Une carte prise dans une zone
        # PUBLIQUE (defausse) ne declenche toujours aucun melange : le deck n'a
        # pas eu a etre fouille (lecture « Find », autre choix de l'utilisateur).
        # `not_move` reste respecte : il annonce une recherche qui ne melange pas.
        if may and not faces and not not_move:
            fouilles: List[Deck] = []
            for zone in zones_avant.values():
                if zone.flags.is_deck and not zone.flags.is_face_up and zone not in fouilles:
                    fouilles.append(zone)
            for deck in fouilles:
                if deck.GetSize() > 0:
                    deck.Shuffle(by_effect)

        def process(targets: Sequence['CardFace']) -> None:
            for face in targets:
                if process_choose:
                    process_choose(face) # type: ignore
                nonlocal return_face
                return_face.append(face)

            if process_other:
                for face in all_faces:
                    if face not in targets:
                        process_other(face)
        if faces:
            process(faces)

        return return_face

    ################################################################################
    #
    @staticmethod
    def FindCards(by_effect: 'Effect',
                *,
                range: 'SELECT.RANGE_TYPE'=(1,1),
                finder: 'CardFinder|None'=None,
                name: str|None=None,
                trait: "CardFace.TRAITS|None"=None,
                card_type: Type['TC']|CardFace=CardFace,
                include_in_play: bool=True,
                **kwargs: Unpack['CardFinder.KWArgs'],
                ) -> List['CardFace']:
        from game.operate.search import Search

        player = by_effect.world.GetFirstPlayer()
        faces = Search.SearchForCards(
            by_effect,
            player,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            include_set_aside=True,
            include_in_play=include_in_play,
            # include_victory_display=True,
            finder=CardFinder(
                name=name,
                trait=trait,
                card_type=card_type,
                **kwargs) & finder,
            range=range,
            # by_find=True,
        )
        return faces

