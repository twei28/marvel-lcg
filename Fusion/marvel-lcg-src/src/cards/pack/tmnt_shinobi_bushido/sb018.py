from . import *

# * Musha Shugyō — MANIGANCE ANNEXE DE JOUEUR unique ✦, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [energy]. Menace 5.
# Victory 0.
# Characters other than the owner of this card cannot remove threat from it.
# When Defeated: The owner of this card may search their deck and discard pile for up to 2 OATH upgrades and put them into play.
#   (Shuffle.)
# « I will endure this soul's winter. » —Leonardo
#
# Mots-cles (fiches lues AVANT le code) : Victory (victory.md : BASE AUTOMATIQUE, `desc.Victory = "0"`, aucun script) ;
# samurai counter / OATH (samurai-counter.md) pour le trait OATH.
#
# Cartes de reference :
#  - « Characters other than X cannot remove threat from it » : `next_evol/cable/40006` Technovirus Purge
#    (`AbilityFactory.ThreatCannotBeRemovedFromWhile("This", by_character=CardFinder(non_name="Cable"))`) ; ici le « X » est le
#    PROPRIETAIRE de la carte, donc une condition sur `message.by_face` (un evenement ou une amelioration passe par l'IDENTITE de
#    celui qui joue : `event.py` `OnRemoveSchemeThreat`) ;
#  - « When Defeated: <joueur> may search their deck and discard pile for ... and put it into play » : `next_evol/40019`
#    Lock and Load (`WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, ..., may=True)` + `face.PutIntoPlay(joueur, effect)`), ici pour le PROPRIETAIRE seul et « up to 2 ».
#
# TEXTE CONTRE CODE
#  ⚠ « Characters OTHER THAN THE OWNER cannot remove threat » : seule l'IDENTITE du proprietaire (heros ou alter-ego), et ce qu'elle
#    joue (evenement, amelioration), retire de la menace ; les allies du proprietaire, les autres joueurs, les sbires, le vilain ne le
#    peuvent pas. Lecture litterale (precedent Cable : « other than Cable » exclut aussi ses allies).
#  ⚠ « The OWNER ... may search THEIR deck AND discard pile » : le proprietaire (pas « each player » comme 40018/40019), son deck ET
#    sa defausse (les deux a la fois dans la meme recherche) ; « up to 2 » : 0, 1 ou 2 (une seconde recherche seulement apres un
#    premier succes) ; « OATH upgrades » : ameliorations OATH ; « put them into play » (pas en main).
#  ⚠ Menace de depart 5 FIXE (« 5 », sans etoile : pas de multiplication par joueur) ; Victory 0.


def GetAbilities() -> Sequence['Ability']:

    def proprietaire(effect: 'Effect') -> 'Player|None':
        return effect.this.GetOwner()

    def pas_le_proprietaire(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        joueur = proprietaire(effect)
        source = message.by_face
        if joueur is not None and source is not None and Identity.IsType(source) and source.GetControlByPlayer() == joueur:
            return False
        return True

    def musha_shugyo(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        joueur = proprietaire(effect)
        if joueur is None:
            return
        for _ in range(2):
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                include_discard_pile=True,
                trait="OATH",
                card_type=Upgrade,
                may=True,
            )
            if face is None:
                break
            face.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            conditions=[pas_le_proprietaire],
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            musha_shugyo,
        ),
    ]
