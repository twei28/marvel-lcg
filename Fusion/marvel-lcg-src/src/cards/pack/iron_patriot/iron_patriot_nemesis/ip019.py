from . import *

# Assembled Resistance — TRAITRISE de nemesis (4/5), x2. Boost 2.
# When Revealed (Alter Ego): Reveal the top card of the REGISTERED deck and put
#   it into play engaged with you.
# When Revealed (Hero): The friendly character with the most remaining hit
#   points attacks you. If no attack was made this way, this card gains surge.
#
# CARTES DE REFERENCE
#  - `02029` Death from Above : DEUX `WhenThisRevealed`, l'une "Alter-Ego",
#    l'autre "Hero". C'est la fabrique qui trie sur la forme, pas le module.
#  - `ip002a` Registration Act : la revelation du deck REGISTERED, deja
#    outillee par `RevelerEtProposerLeRecrutement`.
#  - `ag001a` Agent 13 / `al014` : `unite.BasicAttack([cible], effect)`, et
#    surtout son rappel `if_no_attack_was_made=`, qui EST la derniere phrase de
#    la carte. `DoAttackYou` ne convient PAS ici : elle n'existe que sur les
#    ENNEMIS (can_attacked.py:31 en rend None), et l'attaquant est ami.
#
# TEXTE CONTRE CODE
#  ⚠⚠ La face ALTER EGO revele le sbire MAIS NE PROPOSE PAS DE LE PAYER : le
#    texte s'arrete a « put it into play engaged with you ». C'est une
#    punition, pas un cadeau. D'ou `a_la_fin_du_round=False` ET l'absence
#    d'offre — on appelle donc la revelation SANS passer par le helper de
#    recrutement.
#  ⚠ « THE FRIENDLY CHARACTER with the most remaining hit points » : un seul,
#    le mieux portant, allies ET identite confondus. Egalite : le moteur n'en
#    designe pas, on prend le premier trouve — aucune carte du jeu ne tranche
#    ce cas, et l'ecart est sans consequence mesurable.
#  ⚠ « attacks YOU » : il attaque L'IDENTITE du joueur, pas le vilain. Un allie
#    retourne contre son camp.
#  ⚠ « If NO ATTACK WAS MADE this way » : le moteur le dit lui-meme, par le
#    rappel `if_no_attack_was_made` de `BasicAttack` — qui couvre aussi le cas
#    ou le personnage designe ne PEUT pas attaquer (`IsCanAttack` faux, par
#    exemple `ip018` Cabal Obligations sur un allie REGISTERED). On n'essaie
#    pas de deviner ce cas, on le laisse repondre.
#  ⚠ L'identite est elle-meme un personnage ami : si le joueur est seul et le
#    mieux portant, il s'attaque lui-meme. C'est ce qui est ecrit.


def GetAbilities() -> Sequence['Ability']:

    def cote_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        RevelerLeDessusDuDeckRegistered(joueur, effect)

    def cote_heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            this.GainSurge(1, effect)
            return
        candidats = [f for f in [identite, *joueur.allies.Get()]
                     if f is not None and f.IsInPlay()]
        if not candidats:
            this.GainSurge(1, effect)
            return

        def aucune_attaque() -> None:
            this.GainSurge(1, effect)

        mieux_portant = max(candidats, key=lambda f: f.CastTo(Unit2).health)
        mieux_portant.CastTo(Unit2).BasicAttack(
            [identite], effect, if_no_attack_was_made=aucune_attaque)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            cote_alter_ego,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            cote_heros,
        ),
    ]
