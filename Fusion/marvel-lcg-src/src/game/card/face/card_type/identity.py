from core import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from game.player import *
from cards.paper import Paper
from game.element.damage_property import DamageProperty

class Identity(Friend, HasHandSize, PlayerCard):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        resources_abilities = self.ability.Find(func_name="CanGenerateResources")
        assert len(resources_abilities) <= 1
        if resources_abilities and not self.ability.Find(func_name="DoGenerateResources"):
            name = resources_abilities[0].name
            # "Sync Ratio"
            abilities.append(AbilityFactory.DoGenerateResources(
                resources_abilities[0].second_type, # This function is for select, so it cannot be like a Temp
                "This",
                # `ex_operation` etait perdu ici alors que `CardPlayer` le
                # transmet (card_player.py). Toute identite dont la capacite
                # Resource a un second effet (« ... puis redressez cette carte »)
                # perdait donc cette moitie en silence : Sue Storm iw001b et
                # Reed Richards mf001b ne se redressaient jamais.
                ex_operation=resources_abilities[0].generate_resources_ex_operation
            ).SetName(name))
        return abilities + super().GetAbilities()

    @override
    def OnBeDefeated(self, would_defeated_message: 'Message.WhenSchemeWouldBeDefeated|Message.WhenUnitWouldBeDefeated', *, as_asset: bool, ignore_when_defeated: bool):
        self.GetControlByPlayer().Eliminate(would_defeated_message.by_effect)
        return super().OnBeDefeated(would_defeated_message, as_asset=as_asset, ignore_when_defeated=ignore_when_defeated)

    @override
    def GetInfoDict(self) -> Dict[str, int]:
        player = self.GetControlByPlayer()
        return super().GetInfoDict() | {
            'ally_limit': player.limit_ally.Get(),
            'curr_ally_limit': player.limit_ally.curr_ally,
            'restricted_limit': player.limit_restricted.Get(),
            'curr_restricted_limit': player.limit_restricted.curr_restricted,
        }

    @override
    def OnPutIntoPlay(self, message: 'Message.WhenCardPutIntoPlay') -> 'bool':
        from game.operate.faces import Faces
        if Faces.MoveAllTo([self], message.GetToPlayer().area_hero, message.by_effect):
            return super().OnPutIntoPlay(message)
        else:
            return False

    ################################################################################
    #
    def GetAlterEgoFace(self) -> 'AlterEgo':
        for face in [self] + self.card.back_faces:
            if AlterEgo.IsType(face):
                return face
        assert False, f"{self=}"

    def GetHeroFace(self) -> 'Hero':
        for face in [self] + self.card.back_faces:
            if Hero.IsType(face):
                return face
        assert False, f"{self=}"

    # La face heros de cette identite, ou None si sa carte n'en porte pas.
    #
    # ⚠ Toutes les identites n'ont PAS leur heros au dos : Peni Parker (31002a)
    # est un alter ego dont le heros, SP//dr Suit (31001a), est une carte A
    # PART. `GetHeroFace` pose un assert dans ce cas, ce qui a tue toute
    # partie avec SP//dr du 01/09 au 11/09/2026 (le rendu de chaque ennemi
    # l'appelait, voir `Enemy.GetHoldingHeroPlayerNumber`). Un code qui se
    # demande « ce joueur a-t-il un heros qui... » doit passer par ici.
    def FindHeroFace(self) -> 'Hero|None':
        for face in [self] + self.card.back_faces:
            if Hero.IsType(face):
                return face
        return None

    ################################################################################
    #
    def ChangeToFace(self, card_face: 'AlterEgo|Hero', by_effect: 'Effect') -> bool:
        return self.DefaultChangeToFace(card_face, by_effect)

    def ChangeToForm(self, to_type: CardFinder|Type['AlterEgo|Hero'], by_effect: 'Effect'):
        if not isinstance(to_type, CardFinder):
            finder = CardFinder(card_type=to_type)
        else:
            finder = to_type

        return self.DefaultChangeToForm(finder, by_effect)

    def ChangeToOtherIdentityForm(self, by_effect: 'Effect'):
        if Hero.IsType(self):
            to_form = AlterEgo
        else:
            to_form = Hero
        self.ChangeToForm(to_form, by_effect)

    def ChangeToOtherHeroForm(self, by_effect: 'Effect'):
        for face in self.card.back_faces:
            # AJOUT (25/09/2026, pack custom conan) : ignorer une face mise de
            # cote ou retiree de la partie (drapeau `hors_pile_identite`, voir
            # player_setup.py). Aucune autre face ne porte ce drapeau.
            if getattr(face, 'hors_pile_identite', False):
                continue
            if Hero.IsType(face) and face != self:
                self.ChangeToFace(face, by_effect)
                return
        assert False, f"{self=} {by_effect=}"

    def ChangeToOtherForm(self, by_effect: 'Effect'):
        player = self.GetControlByPlayer()
        # AJOUT (25/09/2026, pack custom conan) : meme filtre `hors_pile_identite`.
        face = player.AskChooseOneText([x.name for x in self.card.back_faces
                                        if not getattr(x, 'hors_pile_identite', False)])
        self.ChangeToForm(CardFinder(name=face), by_effect)

    def SetActive(self, by_effect: 'Effect'):
        # En mode competitif chaque camp a SON jeton de premier joueur
        # (mc56 p.16) : donner le jeton a un joueur ne le retire donc qu'aux
        # joueurs de son propre camp. Hors competitif, `GetTeamOfPlayer` rend 0
        # pour tout le monde et la boucle est celle d'avant.
        world = self.card.world
        camp = world.GetTeamOfPlayer(self.GetOwnerPlayer())
        autres = [x for x in world.const_players if world.GetTeamOfPlayer(x) == camp]
        for other_player in [x.GetIdentity() for x in autres]:
            if other_player != self and other_player.IsActive():
                other_player.RemoveTokensInternal(1, 'first_player_token', by_effect)
        if not self.IsActive():
            from engine import Engine
            if Engine.game.session.version.IsFirstPlayerToken():
                self.PlaceTokensInternal(1, 'first_player_token', by_effect)

    def IsActive(self) -> bool:
        return self.GetTokens('first_player_token') > 0

    def ChangeAdditionalFrom(self, by_effect: 'Effect', action: Callable[[], 'CardFace|None']) -> bool:
        assert isinstance(self, AlterEgo|Hero)
        message = Message.WhenUnitWouldChangeForm(self, self, True, by_effect)
        message.Send()
        if message.is_be_instead:
            return False
        additional_from = action()
        after_message = Message.AfterUnitChangeForm(self, additional_from, by_effect, message)
        after_message.Send()
        return True

