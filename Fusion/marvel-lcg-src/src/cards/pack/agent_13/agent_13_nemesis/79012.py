from . import *

# Doctor Faustus — custom « Rainy » (nemesis d'Agent 13 / Sharon Carter)
# Doctor Faustus cannot take damage while you are engaged with another
#   minion.
# [star] Forced Interrupt: When Doctor Faustus would attack you while you
#   control an ally, that ally deals damage to you equal to its ATK instead.
#
# PREMIERE CAPACITE (ecrite) : « cannot take damage while you are engaged
# with another minion ». Le declencheur suit Jessica's Jacket (jessica_jones/
# jessica_jones/73010.py) pour la forme « would take any amount of damage »
# et Mysterio (spider_man_rainy/spider_man_rainy_nemesis/71015.py) pour le
# remplacement total via `message.PreventDamage("All", effect)`
# (sender_damage.py:808), pose ici SOUS CONDITION plutot qu'inconditionnel.
# La condition lit `this.engaged_player` (card_type/minion.py:157, None si
# Faustus n'est engage avec personne) puis `joueur.GetEngagedMinions()`
# (player/action/player_get.py:175) filtree pour exclure Faustus lui-meme :
# « un AUTRE sbire » exige qu'il en reste au moins un apres exclusion.
#
# SECONDE CAPACITE (NON ECRITE, bloquee) : « that ally deals damage to you
# equal to its ATK instead ». Aucune carte du depot ne retourne un allie
# controle par le joueur contre son propre heros -- toutes les redirections
# trouvees (Maniac 74013, Cull the Weak 76015, Leaping Kick 50096) affectent
# un allie ou en discutent la defausse, jamais son ATK inflige a SON PROPRE
# controleur. Deux points bloquent un montage sans arbitrage, signales par le
# brief et par le §4.1 du guide (« en cas de doute, DEMANDER, carte par
# carte ») :
#   1. Quel allie si le joueur en controle plusieurs ? Le depot n'a pas de
#      precedent net : `Filter.One(..., most_remaining_hp=True)` existe pour
#      un CHOIX AUTOMATIQUE deterministe (ex. Leaping Kick), mais des
#      obligations comme Care for Cassie (12025) et Power Absorption (69015)
#      laissent le JOUEUR choisir la carte qu'il perd parmi les siennes
#      (`player.ChooseAbilities` / `AskDiscardFaces`). Les deux lectures
#      changent le jeu differemment (le joueur sacrifie son allie le plus
#      faible s'il choisit, le plus fort si c'est automatique-au-pire).
#   2. L'allie qui inflige les degats subit-il lui-meme quelque chose au
#      passage (epuisement, degat de retour...) ou le texte imprime est-il
#      lu a la lettre (rien d'autre ne lui arrive) ?
# Reserve consignee dans le rapport de tache 5 : cette seconde capacite
# n'apparait PAS dans `GetAbilities()` tant que ces deux points n'ont pas
# ete tranches par l'utilisateur, conformement au §4.1 (« poser la question
# avant d'ecrire le script, pas apres »).

def GetAbilities() -> Sequence['Ability']:

    def faustus_cannot_take_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Minion)
        joueur = this.engaged_player
        if joueur is None:
            return False
        autres = [m for m in joueur.GetEngagedMinions() if m != this]
        return len(autres) > 0

    def faustus_prevent_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            faustus_prevent_damage,
            conditions=[faustus_cannot_take_damage],
        ),
    ]
