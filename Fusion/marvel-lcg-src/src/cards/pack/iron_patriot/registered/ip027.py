from . import *

# * Moonstone — SBIRE du deck REGISTERED (14/20). 5 PV, ATQ 2, MNG 2, boost 3.
# AERIAL. AVENGER. ELITE.
# Stalwart. Toughness.
# [star] Forced Response: After Moonstone attacks and defeats a character, give
#   her a tough status card.
# Psych Evaluation — Special: Choose 1 other friendly character you control ->
#   heal 2 damage from that character and give them a tough status card.
#
# CARTE DE REFERENCE
#  - `01131` * Tiger Shark : « After Tiger Shark attacks, give him a tough
#    status card » — meme geste, `Faces.GiveStatus([this], "Tough", effect)`.
#    Ici en plus, l'attaque doit AVOIR VAINCU quelqu'un.
#
# TEXTE CONTRE CODE
#  ⚠ « attacks and DEFEATS a character » : pas « damages ». Une attaque qui
#    blesse sans tuer ne donne rien. C'est la difference avec `ip026`.
#  ⚠ « give HER » : Moonstone elle-meme.
#  ⚠ « Choose 1 OTHER friendly character » : pas elle. `non_face` l'exclut.
#  ⚠ « YOU CONTROL » : ses propres personnages, pas ceux des autres joueurs.
#  ⚠ « heal 2 damage AND give them a tough » : les deux, pas au choix.
#  ⚠ « -> » sans cout devant : la fleche separe ici la cible de l'effet.
#  ⚠ Stalwart et Toughness sont des BASES NATIVES.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.


def GetAbilities() -> Sequence['Ability']:

    def se_blinder(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this
        Unused(message)
        Faces.GiveStatus([this], "Tough", effect)

    def evaluation_psy(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        candidats = un_autre_personnage_ami(effect)
        if not candidats:
            return
        cibles = joueur.AskChooseFaces(
            candidats, (1, 1), effect,
            prompt="Choose 1 other friendly character you control")
        if not cibles:
            return
        for cible in cibles:
            cible.CastTo(Unit2).HealHealth(2, effect)
        Faces.GiveStatus(cibles, "Tough", effect)

    def un_autre_personnage_ami(effect: 'Effect') -> Sequence['CardFace']:
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return [f for f in joueur.GetControlCharacters()
                if f is not None and f is not effect.this]

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            "This",
            Unit2,
            se_blinder,
            is_from_attack=True,
        ),
        SpecialRegistered("Psych Evaluation", evaluation_psy),
    ]
