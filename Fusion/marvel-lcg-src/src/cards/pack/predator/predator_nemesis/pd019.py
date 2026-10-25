from . import *

# Hunted By the Hive — TRAITRISE (set « Predator Nemesis »), Boost 2.
# When Revealed: Xenomorph Queen attacks you. If it's not in play, find Xenomorph Queen and put it into play engaged with you.
#
# Cartes de reference :
#  - `27168` Symbiotic Strength (sm) : `villain.DoAttackYou(player, effect)` pour « X attacks you » ;
#  - `Find.Find` (game/operate/find.py, regle « Find » du 23/10/2026) pour « find Xenomorph Queen », comme `AmenerLaReine`
#    (helper du set) ; `br011` / `Search.SearchForCard` pour « put it into play engaged with you ».
#
# ⚠ Mots-pieges :
#  - « If it's not in play » : la Reine ABSENTE est trouvee (deck de rencontre, defausse, cartes mises de cote) ; deja en jeu elle attaque.
#  - ARBITRAGE PROVISOIRE (25/10/2026, question posee a l'auteur, QUESTIONS-AUTEUR.md) : la Reine qui vient d'arriver ATTAQUE aussi
#    (la 1re phrase est resolue apres son arrivee). Si l'auteur dit le contraire : retirer l'appel a `DoAttackYou` apres `AmenerLaReine`.
#  - Reine introuvable (vaincue puis retiree, deja engagee ailleurs...) : rien ne se passe.


def GetAbilities() -> Sequence['Ability']:

    def chasse(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        joueur = message.GetToPlayer() or JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        reine = LaReineEnJeu(effect)
        if reine is None:
            reine = AmenerLaReine(effect, joueur)
        if reine is not None and reine.card.IsOnField():
            reine.CastTo(Enemy).DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            chasse,
        ),
    ]
