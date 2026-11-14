from . import *
# * Keeyah (Leadership, allie 3 [energy], THW 2*, ATK 1*, PV 3). KREE. STARJAMMER.
# [star] Response: After Keeyah uses a basic power, choose another ally → that ally uses the same basic power without exhausting.
# (They take consequential damage as normal.)
#
# Cartes de reference : bw024 (`attaquant.BasicAttack(cibles, effect)`) ; 61023 Grapnel Launcher (`BasicThwart` n'epuise pas de lui-meme :
# « without exhausting » acquis) ; `ally.BasicAttack` / `BasicThwart` : les degats consecutifs de l'allie s'appliquent comme d'habitude.
# « the SAME basic power » : ATQ ou CTR (les allies n'ont pas de recuperation) ; « ANOTHER ally » : pas Keeyah ; l'allie choisi n'a pas besoin
# d'etre pret. Les cibles de ce pouvoir se choisissent dans l'operation (apres l'allie).
def GetAbilities() -> Sequence['Ability']:
    def keeyah(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = JoueurDe(effect)
        if joueur is None or not effect.targets:
            return
        allie = effect.targets[0]
        if message.power == "ATK":
            ennemis = [e for e in Ennemis(effect) if not e.IsDefeated()]
            if ennemis:
                cible = joueur.AskChooseFace(ennemis, effect, prompt="Choose a target for that attack", forced=True)
                allie.CastTo(Ally).BasicAttack([cible or ennemis[0]], effect)
        elif message.power == "THW":
            manigances = [s for s in Worlds.GetOnAllFieldScheme(effect) if s.threat > 0]
            if manigances:
                cible = joueur.AskChooseFace(manigances, effect, prompt="Choose a scheme to thwart", forced=True)
                allie.CastTo(Ally).BasicThwart([cible or manigances[0]], effect)
    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            keeyah,
            powers=["ATK", "THW"],
        ).SetTarget(Ally, check_fn=lambda effect, face: face is not effect.this),
    ]
