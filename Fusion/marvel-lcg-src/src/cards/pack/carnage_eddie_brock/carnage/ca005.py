from . import *

# * Probing Minds : AMELIORATION (SUPERPOWER. SYMBIOTE.), cout 1, [mental]. Classe Hero.
# Hero Interrupt: When you reveal a non-ELITE minion, exhaust this card -> if that minion has boost icons equal to:
#  • 0, heal 1 damage.  • 1, confuse that minion.  • 2, stun that minion.  • 3+, remove 1 threat from a scheme.
#
# CARTES DE REFERENCE
#  - « When you reveal a non-ELITE minion » : `50101` (Batroc's Brigade) : `WhenPlayerRevealCard(HeroInterrupt, "You", NonEliteMinion, "All", op)` (CardFinder.NonEliteMinion du pack commun).
#  - Statuts : `nt004` / `01083` : `Faces.GiveStatus(cibles, "Confused"|"Stunned", effect)` ; soin `my001b` : `HealthUnits([cible], n, effect)` ; retrait de menace d'un complot CHOISI : `RemoveThreatFromSchemes`.
#
# TEXTE CONTRE CODE
#  « Hero Interrupt: When YOU reveal a NON-ELITE MINION » : revelation par le joueur (jamais une mise en jeu directe comme Dark Urges), type sbire, trait ELITE exclu. « exhaust this card → » : COUT.
#  « boost icons equal to » : ICONES DE BOOST IMPRIMEES du sbire (`printed_boost` ; 0 si aucune) : 0 = soin, 1 = confus, 2 = etourdi, 3 ou plus = menace. Les quatre cas sont EXCLUSIFS.
#  « heal 1 damage » : DECISION UTILISATEUR du 03/11 (lecture A) : soigne CARNAGE (l'identite du joueur, forme heros puisque Hero Interrupt), sans choix de cible. « remove 1 threat FROM A SCHEME » : un complot au choix, principal ou annexe.
#  Chiffres : cout 1, 1 soin / 1 menace.


def GetAbilities() -> Sequence['Ability']:

    def probing_minds(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        sbire = message.trigger
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        icones = int(getattr(sbire, "printed_boost", 0) or 0)
        if icones <= 0:
            this.HealthUnits([joueur.GetIdentity()], 1, effect)
        elif icones in (1, 2):
            # Le sbire n'est pas encore en jeu a l'Interruption : un statut pose maintenant ne tient pas (constate le 03/11). On le pose
            # DES QU'IL ENTRE EN JEU, par une capacite temporaire portee par le sbire (`bebop_rocksteady/tk108`, `RegisterTemp`).
            statut = "Confused" if icones == 1 else "Stunned"

            def poser_le_statut(effect2: 'Effect', message2: 'Message.AfterCardEnterPlay') -> None:
                Unused(message2)
                Faces.GiveStatus([effect2.this], statut, effect)

            sbire.effect.RegisterTemp(
                AbilityFactory.AfterCardEnterPlay(AbilityType.Temp0, "This", poser_le_statut),
                unregister_after_exec=True,
            )
        else:
            complots = [f for f in Worlds.FindCardsOnField(effect, card_type=Scheme2) if f.IsInPlay()]
            if not complots:
                return
            cible = joueur.AskChooseFace(complots, effect)
            if cible is not None:
                this.RemoveThreatFromSchemes([cible], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "You",
            NonEliteMinion,
            "All",
            probing_minds,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