################################################################################
#
# We add `CanThwart` for fixing resolve issue with "37013" and "37015" interaction
@final
class AlterEgo(HasRecover, CanRecover, CanThwart, Identity, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    @override
    def GetAbilities(self) -> List['Ability']:
        return [
            AbilityFactory.ThisCanRecover()
        ] + super().GetAbilities()

    @override
    def OnDealDamage(self, units: List['Unit2'], damage: 'int|DamageProperty', by_effect: 'Effect', *, property: 'AttackProperty|None'=None, attack_in_event: bool) -> int|None:
        if self.IsDefeated():
            return None
        return CanAttack.OnDealDamageInternal(self, units, damage, by_effect, property=property, attack_in_event=attack_in_event)

################################################################################
#
@final
# CORRECTIF (01/09/2026, pack custom doctor_doom) : `HasVillainous` ajoute a la
# chaine du HEROS. Le mot-cle etait reserve aux sbires (minion.py:10), et
# dd001a « Doctor Doom » l'accorde pourtant a son propre heros
# (« Overwhelming Power — Action: Remove 3 power counters -> you gain
# villainous until the end of the round »), tandis que dd010 « Doom's Armor »
# le relit (« If Doctor Doom has villainous... »).
#
# ⚠ `HasVillainous` herite de `CanBoost` : un heros devient donc `CanBoost`, ce
# que `can_attack.py:220` teste a chaque attaque de base. Le garde `num <= 0`
# ajoute le meme jour dans `can_boost.py` est INDISPENSABLE — sans lui, tout
# heros non villainous plantait sur le `CastTo(Minion|Villain)` final.
#
# Inerte par defaut : `printed_villainous` vaut 0 sans `desc.Villainous`, donc
# `GetBoostCardNum()` rend 0 et aucune carte de boost n'est distribuee.
# Verifie le 01/09/2026 : spider_man, captain_america, agatha_harkness et beast
# montent tous sans changement, et la batterie complete reste a son etat connu.
#
# ⚠ CE N'EST PAS UN CONTOURNEMENT POUR UN PACK FAN-MADE. VERIFIE le 01/09/2026
# sur l'annonce FFG « Killer Instinct » (13/08/2026) : ELEKTRA est annoncee
# comme LE PREMIER HEROS OFFICIEL a porter le mot-cle villainous. Sa face heros
# « prend une carte de boost du deck rencontre chaque fois qu'elle utilise un
# pouvoir de base (contrer, attaquer ou defendre) ; la carte est retournee face
# visible, son effet de boost se resout, et ses icones s'ajoutent aux
# statistiques du personnage pour cette activation ».
# La place de `HasVillainous` est donc bien ici, dans la chaine du HEROS, et
# non dans un module de carte custom. A GARDER TEL QUEL quand Elektra arrivera.
#
# ⚠ CE QUI RESTERA A FAIRE POUR ELEKTRA : les TROIS pouvoirs de base sont
# concernes. Aujourd'hui seuls l'attaque (can_attack.py:220) et la manigance
# (can_scheme.py:92) distribuent des cartes de boost ; la DEFENSE n'a aucun
# chemin equivalent. Il faudra l'ajouter, ce que le pack doctor_doom n'a pas
# eu besoin de faire (dd010 n'accroche que l'attaque de base).
class Hero(HasThwart, CanThwart, HasAttack, CanAttack, HasDefense, CanDefense, HasAccelerationIcon, HasVillainous, Identity, FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:

        # EXTENSION (01/09/2026, pack custom alligator_loki) : un HEROS peut
        # etre ACCROCHE a un ennemi.
        #
        # al001a « Alligator Loki » s'attache lui-meme a l'ennemi qu'il attaque
        # ou contre lequel il defend, et cinq autres cartes du pack relisent cet
        # etat (al003 Chomp!, al013 Unbreakable Grip, al001b Nap Time...).
        #
        # ⚠ POURQUOI LA CARTE NE BOUGE PAS. La voie « normale » serait de faire
        # heriter `Hero` de `CanAttach` et d'appeler `AttachTo2`, qui deplace la
        # carte dans la zone d'ameliorations de la cible
        # (`Faces.MoveAllTo([self], face.GetInventoryDeck(), ...)`). C'est
        # exactement ce qu'il ne faut PAS faire ici : `Player.GetIdentity`
        # (player_get.py:191) rend l'INSERT DU MONDE des que `player.area_hero`
        # est vide, et ce deplacement la vide. Toutes les cartes du jeu qui
        # demandent « ton identite » recevraient alors la mauvaise face.
        # Mesure faite avant d'ecrire une ligne, pas apres.
        #
        # Le lien est donc porte par le HEROS lui-meme, sa carte restant dans sa
        # zone. Cote regles c'est identique : le heros EST l'attachement, il n'y
        # a aucune carte marqueur intermediaire, et les deux messages officiels
        # (`WhenCardWouldAttachTo`, `AfterCardDetachFrom`) sont emis, ce qui
        # laisse Unbreakable Grip s'accrocher a la fenetre « would detach ».
        # Seule la POSITION de la carte a l'ecran differe de la table.
        self.attached_enemy: 'CardFace|None' = None

        super().__init__(paper)

    ################################################################################
    # ACCROCHAGE DU HEROS A UN ENNEMI (voir le commentaire du constructeur)
    #
    def AttachHeroTo(self, face: 'CardFace', by_effect: 'Effect') -> bool:
        """Accroche CE heros a `face`. Rend False si l'ennemi n'est plus en jeu."""
        from game.message import Message

        if not face.card.IsOnField():
            return False
        if self.attached_enemy is face:
            return True

        # Meme fenetre que pour un attachement ordinaire : une carte peut s'y
        # opposer (`is_be_instead`).
        message = Message.WhenCardWouldAttachTo(self, face, by_effect)
        message.Send()
        if message.is_be_instead:
            return False

        if self.attached_enemy is not None:
            self.DetachHero(by_effect)

        self.attached_enemy = face
        Message.AfterCardAttachTo(face, self, message).Send()
        return True

    def DetachHero(self, by_effect: 'Effect') -> bool:
        """Detache CE heros de l'ennemi qu'il tenait. Rend False s'il n'en tenait aucun.

        ⚠ La fenetre `WhenCardWouldDetachFrom` n'existe pas dans le moteur : le
        `DetachFrom2` officiel n'emet QUE `AfterCardDetachFrom`, une fois le
        detachement acquis. Unbreakable Grip (al013) doit pourtant s'interposer
        AVANT (« when you would detach... exhaust Unbreakable Grip instead »),
        d'ou le message `WhenCardWouldAttachTo` reutilise a l'envers ? Non :
        c'est le module al013 qui intercepte, en enveloppant cet appel. Voir
        `cards/pack/alligator_loki/__init__.py`, helper `DetacherLeHeros`, qui
        est le SEUL point d'entree utilise par les cartes du pack.
        """
        from game.message import Message

        face = self.attached_enemy
        if face is None:
            return False
        self.attached_enemy = None
        Message.AfterCardDetachFrom(face, self).Send()
        return True

    def GetHeldEnemy(self) -> 'CardFace|None':
        """L'ennemi encore EN JEU que ce heros tient, sinon None (et oubli du lien)."""
        face = self.attached_enemy
        if face is not None and not face.card.IsOnField():
            self.attached_enemy = None
            return None
        return face

    @override
    def GetInfoDict(self) -> Dict[str, int]:
        # Marqueur UI : le heros est accroche a un ennemi (l'ennemi porte de
        # son cote `held_by_hero`, voir base/enemy.py).
        return super().GetInfoDict() | {
            'attached_to_enemy': 1 if self.GetHeldEnemy() is not None else 0,
        }

    @override
    def GetAbilities(self) -> List['Ability']:

        abilities: List['Ability'] = []

        if not self.ability.Find(func_name="ATK"):
            abilities.append(AbilityFactory.ThisCanAttack())
        if not self.ability.Find(func_name="THW"):
            abilities.append(AbilityFactory.ThisCanThwart())
        if not self.ability.Find(func_name="DEF"):
            abilities.append(AbilityFactory.ThisCanDefense())

        return abilities + super().GetAbilities()

