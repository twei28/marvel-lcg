from . import *

# * Duality Aspect : AMELIORATION (CONDITION.), PERMANENT, sans cout, [wild]. Classe Hero.
# Permanent.
# Forced Response: After you place a balance counter here, if there are 3+ balance counters here → find Void and reveal him. (If he is already in play, he engages you.)
# Forced Response: After the "Special" ability on a SPLIT card is resolved → shuffle that card into your deck. Then, you may remove 1 balance counter from here.
#
# CARTES DE REFERENCE
#  - Permanent : lu dans `desc` (`Permanent`), aucun code (fiche `permanent.md`).
#  - « After you place a counter here, if there are N+ » : `AbilityFactory.AfterCounterPlacedOn(ForcedResponse, "This", 'balance', op, at_least=3)` (`game/ability/factory/counter.py`).
#  - « Find X and reveal him » : `ca016` Meticulous Targeting (helper `TrouverEtRevelerVoid`).
#  - « After the Special ability on a card is resolved » : `AfterPlayerResolveAbility(.., which_abilities=["Special"])` (RECETTES §27, modele `rz007`).
#
# TEXTE CONTRE CODE
#  « AFTER you place a balance counter HERE » : seulement les compteurs poses SUR cette carte (un compteur detourne par The Watchtower ne declenche rien). « 3+ HERE » : sur cette
#  carte, pas « en jeu ». « he engages YOU » : le joueur de Duality Aspect. « Void » : introuvable -> rien. « SPLIT card » : trait SPLIT, resolue PAR N'IMPORTE QUI (le Void la resout aussi) ;
#  la carte est remelangee dans le deck du joueur SENTRY (proprietaire), pas du Void. « you MAY remove 1 » : la suite est facultative.
#  Chiffres : aucun cout, un seul exemplaire (Permanent).


def GetAbilities() -> Sequence['Ability']:

    def reveler_le_void(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            TrouverEtRevelerVoid(effect, joueur)

    def remelanger_puis_retirer(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        joueur = JoueurDeCetteCarte(effect)
        carte = message.trigger
        if joueur is None or carte is None:
            return
        RemelangerOuGlisser(effect, joueur, carte)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 balance counter from Duality Aspect",
                lambda cibles: RetirerEquilibre(effect, 1),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Do not remove a counter",
                lambda cibles: None,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.ForcedResponse,
            "You",
            None,
            remelanger_puis_retirer,
            which_abilities=["Special"],
            conditions=[lambda effect, message: message.trigger is not None and message.trigger.HasTrait("SPLIT")],
        ).SetName("Reshuffle"),
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedResponse,
            "This",
            NOM_EQUILIBRE,
            reveler_le_void,
            at_least=3,
        ).SetName("Void"),
    ]
