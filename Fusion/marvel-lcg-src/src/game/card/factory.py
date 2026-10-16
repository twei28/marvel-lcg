from core import *

from game.card.face import *
from game.card import *
from game.deck import *
from game.player import *
from game.ability import *
from game.message import *

from cards.paper import Paper
from engine.lib import Json
from engine.file import FileManager
from cards.database import CardsDB
from game.world import *

class CardFactory:

    @staticmethod
    # names ['01001', '01002']
    def GenerateCards(names: Sequence[str], deck: 'Deck|None', world: 'World', *, ui_render: bool=True) -> Sequence['Card']:
        cards: List['Card'] = []
        for name in names:
            if name != '':
                card = CardFactory.GenerateCard(name, deck, world, ui_render=ui_render)
                cards.append(card)
        return cards

    @staticmethod
    def GenerateCard(name: str, deck: 'Deck|None', world: 'World', ui_render: bool=True) -> 'Card':
        from game.card import Card

        papers = CardFactory.FindCardPapers(name)

        faces: List['CardFace'] = []

        def create_linked_faces(paper: Paper):
            card_ids = CardsDB.FindLikedPapers(paper)
            if card_ids != []:
                CardFactory.GenerateCards(card_ids, world.aside_deck, world)

        for paper in papers:
            faces.append(CardFactory.CreateFace(paper, world))
            create_linked_faces(paper)

        if deck and deck.GetOwner():
            owner = deck.GetOwner()
        else:
            owner = world.GetScenario()

        card = Card(owner, *faces, world=world)

        if not deck:
            deck = world.area_removed

        CardFactory.CardInstantiate(card, deck, owner, world)

        if ui_render and not world.is_initializing:
            Message.AfterCardsGenerated_Text(card)
        return card

    ################################################################################
    #
    @staticmethod
    def FindCardPapers(names: str) -> Sequence['Paper']:
        papers: List['Paper'] = []
        for name in names.split(','):
            papers.append(CardsDB.FindCardPaper(name))
        return papers

    ################################################################################
    #
    @staticmethod
    def CreateFace(paper: 'Paper', world: 'World') -> 'CardFace':
        from game.card.face.base import ClassCard
        from game.card.face.card_type import Ally
        from game.card.face.card_type import Hero
        from game.card.face.card_type import AlterEgo
        from game.card.face.card_type import Event
        from game.card.face.card_type import Resource
        from game.card.face.card_type import Path

        face = paper.GetType()(paper)
        player_num = world.GetPlayerNumIcon()
        face.Initialize(player_num)
        face.ability.Add(*CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name))
        face.ability.Add(*face.GetAbilities())

        # Check abilities
        from build import Build
        if not Build.release:
            if ClassCard.IsType(face):
                # AJOUT (16/10/2026, pack jennika) : une Voie (Path) ne se joue jamais depuis la
                # main (Setup d'une identite) : pas de capacite `Play`, comme une Resource.
                if type(face) != Resource and type(face) != Path:
                    if type(face) == Ally:
                        # CORRECTIF (02/09/2026) : `dd003` Doombot, pack custom
                        # doctor_doom. Meme motif que les evenements ci-dessous,
                        # mais cote ALLIE : la carte porte DEUX capacites
                        # « Play » — `CanPlayThisAllyCard()` pour la pose
                        # normale, et l'Interruption imprimee « play Doombot
                        # from your hand and declare it the defender », qui est
                        # elle aussi `.SetPlay()`. Sans cette declaration, le
                        # deck `doctor_doom` ne monte AUCUNE partie (assert au
                        # setup, invisible pour test_cards). Trouve par la passe
                        # complete des 112 decks le 02/09/2026.
                        if face.paper.card_id in ["45031", "dd003"]:
                            pass
                        else:
                            assert len(face.ability.Find(func_name="Play")) == 1, f"{face.paper.card_id=}"
                    elif type(face) == Event:
                        play_count = len(face.ability.Find(func_name="Play"))
                        if play_count == 1:
                            pass
                        elif face.paper.card_id in ["30004", "26008", "18015", "42003", "42004", "27003", "13003", "13006", "46009",
                                                    # CORRECTIF : evenements « Choose one » des packs custom,
                                                    # qui portent DEUX capacites de jeu comme 30004 et 13006.
                                                    # Sans eux, la creation de partie du heros PLANTE
                                                    # (constate le 4/8/2026 en montant les 88 decks).
                                                    "ht009",   # Radiate (human_torch)
                                                    "ra004",   # Hammer Swing (rainy)
                                                    "sr006",   # spider_man_rainy
                                                    "mk008",   # Fight or Foil (moon_knight)
                                                    "mk010",   # Where'd He Go? (moon_knight)
                                                    "lj024",   # Wet Slobbering Kiss (lockjaw)
                                                    # CORRECTIF (29/08/2026) : carte OFFICIELLE du pack
                                                    # Jessica Jones (sorti le 21/08/2026). Elle porte
                                                    # deux capacites de jeu DISTINCTES, une en alter-ego
                                                    # (chercher un player side scheme) et une en heros
                                                    # (en retirer 3 menaces). Sans cette declaration,
                                                    # le deck jessica_jones ne montait pas.
                                                    "61019",   # Strategy Session (jj)
                                                    # CORRECTIF (30/08/2026) : Quick Draw, pack
                                                    # custom kate_bishop. Motif IDENTIQUE a
                                                    # 61019 : une AlterEgoAction (« Flip to hero
                                                    # form and ready your hero ») et une
                                                    # HeroAction (« Ready your hero and place 2
                                                    # arrow counters on Kate's Bow »), les deux
                                                    # `.SetPlay()`. Le module n'a aucun defaut ;
                                                    # sans cette declaration le deck
                                                    # kate_bishop ne montait pas (assert au
                                                    # setup, invisible pour test_cards).
                                                    "kb005",   # Quick Draw (kate_bishop)
                                                    # CORRECTIF (31/08/2026) : Talk About Armed
                                                    # Assault, pack custom venompool. Ce n'est PAS
                                                    # un « Choose one » : c'est UNE capacite dont
                                                    # la portee change (« 4 damage divided among
                                                    # enemies, 6 instead if True Form is in
                                                    # play »). `range` etant fige a la
                                                    # construction, il faut deux capacites
                                                    # mutuellement exclusives — modele 13006 Wasp
                                                    # Sting, deja dans cette liste pour la meme
                                                    # raison (formes GIANT / TINY). Sans cette
                                                    # declaration, le deck venompool ne monte pas,
                                                    # et test_cards ne le voit pas.
                                                    "vp003",   # Talk About Armed Assault (venompool)
                                                    # CORRECTIF (31/08/2026) : Heven's Fury, pack
                                                    # custom angela. Meme motif que vp003 : « Deal 7
                                                    # damage to an enemy. You MAY exhaust a WEAPON.
                                                    # If you do, divide the damage among enemies
                                                    # INSTEAD. » `range` etant fige a la
                                                    # construction, les deux portees demandent deux
                                                    # capacites, et le « you may » devient le choix
                                                    # entre elles.
                                                    "an003",   # Heven's Fury (angela)
                                                    # CORRECTIF (02/09/2026) : Solar Beam, pack
                                                    # custom viv_vision. Meme carte, meme nom et
                                                    # meme structure que son HOMONYME OFFICIEL
                                                    # 26008, deja en tete de cette liste : deux
                                                    # Hero Action distinctes, l'une (attack),
                                                    # l'autre (thwart), les deux `.SetPlay()`.
                                                    # Sans cette declaration le deck viv_vision
                                                    # ne monte pas, et test_cards ne le voit pas.
                                                    "vv005",   # Solar Beam (viv_vision)
                                                    # CORRECTIF (03/09/2026) : To Arms!, pack custom
                                                    # lady_sif. Meme motif que 61019 Strategy Session
                                                    # et kb005 Quick Draw : une AlterEgoAction
                                                    # (« Change to hero form. You may spend a
                                                    # resource to ready your hero. ») et une
                                                    # HeroAction (« Search your deck and discard pile
                                                    # for a WEAPON upgrade »), les deux `.SetPlay()`.
                                                    # ⚠ LE DECK lady_sif NE MONTAIT PLUS AUCUNE
                                                    # PARTIE depuis son portage du 03/09/2026 :
                                                    # AssertionError au setup, invisible pour
                                                    # `test_cards`, `test_capacites` (qui ne monte
                                                    # que les cas ecrits) et `substituer_pack`.
                                                    # Seul `verifier_tous_les_decks` le voit, et il
                                                    # n'avait pas ete relance apres ce pack.
                                                    "ls005",   # To Arms! (lady_sif)
                                                    # CORRECTIF (05/09/2026) : Hammer Twirl, pack
                                                    # custom beta_ray_bill. « exhaust Stormbreaker
                                                    # OR spend 1 resource of any type » : deux
                                                    # COUTS pour le meme effet, et un cout est fige
                                                    # a la construction. Le « or » devient donc le
                                                    # choix entre deux Hero Interrupt (defense),
                                                    # les deux `.SetPlay()`. Declaree AVANT
                                                    # d'ecrire le module, la leçon ls005 ayant
                                                    # coute une journee de deck injouable.
                                                    "br004",   # Hammer Twirl (beta_ray_bill)
                                                    # CORRECTIF (09/09/2026) : pack custom
                                                    # iron_patriot (Neptune). DEUX cartes y
                                                    # portent deux capacites de jeu, et elles
                                                    # sont DECLAREES AVANT d'ecrire leur module,
                                                    # comme le conseille la lecon ls005 juste
                                                    # au-dessus.
                                                    #  ip010 Deceptive Guard : une Interruption
                                                    #    d'alter ego (une manigance retire de la
                                                    #    menace au lieu d'en poser) ET une
                                                    #    Interruption de heros (defense) — deux
                                                    #    formes, deux fenetres.
                                                    #  ip011 Foreboding Influence : une Action
                                                    #    d'alter ego (remelanger la defausse
                                                    #    REGISTERED) ET une Reponse de heros
                                                    #    (recruter le sbire attaque).
                                                    "ip010",   # Deceptive Guard (iron_patriot)
                                                    "ip011"]:  # Foreboding Influence (iron_patriot)
                            assert play_count == 2, f"{face.paper.card_id=}"
                        elif face.paper.card_id in ["09032", "09033", "09034", "09035", "09036",
                                                    # CORRECTIF : Photographic Reflexes n'a aucune
                                                    # capacite de jeu, elle se DEFAUSSE pour jouer un
                                                    # evenement glisse sous Echo. La partie plantait.
                                                    "60040a", "60040b", "60040c"]:
                            assert play_count == 0, f"{face.paper.card_id=}"
                        else:
                            assert False, f"{face.paper.card_id=}"
                    else:
                        assert len(face.ability.Find(func_name="Play")) == 1, f"{face.paper.card_id=}"

                if face.printed_resource_internal.val > 0:
                    if Resource.IsType(face):
                        assert len(face.ability.Find(func_name="CheckPay")) == 1, f"{face.paper.card_id=}"
                    else:
                        assert len(face.ability.Find(func_name="CheckPay")) >= 1, f"{face.paper.card_id=}"
            if Ally.IsType(face):
                assert len(face.ability.Find(func_name="ATK")) == 1, f"{face.paper.card_id=}"
                assert len(face.ability.Find(func_name="THW")) == 1, f"{face.paper.card_id=}"
                assert len(face.ability.Find(func_name="DEF")) == 1, f"{face.paper.card_id=}"
            if Hero.IsType(face):
                assert len(face.ability.Find(func_name="ATK")) == 1, f"{face.paper.card_id=}"
                assert len(face.ability.Find(func_name="THW")) == 1, f"{face.paper.card_id=}"
                assert len(face.ability.Find(func_name="DEF")) == 1, f"{face.paper.card_id=}"
                pass
            if AlterEgo.IsType(face):
                assert len(face.ability.Find(func_name="REC")) == 1, f"{face.paper.card_id=}"
            # if Enemy.IsType(face):
            #     assert len(face.FindAbility('Scheme')) == 1, f"{face.paper.card_id=}"
        return face

    @staticmethod
    def CardInstantiate(card: 'Card', area: 'Deck', owner: 'Player|Scenario', world: 'World') -> None:
        card.area = area
        card.game_area = world.GetFirstGameArea()
        card.bind_discard_pile = area.bind_discard_pile
        area.Append(card)

        CardFactory.CardRegisterEffects(card)

    @staticmethod
    def CardRegisterEffects(card: 'Card'):
        CardFactory.FaceRegisterEffects(card.face)
        for face in card.back_faces:
            CardFactory.FaceRegisterEffects(face)
        # from game.message import Message
        # message = Message.WhenCardBeCreated(card.face)
        # message.Send()

    @staticmethod
    def FaceRegisterEffects(face: 'CardFace'):
        for ability in face.ability.abilities:
            face.effect.Registers(ability)

    @staticmethod
    # return like ['01001', '01002']
    def LoadEncounterSet(encounter_set: str) -> List[str]:
        from game.scene.replay.encounter_set import EncounterSetDescriptor
        file_path = FileManager.FindJsonPath('EncounterSet', encounter_set)
        if file_path:
            return Json.LoadAs(file_path, EncounterSetDescriptor).encounters
        else:
            return []

