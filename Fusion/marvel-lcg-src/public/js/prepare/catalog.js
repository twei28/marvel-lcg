// catalog.js — construit les modèles de haut niveau (héros, scénarios, extensions,
// sets de rencontre) à partir des données brutes + métadonnées de cartes.
"use strict";
import { api, fileName } from "/public/js/prepare/api.js";
import { cards } from "/public/js/prepare/cards.js";

const TEAMS = ["Avenger", "X-Men", "Guardian", "Champion", "Defender", "X-Force", "Inhuman", "S.H.I.E.L.D.", "Web-Warrior"];
const num = (s) => { const m = String(s).match(/^\s*(\d+)/); return m ? +m[1] : 9999; };
const titleize = (s) => String(s).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
const cleanName = (s) => String(s || "").replace(/^\*\s*/, "").trim();

function teamFromTraits(card) {
    if (!card || !card.traits) return "";
    for (const t of TEAMS) if (card.traits.some((x) => String(x).toLowerCase().includes(t.toLowerCase().replace(/\W/g, "")))) return t;
    return card.traits[0] || "";
}
function aspectsOfDeck(deck) {
    if (!deck || !deck.player_deck) return [];
    const s = new Set();
    for (const id of deck.player_deck) { const a = cards.aspectOf(id); if (a && a !== "basic") s.add(a); }
    return [...s];
}

/** Traits qui distinguent une identité d'une autre (les traits communs sautent). */
function traitsDistinctifs(traitsA, traitsB) {
    const b = new Set(traitsB || []);
    return (traitsA || []).filter((t) => !b.has(t));
}

/** Identités jouables d'un héros : la face de base, puis `metadata.hero_alts`.
 *  Renvoie [] quand il n'y a pas de variante, pour que le wizard n'affiche
 *  aucun sélecteur dans le cas courant. */
function identityVariants(deck, heroCardId, heroCard) {
    const alts = (deck.metadata && deck.metadata.hero_alts) || [];
    if (!alts.length) return [];
    const base = {
        hero: deck.hero,
        heroCardId,
        name: cleanName(heroCard && heroCard.name) || deck.name,
        traits: (heroCard && heroCard.traits) || [],
    };
    const out = [base];
    for (const alt of alts) {
        if (!alt || !alt.hero || !alt.hero.length) continue;
        const id = String(alt.hero[0]).split(",")[0];
        const c = cards.get(id);
        out.push({
            hero: alt.hero,
            heroCardId: id,
            name: alt.name || cleanName(c && c.name) || base.name,
            traits: (c && c.traits) || [],
        });
    }
    // Ce qui différencie chaque identité des autres : sert de libellé.
    for (const v of out) {
        const autres = out.filter((x) => x !== v).flatMap((x) => x.traits);
        v.distinctif = traitsDistinctifs(v.traits, autres);
    }
    return out.length > 1 ? out : [];
}
/* --------------------------------------------------------------------------
 * Les vagues de sortie
 *
 * REGLE : une vague s'ouvre sur une GRANDE BOITE et court jusqu'a la suivante.
 * Le Set de base est a part — c'est le point de depart, pas une vague.
 * L'exception est la vague 1, qui n'a pas de grande boite a son ouverture : elle
 * regroupe tout ce qui a suivi le Set de base jusqu'a Hulk (7/8/2020), La
 * Chute du Crane Rouge (4/9/2020) ouvrant la vague 2.
 *
 * La table est indexee par le NUMERO que porte la cle d'extension dans
 * sets_info.json (« 12. Ant-Man » -> 12). Ce numero est deja l'ordre de sortie
 * du jeu, donc la table se lit comme une frise et un nouveau paquet se range
 * en ajoutant une seule borne.
 *
 * Sources : dates de sortie de marvelcdb.com/api/public/packs, et le decoupage
 * des vagues 1 a 7 publie par la communaute. Les vagues 8 a 11 prolongent la
 * MEME regle (Age of Apocalypse, Agents du S.H.I.E.L.D., Civil War, Fear No
 * Evil ouvrent chacune la leur) sans qu'une liste publiee ne les confirme
 * encore : si FFG les decoupait autrement, il suffirait de deplacer une borne.
 *
 * Les paquets fan-made (98 et au-dela) n'ont pas de vague : ils vivent derriere
 * le bouton « Fan-made », qui ne les melange jamais aux officiels.
 * ------------------------------------------------------------------------ */
