from core import *
from game.card.face import *
from game.effect import *
from game.ability.factory import *
from game.selector import *
from game.player import *

HACK_HERO_ID = '3100'

# ---------------------------------------------------------------------------
# CARTES QU'UN ASPECT IMPOSE AU DECK
#
# L'aspect fan-made VENOMIZED (ekAugust, set 168) est le premier a en avoir
# besoin. Son insert, mot pour mot :
#
#   « After you have built your deck, if you have chosen to include Venomized
#     (black) aspect cards into your deck, you will need to randomly include a
#     certain number of cards from the Venomized Weakness set into your deck.
#     The number of required cards depends on the TOTAL RESOURCE COST of all
#     Venomized (black) aspect cards in your deck. You can randomly get
#     multiple copies of the same Venomized Weakness card. »
#
#     Cout total  1-20 -> 1 carte Weakness
#     Cout total 21-40 -> 2 cartes Weakness
#
# ⚠ LE TABLEAU DE L'AUTEUR S'ARRETE A 40, et un deck de 50 cartes peut
# depasser ce total : le cas est atteignable. On garde alors la DERNIERE
# tranche (2 cartes) plutot que d'extrapoler « une de plus par tranche de 20 »,
# qui serait une regle INVENTEE. Choix volontaire, a confirmer avec l'auteur.
#
# ⚠ CES CARTES NE COMPTENT PAS DANS LA TAILLE DU DECK, et il n'y a rien a
# soustraire nulle part : elles sont ajoutees ICI, apres que l'editeur a valide
# les 40-50 cartes. C'est exactement ce que dit le mot-cle `weakness`
# (docs/reference/mots-cles/weakness.md).
#
# ⚠ LE TIRAGE PASSE PAR `Random.RandomChoice`, le generateur SEME du moteur, et
# JAMAIS par le module `random` : une partie rejouee a la meme graine doit
# tirer les memes faiblesses, sans quoi les rejeux et le multijoueur divergent.
# Le tirage est AVEC REMISE, le texte autorisant les doublons.
#
# La regle est en DONNEE et non en dur dans la logique : un second aspect qui
# imposerait des cartes n'aurait qu'une ligne a ajouter ici.
CARTES_IMPOSEES_PAR_ASPECT = (
    {
        "aspect": "Venomized",
        "set_impose": "Venomized Weakness",
        # (cout maximal de la tranche, nombre de cartes). La derniere tranche
        # vaut aussi au-dela de son plafond.
        "tranches": ((20, 1), (40, 2)),
    },
)

