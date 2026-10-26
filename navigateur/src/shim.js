// Injecte en tete de CHAQUE page du jeu (voir construire.py). Les pages tournent dans un <iframe> de la
// coquille (navigateur.html) : c'est elle qui tient le moteur, et elle ne se recharge jamais.
// Ici, on redirige fetch, XMLHttpRequest et WebSocket du cadre vers ce moteur.
(() => {
  if (window === window.top) return;
  const M = window.top.__moteur;
  if (!M) return;
  const STATIQUE = /^\/(app|public|css|js|fonts|img|effects|stories|scan|assets|sounds|favicon\.ico|[A-Za-z0-9_.-]+\.html$)/;
  const natif = window.fetch.bind(window);
  const routeMoteur = (url) => url.origin === location.origin && !STATIQUE.test(url.pathname);

  // Version publique, SANS compte : ni signalement de bug, ni administration (ils passent par le serveur du site).
  const BUG = new Set(["/post_rapport_bug", "/get_rapport_actif", "/get_site_admin", "/get_messages_prives", "/post_messages_lus"]);
  // Compteur ANONYME des parties lancees sur play (09/10/2026) : le moteur tourne ici, le site
  // n'en saurait rien sinon. Texte brut via sendBeacon (pas de preflight CORS), jamais bloquant.
  function compterPartie(url) {
    try {
      if (!location.hostname.startsWith("play.") || !navigator.sendBeacon) return;
      const d = JSON.parse(url.searchParams.get("data") || "{}");
      const scenario = JSON.parse(d.campaign_json || "{}");
      const heros = (d.hero_json || []).map((j) => { try { return JSON.parse(j).name; } catch (e) { return null; } })
        .filter((n) => typeof n === "string").slice(0, 4);
      const signal = {
        mechant: typeof scenario.name === "string" ? scenario.name : null,
        heros,
        joueurs: Math.max(1, heros.length),
        mode: (d.rules || []).includes("mode_campaign") ? "campagne" : "solo",
        difficulte: scenario.expert ? "expert" : "normal",
      };
      navigator.sendBeacon(location.origin.replace("//play.", "//") + "/compteur_play", JSON.stringify(signal));
    } catch (e) { /* le compteur ne doit jamais gener une partie */ }
  }
  window.fetch = async (input, init) => {
    const url = new URL(typeof input === "string" ? input : input.url, location.href);
    if (url.origin === location.origin && BUG.has(url.pathname)) {
      const corps = url.pathname === "/get_rapport_actif" ? '{"actif":false}' : url.pathname === "/get_messages_prives" ? "[]" : "";
      return new Response(corps, { status: url.pathname === "/post_rapport_bug" ? 403 : 200, headers: { "Content-Type": "application/json" } });
    }
    if (!routeMoteur(url)) return natif(input, init);
    if (url.pathname === "/new") compterPartie(url);
    const methode = ((init && init.method) || (typeof input !== "string" && input.method) || "GET").toUpperCase();
    const corps = init && typeof init.body === "string" ? init.body : "";
    const rep = await M.requete(methode, url.pathname, url.search.slice(1), corps);
    // Un fichier que le moteur n'a pas (image, son...) : on retente sur l'hebergeur statique.
    if (rep.status === 404 && methode === "GET") return natif(input, init);
    return rep;
  };

  // XMLHttpRequest (runtime historique) : emule par-dessus fetch, requetes asynchrones seulement.
  class FauxXHR {
    constructor() { this.readyState = 0; this.status = 0; this.responseText = ""; this.response = null; this.responseType = ""; this._h = {}; this._ev = {}; }
    open(m, u) { this._m = m; this._u = u; this.readyState = 1; this._maj(); }
    setRequestHeader() {}
    getResponseHeader(n) { return this._rh ? this._rh.get(n) : null; }
    getAllResponseHeaders() { return ""; }
    overrideMimeType() {}
    addEventListener(t, f) { (this._ev[t] = this._ev[t] || []).push(f); }
    removeEventListener(t, f) { this._ev[t] = (this._ev[t] || []).filter((x) => x !== f); }
    abort() { this._abort = true; }
    _maj() { this.onreadystatechange && this.onreadystatechange.call(this); (this._ev.readystatechange || []).forEach((f) => f.call(this)); }
    _fin(t) { const e = { target: this, type: t }; this["on" + t] && this["on" + t].call(this, e); (this._ev[t] || []).forEach((f) => f.call(this, e)); }
    send(corps) {
      window.fetch(new URL(this._u, location.href).href, { method: this._m, body: typeof corps === "string" ? corps : undefined })
        .then(async (r) => {
          if (this._abort) return;
          this._rh = r.headers; this.status = r.status; this.statusText = r.statusText;
          if (this.responseType === "arraybuffer") this.response = await r.arrayBuffer();
          else if (this.responseType === "blob") this.response = await r.blob();
          else { this.responseText = await r.text(); this.response = this.responseType === "json" ? JSON.parse(this.responseText || "null") : this.responseText; }
          this.readyState = 4; this._maj(); this._fin("load"); this._fin("loadend");
        })
        .catch(() => { this.readyState = 4; this.status = 0; this._maj(); this._fin("error"); this._fin("loadend"); });
    }
  }
  window.XMLHttpRequest = FauxXHR;

  // Retire du DOM les boutons de signalement de bug (l'ecran de preparation les construit sans demander au serveur)
  // et ajoute « Exporter / Importer mes parties » a la rangee des boutons d'en-tete.
  const MASQUES = /^(🐞\s*)?(Signaler un bug|Report a bug|Mes signalements|My reports|Bug)$/i;
  let ajoute = false;
  const parler = (msg) => { try { window.top.alert(msg); } catch (e) { /* */ } };
  // Lue a chaque appel : le joueur peut changer de langue sans recharger la page.
  // LANGUE-PLAY-DEBUT
  // Langue de l'habillage de Play. ATTENTION : play.<domaine> et <domaine> sont deux ORIGINES : le choix fait sur le site
  // n'existe pas dans le localStorage d'ici (constat du 26/10/2026 : un joueur anglophone voyait le francais).
  // Ordre : ?langue=en|fr (puis retenu), choix deja fait ici (meme cle que le jeu, public/js/prepare/langue.js),
  // cookie nc_langue pose par le SITE sur le domaine parent (site/orchestrateur.py, route /langue : lisible ici),
  // langue du navigateur, francais. Ce bloc est identique dans shim.js (verifie par tools/tests-lanceur/langue-play.test.mjs).
  function langueDePlay(storage, nav, loc, cookie) {
    try {
      const q = new URLSearchParams(loc.search).get("langue");
      if (q === "en" || q === "fr") { try { storage.setItem("marvel-langue", q); } catch (e) { /* stockage bloque */ } return q; }
    } catch (e) { /* adresse illisible */ }
    try { const s = storage.getItem("marvel-langue"); if (s === "en" || s === "fr") return s; } catch (e) { /* stockage bloque */ }
    for (const morceau of String(cookie || "").split(";")) {
      const i = morceau.indexOf("="), nom = morceau.slice(0, i).trim(), valeur = morceau.slice(i + 1).trim();
      if (nom === "nc_langue" && (valeur === "en" || valeur === "fr")) return valeur;
    }
    const l = String((nav && (nav.language || (nav.languages && nav.languages[0]))) || "").toLowerCase();
    return l.startsWith("en") ? "en" : "fr";
  }
  // LANGUE-PLAY-FIN
  const tr = (fr, en) => {
    let st = null, ck = ""; try { st = localStorage; } catch (e) { /* stockage bloque */ } try { ck = document.cookie; } catch (e) { /* cookies bloques */ }
    return langueDePlay(st, navigator, location, ck) === "en" ? en : fr;
  };
  function bouton(texte, titre, action) {
    const b = document.createElement("button");
    b.type = "button"; b.textContent = texte; b.title = titre; b.addEventListener("click", action); return b;
  }
  function ajouterSauvegardes(rangee) {
    if (ajoute || !rangee || !location.pathname.endsWith("/prepare.html")) return;
    ajoute = true;
    const champ = document.createElement("input");
    champ.type = "file"; champ.accept = ".json,application/json"; champ.style.display = "none";
    champ.addEventListener("change", async () => {
      const f = champ.files[0]; champ.value = ""; if (!f) return;
      try { parler((await M.importer(f)) + tr(" fichier(s) importé(s). Ouvre « Reprendre » pour retrouver tes parties.", " file(s) imported. Open « Resume » to find your games.")); }
      catch (e) { parler(tr("Import impossible : ", "Import failed: ") + (e && e.message ? e.message : e)); }
    });
    rangee.append(
      bouton("💾 " + tr("Exporter mes parties", "Export my games"), tr("Télécharge un fichier avec toutes tes parties et réglages", "Downloads a file with all your games and settings"), () => M.exporter().catch((e) => parler(tr("Export impossible : ", "Export failed: ") + e.message))),
      bouton("📂 " + tr("Importer", "Import"), tr("Recharge un fichier d'export", "Loads an export file"), () => champ.click()),
      champ);
  }
  function nettoyer() {
    document.querySelectorAll("button, a").forEach((b) => { if (MASQUES.test((b.textContent || "").trim())) b.remove(); });
    ajouterSauvegardes(document.querySelector(".reprise-boutons"));
  }
  new MutationObserver(nettoyer).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("DOMContentLoaded", nettoyer);

  class FauxWS {
    constructor(url) { this.url = url; this.readyState = 0; this._ev = {}; M.ouvrirWS(this); }
    send(t) { M.envoyerWS(String(t)); }
    close() { if (this.readyState === 3) return; this.readyState = 3; M.fermerWS(this); this._f("close", { code: 1000 }); }
    addEventListener(t, f) { (this._ev[t] = this._ev[t] || []).push(f); }
    removeEventListener(t, f) { this._ev[t] = (this._ev[t] || []).filter((x) => x !== f); }
    _f(t, e) { this["on" + t] && this["on" + t](e); (this._ev[t] || []).forEach((f) => f(e)); }
    _ouvert() { this.readyState = 1; this._f("open", {}); }
    _recevoir(json) { this._f("message", { data: json }); }
  }
  FauxWS.CONNECTING = 0; FauxWS.OPEN = 1; FauxWS.CLOSING = 2; FauxWS.CLOSED = 3;
  window.WebSocket = FauxWS;
})();