const BORNES_VAGUES = [
    { depuis: 1,  vague: 0 },    // Set de base
    { depuis: 2,  vague: 1 },    // Bouffon Vert -> Hulk
    { depuis: 4,  vague: 2 },    // The Rise of Red Skull
    { depuis: 5,  vague: 1 },    // (la boite 4 s'intercale dans l'ordre du jeu)
    { depuis: 11, vague: 2 },    // Kang -> Sorciere Rouge
    { depuis: 16, vague: 3 },    // The Galaxy's Most Wanted
    { depuis: 21, vague: 4 },    // The Mad Titan's Shadow
    { depuis: 27, vague: 5 },    // Sinister Motives
    { depuis: 32, vague: 6 },    // Mutant Genesis
    { depuis: 40, vague: 7 },    // NeXt Evolution
    { depuis: 45, vague: 8 },    // Age of Apocalypse
    { depuis: 50, vague: 9 },    // Agents of S.H.I.E.L.D.
    { depuis: 56, vague: 10 },   // Civil War
    { depuis: 60, vague: 11 },   // Fear No Evil
    { depuis: 61, vague: null }, // au-dela : hors vague (modulaires, defis)
];

/* Le NOM d'une vague est celui de la grande boite qui l'ouvre — c'est la meme
 * regle que les bornes ci-dessus, lue dans l'autre sens, donc les deux tables
 * se completent ligne a ligne et une nouvelle vague s'ajoute aux deux endroits.
 *
 * Titres EN, ET EN FRANCAIS AUSSI : ils ne passent pas par le dictionnaire.
 * C'est le titre imprime sur la boite, celui que porte la cle d'extension dans
 * sets_info.json et celui qu'affiche l'ecran des campagnes (`nom_en` des
 * definitions) — donc le seul sous lequel on retrouve la boite, en rayon comme
 * dans le reste de l'appli. A revoir le jour ou on voudra les titres FR : ce
 * sera cette table, et rien d'autre.
 *
 * La vague 1 n'est pas ici : sans grande boite, elle n'a pas de titre a copier.
 * Son libelle est du texte a nous, donc traduit comme le reste (voir
 * `nomDeVague` dans app.js). */
const NOMS_VAGUES = {
    2:  "The Rise of Red Skull",
    3:  "The Galaxy's Most Wanted",
    4:  "The Mad Titan's Shadow",
    5:  "Sinister Motives",
    6:  "Mutant Genesis",
    7:  "NeXt Evolution",
    8:  "Age of Apocalypse",
    9:  "Agents of S.H.I.E.L.D.",
    10: "Civil War",
    11: "Fear No Evil",
};

/** Titre de la grande boite qui ouvre une vague. "" si la vague n'en a pas —
 *  le Set de base (0), ou une vague future dont la table ignore encore le nom :
 *  l'appelant retombe alors sur le seul numero, jamais sur un trou. */
function titreDeVague(vague) {
    return NOMS_VAGUES[vague] || "";
}

/** Vague d'une extension, d'apres le numero que porte sa clé. null si aucune
 *  (fan-made, sets modulaires, defis hebdomadaires). */
function vagueDeLExtension(cle) {
    const n = parseInt(String(cle || ""), 10);
    if (!Number.isFinite(n) || n >= 90) return null;
    let vague = null;
    for (const borne of BORNES_VAGUES) {
        if (n >= borne.depuis) vague = borne.vague;
    }
    return vague;
}

