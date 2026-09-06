from . import *

# Tachyon Whip — ATTACHEMENT nemesis (N 5/5). TECH. WEAPON.
#   Aucune icone chiffree, une icone ETOILE.
# Attach to your hero. Otherwise, this card gains surge. You cannot change to
#   alter-ego form.
# Forced Response: After you use a basic power, take 2 damage.
# Hero Action: Spend [physical][physical] resources -> discard this card.
# [star] Boost: After this activation, reveal this card.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `surge` (mots-cles/surge.md) : ici il n'est PAS une base automatique, la
#    carte le GAGNE quand elle ne trouve pas de heros a qui s'attacher.
#    `ThisCardGainSurge` (cards/pack/__init__.py:100).
#  - `boost` (mots-cles/boost.md) : `desc.Boost = "0"` plus une capacite
#    `WhenCardBecomeBoost`, sans quoi le moteur ne voit AUCUNE etoile.
#
# CARTES DE REFERENCE
#  - `04072` Laser Rifle / `sd020` : la Hero Action de defausse a cout colore.
#  - `AbilityFactory.PlayersCannotChangeForms` (player.py:98) pour la
#    troisieme phrase.
#  - `sn014` : le ★ Boost qui repousse un effet APRES l'activation.
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to YOUR HERO. OTHERWISE, this card gains surge. » -> le fouet ne
#    peut pas s'accrocher a un joueur en forme CIVILE : il est alors defausse
#    avec Deferlement, ce qui revele une carte de plus. Rester en civil ne
#    protege donc pas, cela accelere.
#  ⚠ « You cannot change to ALTER-EGO form » -> `to_form=AlterEgo` : le
#    passage EN CIVIL est interdit, le retour en heros ne l'est pas. La
#    direction est imprimee, et un filtre absent bloquerait les deux.
#  ⚠ « After you use A BASIC POWER, take 2 damage » -> les quatre pouvoirs de
#    base, recuperation comprise... sauf que la recuperation exige la forme
#    civile, elle-meme interdite par la phrase precedente. Les trois pouvoirs
#    de heros sont donc les seuls atteignables, et c'est une consequence du
#    texte, pas une restriction qu'on ajoute.
#  ⚠ « Spend [physical][physical] » -> `Cost("RR")`, cout releve sur le scan
#    (deux poings) et non devine. Lecon Lockjaw.
#  ⚠ « [star] Boost: AFTER THIS ACTIVATION, reveal this card » -> pas
#    « maintenant » : la revelation attend la fin de l'activation en cours,
#    d'ou `RunAt.AfterEnemyActivationEnd` (run_at.py:175), modele `sn014`.
#  ⚠ Le message de boost porte l'activation sur `message.would_atk_message`, A
#    LIRE AVEC `getattr(..., None)` : elle n'existe pas quand le boost sert
#    une MANIGANCE (fiche boost.md).


def GetAbilities() -> Sequence['Ability']:

    def sattacher_ou_deferler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            joueur = JoueurDeCetteCarte(effect)
        heros = None
        if Player.IsType(joueur):
            identite = joueur.GetIdentity()
            if identite is not None and Hero.IsType(identite):
                heros = identite
        if heros is not None:
            this.AttachTo2(heros, effect)
            return
        # « OTHERWISE, this card gains surge. »
        ThisCardGainSurge(effect)

    def cest_mon_hote(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        return Hote(effect.this) is message.trigger

    def morsure_du_fouet(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        hote = Hote(this)
        if hote is not None:
            hote.TakeDamage(this, 2, effect)

    def reveler_apres_lactivation(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        activation = getattr(message, "would_atk_message", None)
        if activation is None:
            return
        joueur = getattr(activation.property, "against_player", None)
        if not Player.IsType(joueur):
            return

        def reveler() -> None:
            this.Reveal(joueur, effect)

        RunAt.AfterEnemyActivationEnd(effect, activation, reveler)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            sattacher_ou_deferler,
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "You",
            to_form=AlterEgo,
        ),
        # ⚠ `None` ET UNE CONDITION, PAS `"YourHero"`. Le litteral passe par
        # `Select.GetYou(effect)`, or `effect.this` est ici une carte de
        # RENCONTRE qui n'appartient a aucun joueur : la Reponse ne partait
        # jamais et le fouet ne mordait pas. Meme lecon que `bk009` Portal
        # (« "You" passe par Select.GetYou, or effect.this est une amelioration
        # attachee a un ENNEMI »). On filtre sur l'HOTE, qui est le seul
        # personnage que la carte nomme. Trouve par le cas le 06/09/2026.
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            None,
            morsure_du_fouet,
            conditions=[cest_mon_hote],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("RR")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            reveler_apres_lactivation,
        ),
    ]
