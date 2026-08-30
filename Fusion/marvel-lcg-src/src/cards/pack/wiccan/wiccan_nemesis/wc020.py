from . import *

# * Moridun — carte nemesis de Wiccan (2/5), type imprime ATTACHMENT
# Attach to the Billy Kaplan player's identity.
# When Revealed: Reveal your set-aside New Vessel side scheme.
# Forced Interrupt: When Wiccan would deal damage to an enemy or remove
#   threat from a scheme, place 1 threat on the New Vessel side scheme.
# (Wiccan's Nemesis Minion.)
#
# ECART D'AUTEUR ASSUME, NON CORRIGE : la parenthese finale annonce un
# « Nemesis Minion », mais le type IMPRIME de la carte est Attachment, elle
# n'a ni PV, ni ATQ, ni MNG, et son premier mot est « Attach to... ». Le type
# imprime fait foi ; la parenthese est une coquille de l'auteur. Documenté
# dans wiccan_nemesis/__init__.py et dans la fiche de la carte.
#
# « Attach to the Billy Kaplan player's identity » ->
# `AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity")`, modele 24007
# Established Dominance (meme phrase « Attach to your identity », meme
# fabrique). « YourIdentity » designe l'identite du joueur a qui la carte est
# distribuee — et une carte nemesis de Wiccan n'est distribuee qu'au joueur
# de Wiccan. Ce n'est PAS un `CardFinder(name="Billy Kaplan")` : la carte
# doit s'attacher aussi quand le joueur est en forme HEROS, ou le nom de sa
# face courante est « Wiccan ». Le piege du `*` d'unicite ne se pose donc meme
# pas ici.
#
# « Reveal your set-aside New Vessel side scheme » ->
# `Worlds.GetSetAsideAreaCards(effect, CardFinder(name="New Vessel"))` puis
# `face.Reveal(player, effect)`. Modele de la recherche en zone de reserve :
# The Grim Hunt (`mw018`), qui va chercher son Kraven mis de cote exactement
# comme ca. `Reveal` (et non `PutIntoPlay`) : le texte imprime dit « reveal »,
# donc la manigance repasse par le pipeline de revelation complet.
# Garde : si New Vessel n'est PAS de cote (deja en jeu, par exemple), rien ne
# se passe — aucune erreur.
#
# « When Wiccan would deal damage to an enemy OR remove threat from a scheme »
# -> DEUX declencheurs distincts, jamais un `if` :
#   - `AbilityFactory.WhenFaceWouldDealDamage(ForcedInterrupt, CardFinder(
#     name="Wiccan"), ..., who_take_damage=CardFinder(card_type=Enemy))`
#     (game/ability/factory/damage.py:495) ;
#   - `AbilityFactory.WhenSchemeWouldRemoveThreat(ForcedInterrupt, None, ...)`
#     (scheme.py:53), dont la condition interne exige deja `message.value > 0` :
#     un retrait de 0 menace ne declenche pas.
# C'est bien « WICCAN », le nom de la face HEROS, pas « votre identite » : en
# forme civile Billy Kaplan n'inflige pas de degats et ne contre pas. Le nom
# est ecrit SANS l'etoile d'unicite (`cards/paper.py:45-46` la retire).
#
# ASYMETRIE DU MOTEUR, constatee au journal et rendue a la main (correctif du
# 30/08/2026, trouve par test_capacites.py) : pour les DEGATS, le moteur
# attribue deja la source a l'IDENTITE meme quand ils viennent d'un evenement
# joue par elle (« [Wiccan] would deal 3 damage to [Rhino] ([Magic Bolt]) »),
# donc `who_deal_damage=CardFinder(name="Wiccan")` suffit et couvre Magic Bolt
# comme l'attaque de base. Pour le RETRAIT DE MENACE, non : le
# `message.by_effect.this` d'un Magic Portal est L'EVENEMENT, pas Wiccan, et
# `who_make_thwart=CardFinder(name="Wiccan")` ne voyait donc QUE le contre de
# base (constate : New Vessel restait a 4 menaces). Le filtre est ecrit a la
# main dans `wiccan_retire_de_la_menace` : Wiccan lui-meme, ou une carte NON
# PERSONNAGE que le joueur de Billy Kaplan possede — ses sorts. Un ALLIE qui
# contre n'est pas Wiccan et ne declenche rien : c'est la lecture stricte du
# texte imprime.
#
# « place 1 threat on the New Vessel side scheme » -> `this.PlaceThreatOnSchemes
# ([new_vessel], 1, effect)`. Si New Vessel n'est pas en jeu (elle a ete
# vaincue et mise de cote), rien ne se passe : le texte ne prevoit pas de
# repli.
# ForcedInterrupt et non ForcedResponse : la menace se pose AVANT que les
# degats / le retrait ne soient appliques (piege des deux fabriques,
# PROCESSUS-CARTE).

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        player = message.GetToPlayer()
        if player is None:
            return

        faces = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_NEW_VESSEL))
        if faces:
            faces[0].Reveal(player, effect)

    def poser_une_menace(effect: 'Effect') -> None:
        this = effect.this.CastTo(Attachment)

        new_vessel = NewVesselEnJeu(effect)
        if new_vessel is not None:
            this.PlaceThreatOnSchemes([new_vessel], 1, effect)

    def sur_degats(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        Unused(message)
        poser_une_menace(effect)

    def wiccan_retire_de_la_menace(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        source = message.by_effect.this
        if source is None:
            return False
        if source.IsName(NOM_WICCAN):
            return True
        # Un ALLIE (ou tout autre personnage) qui contre n'est pas Wiccan.
        # `Unit2` est la classe des personnages du moteur (identites, allies,
        # sbires, vilains) ; le test vient APRES la comparaison de nom, donc
        # Wiccan lui-meme n'est jamais ecarte par cette ligne.
        if Unit2.IsType(source):
            return False
        joueur = Worlds.FindPlayerByName(NOM_BILLY, effect)
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        if identite is None or not identite.IsName(NOM_WICCAN):
            return False
        return source.GetOwner() == joueur

    def sur_retrait_de_menace(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        Unused(message)
        poser_une_menace(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
        AbilityFactory.WhenFaceWouldDealDamage(
            AbilityType.ForcedInterrupt,
            CardFinder(name=NOM_WICCAN),
            sur_degats,
            who_take_damage=CardFinder(card_type=Enemy),
        ),
        AbilityFactory.WhenSchemeWouldRemoveThreat(
            AbilityType.ForcedInterrupt,
            None,
            sur_retrait_de_menace,
            conditions=[wiccan_retire_de_la_menace],
        ),
    ]
