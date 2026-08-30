from . import *

# Bulldozing Charge — TRAHISON nemesis, custom « CptScorp »
# 1 icone de bonus + une capacite de bonus etoilee. Deux exemplaires
# physiques : pt021 et pt022, meme texte, meme code.
#
# When Revealed: Mr. Hyde attacks you. If no attack was made this way, deal 1
#   damage to each friendly character.
# ---
# [star] Boost: If this card resolves during an attack, this attack gains
#   overkill.
#
# ---------------------------------------------------------------------------
# LE WHEN REVEALED
#
# Carte de reference : `02040` Tail Sweep, qui imprime EXACTEMENT la meme
# structure (« Scorpion attacks your hero. If no attack was made this way,
# you are stunned. ») et s'ecrit :
#   1. `Worlds.FindCardOnField(effect, name=..., card_type=Enemy)` ;
#   2. si trouve -> `enemy.DoAttackYou(player, effect,
#      if_no_attack_was_made=action)` ;
#   3. sinon -> `action()` directement.
# `22031` Old Rivals fait de meme.
#
# Le repli part donc dans DEUX cas : Mr. Hyde n'est pas en jeu, ou il est en
# jeu mais l'attaque n'a pas eu lieu (joueur en identite civile, attaque
# annulee...).
#
# « ATTACKS **YOU** » : le joueur a qui la carte est distribuee,
# `message.GetToPlayer()`.
#
# « DEAL 1 DAMAGE TO **EACH FRIENDLY CHARACTER** » : les identites ET les
# allies de TOUS les joueurs (`Worlds.GetOnFieldFriendlyCharacters`), pas
# seulement ceux du joueur vise — le texte ne dit ni « your », ni « you
# control » (mot-piege `each` du PROCESSUS-CARTE §5 : ne pas restreindre une
# portee qui n'est pas restreinte). En solo la difference est nulle, en
# multijoueur elle est majeure.
#
# ---------------------------------------------------------------------------
# « [star] BOOST: IF THIS CARD RESOLVES DURING AN ATTACK, THIS ATTACK GAINS
# OVERKILL »
#
# Carte de reference : `16134` Kree Private et `wd066` Scaly Setback, toutes
# deux ecrites `WhenCardBecomeBoost("This", fn, during_attack=True)` avec
# `message.would_atk_message.GainOverKill(effect)`.
#
# `during_attack=True` PORTE la condition « si cette carte se resout pendant
# une attaque » : hors d'une attaque, la fabrique ne declenche rien et
# `would_atk_message` n'est jamais lu. C'est la raison pour laquelle il n'y a
# aucune garde a ecrire dans le corps.


def GetAbilities() -> Sequence['Ability']:

    def bulldozing_charge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()

        def degat_a_chaque_personnage_ami():
            amis = list(Worlds.GetOnFieldFriendlyCharacters(effect))
            if amis:
                this.DealDamage(amis, 1, effect)

        hyde = Worlds.FindCardOnField(effect, name=NOM_MR_HYDE, card_type=Enemy)
        if hyde:
            hyde.DoAttackYou(joueur, effect,
                             if_no_attack_was_made=degat_a_chaque_personnage_ami)
        else:
            degat_a_chaque_personnage_ami()

    def bulldozing_charge_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bulldozing_charge,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            bulldozing_charge_boost,
            during_attack=True,
        ),
    ]
