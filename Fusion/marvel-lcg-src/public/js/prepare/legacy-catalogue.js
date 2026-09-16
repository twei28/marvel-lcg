// legacy-catalogue.js — le raccord entre le catalogue réel et les règles.
//
// `legacy.js` ne connaît rien au jeu : on lui passe des paliers, il répond. Ce
// fichier-ci fabrique ces paliers à partir du vrai catalogue, et c'est tout ce
// qu'il fait. La séparation tient parce qu'ici il n'y a aucune règle, et que
// là-bas il n'y a aucune entrée-sortie.
//
// ⚠ LE RACCORD FRAGILE EST LE NOM DU SCÉNARIO. L'historique des parties
// (`games_history`) ne garde que le nom AFFICHÉ d'un scénario, « Rhino », pas
// son identifiant de fichier. C'est donc par le nom qu'on recolle les deux, et
// `legacy.cleNom` s'occupe de la casse et des accents. Si un jour l'historique
// gardait l'identifiant, ce serait mieux, et ce fichier serait le seul à
// changer.
//
// ⚠ SEUL L'OFFICIEL FAIT LES PALIERS. Les héros fan-made n'ont pas de vague :
// ils ne sont ni verrouillés ni libres, ils s'achètent avec des jetons. Les
// sets modulaires et les défis n'en ont pas non plus.
"use strict";

import { catalog, titreDeVague, vagueDeLExtension } from "./catalog.js";

let _paliers = null;

/** Le libellé d'un palier, dans la langue de l'écran.
 *
 *  La vague 0 est le Set de base, la vague 1 n'a pas de grande boîte à son
 *  ouverture (voir BORNES_VAGUES) : toutes deux ont un libellé à nous. Les
 *  autres portent le titre imprimé sur la boîte, qui ne se traduit pas. */
export function nomDePalier(vague, t = (x) => x) {
    if (vague === 0) return t("Set de base");
    const titre = titreDeVague(vague);
    return titre ? `${t("Vague")} ${vague} · ${titre}` : `${t("Vague")} ${vague}`;
}

/** Les douze paliers, dans l'ordre, prêts pour `legacy.parcours`.
 *
 *  Coûteux la première fois (un appel par extension pour ses scénarios), donc
 *  retenu. `oublier()` vide le cache, pour les tests.
 */
export async function paliers(t = (x) => x) {
    if (_paliers) return _paliers;
    const extensions = await catalog.extensions();
    const heros = await catalog.heroes();

    // Les héros d'abord : ils portent déjà leur vague, calculée par le
    // catalogue à partir de leur extension.
    const parVague = new Map();
    const palier = (vague) => {
        if (!parVague.has(vague)) {
            parVague.set(vague, { vague, nom: nomDePalier(vague, t),
                                  scenarios: [], heros: [] });
        }
        return parVague.get(vague);
    };
    for (const h of heros) {
        if (h.homebrew || h.vague === null || h.vague === undefined) continue;
        palier(h.vague).heros.push({ id: h.heroCardId, nom: h.name });
    }

    // Puis les scénarios, extension par extension. On ne demande QUE celles
    // qui ont une vague : les défis et les paquets fan-made n'en ont pas, et
    // chaque extension interrogée coûte un aller-retour par scénario.
    for (const ext of extensions) {
        const vague = vagueDeLExtension(ext.key);
        if (vague === null) continue;
        if (!ext.scenarios || !ext.scenarios.length) { palier(vague); continue; }
        const liste = await catalog.scenariosForExtension(ext.key);
        for (const s of liste) {
            // ⚠ LA VARIANTE EXPERTE N'EST PAS UN SCÉNARIO DE PLUS. Elle porte
            // le même nom et le même vilain : la compter doublerait la marche
            // sans rien ajouter, et une victoire normale ne la cocherait
            // jamais.
            if (String(s.id).endsWith("_expert")) continue;
            // ⚠ NI LA TABLE COMPÉTITIVE, POUR LA MÊME RAISON (16/09/2026).
            // `she_hulk_pvp_competitive` porte le même vilain (57001, 57002),
            // les mêmes complots et les mêmes modulaires que `she_hulk_pvp` :
            // seul le nom change, « She-Hulk (Competitive Table) ». Or
            // l'historique ne garde que le NOM d'un scénario : les compter
            // tous les deux obligerait à rejouer le même affrontement pour la
            // seule raison qu'on l'a lancé depuis l'autre table.
            //
            // Ce qui reste dans la vague 10 : les six vrais adversaires, tous
            // jouables en COOPÉRATIF contre un leader automatisé. Le moteur
            // n'a pas d'autre mode pour eux (`IsCooperativeMode`), et c'est ce
            // qui les rend accessibles à un joueur seul.
            if (String(s.id).endsWith("_competitive")) continue;
            palier(vague).scenarios.push({ id: s.id, nom: s.name });
        }
    }

    _paliers = [...parVague.values()].sort((a, b) => a.vague - b.vague);
    return _paliers;
}

/** Vide le cache. Pour les tests, et pour un changement de langue. */
export function oublier() {
    _paliers = null;
}
