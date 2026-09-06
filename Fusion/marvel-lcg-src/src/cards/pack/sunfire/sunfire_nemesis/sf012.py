from . import *

# * Silver Samurai — SBIRE nemesis (N 2/5). CRIMINAL. ELITE. HAND. UNIQUE.
#   MNG 2 / ATQ 2 — 4 PV, 3 icones de boost. Quickstrike. Retaliate 1.
# Forced Interrupt: When Silver Samurai enters play, if it is not in play,
#   find Silver Samurai's Katana and attach it to him.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `quickstrike` (mots-cles/quickstrike.md) : BASE AUTOMATIQUE,
#    `desc.Quickstrike = "1"`. AUCUN SCRIPT.
#  - `retaliate` (mots-cles/retaliate.md) : BASE AUTOMATIQUE,
#    `desc.Retaliate = "1"`. AUCUN SCRIPT.
#  - ⚠ `ELITE` N'EST PAS UN MOT-CLE, c'est un TRAIT : il va dans `traits`,
#    jamais dans `desc` (encadre du README des mots-cles).
#
# CARTES DE REFERENCE
#  - `tg013` * Alligator Loki : « find <attachement> and attach it ».
#    ⚠ MAIS `Find.FindAndAttachTo` NE SUFFIT PAS ICI : elle passe par
#    `Find.Find`, qui ne voit pas `set_aside_nemesis_sets` — la pile ou
#    vivent les cinq cartes nemesis avant d'entrer en jeu. La katana n'y
#    etait jamais trouvee et la carte etait MORTE. Voir `TrouverCarteDuSet`
#    dans le `__init__.py` du set nemesis. Trouve par le cas le 06/09/2026.
#
# TEXTE CONTRE CODE
#  ⚠ « IF IT IS NOT IN PLAY » -> « it » designe LA KATANA, pas Silver Samurai
#    (qui vient justement d'entrer en jeu, la clause serait absurde). La
#    lecture est confirmee par `sf014` : la katana peut deja etre en jeu,
#    posee sur lui par sa propre clause « Attach to Silver Samurai ». Sans ce
#    test, un Silver Samurai qui revient par `sf011` Hand Ambush chercherait
#    une seconde katana.
#  ⚠ « FIND » couvre le deck de rencontre, sa defausse ET le terrain : c'est
#    ce que fait `Find.FindAndAttachTo`, et c'est pourquoi le test « pas deja
#    en jeu » est necessaire.
#  ⚠ FORCED INTERRUPT a l'entree en jeu : la katana est donc la AVANT la
#    premiere activation, et le +1 ATQ compte des le premier coup.
#  `desc.Nemesis = "Sunfire"` marque ce sbire comme LE sbire nemesis du heros,
#    ce que `01190` Shadow of the Past va chercher.


def GetAbilities() -> Sequence['Ability']:

    def la_katana_est_en_jeu(effect: 'Effect') -> bool:
        return Worlds.FindCardOnField(
            effect, name=NOM_KATANA, card_type=Attachment) is not None

    def convoquer_la_katana(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        # « IF IT IS NOT IN PLAY » : « it » = la katana. Voir l'encadre.
        if la_katana_est_en_jeu(effect):
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        # ⚠ PAS `Find.FindAndAttachTo` : elle passe par `Find.Find`, qui ne
        # voit PAS le set nemesis mis de cote (voir `TrouverCarteDuSet`).
        katana = TrouverCarteDuSet(effect, joueur, NOM_KATANA, Attachment)
        if katana is not None:
            katana.AttachTo2(this, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedInterrupt,
            "This",
            convoquer_la_katana,
        ),
    ]
