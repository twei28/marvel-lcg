from . import *

# Intimidating Roar — AMELIORATION signature, x1 (n/15 = 13).
# SKILL. SUPERPOWER. Cout 1, ressource [mental].
# Hero Response (thwart): After Hulk takes damage from an attack, exhaust
#   Intimidating Roar -> remove 1 threat from a scheme (2 threat instead if
#   you took 3 or more damage).
#
# Cartes de reference :
#  - `aa001a` * Agatha Harkness pour `AfterUnitTookDamage(..., "You", ...,
#    is_from_attack=True)` — et c'est elle qui documente que le montant subi
#    se lit sur le message ;
#  - `ho009` / `sd015` pour `CanPlayThisUpgradeCard()` +
#    `CostFunc.Exhaust("This")`.
#
# ⚠ L'ECART AVEC `Anger` (hk001a), ET IL EST IMPRIME. Anger dit « After Hulk
# takes damage » : tout degat, y compris celui que Hulk s'inflige avec hk006
# Reckless Charge ou hk005 Interception. Intimidating Roar dit « takes damage
# FROM AN ATTACK » : d'ou `is_from_attack=True`, qui inclut automatiquement
# les degats d'overkill (voir la signature, damage.py:95). Les deux cartes du
# meme pack, a deux lettres pres, ne se declenchent donc pas aux memes
# moments.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « (2 threat instead IF you took 3 or more damage) » : « instead », donc
#    2 OU 1, jamais 3. Le montant se lit sur le message
#    (`message.took_damage`), pas sur les PV perdus — une prevention partielle
#    change le nombre reellement subi.
#  - « exhaust ... -> » : la fleche fait de l'epuisement un COUT, donc une
#    fois par round sans redressement.
#  - Le libelle `(thwart)` alimente Sonne/Desoriente.
#  - `Hero Response` : indisponible en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def intimidating_roar(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        # ⚠ Le champ s'appelle `took_damage` (sender_damage.py:892), PAS
        # `damage`. Un `getattr(message, "damage", 0)` aurait rendu 0 en
        # silence et la carte n'aurait JAMAIS donne ses 2 menaces, sans que
        # rien ne le signale. Meme lecture que aa001a.
        subis = message.took_damage
        valeur = 2 if subis >= 3 else 1

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, valeur, effect),
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            intimidating_roar,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
