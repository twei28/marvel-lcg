from cards.pack import *

# ===========================================================================
# Pack OKOYE — contenu custom de BLUEHG (Marvel Champions Custom Project,
# "Okoye [3.0]"), reproduit a l'identique.
#
# Okoye est une heroine d'equipe : ses signatures creent/renforcent des allies
# DORA MILAJE (Aneka, Ayo, et deux jetons "Created Ally" jamais tires du deck :
# Dora Milaje et Midnight Angel, generes a la volee par Adored Ones / Angelic
# Warfare). Modele du jeton cree hors deck : moon_knight/age_of_khonshu
# (`CardFactory.GenerateCard(card_id, player.player_deck, effect.world)` puis
# `card.face.PutIntoPlay(initiator, effect)`), qui cree deja des cartes qui ne
# vivent dans AUCUN deck (les 4 artefacts mk021-024, crees au When Defeated).
#
# Collision de nom deliberee, non bloquante : le pack officiel `bp` a deja
# code Aneka (51022), Ayo (51023) et Okoye elle-meme (51024) comme allies, et
# Dora Milaje (51030) comme support -- avec un texte totalement different
# (mecanique "Resolve Special" du set Black Panther/Shuri). Le moteur
# identifie les cartes par card_id (ok002/ok003 ici, 51022/51023 la-bas), donc
# aucune collision technique. "Adored Ones" (ok004/ok005) cherche "Aneka" OU
# "Ayo" PAR NOM dans le deck/la defausse du joueur Okoye -- modele kb003
# (Family = Trouble, `Search.PlayerCard(..., name="Hawkeye")`) qui fait deja
# exactement cela pour l'allie "Hawkeye" de Kate Bishop sans se soucier d'un
# autre "Hawkeye" ailleurs dans le depot : le nom seul suffit, le deck d'un
# joueur Okoye ne contient normalement QUE ses propres Aneka/Ayo.
# ===========================================================================

NOM_ANEKA = "Aneka"
NOM_AYO = "Ayo"
NOM_ARMURE_MIDNIGHT_ANGEL = "Midnight Angel Armor"

# card_id des deux jetons "Created Ally" : jamais lists dans un deck (comme
# les artefacts mk021-024 de moon_knight), toujours generes par
# `CardFactory.GenerateCard` au moment ou une carte les cree.
ID_JETON_DORA_MILAJE = "ok017"
ID_JETON_MIDNIGHT_ANGEL = "ok018"

# Les deux seuls porteurs du mot-cle "Legion" (jamais nommes ni exhaustifs
# autrement -- le pack entier n'a que ces deux jetons).
NOM_JETON_DORA_MILAJE = "Dora Milaje"
NOM_JETON_MIDNIGHT_ANGEL = "Midnight Angel"


def CreerJetonEtMettreEnJeu(card_id: str, initiator: 'Player', effect: 'Effect') -> None:
    """Cree un jeton "Created Ally" (jamais dans un deck) et le met en jeu
    sous le controle du joueur. Modele exact : moon_knight/age_of_khonshu
    (`DonnerArtefact`), meme couple GenerateCard + PutIntoPlay.
    """
    from game.card.factory import CardFactory
    card = CardFactory.GenerateCard(card_id, initiator.player_deck, effect.world)
    card.face.PutIntoPlay(initiator, effect)


def EstAllieLegion(face: 'CardFace') -> bool:
    """Un allie portant le mot-cle Legion (Dora Milaje ou Midnight Angel,
    les deux seuls jetons de ce pack)."""
    return face.IsName(NOM_JETON_DORA_MILAJE) or face.IsName(NOM_JETON_MIDNIGHT_ANGEL)


def Legion() -> 'Ability':
    """« Legion. (2 allies with the legion keyword count as 1 ally toward
    your ally limit.) »

    Pas de primitive "compte N comme 1" dans ce moteur : seul
    `Message.CheckIfAllyCountLimit` / `SetNotCountAlly` existe (utilise par
    aoa/missions.py pour un allie qui NE compte JAMAIS). Modele adapte : on
    classe les allies Legion du joueur par ordre de creation stable
    (`card.object_id`, cf. card.py : `self.object_id < other.object_id`) et
    UN SUR DEUX (index impair) ne compte pas -- N allies Legion valent alors
    ceil(N/2) au lieu de N, exactement la regle « 2 comptent comme 1 ».
    Utilise `AbilityFactory.ThisNotCountAllyLimit` (friend.py), meme crochet
    que aoa/missions.py, avec une condition personnalisee au lieu du "toujours
    vrai" de la mission.
    """
    def est_le_second_du_couple(effect: 'Effect', message: 'Message.CheckIfAllyCountLimit') -> bool:
        joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return False
        allies_legion = sorted(
            (a for a in joueur.allies.Get() if EstAllieLegion(a)),
            key=lambda a: a.card.object_id,
        )
        if effect.this not in allies_legion:
            return False
        return allies_legion.index(effect.this) % 2 == 1

    return AbilityFactory.ThisNotCountAllyLimit(conditions=[est_le_second_du_couple])[0]


def Fragile() -> 'Ability':
    """« Fragile. (Attacks against this character gain overkill.) »

    Modele exact : determination/__init__.py (`Fragile`), qui reprend le
    crochet officiel de Marked (33032) sur `WhenUnitWouldAttackUnit` +
    `GainOverKill`. Seule difference : Midnight Angel Armor (ok012/ok013)
    retire ce mot-cle au personnage attache (« loses the fragile keyword »),
    et ce moteur n'a pas de mecanisme generique pour desactiver une ability
    imprimee sur une AUTRE carte -- la condition est donc integree ICI (pas
    d'overkill si l'armure est attachee), ce qui produit exactement le meme
    resultat observable que « perdre Fragile ».
    """
    def fragile(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        if any(u.IsName(NOM_ARMURE_MIDNIGHT_ANGEL) for u in effect.this.GetAttachedUpgrades()):
            return
        message.GainOverKill(effect)

    return AbilityFactory.WhenUnitWouldAttackUnit(
        AbilityType.NonKeyword,
        None,
        "This",
        fragile,
    )