/** Seconde identité d'un héros qui en compte DEUX pour un seul joueur.
 *
 *  Le pack Cloak & Dagger est bâti ainsi : `linked_identity` porte une identité
 *  complète (faces héros/alter-ego + son propre mini-deck), jouée en même temps
 *  que la principale et par le même joueur. C'est la seule clé qui le dit, donc
 *  la seule sur laquelle s'appuyer : aucun identifiant en dur ici, un futur duo
 *  bâti pareil sera montré double sans rien toucher.
 *
 *  Renvoie null pour les 66 autres héros, qui gardent exactement leur rendu. */
function identiteLiee(deck) {
    const lie = deck.linked_identity;
    if (!lie || !lie.hero || !lie.hero.length) return null;
    const heroCardId = String(lie.hero[0]).split(",")[0];
    const c = cards.get(heroCardId);
    return {
        hero: lie.hero,
        heroCardId,
        name: cleanName(c && c.name) || "",
        hp: c ? c.hp : undefined,
    };
}

/** Héros fan-made : soit rattaché à une extension « Custom » (ex. « 99. Custom
 *  (Rainy) » pour Thor Jane Foster), soit rattaché à aucune extension officielle
 *  (Stan Lee, Hulk (Rainy)). Rien à maintenir à la main. */
function isHomebrew(extension) {
    return !extension || /custom/i.test(extension);
}
/** Packages d'aspect proposables à un héros ABSENT du tableur : uniquement les
 *  génériques. Tout ce qui porte un nom d'équipe (X-Men, X-Force, S.H.I.E.L.D.,
 *  Web-Warrior, Guardian, Champion, Guerrilla, Assembled) ou de héros
 *  (Spider-Woman, Adam Warlock, Silly 'Pool) est écarté : ces decks supposent
 *  des traits ou des règles que le héros n'a probablement pas. */
const GENERIQUES = [
    "Brutish Aggression", "Graceful Aggression", "Warrior's Aggression", "Reckless Aggression",
    "Defiant Justice", "Evasive Justice", "Strategic Justice",
    "Courageous Leadership", "Commanding Leadership", "Sacrificial Leadership",
    "Unyielding Protection", "Debilitating Protection",
];

/** Les trois ressources de base, socle commun à TOUTES les colonnes du tableur.
 *
 *  Vérifié colonne par colonne : sur les 32 paquets, aucun ne se passe d'Energy,
 *  Genius et Strength. Les cinq colonnes de Spider-Woman sont les seules à
 *  n'avoir AUCUNE carte Basic — elles ne listent que l'aspect, parce qu'elles
 *  sont faites pour être jouées par deux. Voir resoudrePackage(). */
const SOCLE_BASIC = ["01088", "01089", "01090"]; // Energy, Genius, Strength

function encounterKind(name) {
    if (name.startsWith("standard")) return "standard";
    if (name.startsWith("expert")) return "expert";
    if (name.endsWith("_nemesis")) return "nemesis";
    return "modular";
}

let _extensions = null, _heroes = null, _encounterSets = null;
// `set_name` des héros marqués `metadata.indisponible` dans leur deck de
// départ. Rempli par heroes(), lu par setsMasques() : le deckbuilder s'en sert
// pour ne pas proposer les cartes signature d'un héros retiré du jeu.
let _setsMasques = new Set();
const _scenariosByExt = new Map();

