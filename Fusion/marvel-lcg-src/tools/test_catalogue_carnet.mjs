// Test de public/js/campagne/catalogue-carnet.js (node, sans navigateur) : chaque combinaison du carnet designe un scenario QUI EXISTE.
// Usage : node tools/test_catalogue_carnet.mjs   (depuis Fusion/marvel-lcg-src)
import fs from "node:fs";
import { catalogueSelonCarnet, scenarioDuCatalogueDeLEtape } from "../public/js/campagne/catalogue-carnet.js";

const def = JSON.parse(fs.readFileSync("data/campagnes/punisher_mcdc_2026.json", "utf-8"));
const etape = (id) => def.scenarios.find((s) => s.id === id);
const existe = (id) => fs.existsSync(`data/scenarios/${id}.json`);
let ko = 0;
const verifier = (ok, msg) => { if (!ok) { ko++; console.log("ECHEC", msg); } };

const c2 = etape("tracking_the_buyer");
const lieux = Object.keys(c2.catalogue_selon_carnet.variables.manigance.table);
const trafiquants = Object.keys(c2.catalogue_selon_carnet.variables.sous_fifre.table);
for (const lieu of lieux) for (const trafiquant of trafiquants) for (const expert of [false, true]) {
    const id = catalogueSelonCarnet(c2, { "Final LEAD Location": lieu, "Gunrunner": trafiquant }, expert);
    verifier(id && existe(id), `combat 2 : ${lieu} / ${trafiquant} / expert=${expert} -> ${id} (fichier absent)`);
}
// Exemples du livret : Theater District + Nightshade -> Art Museum Heist contre Hobgoblin.
verifier(catalogueSelonCarnet(c2, { "Final LEAD Location": "Theater District", "Gunrunner": "Nightshade" }, false) === "tracking_the_buyer_art_museum_heist_hobgoblin", "exemple 1");
verifier(catalogueSelonCarnet(c2, { "Final LEAD Location": "Chinatown", "Gunrunner": "The Rose" }, true) === "tracking_the_buyer_protection_racket_jigsaw_expert", "exemple 2");
// Carnet incomplet : le defaut, jamais d'exception.
verifier(catalogueSelonCarnet(c2, {}, false) === c2.catalogue_selon_carnet.defaut, "carnet vide -> defaut");
verifier(catalogueSelonCarnet(c2, { "Final LEAD Location": "Midtown" }, true) === c2.catalogue_selon_carnet.defaut + "_expert", "carnet sans Trafiquant -> defaut expert");
verifier(existe(c2.catalogue_selon_carnet.defaut) && existe(c2.catalogue_selon_carnet.defaut + "_expert"), "le defaut du combat 2 existe");

const c3 = etape("punishment");
for (const [fifre, autre] of [["Jigsaw", "hobgoblin"], ["Hobgoblin", "jigsaw"], ["jigsaw", "hobgoblin"]]) {
    for (const expert of [false, true]) {
        const id = catalogueSelonCarnet(c3, { Underling: fifre }, expert);
        verifier(id === `punishment_${autre}${expert ? "_expert" : ""}` && existe(id), `combat 3 : ${fifre} -> ${id}`);
    }
}
verifier(catalogueSelonCarnet(c3, {}, false) === "punishment_hobgoblin", "combat 3 : carnet vide -> defaut");

// Les autres etapes : pas de regle de carnet, l'id de l'etape.
verifier(catalogueSelonCarnet(etape("kingsfall"), {}, false) === null, "combat 4 : pas de regle");
verifier(scenarioDuCatalogueDeLEtape(etape("kingsfall"), {}, false) === "kingsfall" && existe("kingsfall") && existe("kingsfall_expert"), "combat 4 : kingsfall");
verifier(scenarioDuCatalogueDeLEtape(etape("the_big_apple"), {}, false) === "the_big_apple" && existe("the_big_apple"), "combat 1 : the_big_apple");
console.log(ko ? `${ko} ECHEC(S)` : `OK : ${lieux.length * trafiquants.length * 2 + 11} verifications`);
process.exit(ko ? 1 : 0);
