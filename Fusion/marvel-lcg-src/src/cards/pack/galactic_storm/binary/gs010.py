from . import *

# Energy Conversion — AMELIORATION, cout 0, [mental]. SUPERPOWER. x2 (Binary 13/15, 14/15).
# Temporary.
# Treat the printed resources of each card in your hand as if they were
#   [energy] resources.
#
# Cartes de reference :
#  - **`ironheart/zzzax/29038`** Haywire : « traiter les cartes en main comme
#    [energy] » = `AbilityFactory.WhenCountingResourcesOnCards(None, op,
#    from_where=...)` + `message.SetReturnValue(Resources(...), effect)`. Ce
#    message part a CHAQUE lecture de `printed_resource` (has_resources.py) :
#    le paiement, `has_printed_res`, `FacesCounter` voient tous la conversion.
#  - **`next_evol/domino/40037a`** Domino : meme fenetre, en gardant le NOMBRE
#    d'icones (Domino double les wild).
#  - Temporary : base automatique lue dans `desc` (fiche `mots-cles/temporary.md`),
#    aucun script.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the printed resourceS of each card » : chaque icone devient [energy], le
#    NOMBRE est garde (Strength RR -> YY ; Haywire, lui, ramene a UNE icone : ne
#    pas recopier). Une carte sans ressource reste sans ressource ; un [wild]
#    devient [energy] (il est imprime, il est donc traite comme [energy]).
#  - « in YOUR hand » : la main du joueur qui controle Energy Conversion,
#    jamais celle d'un autre joueur, jamais le deck ni la defausse (White Hole
#    lit le deck : non touche).
#  - « treat ... as if they were [energy] resources » : vaut pour TOUT ce qui
#    lit la ressource en main, y compris la depense (une Strength payee donne
#    deux [energy]) ; FAQ du livret 1.2 p.22 pour le compte de Cosmic Influx.
#  - Deux exemplaires en jeu : meme effet (pas de cumul possible).
#  - Amelioration sans « Attach to » : `CanPlayThisUpgradeCard()` sans cible.


def GetAbilities() -> Sequence['Ability']:

    def main_du_controleur(effect: 'Effect') -> 'Deck|None':
        joueur = JoueurDeCetteCarte(effect)
        return None if joueur is None else joueur.hand_cards

    def convertir(effect: 'Effect', message: 'Message.WhenCountingResourcesOnCards') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        res = message.return_res
        n = sum(res.GetColor(c, convert_green_res=False) for c in ("R", "B", "Y", "G", "L"))
        if n > 0:
            message.SetReturnValue(Resources("Y" * n), effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenCountingResourcesOnCards(
            None,
            convertir,
            from_where=main_du_controleur,
        ),
    ]
