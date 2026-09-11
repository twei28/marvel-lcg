from . import *

# Crisis Averted

def GetAbilities() -> Sequence['Ability']:

    def crisis_averted(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        if effect.GetPaidResources().HasColor("B"):
            ignore_crisis = True
        else:
            ignore_crisis = False

        this.RemoveThreatFromSchemes(effect.targets, 6, effect, ignore_crisis=ignore_crisis)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            crisis_averted,
        ).SetPlay().SetLabel('thwart')
        # ⚠ IGNORANCE DECLAREE SANS CONDITION, ET C'EST VOULU (11/09/2026).
        #
        # Depuis que la Crise verrouille la CIBLE (`MainScheme.CanBeThwartBy`),
        # un contre ne peut plus viser le complot principal tant qu'une icone
        # de crise est en jeu, sauf s'il declare ignorer la Crise.
        #
        # Or cette carte-ci ne l'ignore QUE si elle a ete payee avec une
        # ressource mentale, et le paiement vient APRES le ciblage
        # (`effect_checker` : `check_target` puis `check_pay`). Au moment ou
        # le moteur calcule les cibles legales, la reponse n'existe pas
        # encore. Une declaration conditionnelle serait donc soit fausse, soit
        # impossible a evaluer.
        #
        # On declare donc l'ignorance INCONDITIONNELLEMENT : la carte reste
        # ciblable, exactement comme avant le verrou, et c'est la RESOLUTION
        # qui tranche selon les ressources reellement depensees (le `if` plus
        # haut). Consequence assumee : payee sans mental sous une Crise, elle
        # ne retire rien. C'est le texte de la carte, et le joueur choisit ses
        # ressources en connaissance de cause — le bandeau « Crise » du
        # plateau le lui rappelle.
        .SetIgnoreKeyword('Crisis')
        .SetTarget(MainScheme)
    ]

