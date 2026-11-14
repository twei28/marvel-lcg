from . import *

# Zombie Human Torch — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). FANTASTIC. SCH 1.
# ATK 2. PV 5. Guard. Villainous. Boost 2.
# Guard. Villainous.
# Forced Response: After this minion deals damage with an attack, deal 1 damage to each ally controlled by
# the attacked player.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, `desc.Guard` = "1". Aucun script requis.
# - [[villainous]] (mots-cles/villainous.md) : BASE NATIVE, `desc.Villainous` = "1" (meme statut deja constate
#   sur `hg063`/`hg067` par l'autre agent, meme pack). Aucun script requis -- ce mot-cle ne fait QUE changer la
#   facon dont le moteur annonce la carte (vilain-type) ; il n'ajoute aucune regle de jeu a coder ici.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After this minion deals damage with an attack » : `AbilityFactory.AfterUnitAttackAndDamageUnit
#   (ForcedResponse, "This", CardFinder(card_type=Identity|Ally), op, target_in_play=True)`, modele EXACT
#   `hg010` Zombie Spider-Man (meme pack, meme fabrique, meme cible generique Identity|Ally puisque Zombie
#   Human Torch n'attaque QUE l'identite ou un allie defenseur -- deux seules cibles possibles d'une attaque de
#   sbire) ; `hg010` filtrait en plus sur `Hero` ("a hero", texte different), ici le texte dit "an attack" sans
#   restriction de cible, donc Identity|Ally generique comme `hg009`/`hg012`.
# - « deal 1 damage to EACH ALLY controlled by THE ATTACKED PLAYER » : `message.GetToPlayer()` puis
#   `joueur.GetControlAllies()` + `this.DealDamage(allies, 1, effect)`, modele EXACT `hg012` Zombie Thor (meme
#   pack : « deal 1 damage to each ally that player controls », meme paire d'appels) -- seule la SOURCE du
#   joueur differe : `hg012` lit `message.GetAgainstPlayer()` sur un message d'ACTIVATION
#   (`AfterEnemyActivationEnd`), ici `message.GetToPlayer()` sur un message d'ATTAQUE
#   (`AfterUnitAttackUnit`), qui rend le meme concept (« le joueur vise ») pour le message different utilise par
#   cette carte -- confirme par le commentaire natif de la fabrique (`do_attack.py:391-409`, citation : « For
#   abilities that trigger "after [enemy] attacks you," "you" refers to the attacked player, even if that
#   player defended with an ally » -- exactement la lecture de « the attacked player » retenue ici) et par
#   `sender_damage.py:541` (`AfterUnitAttackUnit` recoit `player=would_atk_message.property.against_player`,
#   donc `GetToPlayer()` rend bien le joueur CIBLE de l'attaque, pas l'allie qui a defendu a sa place).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. Villainous. » -> natifs, rien a coder.
# « After this minion deals damage WITH AN ATTACK » -> `AfterUnitAttackAndDamageUnit` EXIGE deja des degats
#   reellement infliges (`target_took_damage=True` interne a la fabrique, voir `do_attack.py:477-509`) : pas de
#   garde supplementaire a ecrire si l'attaque est annulee, reduite a 0 par Toughness, etc.
# « deal 1 damage to EACH ally » -> `this.DealDamage(allies, 1, effect)` sur la LISTE entiere des allies du
#   joueur vise : chaque allie recoit separement 1 degat (pas un degat partage), comme sur `hg012`. Liste vide
#   (joueur sans allie) -> `DealDamage` sur une liste vide ne fait rien, natif, pas de garde manuelle.
# « controlled by THE ATTACKED PLAYER » -> uniquement les allies du joueur VISE par CETTE attaque precise
#   (`GetControlAllies()` appele sur `message.GetToPlayer()`), jamais tous les allies de la table ni ceux d'un
#   autre joueur -- important en multijoueur, meme piege deja documente sur `hg012`.
# `target_in_play=True` (modele `hg010`) : si la cible attaquee est deja hors jeu au moment du Forced Response
#   (cas limite, vaincue entre-temps par un effet simultane), aucun degat supplementaire n'est inflige a ses
#   allies pour autant -- en realite ce garde-fou porte sur `message.attacked`, la cible ATTAQUEE, pas sur les
#   allies vises par CETTE capacite (qui restent toujours en jeu au moment ou on leur infligerait des degats,
#   `DealDamage` etant lui-meme sans danger sur une carte sortie). Conserve par coherence avec le modele, sans
#   effet pratique different.
#
# Bloc nombres texte <-> code : "1 damage" -> `this.DealDamage(allies, 1, effect)`, seule valeur numerique du
# script, identique au texte imprime et a `data/cards_custom.json`.


def GetAbilities() -> Sequence['Ability']:

    def human_torch_degats(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        allies = joueur.GetControlAllies()
        this.DealDamage(allies, 1, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            CardFinder(card_type=Identity|Ally),
            human_torch_degats,
            target_in_play=True,
        ),
    ]
