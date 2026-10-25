from . import *

# M134 Minigun — ATTACHEMENT (set « Predator Alt Nemesis »), WEAPON, +1 ATQ, Boost 1.
# Attach to Dutch Schaefer. If he is not in play, search the encounter deck and discard pile for him, reveal him and attach
#   this card to him.
# ★ Forced Response: After Dutch Schaefer attacks you, place 1 threat on the Chopper side scheme.
#
# Cartes de reference :
#  - `Find.FindAndReveal` (game/operate/find.py) pour « search ... for him, reveal him » ; `this.AttachTo2(face, effect)` (ts007) ;
#  - `GiveKeywordToAttached("Character", attack=1)` (retaliate/ATQ pour l'hote) ;
#  - `AfterUnitAttackEnd(.., against_who="You")` (pd028) ; `PoserDeLaMenaceSurLeChopper` (helper du set).
#
# ⚠ Mots-pieges :
#  - « +1 ATK » : l'icone imprimee : bonus d'ATQ de l'hote (Dutch) ;
#  - « Attach to Dutch Schaefer. IF HE IS NOT IN PLAY, search ... » : Dutch en jeu = on s'attache a lui ; sinon on le cherche,
#    on le REVELE (il s'engage) et on s'attache ; introuvable : defaussee ;
#  - « After Dutch Schaefer attacks you » : le PORTEUR, contre le joueur ; « the Chopper side scheme » : le nom propre
#    (`pd026`), rien si Chopper n'est pas en jeu.


def GetAbilities() -> Sequence['Ability']:

    def porter_l_arme(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer() or JoueurDeCetteCarte(effect)
        dutch = next((m for m in Worlds.GetOnFieldMinions(effect) if m.paper.card_id == ID_DUTCH), None)
        if dutch is None and joueur is not None:
            dutch = Find.FindAndReveal(effect, joueur, finder=CardFinder(card_ids=[ID_DUTCH]))
        if dutch is not None and dutch.card.IsOnField():
            this.AttachTo2(dutch, effect)
        else:
            Faces.DiscardAll([this], effect)

    def rafale(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        PoserDeLaMenaceSurLeChopper(effect, 1)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            attack=1,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            porter_l_arme,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "AttachedCharacter",
            rafale,
            against_who="You",
        ),
    ]
