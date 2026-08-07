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
# SECONDE CAPACITE (ecrite le 7/8/2026, apres tranchage utilisateur) :
# « that ally deals damage to you equal to its ATK instead ». Aucune carte du
# depot ne retourne un allie controle par le joueur contre son propre heros --
# toutes les redirections trouvees (Maniac 74013, Cull the Weak 76015,
# Leaping Kick 50096) affectent un allie ou en discutent la defausse, jamais
# son ATK inflige a SON PROPRE controleur. Deux points ont ete tranches par
# l'utilisateur (§4.1 du guide, question posee avant d'ecrire le script) :
#   1. Quel allie si le joueur en controle plusieurs ? DECISION : le joueur
#      choisit lui-meme, comme toute carte qu'il controle et qui n'est pas
#      visee nommement. Precedent officiel : Electric Whip Attack
#      (core/iron_man_nemesis/01173.py), traitrise qui fait deja choisir au
#      joueur laquelle de ses propres ameliorations elle affecte via
#      `player.ChooseAbilities` + `.SetTarget(Upgrade,
#      from_where=["YouControlCards"], ...)`. Meme mecanique ici, portee sur
#      Ally : `.SetTarget(Ally, from_where=["YouControlCards"])` sur
#      l'ability elle-meme (pas besoin de `ChooseAbilities`, il n'y a qu'une
#      seule branche -- cf. `79001a`, deja de ce pack, qui fait de meme avec
#      `.SetTarget(Enemy)` sur une Response). Qui choisit est determine par
#      `Select.GetYou` (selector/factory.py:48) : pour une capacite portee
#      par un Minion, « You » resout deja vers
#      `effect.this.GetEngagedPlayer()` -- le joueur attaque par Faustus,
#      pas le camp de la rencontre. Coherence verifiee avec la capacite 1,
#      qui lit le meme « vous » via `this.engaged_player`.
#   2. L'allie subit-il quelque chose au passage ? DECISION : rien d'autre ne
#      lui arrive -- lecture litterale du texte imprime, aucune consequence
#      codee sur l'allie apres qu'il ait inflige ses degats.
# Remplacement et non ajout (point 3 du message du coordinateur) : meme
# mecanique que « that enemy schemes instead » de Parting Shots (79005 de ce
# pack) et d'Invisibility Gear (51019, officiel), `message.SetBeInstead(effect)`
# sur le `WhenUnitWouldAttack` annule l'attaque de Faustus avant que le
# substitut ne s'execute.
# Valeur des degats : `allie.attack` (ATK COURANTE, amelioration comprises),
# PAS `allie.printed_attack` -- meme distinction que `hero.thwart` dans
# 79014 de ce meme pack.
# Si le joueur ne controle aucun allie, la capacite ne s'applique pas et
# Faustus attaque normalement : gere par une condition explicite
# (`faustus_a_un_allie`) plutot que par la seule absence de cible legale du
# `.SetTarget()`, pour ne jamais exposer un Forced a une resolution de cible
# vide -- meme prudence que la condition de la capacite 1.

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

    def faustus_a_un_allie(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        return bool(joueur.allies.Get())

    def faustus_allie_encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        allie = effect.targets[0].CastTo(Ally)
        joueur = message.GetAgainstPlayer()

        message.SetBeInstead(effect)
        allie.DealDamage([joueur.GetIdentity()], allie.attack, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            faustus_prevent_damage,
            conditions=[faustus_cannot_take_damage],
        ),

        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            faustus_allie_encaisse,
            against_player="You",
            conditions=[faustus_a_un_allie],
        ).SetTarget(Ally, from_where=["YouControlCards"]),
    ]
