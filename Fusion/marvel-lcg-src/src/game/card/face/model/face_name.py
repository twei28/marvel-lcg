from core import *
from game.card.face import *
from game.ability import *
from game.card.face.model.base import ModelBase

class ModelName(ModelBase):

    def SetName(self, printed_name: str):
        def extract_prefix(input_string: str):
            import re
            # Define the regex patterns with capturing groups
            patterns = [
                r"(.*) - \d?[A-F]$",
                r"(.*) \d?[A-F]$",      # The Injured Senator 2A
                r"(.*) \([^()]+\)$"     # Kang (The Conqueror)
            ]
            
            # Iterate through the patterns and try to match
            for pattern in patterns:
                match = re.match(pattern, input_string)
                if match:
                    return match.group(1)
                    
            # If no pattern matches, return the original string or handle as needed
            return input_string

        self.name = extract_prefix(printed_name)
        self.printed_name = printed_name

    def SetSubtitle(self, printed_subtitle: str):
        self.printed_subtitle = printed_subtitle

    @final
    def IsName(self, name: str, check_cosider_as: bool=True, check_all_face: bool=False) -> bool:
        this = self.GetThis()
        if check_all_face:
            faces = [this] + this.card.back_faces
            for face in faces:
                if face and face.IsName(name, check_cosider_as):
                    return True
            return False
        else:
            if name == this.printed_name:
                return True
            if name == this.name:
                return True
            if name == "Ronan" and this.printed_name == "Ronan the Accuser":
                return True
            if this.IsCardId(name):
                return True
            if check_cosider_as and this.IsConsiderAs(name=name):
                return True
            return False

    ################################################################################
    #
    @final
    def IsUnique(self) -> bool:
        this = self.GetThis()
        return this.paper.is_unique

    @final
    def IsCardId(self, name: str) -> bool:
        this = self.GetThis()
        return name == this.paper.card_id

    @final
    def IsSubName(self, subname: str) -> bool:
        this = self.GetThis()
        return this.paper.subtitle == subname

    @final
    def TitleContain(self, title_contain: str) -> bool:
        this = self.GetThis()
        for name in [this.name] + [x for x in this.consider_as.names]:
            if title_contain in name:
                return True
        return False

    # If two identities share the same title, but each has a different alter-ego, they may coexist in play
    # If two unique allies share the same title, but each has a different subtitle, they may coexist in a player’s deck and in play.
    # If a hero and a unique ally share the same title, but the alter-ego and the subtitle are different, they may coexist in deckbuilding and in play.
    @final
    def CanCoexistWith(self, that: 'CardFace') -> bool:
        from game.card.face.card_type import Identity
        from game.card.face.card_type import Hero
        from game.card.face.card_type import AlterEgo

        this = self.GetThis()

        if not that.IsUnique():
            return True
        if not this.IsUnique():
            return True
        if this == that:
            return True

        if not this.card.IsApplyUniqueRule():
            return True
        if not that.card.IsApplyUniqueRule():
            return True

        def get_titles(face: 'CardFace') -> Set[str]:
            if not Identity.IsType(face):
                return set([face.name])
            names: Set[str] = set()
            for check_face in [face] + face.card.back_faces:
                if Hero.IsType(check_face):
                    names.add(check_face.name)
            return names

        def get_subtitle(face: 'CardFace') -> str:
            if not Identity.IsType(face):
                return face.printed_subtitle
            subtitle = ""
            for check_face in [face] + face.card.back_faces:
                if AlterEgo.IsType(check_face):
                    subtitle = check_face.name
            # Fix "50034b"
            if subtitle in get_titles(face):
                subtitle = ""
            return subtitle

        if get_titles(this) & get_titles(that) and \
            get_subtitle(this) == get_subtitle(that):
            return False

        # AJOUT (17/10/2026, decision de l'utilisateur, unicite par sous-titre). Le moteur ne jugeait que
        # « meme titre ET meme sous-titre » ; le deck-builder (`public/js/deckbuilder/regles.js`,
        # `correspondent`, Rules Reference v1.8) juge aussi : le sous-titre (ou le titre d'alter ego) d'une
        # carte unique egale le titre, le sous-titre ou le titre d'alter ego de l'autre. Un sous-titre
        # d'allie est le PERSONNAGE : Ronin (Mikey) ne coexiste pas avec Michelangelo (alter ego Mikey),
        # Heavy Metal (Jenny) ne coexiste pas avec Nightwatcher (Jenny).
        # Limites : (1) cartes cote JOUEUR seulement (identite, allie, soutien, amelioration, ressource) ;
        # les cartes de la rencontre gardent l'ancien jugement (le vilain Lizard « Curtis Connors »
        # reste compatible avec un heros dont l'alter ego est Curtis Connors) ; (2) pas d'identite contre
        # identite (le deck-builder ne les compare pas non plus : deux joueurs peuvent jouer deux
        # Spider-Man de meme alter ego).
        def cote_joueur(face: 'CardFace') -> bool:
            from game.card.face.card_type import Ally, Support, Upgrade, Resource
            return Identity.IsType(face) or Ally.IsType(face) or Support.IsType(face) or \
                Upgrade.IsType(face) or Resource.IsType(face)

        def descripteurs(face: 'CardFace') -> List[Tuple[str, str, str]]:
            # (titre, sous-titre, titre d'alter ego), comme `correspondent` cote deck-builder
            if not Identity.IsType(face):
                return [(face.name, face.printed_subtitle, "")]
            alter = ""
            for check_face in [face] + face.card.back_faces:
                if AlterEgo.IsType(check_face):
                    alter = check_face.name
            return [(title, "", alter) for title in get_titles(face)]

        def correspondent(a: Tuple[str, str, str], b: Tuple[str, str, str]) -> bool:
            if a[0] == b[0] and not a[1] and not b[1] and not a[2] and not b[2]:
                return True
            def autres(x: Tuple[str, str, str]) -> List[str]:
                return [v for v in x if v]
            return any(v in autres(b) for v in (a[1], a[2]) if v) or \
                any(v in autres(a) for v in (b[1], b[2]) if v)

        if cote_joueur(this) and cote_joueur(that) and \
            not (Identity.IsType(this) and Identity.IsType(that)):
            for desc_this in descripteurs(this):
                for desc_that in descripteurs(that):
                    if correspondent(desc_this, desc_that):
                        return False

        # AJOUT (16/10/2026, aspects TMNT) : titre unique secondaire du bandeau (`unique_also`,
        # Bo-Wing « ✦ Winter Soldier »). Decision de l'utilisateur : l'unicite se juge sur les
        # deux titres. Le bandeau n'a pas de sous-titre : il suffit que le TITRE corresponde.
        def get_aliases(face: 'CardFace') -> Set[str]:
            return set(face.paper.unique_also)
        if get_aliases(this) & (get_titles(that) | get_aliases(that)) or \
            get_aliases(that) & get_titles(this):
            return False

        return True

    ################################################################################
    #
    @final
    def GetDisplayName(self, *, no_hidden: bool=False, no_object_id: bool=False) -> str:
        this = self.GetThis()
        if no_object_id:
            object_id = 0
        else:
            object_id = '{:02}'.format(this.card.object_id)

        if this.card.IsAsOtherCard():
            id = f"({object_id},{this.paper.card_id},{this.card.printed_faces[0].paper.card_id}) "
        else:
            id = f"({object_id},{this.paper.card_id}) "

        hidden = ''
        if not no_hidden and not this.card.IsVisible("Any"):
            hidden = ' ?'
        return "[{}{}{}]".format(id, self.name, hidden)

