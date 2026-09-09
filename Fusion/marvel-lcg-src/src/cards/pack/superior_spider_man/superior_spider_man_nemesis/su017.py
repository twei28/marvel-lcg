from . import *

# Lunatic Laugh — TRAITRISE nemesis. Boost 1 + etoile.
# When Revealed: Take 2 indirect damage. Confuse each character damaged this
#   way.
# [star] Boost: Each player takes 1 indirect damage.
#
# CARTES DE REFERENCE
#  - `an011`, `ho014` : `WhenThisRevealed(None, op)`.
#  - `16026` Blazing Inferno : `Players.ForEachPlayer(effect, action)` pour
#    « each player ». ⚠ `World()` n'est PAS dans le namespace d'un pack (lecon
#    `sm014`, 08/09/2026 : `NameError` avale, carte muette).
#  - `05015` : `Faces.GiveStatus(..., "Confused", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « CONFUSE EACH CHARACTER **DAMAGED THIS WAY** » : les degats sont
#    INDIRECTS, donc REPARTIS PAR LE JOUEUR — l'identite, mais aussi ses allies.
#    On ne peut pas deviner qui a encaisse : il faut le LIRE. D'ou l'operation
#    passee a `TakeIndirectDamage`, qui rend les personnages reellement touches.
#    Confondre « le joueur » et « les personnages damaged this way » raterait
#    tous les allies.
#  ⚠ Le « When Revealed » vise LE joueur a qui la carte est revelee
#    (`message.GetToPlayer()`) ; la capacite BOOST, elle, dit « EACH player ».
#    Deux portees sur la meme carte.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def rire(effect: 'Effect', message: 'Message.WhenThisRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        touches: List['CardFace'] = []

        def noter(m: 'Message.AfterUnitTookDamage') -> None:
            cible = getattr(m, "trigger", None)
            if cible is not None and cible not in touches:
                touches.append(cible)

        identite.TakeIndirectDamage(this, 2, effect, operation=noter)
        if touches:
            Faces.GiveStatus(touches, "Confused", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        def frapper(joueur: 'Player') -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 1, effect)

        Players.ForEachPlayer(effect, frapper)

    return [
        AbilityFactory.WhenThisRevealed(None, rire),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