class PlayerSetup:

    def __init__(self, player: 'Player') -> None:
        self.player = player

    def SetupPlayerAbility(self, hero: 'CardFace'):
        from game.message import Message
        player = self.player

        def register_change_form():
            from game.ability import AbilityType
            from game.card.face.card_type import AlterEgo
            from game.card.face.card_type import Hero

            def add_change_form_effect(identity: 'AlterEgo|Hero', identities: List['AlterEgo|Hero']):

                def check_is_same_card(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
                    this = effect.this
                    if len(this.card.back_faces) == 1:
                        return True
                    # if this.paper.card_id in ["29001a", "29001b", "29002a", "29002b", "29003a", "29003b"]:
                    return face.paper.card_id[:-1] == this.card.face.paper.card_id[:-1]

                def invoke_change_form(to_face: 'AlterEgo|Hero', effect: 'Effect'):
                    initiator = effect.GetInitiator()
                    initiator.has_change_form = True
                    initiator.GetIdentity().ChangeToFace(to_face, effect)

                faces = identities[:]
                faces.remove(identity)

                if not identity.paper.card_id.startswith(HACK_HERO_ID) and len(identities) > 2:
                    faces = [x for x in faces if x.paper.card_id[:-1] == identity.paper.card_id[:-1]]

                for face in faces:
                    def register_change_to(face: 'AlterEgo|Hero', name: str):
                        identity.effect.Registers(
                            AbilityFactory.WhenInYourPlayTurn(
                                AbilityType.PlayTurnOption,
                                lambda effect, message:
                                    invoke_change_form(face, effect),
                                conditions=[
                                    lambda effect, message:
                                        not effect.GetInitiator().has_change_form and \
                                        identity.card.face != face and \
                                        identity.IsInPlay(is_same_face=True),
                                    check_is_same_card,
                                    # AJOUT (25/09/2026, pack custom conan) : une face
                                    # marquee `hors_pile_identite` (King Conan mis de cote
                                    # au Setup, puis Thief/Barbarian/alter-ego retires de la
                                    # partie au couronnement) n'est plus proposee au
                                    # changement volontaire. Filtrer ICI, a l'offre, et non
                                    # annuler a la resolution : un refus apres coup couterait
                                    # au joueur son changement du tour (lecon Moon Knight/TAH).
                                    # AJOUT PUR : aucune face existante ne porte ce drapeau.
                                    lambda effect, message:
                                        not getattr(face, 'hors_pile_identite', False),
                                ],
                            ).SetFuncName("Change Form").SetName(name).NoOutOfPlayLimit()
                        )

                    name = ""
                    if len(faces) > 1:
                        if face.name in [x.name for x in identities if x != face]:
                            # Deux formes du meme nom (Ant-Man Geant / Minuscule) : seuls les traits qui DISTINGUENT
                            # cette forme des autres du meme nom (24/10/2026 : « Change To AVENGER GIANT » au lieu de
                            # « Change To GIANT ») ; aucun trait propre -> tous, comme avant.
                            communs = [x.traits_str.split() for x in identities if x != face and x.name == face.name]
                            propres = [mot for mot in face.traits_str.split() if not all(mot in autres for autres in communs)]
                            name = " ".join(propres) if propres else face.traits_str
                            name = "Change To " + name.strip()
                        else:
                            name = "Change To " + face.name
                    register_change_to(face, name)

            identities: Set['AlterEgo|Hero'] = set([])
            for face in player.area_hero.GetAll() + [hero.card.face]:
                for identity in [face] + face.card.back_faces:
                    if isinstance(identity, AlterEgo|Hero):
                        identities.add(identity)
            # ⚠ UN TRI TOTAL, PAS `sorted(identities)` SEUL (07/10/2026). Les formes d'un heros a plusieurs
            # formes (Conan : cn001a a cn001e) sont les FACES d'UNE SEULE carte : `CardFace.__lt__` compare
            # `card.object_id`, donc toutes egales, et le tri laissait l'ordre d'iteration du `set` (des objets
            # haches par adresse memoire). L'ordre d'enregistrement des « Change To ... », donc leurs
            # `object_id`, donc l'ORDRE DES BOUTONS, changeait d'un processus a l'autre : meme graine, memes
            # reponses, parties differentes (mesure : Conan, 3 issues pour 1 graine dans le navigateur ;
            # Invisible Woman). `paper.card_id` departage deux faces de la meme carte, de facon stable.
            identities_triees = sorted(identities, key=lambda x: (x.card.object_id, x.paper.card_id))
            for identity in identities_triees:
                add_change_form_effect(identity, identities_triees)

        def register_ask_effect():
            if player.world.GetPlayerNum() > 1:
                # In turn
                def invoke_ask(effect: 'Effect', message: 'Message.WhenPlayerInTurn'):
                    # v1.5
                    # Ask another player to trigger an “Action” ability on
                    # a card in play they control or on an event card they
                    # might have in hand. The other player then decides
                    # whether or not to trigger the ability. (Another player
                    # may offer to use an action during the active player’s
                    # turn, as well.)
                    # v1.6
                    # Ask another player to trigger any “Action” ability
                    # that player could trigger on their own turn. The other
                    # player then decides whether or not to trigger the
                    # ability. (Another player may offer to use an action
                    # during the active player’s turn, as well.)
                    def get_player_can_asked_effects(player: 'Player') -> List['Effect']:
                        return [
                            x
                            for x in 
                            effect.world.event_manager.FindEffectsList("Optional", Message.WhenPlayerInTurn, TimingPriority.Normal)
                            if
                            x.is_action
                        ]

                    with effect.targets[0].GetControlByPlayer() as player:
                        turn_message = Message.WhenPlayerLikeInTurn(player, effect)
                        turn_message.Send()
                        player.ChooseEffects(get_player_can_asked_effects(player), turn_message)

                hero.effect.Registers(
                    AbilityFactory.WhenInYourPlayTurn(
                        AbilityType.Ask,
                        lambda effect, message:
                            invoke_ask(effect, message)
                    ).SetFuncName("Ask")
                    .SetTarget("OtherPlayers")
                    .NoOutOfPlayLimit()
                )

                # Defense
                def get_player_can_def_effects(player: 'Player') -> List['Effect']:
                    effects: List[Effect] = []
                    for face in player.GetControlCharacters():
                        for face_effect in face.effects:
                            if face_effect.ability.IsFunction("DEF") and face.CanExhaust():
                                effects.append(face_effect)
                            elif face_effect.ability.IsLabel('defense'):
                                effects.append(face_effect)
                    return effects

                def invoke_defense(effect: 'Effect', message: 'Message.WhenUnitBeingAttack'):
                    with effect.targets[0].GetControlByPlayer() as player:
                        bing_atk_message = Message.WhenUnitLikeBeingAttack(player.GetIdentity(), message.would_atk_message, message)
                        bing_atk_message.Send()
                        player.ChooseEffects(get_player_can_def_effects(player), bing_atk_message)

                def on_field_other_players(effect: 'Effect') -> Sequence['AlterEgo|Hero']:
                    from game.card.face.card_type import AlterEgo
                    from game.card.face.card_type import Hero

                    units = Select.From("OtherPlayers").GetAllLegalTargets(effect)
                    return [x for x in units if get_player_can_def_effects(x.GetControlByPlayer()) != [] and isinstance(x, AlterEgo|Hero)]

                hero.effect.Registers(
                    Ability(
                        AbilityType.Ask,
                        Message.WhenUnitBeingAttack,
                        [
                            lambda effect, message:
                                message.defender == None and \
                                # not Enemy.IsType(message.trigger) and \
                                # effect.initiator == message.trigger.GetOwner(),
                                effect.initiator == message.trigger.card.GetController(),
                        ],
                        invoke_defense
                        # If the attacked player does not defend, any other player may defend against the attack by exhausting their hero or an ally they control
                    ).SetFuncName("Ask")
                    .SetTarget(on_field_other_players)
                    .NoOutOfPlayLimit()
                )

                # Resoruce
                # def invoke_res(effect: 'Effect', message: 'Send.WhenPlayerPayingResources'):
                #     player = effect.targets[0].GetPlayer()
                #     paying_message = Send.WhenPlayerLikePayingResources(player, message.for_effect)
                #     player.ChooseEffects(player.GetPayEffects(), paying_message)

                # hero.RegisterEffect(
                #     Ability(
                #         AbilityType.Ask,
                #         Send.WhenPlayerPayingResources,
                #         lambda effect, message:
                #             effect.GetInitiator() == message.to_player,
                #         do_res
                #     ).SetSubType('Ask')
                #     .SetTarget2(Select.OnFieldOtherPlayers).SetActiveOutOfPlay()
                # )

        register_change_form()
        register_ask_effect()

    @staticmethod
    def CartesImposeesParLesAspects(card_ids: Sequence[str], world: 'World') -> List[str]:
        """Les card_id que les aspects du deck AJOUTENT d'office.

        Voir `CARTES_IMPOSEES_PAR_ASPECT` en tete de fichier pour la regle et
        ses pieges. Rend une liste vide quand aucun aspect concerne n'est
        represente, ce qui est le cas de tous les decks officiels.
        """
        from cards.database import CardsDB
        from engine.lib.random import Random

        imposees: List[str] = []
        for regle in CARTES_IMPOSEES_PAR_ASPECT:
            # 1. Le cout cumule des cartes de CET aspect presentes dans le deck.
            #    ⚠ Un cout « X » n'est pas un nombre : il vaut 0 ici. C'est le
            #    seul choix sur : X est decide en jouant la carte, pas en
            #    construisant le deck, et l'auteur parle du cout IMPRIME.
            cout = 0
            for card_id in card_ids:
                paper = CardsDB.papers.get(str(card_id).split(',')[0])
                if paper is None:
                    continue
                classes = [c.strip() for c in (paper.desc.get("Class") or "").split(';')]
                if regle["aspect"] not in classes:
                    continue
                brut = str(paper.desc.get("Cost") or "").strip()
                if brut.isdigit():
                    cout += int(brut)
            if cout <= 0:
                continue

            # 2. La tranche. La derniere vaut aussi au-dela de son plafond.
            combien = regle["tranches"][-1][1]
            for plafond, nombre in regle["tranches"]:
                if cout <= plafond:
                    combien = nombre
                    break

            # 3. Le tirage, AVEC REMISE, dans le set impose. On lit le set dans
            #    le catalogue plutot que d'ecrire les card_id en dur : une
            #    troisieme carte de faiblesse entrerait dans le tirage sans
            #    toucher a ce code.
            pioche = sorted(cid for cid, paper in CardsDB.papers.items()
                            if paper.set_name == regle["set_impose"])
            if not pioche:
                continue
            for _ in range(combien):
                imposees.append(str(Random.RandomChoice(pioche)))
        return imposees

    @staticmethod
    def EstUnPath(card_id: str) -> bool:
        """Le card_id designe-t-il une carte de type PATH (catalogue, `paper.type`) ?"""
        from cards.database import CardsDB
        paper = CardsDB.papers.get(str(card_id).split(',')[0])
        return paper is not None and paper.type == "Path"

    @staticmethod
    def MettreLesPathsDeCoteEtEnJeuAuSetup(player: 'Player', hero_card: 'CardFace', chemins: Sequence[str]) -> None:
        """Fabrique chaque Path dans la reserve du joueur (`additional_discard_pile`, comme les cartes
        mises de cote) et le met en jeu SOUS SON CONTROLE quand le Setup de la partie commence."""
        if not chemins:
            return
        from game.card.factory import CardFactory
        from game.effect.rule import GameRule
        from game.operate.run_at import RunAt
        from game.card.face.card_type import Path

        cartes = CardFactory.GenerateCards(chemins, player.additional_discard_pile, player.world)
        for carte in cartes:
            def mettre_en_jeu(carte=carte):
                for face in carte.printed_faces:
                    if Path.IsType(face):
                        face.PutIntoPlay(player, GameRule(hero_card), under_control=True)
            RunAt.WhenGameBeginSetup(hero_card, mettre_en_jeu)

    def SelectIdentity(self, name: str, hero_names: Sequence[str], hero_deck: Sequence[str], obligations: Sequence[str], nemesis_set: Sequence[str], player_deck: Sequence[str]) -> None:
        from game.effect.rule import GameRule
        from game.message import Message
        from game.card.factory import CardFactory

        player = self.player

        player.hero_name = name

        def move_b_to_front(s: str):
            parts = s.split(',')
            b_part = [part for part in parts if part.endswith('b')]
            other_parts = [part for part in parts if not part.endswith('b')]
            result = b_part + other_parts
            return ','.join(result)
        if hero_names[0].startswith(HACK_HERO_ID):
            hero_names = ["31002a,31002b"]
        else:
            hero_names = [move_b_to_front(s) for s in hero_names]
        CardFactory.GenerateCards(hero_names, player.set_aside_deck, player.world)

        hero_card = player.set_aside_deck.GetAll()[0]
        rule = GameRule(hero_card)
        hero_card.PutIntoPlay(player, rule)

        # hero_card.Reset(False)
        # hero_card.ResetHealth(GameRule(hero_card))
        # We do this by effect

        if player.world.is_game_over:
            return

        # CardFactory.GenerateCards(set_aside, player.set_aside_deck, player.world)
        select_message = Message.WhenPlayerSelectHero(player, player.GetIdentity())
        select_message.Send()

        # After set aside is create for `HACK_HERO_ID`
        if hero_card.card.back_faces:
            # hero_card.ChangeToForm(AlterEgo, GameRule(hero_card))
            self.SetupPlayerAbility(hero_card)

        # ~~3. Select First Player~~
        # We don't need this

        # 4. Set Aside Obligation
        player.set_aside_obligations = []
        player.set_aside_obligations += CardFactory.GenerateCards(obligations, player.set_aside_nemesis_sets, player.world)

        # 5. Set Aside Nemesis Sets
        cartes_nemesis = CardFactory.GenerateCards(nemesis_set, player.set_aside_nemesis_sets, player.world)

        # CORRECTIF (02/09/2026) : marquer les cartes du set nemesis avec le
        # joueur a qui elles appartiennent.
        #
        # Pourquoi. `CardEncounter.IsNemesis` decidait jusqu'ici en comparant
        # des NOMS DE SET : la carte devait porter un `set_name` finissant par
        # « Nemesis » et egal a celui du heros. Cela marche pour les heros
        # officiels, dont le set nemesis porte leur nom, et CASSE des qu'un
        # deck EMPRUNTE le set nemesis d'un autre — ce que font sans arret les
        # packs fan-made, dont les auteurs ne livrent pas toujours de nemesis.
        # Constate le 02/09/2026 : Viv Vision emprunte le modulaire officiel
        # Zzzax (set_name « Zzzax », qui ne finit pas par « Nemesis »), et
        # `01190` Shadow of the Past — carte du set STANDARD, donc presente a
        # CHAQUE partie — ne mettait jamais le sbire en jeu : il partait
        # melange au deck rencontre et la traitrise gagnait surge. Prouve par
        # sonde, avec temoin (Spider-Man / Vulture entre bien en jeu).
        #
        # Le marqueur suit la carte partout, ce qu'une regle « la carte est
        # dans la reserve nemesis » ne ferait pas : `49022` Face the Past
        # (Magneto) cherche le sbire nemesis jusque dans le deck rencontre.
        for carte in cartes_nemesis:
            for face in carte.printed_faces:
                face.nemesis_of_player = player

        # CORRECTIF (04/10/2026) : le set contient-il un sbire MARQUE
        # « Nemesis » ? Si oui, lui seul est le sbire nemesis (voir
        # `IsNemesis`). Signale en jeu sur Hercules : Face the Past mettait en
        # jeu Ares ET la Lernean Hydra, second sbire de son set.
        from game.card.face.card_type import Minion
        player.set_nemesis_a_un_sbire_marque = any(
            Minion.IsType(face) and getattr(face, "nemesis", "")
            for carte in cartes_nemesis for face in carte.printed_faces
        )

        # 6. Shuffle Player Decks
        if player.world.rule.create_player_deck_first:
            player_hero_deck = list(player_deck) + list(hero_deck)
        else:
            player_hero_deck = list(hero_deck) + list(player_deck)
        # Les cartes qu'un aspect IMPOSE (voir CARTES_IMPOSEES_PAR_ASPECT) :
        # ajoutees AVANT la creation des cartes, elles sont donc melangees au
        # deck comme n'importe quelle autre. Liste vide pour tout deck qui ne
        # contient aucun aspect concerne.
        player_hero_deck += PlayerSetup.CartesImposeesParLesAspects(player_hero_deck, player.world)

        # AJOUT (17/10/2026, pack TMNT Shinobi, Inkwire) : LE PATH CHOISI AU DECK-BUILDING.
        # « During deck-building, select a Shinobi Path card [...] Make sure to put your Path card
        # into play during setup. » Un Path (type imprime PATH, card_type/path.py) n'est JAMAIS
        # melange au deck : il est MIS DE COTE puis mis en jeu au Setup (etape « Set Up », avant la
        # pioche de depart, donc le « -1 hand size » vaut deja pour la main de depart), pour N'IMPORTE
        # QUEL heros. Le Path propre a un heros (Sosaiken de Jennika, `tj011`) n'est pas concerne : il
        # ne figure pas dans ces listes, `BeginGameWithSetAside` de tj001b le gere. Voir
        # docs/reference/mots-cles/shinobi.md, §Path.
        chemins = [c for c in player_hero_deck if PlayerSetup.EstUnPath(c)]
        if chemins:
            player_hero_deck = [c for c in player_hero_deck if not PlayerSetup.EstUnPath(c)]
        CardFactory.GenerateCards(player_hero_deck, player.player_deck, player.world)
        PlayerSetup.MettreLesPathsDeCoteEtEnJeuAuSetup(player, hero_card, chemins)

        player.stat.ResetPlayedRevealedCards()
        player.flag.Reset()
        player.res_pool.Reset()

        Message.WhenDeckCreated_Text(player.player_deck)
        # rule = GameRule(player.GetIdentity())
        player.player_deck.Shuffle(rule)

        if player.world.is_game_over:
            return

        selected_message = Message.AfterPlayerSelectHeroEnd(player, player.GetIdentity())
        selected_message.Send()

