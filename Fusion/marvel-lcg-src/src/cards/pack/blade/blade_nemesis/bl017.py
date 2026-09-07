from . import *

# Turned — ATTACHEMENT nemesis (N 8/8). CONDITION. ATQ +1, 1 boost.
# Attached ally gains traitor, the VAMPIRE trait and the following text:
#   "Attacks with piercing deal double damage to this enemy." and gets +3 hit
#   points.
# When Revealed: Attach to the ally with the fewest remaining hit points. If you
#   cannot, this card gains surge. Heal all damage from that ally.
#
# CARTES DE REFERENCE
#  - `27171` Manipulated Mind : `TreatAttachedCardAsMinion(Ally, <gabarit>,
#    process)` + `Filter.One(allies, effect, ...)` + `ThisCardGainSurge`.
#  - fiche traitor.md : le gabarit « Traitor Minion » (aav_traitor_minion, pack
#    agent_anti_venom) et le SCH force a 1 par `process`.
#  - le trait VAMPIRE et les +3 PV sont poses dans `process` (voir le
#    commentaire de `traitre`) ; `desc.ATK+` = "1" pour l'ATQ +1 (modele sf014).
#  - `Filter.One(..., fewest_remaining_hp=True)` (filter.py:12).
#
# TEXTE CONTRE CODE
#  ⚠ « gains traitor » -> l'allie devient un sbire engage avec son proprietaire
#    (1 SCH, texte vide, pas de degats consecutifs). Son ATQ imprimee est
#    gardee, +1 par l'attachement.
#  ⚠ « the ally with the FEWEST remaining hit points » -> parmi les allies du
#    joueur a qui la carte est revelee ; egalite -> le joueur choisit
#    (`Filter.One`).
#  ⚠ « If you cannot, this card gains surge » -> aucun allie : surge, et la
#    carte est defaussee (attachement sans hote).
#  ⚠ « Heal ALL damage from that ally » -> AVANT la conversion (meme resultat :
#    le sbire arrive a pleins PV, +3).
#  ⚠ Sous Blood Hunt (bl012), le sbire converti a un trait VAMPIRE non imprime :
#    il cumule les deux textes de doublement (x4), lecture litterale assumee.


def GetAbilities() -> Sequence['Ability']:

    def traitre(minion: 'Minion', allie: 'Ally', effect: 'Effect') -> None:
        # ⚠ TOUT le bonus est pose ICI, dans la conversion, et pas par
        # `GiveKeywordToAttached` : ce dernier applique/retire ses bonus sur les
        # DEUX faces de la carte echangee (l'allie puis le sbire) et retirait le
        # trait VAMPIRE d'une face qui ne l'avait jamais recu -> `KeyError:
        # 'VAMPIRE'` (trait.py:81), trouve par le cas bl017 du 07/09/2026.
        # Modele 27171 Manipulated Mind : `process=lambda minion, ally, effect:
        # minion.CopyTrait(ally, effect)`.
        minion.printed_scheme = 1
        minion.CopyTrait(allie, effect)
        minion.GainTraits(+1, TRAIT_VAMPIRE, effect)

    def tourner(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        allies = [a for a in (joueur.GetControlAllies() if EstJoueur(joueur) else []) if a is not None]
        allie = Filter.One(allies, effect, fewest_remaining_hp=True) if allies else None
        if allie is None:
            ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)
            return
        allie.HealHealth("All", effect)
        this.AttachTo2(allie, effect)
        # « gets +3 hit points » : pose APRES la conversion (qui a lieu pendant
        # l'attache, via AfterCardGainUpgrade), sur la face SBIRE. Un
        # `printed_health` modifie dans `process` etait ecrase par la remise a
        # zero des PV a l'entree en jeu (cas bl017 : 3 PV max au lieu de 6).
        sbire = Hote(this)
        if sbire is not None and Minion.IsType(sbire):
            sbire.GainHealthAndMaxHealth(3, effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(
            Ally,
            "Traitor Minion",
            traitre,
        ),
        DoubleDegatsPercants("AttachedMinion"),
        AbilityFactory.WhenThisRevealed(
            None,
            tourner,
        ),
    ]
