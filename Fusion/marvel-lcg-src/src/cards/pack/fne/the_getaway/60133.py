from . import *

# Pedestrians
# When Revealed: For each speed counter on the main scheme, choose:
#   • Exhaust a character you control.  • Take 1 indirect damage.
# « a character you control » : un personnage PRET (sinon la branche ne fait
# rien) ; le choix du personnage passe par la cible de la branche.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def incliner(targets: Sequence['CardFace']) -> None:
            prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
            if not prets:
                return
            cible = prets[0] if len(prets) == 1 else joueur.AskChooseFace(prets, effect)
            if cible is not None:
                Faces.ExhaustAll([cible], effect)

        def branches() -> Sequence['Ability']:
            # ⚠ ForChoiceAbility n'a pas de `conditions` (seule la variante
            # WithCost en a) : `condition` est un BOOLEEN evalue a la
            # construction, et branches() est rappelee a chaque compteur.
            un_pret_existe = any(c.IsReady() for c in joueur.GetControlCharacters())
            return [
                AbilityFactory.ForChoiceAbility("Exhaust a character you control", incliner, condition=un_pret_existe),
                AbilityFactory.ForChoiceAbility("Take 1 indirect damage", lambda targets: joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)),
            ]

        PourChaqueCompteurDeVitesse(effect, joueur, branches)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
