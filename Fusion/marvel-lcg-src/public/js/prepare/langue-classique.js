// langue-classique.js — la langue du jeu pour les PETITS SCRIPTS NON-MODULES de la page de préparation (reprise.js, annonce.js,
// maj.js, messages.js, invitations.js, lien-*.js) : script CLASSIQUE (defer + IIFE), donc rien à importer. Expose
// window.MarvelLangue = { actuelle(), ecrire(langue) }.
//
// ⚠ JUMEAU de langue-resolution.js (même règle : choix dans le jeu « marvel-langue » > cookie « nc_langue » du site > navigateur >
// français ; décision du 26/10/2026). Les deux doivent rester identiques : tools/tests-lanceur/langue-jeu.test.mjs évalue ce
// fichier dans un bac à sable et le compare au module pur sur les mêmes cas. À charger AVANT les petits scripts, dans les pages.
(function () {
  "use strict";
  var CLE = "marvel-langue";
  var COOKIE = "nc_langue";

  function valide(v) { return v === "en" || v === "fr" ? v : ""; }

  function lireCookie(cookie) {
    var morceaux = String(cookie || "").split(";");
    for (var k = 0; k < morceaux.length; k++) {
      var m = morceaux[k], i = m.indexOf("=");
      if (i < 0) continue;
      if (m.slice(0, i).trim() === COOKIE) {
        var v = m.slice(i + 1).trim();
        if (v === "en" || v === "fr") return v;
      }
    }
    return "";
  }

  function duNavigateur(nav) {
    var l = String((nav && (nav.language || (nav.languages && nav.languages[0]))) || "").toLowerCase();
    return l.indexOf("en") === 0 ? "en" : "fr";
  }

  function domaineParent(hote) {
    var brut = String(hote || "").trim().toLowerCase();
    if (!brut) return "";
    if (brut.charAt(0) === "[") return "";
    var sansPort = brut.replace(/:\d+$/, "");
    if (!sansPort || sansPort.indexOf(":") >= 0) return "";
    if (/^\d+(\.\d+){3}$/.test(sansPort)) return "";
    var e = sansPort.split(".");
    if (e.length < 2) return "";
    for (var k = 0; k < e.length; k++) if (!e[k]) return "";
    if (e.length >= 3 && /^(p\d+|play|www)$/.test(e[0])) return "." + e.slice(1).join(".");
    if (e.length === 2) return "." + sansPort;
    return "";
  }

  function stockee() {
    try { return valide(window.localStorage.getItem(CLE)); } catch (e) { return ""; }
  }
  function cookieDuDocument() {
    try { return window.document.cookie; } catch (e) { return ""; }
  }

  function actuelle() {
    return stockee() || lireCookie(cookieDuDocument()) || duNavigateur(typeof navigator === "undefined" ? null : navigator);
  }

  function ecrire(langue) {
    var l = langue === "en" ? "en" : "fr";
    var c = COOKIE + "=" + l + "; Path=/; Max-Age=31536000; SameSite=Lax";
    var d = domaineParent(location.host);
    if (d) c += "; Domain=" + d;
    if (location.protocol === "https:") c += "; Secure";
    try { window.document.cookie = c; } catch (e) { /* cookies bloqués */ }
  }

  window.MarvelLangue = { actuelle: actuelle, ecrire: ecrire };
})();
