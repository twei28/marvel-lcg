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
# SECONDE CAPACITE (ecrite le 7/8/2026, corrigee le meme jour apres un echec
# reel de montee de partie) : « that ally deals damage to you equal to its
# ATK instead ». Deux points ont ete tranches par l'utilisateur (§4.1 du
# guide, question posee avant d'ecrire le script) :
#   1. Quel allie si le joueur en controle plusieurs ? DECISION : le joueur
#      choisit lui-meme.
#   2. L'allie subit-il quelque chose au passage ? DECISION : rien d'autre ne
#      lui arrive -- lecture litterale du texte imprime.
#
# CORRECTIF (7/8/2026, apres verifier_tous_les_decks.py) : la premiere
# version posait `.SetTarget(Ally, from_where=["YouControlCards"])`
# DIRECTEMENT sur l'ability portee par Faustus. `Ability.Initialize`
# (ability.py:167) l'interdit formellement pour toute ability dont le
# porteur (`this`) est un `Enemy` (Villain ou Minion) :
# `assert self.selectors == [], f"{this=}"`. `test_cards.py`,
# `verifier_api_cartes.py` et `verifier_coherence_cartes.py` ne l'ont jamais
# vu : ces trois outils construisent des capacites ou verifient des noms
# d'API, ils ne montent jamais de partie et n'appellent jamais
# `Ability.Initialize` sur une capacite d'ennemi en conditions reelles.
# Seul `verifier_tous_les_decks.py`, qui monte reellement une partie avec le
# deck `agent_13`, a fait planter le setup sur `this=[(04,79012) Doctor
# Faustus]` -- l'assertion se declenche des l'initialisation de la capacite,
# avant meme qu'elle se declenche en jeu.
#
# Une carte de rencontre NE PEUT PAS faire choisir une cible au joueur en
# posant `.SetTarget()` sur sa PROPRE ability. Le patron correct, utilise
# partout au depot des qu'un joueur doit choisir une de ses propres cartes en
# reponse a un effet adverse (Electric Whip Attack, core/iron_man_nemesis/
# 01173.py, traitrise qui fait choisir au joueur laquelle de ses ameliorations
# elle affecte ; Hex Bolt, scw/scarlet_witch/15004.py, qui pose `.SetTarget()`
# sur un `ForChoiceAbility` plutot que sur l'ability portante) : le
# `.SetTarget()` se pose sur un `AbilityFactory.ForChoiceAbility(...)` passe
# a `joueur.ChooseAbilities(effect, ...)`. Verifie en lisant
# `player_action.py:184-219` : `ChooseAbilities` construit un NOUVEL `Effect`
# via `Effect(identity, ability, world=by_effect.world)` -- `identity` (la
# face Hero/AlterEgo du joueur choisissant) devient le `this` de CETTE
# capacite-la, pas Faustus. `identity` n'est pas de type `Enemy` : l'assertion
# ne s'applique plus, et le `.SetTarget(Ally, from_where=["YouControlCards"])`
# porte desormais sur une capacite dont le porteur est bien un joueur.
#
# Remplacement et non ajout (point 3 du message du coordinateur) : validation
# inchangee, meme mecanique que « that enemy schemes instead » de Parting
# Shots (79005 de ce pack) et d'Invisibility Gear (51019, officiel),
# `message.SetBeInstead(effect)` sur le `WhenUnitWouldAttack` annule
# l'attaque de Faustus avant que le substitut ne s'execute.
# Valeur des degats : `allie.attack` (ATK COURANTE, amelioration comprises),
# PAS `allie.printed_attack` -- meme distinction que `hero.thwart` dans
# 79014 de ce meme pack.
# Si le joueur ne controle aucun allie, la capacite ne s'applique pas et
# Faustus attaque normalement : gere par une condition explicite
# (`faustus_a_un_allie`, sur l'ability de Faustus -- une simple fonction de
# condition n'est PAS un selecteur, l'assertion ne la concerne pas) plutot
# que par la seule absence de cible legale du `.SetTarget()` interne, pour ne
# jamais exposer un Forced a une resolution de cible vide -- meme prudence
# que la condition de la capacite 1.

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
        joueur = message.GetAgainstPlayer()

        message.SetBeInstead(effect)

        def infliger_les_degats(targets: Sequence['CardFace']) -> None:
            allie = targets[0].CastTo(Ally)
            allie.DealDamage([joueur.GetIdentity()], allie.attack, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Choose an ally to deal you damage equal to its ATK instead",
                infliger_les_degats,
            ).SetTarget(Ally, from_where=["YouControlCards"]),
        )

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
        ),
    ]