export const catalog = {
    async extensions() {
        if (_extensions) return _extensions;
        const raw = await api.setsInfo();
        _extensions = Object.entries(raw).map(([key, v]) => ({
            key, code: v.name, scenarios: v.scenarios || [], heroes: v.heroes || [],
            encounters: v.encounters || [], maxId: v.max_id,
        })).sort((a, b) => num(a.key) - num(b.key));
        // Onglet synthétique « Défis » : les défis mensuels de data/challenges
        // sont des scénarios complets (méchant fixe + carte Défi via
        // raw.challenges), absents de sets_info.json. Détectés par leur nom.
        try {
            const defis = (await api.listScenarios()).map(fileName)
                .filter((n) => /^24\d{2}_/.test(n) || n === "wild").sort();
            if (defis.length) {
                _extensions.push({ key: "defis", code: "Défis", scenarios: defis, heroes: [], encounters: [], maxId: 0 });
            }
        } catch (e) {}
        return _extensions;
    },

    async heroes() {
        if (_heroes) return _heroes;
        await cards.load();
        const exts = await this.extensions();
        const heroExt = {};
        exts.forEach((e) => e.heroes.forEach((h) => (heroExt[h] = e.key)));
        const ids = (await api.listStarterDecks()).map(fileName);
        const loaded = await Promise.all(ids.map((id) => api.deck(id).then((d) => ({ id, d })).catch(() => null)));
        // Héros RETIRÉS du jeu : `metadata.indisponible` dans leur deck de
        // départ. Le fichier reste dans deck/starter/ — c'est volontaire, pour
        // que les cas de tools/test_capacites.py continuent de tourner (le
        // harnais charge le deck par son nom) : on masque un héros sans perdre
        // sa couverture de test. Ajouté le 01/09/2026 pour Squirrel Girl.
        // Cette liste sert aussi au deckbuilder, qui appelle heroes().
        // ⚠ On collecte les set_name depuis TOUTES les cartes du deck, pas
        // seulement depuis la face héros : un pack en compte souvent plusieurs.
        // Squirrel Girl en a trois (« Squirrel Girl », « Squirrel Deck » pour
        // les six écureuils mis de côté, « Squirrel Girl Nemesis »), et ses six
        // cartes empruntables sont justement dans « Squirrel Deck ».
        _setsMasques = new Set();
        loaded.forEach((x) => {
            if (!x || !x.d || !x.d.metadata || !x.d.metadata.indisponible) return;
            const d = x.d;
            const listes = [d.hero, d.hero_deck, d.set_aside, d.obligations, d.nemesis_set];
            listes.forEach((liste) => (liste || []).forEach((entree) => {
                const cid = String(entree).split(",")[0];
                const c = cards.get(cid);
                if (c && c.set_name) _setsMasques.add(c.set_name);
            }));
        });
        _heroes = loaded.filter((x) => x && x.d && x.d.hero && x.d.hero.length
                                       && !(x.d.metadata && x.d.metadata.indisponible)).map(({ id, d }) => {
            const heroCardId = d.hero[0].split(",")[0];
            const c = cards.get(heroCardId);
            const extension = heroExt[id] || "";
            return {
                id, heroCardId, baseDeckId: id, deck: d,
                name: cleanName(c && c.name) || cleanName(d.name) || titleize(id),
                hp: c ? c.hp : undefined,
                handSize: cards.handSizeOf(heroCardId),
                traits: c ? c.traits || [] : [],
                team: teamFromTraits(c),
                extension,
                vague: vagueDeLExtension(extension),
                homebrew: isHomebrew(extension),
                aspects: aspectsOfDeck(d),
                // Identités alternatives : même deck, autres faces héros /
                // alter-ego (ex. The Thing en Gardien de la Galaxie). Elles
                // ne créent PAS un second héros dans la grille : le wizard les
                // propose comme un choix d'identité à l'étape des decks.
                variants: identityVariants(d, heroCardId, c),
                // Identité LIÉE : deux héros pour un seul joueur (Cloak &
                // Dagger). Rien à voir avec `variants`, qui propose un choix :
                // ici les deux identités arrivent ENSEMBLE, chacune avec son
                // mini-deck. La grille doit donc les montrer toutes les deux.
                lie: identiteLiee(d),
            };
        }).sort((a, b) => a.name.localeCompare(b.name));
        return _heroes;
    },

    /** `set_name` des héros retirés du jeu (`metadata.indisponible`).
     *  Appeler heroes() d'abord : c'est lui qui remplit la liste. */
    async setsMasques() {
        await this.heroes();
        return _setsMasques;
    },

    /** Decks jouables pour un héros donné : base + identités alternatives + sauvegardés. */
    async decksForHero(hero) {
        await cards.load();
        const out = [{ id: hero.baseDeckId, name: hero.deck.name || hero.name, source: "base", deck: hero.deck, aspects: hero.aspects }];
        try {
            const savedIds = (await api.listSavedDecks()).map(fileName);
            for (const id of savedIds) {
                try {
                    const d = await api.deck(id);
                    if (d && d.hero && d.hero[0] && d.hero[0].split(",")[0] === hero.heroCardId) {
                        out.push({ id, name: d.name || id, source: "saved", deck: d, aspects: aspectsOfDeck(d) });
                    }
                } catch (e) {}
            }
        } catch (e) {}
        out.push(...await this.packagesAspect(hero));
        return out;
    },

    /** Packages d'aspect proposes a CE heros, assembles a la volee.
     *  Les 30 cartes d'un package ne sont que la partie « aspect » : on y colle
     *  les cartes signature, l'obligation et le nemesis du deck de base.
     *
     *  On ne propose QUE les 4 packages que le tableur conseille au heros. Lui
     *  offrir les 32 reviendrait a proposer le deck d'Adam Warlock a Black
     *  Widow. Pour un heros absent du tableur, on retombe sur une liste
     *  generique, sans aucun package lie a une equipe ou a un autre heros. */
    async packagesAspect(hero) {
        let data;
        try {
            data = await api.aspectDecks();
        } catch (e) { return []; }
        const packages = (data && data.packages) || {};
        const reco = (data && data.recommandations) || {};

        // La matrice nomme les heros comme le tableur (« Spider-Man (Peter
        // Parker) ») : on retrouve l'entree par le nom du heros ou de l'alter-ego.
        const identites = [hero.name, ...(hero.deck.hero[0] || "").split(",")
            .map((id) => { const c = cards.get(id); return c ? cleanName(c.name) : ""; })]
            .filter(Boolean).map((x) => x.toLowerCase());
        let conseille = null;
        for (const [cle, valeurs] of Object.entries(reco)) {
            const bas = cle.toLowerCase();
            if (identites.some((n) => n && bas.includes(n))) { conseille = valeurs; break; }
        }

        // Un nom de package peut designer DEUX packages a fusionner : c'est le
        // cas de Spider-Woman, qui joue deux aspects a la fois.
        const resoudrePackage = (nom) => {
            if (packages[nom]) return [nom];
            const m = nom.match(/^(.*?)\s+(\w+)\/(\w+)$/);
            if (m) {
                const [, prefixe, a, b] = m;
                const p1 = `${prefixe} ${a}`, p2 = `${prefixe} ${b}`;
                if (packages[p1] && packages[p2]) return [p1, p2];
            }
            return [];
        };

        let choisis;
        if (conseille) {
            const vus = new Set();
            choisis = [];
            for (const nom of Object.values(conseille)) {
                const parties = resoudrePackage(nom);
                if (!parties.length || vus.has(nom)) continue;
                vus.add(nom);
                choisis.push({ libelle: nom, parties });
            }
        } else {
            // Heros hors tableur : que du generique, jamais un package d'equipe
            // (X-Men, Avengers, S.H.I.E.L.D....) ni lie a un heros precis.
            choisis = GENERIQUES.filter((n) => packages[n])
                .map((n) => ({ libelle: n, parties: [n] }));
        }

        return choisis.map(({ libelle, parties }) => {
            const cartes = parties.flatMap((p) => packages[p] || []);
            // Un package assemblé à partir de PLUSIEURS colonnes vient des
            // colonnes bi-aspect, qui ne listent que l'aspect : 11 + 11 = 22, là
            // où un générique compte 30 cartes dont 6 Basic. Le deck tombait donc
            // à 37 (15 signature + 22), sous le minimum de 40. En rendant son
            // socle de ressources, la partie joueur revient à 25 cartes —
            // exactement la taille du player_deck de tous les decks de base.
            if (parties.length > 1) cartes.push(...SOCLE_BASIC);
            const deck = { ...hero.deck, name: libelle, player_deck: cartes };
            return {
                id: "aspect:" + libelle, name: libelle, source: "aspect", deck,
                aspects: aspectsOfDeck(deck), recommande: !!conseille,
            };
        });
    },

    _buildScenario(id, raw, extKey, hasExpert) {
        const villains = raw.villain || [];
        const schemes = raw.schemes || [];
        const setAside = raw.set_aside || [];
        const mod = raw.modular_sets || [];
        // Cartes de vilain(s) à afficher :
        //  - villain[] rempli  -> étapes d'UN vilain : on montre la 1re carte.
        //  - villain[] vide    -> scénario multi-vilains : on récupère les cartes de
        //                          type "Villain" dans set_aside (dédupliquées par nom).
        let villainCards;
        if (villains.length) {
            villainCards = [villains[0].split(",")[0]];
        } else {
            const seen = new Set(); villainCards = [];
            for (const c of setAside) {
                const card = cards.get(c);
                if (card && String(card.type).includes("Villain")) {
                    const nm = cleanName(card.name);
                    if (nm && !seen.has(nm)) { seen.add(nm); villainCards.push(String(c).split(",")[0]); }
                }
            }
        }
        const villainNames = villainCards.map((c) => { const card = cards.get(c); return cleanName(card ? card.name : c); });
        // Scénario-défi : on affiche le NOM DU DÉFI (carte challenge) plutôt que
        // celui du scénario de base, plus parlant dans la grille et le récap.
        const challenges = raw.challenges || [];
        let name = cleanName(raw.name) || titleize(id);
        if (challenges.length) {
            const cdefi = cards.get(challenges[0]);
            if (cdefi && cdefi.name) name = cleanName(cdefi.name);
        }
        return {
            id, name, challenges, version: raw.version, extension: extKey,
            expert: !!raw.expert, hasExpertVariant: hasExpert,
            villains, schemes, setAside,
            villainCards,
            encounterDeckBase: raw.encounters || [],
            mandatoryEncounterSets: raw.encounter_sets || [],
            recommendedModularSets: mod,
            modularSlots: { min: mod.length, max: Math.max(4, mod.length) },
            tileImage: (villainCards[0] || schemes[0] || "").split(",")[0],
            villainNames,
            rawJson: raw,
        };
    },

    async scenariosForExtension(extKey) {
        if (_scenariosByExt.has(extKey)) return _scenariosByExt.get(extKey);
        await cards.load();
        const exts = await this.extensions();
        const ext = exts.find((e) => e.key === extKey);
        const avail = new Set((await api.listScenarios()).map(fileName));
        const out = [];
        if (ext) {
            for (const name of ext.scenarios) {
                if (!avail.has(name)) continue;
                try {
                    const raw = await api.scenario(name);
                    out.push(this._buildScenario(name, raw, extKey, avail.has(name + "_expert")));
                } catch (e) {}
            }
        }
        _scenariosByExt.set(extKey, out);
        return out;
    },

    /** Variante Expert d'un scénario (fichier *_expert). */
    async expertVariant(scenarioId) {
        try {
            const raw = await api.scenario(scenarioId + "_expert");
            return this._buildScenario(scenarioId + "_expert", raw, "", false);
        } catch (e) { return null; }
    },

    async encounterSets() {
        if (_encounterSets) return _encounterSets;
        const names = (await api.listEncounterSets()).map(fileName);
        _encounterSets = names.map((n) => ({ name: n, displayName: titleize(n), kind: encounterKind(n) }));
        return _encounterSets;
    },

    /** Image d'un set de rencontre (1re carte) — chargée à la demande. */
    async encounterSetImage(name) {
        try { const j = await api.encounterSet(name); return (j.encounters && j.encounters[0]) ? j.encounters[0].split(",")[0] : ""; }
        catch (e) { return ""; }
    },
};

export { titleize, titreDeVague };
