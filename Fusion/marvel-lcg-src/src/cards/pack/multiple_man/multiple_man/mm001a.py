from . import *

# Multiple Man (face HEROS) : X-FACTOR. THW 1 / ATQ 1 / DEF 1, main 5, PV 9.
# When an effect targets "You" or "Your Hero" or "Your Identity" you may have it target a Dupe ally in play instead.
# Makin' Dupes — Action: Exhaust Multiple Man, discard 1 card → search your deck, hand, and discard pile for a Dupe ally and put it into play. (Limit once per round.)
# + les bonus des trois complots annexes joueur « While <X> is in the victory display » (Madrox Prime +1 ATK et Makin' Dupes sans epuiser ; Madrox Agent of S.H.I.E.L.D. +1 THW, trait S.H.I.E.L.D., limite
#   d'allies +1 ; Prepare For Future Tragedy +1 DEF et Tenace pour les Dupe).
#
# CARTES DE REFERENCE
#  - Substitution de cible : `41028` / `ca022` / `gmw16019` (`WhenUnitWouldAttackUnit` + `message.ChangeTarget`), `nt007` (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", ..)` + `PreventDamage("All")`).
#  - Makin' Dupes : `ar010` (`CostFunc.Discard("YourHandCards", range=(1, 1))`), `CostFunc.Custom` (epuisement conditionnel, `27150`), `Search.PlayerCard(.., include_player_hand_cards=True)`.
#  - Bonus en zone de victoire : RECETTES §3bis + `conan/__init__::CapacitesCitadelle` (`ThisGainKeyword(fn, .., change_on_event=OnEvent.Victory(..))` sur l'IDENTITE).
#
# TEXTE CONTRE CODE
#  « you MAY have it target a Dupe ally INSTEAD » : remplacement FACULTATIF. (1) une ATTAQUE ennemie dirigee contre l'identite -> `ChangeTarget(dupe)` ; la cible du Dupe est un `SetTarget(range=(0, 1))` DECLINABLE
#  (sans cible choisie : rien n'est redirige, le joueur garde l'attaque -- c'est ce qui laisse He's Got This se declencher). (2) des DEGATS d'effet (hors attaque) sur l'identite -> prevenus puis infliges au Dupe.
#  LIMITE DU PORTAGE : les effets sans degats qui ciblent l'identite (soins, statuts) ne sont pas rediriges. « Your Hero »/« Identity » : la face heros porte la capacite, donc seulement en forme heros.
#  Makin' Dupes : UNE capacite (`LimitOncePerRound` natif). Couts : defausser 1 carte (toujours) + epuiser Multiple Man via `CostFunc.Custom` SAUF si Madrox Prime est en zone de victoire (« does not require
#  exhausting »). Le Dupe vient du deck, de la main ou de la defausse ; le deck consulte est melange (RRG « Search »).
#  « +1 ATK » etc. : bonus continus lus dans la zone de victoire (`OnEvent.Victory`). Chiffres : PV 9, main 5, THW/ATQ/DEF 1.


def GetAbilities() -> Sequence['Ability']:

    def dupes_possibles(effect: 'Effect') -> 'List[CardFace]':
        joueur = JoueurDeCetteCarte(effect)
        return [d for d in DupesDuJoueur(joueur) if d.IsInPlay()] if joueur is not None else []

    def attaque_contre_l_identite(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or message.target is not joueur.GetIdentity() or not Enemy.IsType(message.attacker):
            return False
        return bool(dupes_possibles(effect))

    def attaque_vers_un_dupe(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        cibles = [c for c in effect.targets if EstDupe(c) and c.IsInPlay()]
        if cibles:
            message.ChangeTarget(cibles[0], effect)

    def degats_d_effet_sur_l_identite(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return bool(dupes_possibles(effect)) and message.will_take_damage > 0

    def degats_vers_un_dupe(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        joueur = JoueurDeCetteCarte(effect)
        dupes = dupes_possibles(effect)
        subi = message.will_take_damage
        if joueur is None or not dupes or subi <= 0:
            return
        choisi = joueur.AskChooseFace(dupes, effect, forced=True) if len(dupes) > 1 else dupes[0]
        if choisi is None:
            return
        message.PreventDamage("All", effect)
        effect.this.DealDamage([choisi], subi, effect)

    def exhaust_si_pas_prime(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        # « Exhaust Multiple Man » : coût, SAUF si Madrox Prime est en zone de victoire (« does not require exhausting »).
        if prime_en_vitrine(effect):
            return True
        joueur = JoueurDeCetteCarte(effect)
        identite = joueur.GetIdentity() if joueur is not None else None
        if identite is None or identite.IsExhaust():
            return False
        Faces.ExhaustAll([identite], effect)
        return True

    def makin_dupes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        ChercherEtMettreUnDupe(effect, joueur)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.HeroInterrupt,
            Unit2,
            Unit2,
            attaque_vers_un_dupe,
            conditions=[attaque_contre_l_identite],
        ).SetName("Dupe stand-in").SetTarget(finder=CardFinder(card_type=Ally, name=NOM_DUPE), range=(0, 1)),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            degats_vers_un_dupe,
            is_from_attack=False,
            conditions=[degats_d_effet_sur_l_identite],
        ).SetName("Dupe stand-in (effect damage)"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            makin_dupes,
        ).SetName("Makin' Dupes")
        .LimitOncePerRound()
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1)))
        .SetCostFunc(CostFunc.Custom(None, exhaust_si_pas_prime)),
        # Bonus en zone de victoire, sur le HEROS
        BonusStatsHeros(NOM_PRIME, attack=1),
        BonusStatsHeros(NOM_AGENT, thwart=1),
        BonusStatsHeros(NOM_TRAGEDY, defense=1),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", trait="S.H.I.E.L.D", condition=agent_en_vitrine, change_on_event=OnEvent.Victory(CardFinder(name=NOM_AGENT))),
        *CapacitesCommunesIdentite(),
    ]
