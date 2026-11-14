from . import *

# Obliterate : EVENEMENT (ATTACK. SPLIT. SUPERPOWER. THWART.), cout 4, [wild]. Classe Hero. (TEXTE MIS A JOUR le 03/11/2026.)
# Hero Action (attack/thwart): Choose to discard all attachments from an enemy or defeat a non-ELITE minion, ignoring any "When Defeated" abilities on that minion (you may choose a side scheme instead if there are 3+ balance counters in play).
# Special: Discard the highest-cost card you control, highest hit point minion, and side scheme with the most threat.
#
# CARTES DE REFERENCE
#  - `ChooseAbilities` de `ForChoiceAbility` avec cibles : `rz007` (`SetTarget(Enemy, ..)`) ; critere « non-ELITE » : `CardFinder(card_type=Minion, non_trait="ELITE")` (ca022) ; attachements d'un ennemi : `ennemi.GetAttachedAttachments()` (ca020).
#  - « defeat, ignoring When Defeated » : `Faces.DefeatUnits(cibles, None, effect, ignore_when_defeated=True)` ; « defeat a side scheme » : `this.RemoveThreatFromSchemes(cibles, "All", effect)`.
#  - Special : cout imprime `carte.printed_cost.val` (ra031), PV `carte.max_health`, menace `scheme.threat` ; `.NoOutOfPlayLimit()`.
#
# TEXTE CONTRE CODE
#  DECISION UTILISATEUR du 03/11 (valable pour la nouvelle version) : « choix direct SANS DEGATS » : aucune attaque (Toughness, gardes, effets « apres une attaque » ne comptent pas). « ALL attachments from AN enemy » : tous ceux de l'ennemi choisi.
#  « NON-ELITE minion » : un sbire sans le trait ELITE. « (or side scheme IF 3+ counters IN PLAY) » : troisieme choix, seulement a 3+ compteurs. Special : TROIS defausses : la carte au plus haut cout que vous controlez, le sbire aux PV les plus hauts (tout sbire,
#  Void compris : le texte ne l'exclut pas) et le complot annexe a la plus haute menace. Chiffres : cout 4.


def GetAbilities() -> Sequence['Ability']:

    def obliterate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def defausser_les_attachements(cibles: Sequence['CardFace']) -> None:
            for ennemi in cibles:
                attaches = list(ennemi.CastTo(Enemy).GetAttachedAttachments())
                if attaches:
                    Faces.DiscardAll(attaches, effect)

        def vaincre_le_sbire(cibles: Sequence['CardFace']) -> None:
            Faces.DefeatUnits(cibles, None, effect, ignore_when_defeated=True)

        def vaincre_l_annexe(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, "All", effect)

        choix = [
            AbilityFactory.ForChoiceAbility("Discard all attachments from an enemy", defausser_les_attachements).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility("Defeat a non-ELITE minion", vaincre_le_sbire).SetTarget(Minion, non_trait="ELITE"),
        ]
        if EquilibreEnJeu(effect) >= 3:
            choix.append(AbilityFactory.ForChoiceAbility("Defeat a side scheme", vaincre_l_annexe).SetTarget(EncounterSideScheme))
        joueur.ChooseAbilities(effect, *choix)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect) or JoueurSentry(effect)
        a_defausser: 'List[CardFace]' = []
        if joueur is not None:
            cartes = [f for f in joueur.GetControlCards() if f.IsInPlay() and not (Hero.IsType(f) or AlterEgo.IsType(f))]
            if cartes:
                plus_haut = max(f.printed_cost.val for f in cartes)
                a_defausser.append([f for f in cartes if f.printed_cost.val == plus_haut][0])
        sbires = Worlds.FindCardsOnField(effect, card_type=Minion)
        if sbires:
            pv = max(f.max_health for f in sbires)
            a_defausser.append([f for f in sbires if f.max_health == pv][0])
        annexes = Worlds.FindCardsOnField(effect, card_type=EncounterSideScheme)
        if annexes:
            menace = max(f.threat for f in annexes)
            a_defausser.append([f for f in annexes if f.threat == menace][0])
        if a_defausser:
            Faces.DiscardAll(a_defausser, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, obliterate).SetPlay().SetLabel('attack').SetHasNoTargetEffect(),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
