"""
VP-NORM-1 corpus variable normalizer (layered, deterministic, non-destructive).

Maps a sidecar `variables_measured[].raw_label` to a canonical variable id.
Returns None (-> stays `raw_label_only`) when no confident match — NEVER force.

Layers (PR#16 §0.7) + cycle-3 precision pre-passes (Codex 006 verdict):
  pre  block placeholders, ions-before-L0, corpus overrides, age preemption, CO2 split
  L0   isotope vocab     -- reuse geochem normalize.py
  L1   standard geochem  -- major oxides, trace, REE, ratios, gases, cations, anomalies...
  L2   structural clean   -- strip unit-parens / trailing words / time-marker, retry L0+L1
Guardrail: oxide *_wt_pct ids are rejected when an explicit concentration unit
(ppm/mg-kg/mol-kg...) is present in label or unit field.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# L0 — reuse the existing geochem isotope normalizer (do NOT reinvent)
# ---------------------------------------------------------------------------
L0_DIR = Path(r"C:\Users\USER\Documents\geochem-corpus-v2\tools\geochem-stats\index")
sys.path.insert(0, str(L0_DIR))
import normalize as L0  # noqa: E402  (ascii_fold, canonicalize, normalize_axis)


# ---------------------------------------------------------------------------
# L1 — standard geochem species (code-defined for reviewability)
# ---------------------------------------------------------------------------
MAJOR_OXIDES = [
    "SiO2", "TiO2", "Al2O3", "Fe2O3", "FeO", "MnO", "MgO", "CaO",
    "Na2O", "K2O", "P2O5", "Cr2O3", "NiO", "SO3", "BaO", "SrO", "CoO",
]
FE_TOTAL_ALIASES = ["FeOt", "FeO*", "FeOT", "FeO(t)", "Fe2O3t", "Fe2O3*", "Fe2O3T",
                    "FeOtot", "Fe2O3tot", "total Fe", "total iron", "FeO_total", "Fe2O3_total",
                    "TFe2O3", "TFeO", "Fe2O3(T)"]
VOLATILES_OXIDE = {  # special wt% volatiles (CO2 handled separately by _try_co2)
    "LOI": ["LOI", "L.O.I.", "loss on ignition"],
    "H2O_plus": ["H2O+", "H2O(+)"],
    "H2O_minus": ["H2O-", "H2O(-)"],
    "H2O_total": ["H2O", "H2O total", "total H2O", "H2Ot"],
}

TRACE_ELEMENTS = [
    "Li", "Be", "B", "Sc", "V", "Cr", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",
    "As", "Se", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "Cs", "Ba", "Hf", "Ta", "W", "Re", "Tl", "Pb", "Bi", "Th", "U",
]
REE = ["La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]

RATIOS = [
    "La/Yb", "La/Sm", "Sm/Nd", "Ce/Pb", "Nb/Ta", "Zr/Hf", "Th/U", "Ba/Nb",
    "Ba/La", "Ba/Th", "Nb/U", "Rb/Sr", "Sr/Y", "La/Nb", "Th/Yb", "Nb/Yb",
    "Gd/Yb", "Dy/Yb", "Ce/Y", "Zr/Nb", "K/Ti", "Ti/V", "Y/Nb", "Th/Nb",
    "La/Ce", "Sr/Ba", "Zr/Y", "Nb/La", "Ce/Yb", "Tb/Yb", "U/Th", "Nb/Zr",
    "La/Lu", "Lu/Hf", "Sm/Yb", "Fe/Mn", "Nb/Y", "Th/La", "Ti/Eu",
]
OXIDE_RATIOS = ["CaO/Al2O3", "Al2O3/TiO2", "K2O/Na2O", "CaO/MgO", "SiO2/Al2O3",
                "FeO/MgO", "Na2O/K2O", "MgO/CaO"]

EXTRA_ISOTOPE_ALIASES = {
    "d18O_rock": ["d18O", "δ18O", "d18O rock", "d18O mineral"],   # rock default; do not override d18O_water
    "d11B": ["d11B", "δ11B"], "d7Li": ["d7Li", "δ7Li"],
    "d26Mg": ["d26Mg", "δ26Mg"], "d44Ca": ["d44Ca", "δ44Ca"],
    "d56Fe": ["d56Fe", "δ56Fe"], "d30Si": ["d30Si", "δ30Si"],
    "d98Mo": ["d98Mo", "δ98Mo"], "d66Zn": ["d66Zn", "δ66Zn"],
    "d37Cl": ["d37Cl", "δ37Cl"], "d15N_bare": ["d15N", "δ15N"],
    "epsilon_Nd": ["eNd", "εNd", "epsilon Nd", "epsilon-Nd", "ENd"],
    "epsilon_Hf": ["eHf", "εHf", "epsilon Hf", "epsilon-Hf", "EHf"],
}

CATIONS = ["Si", "Ti", "Al", "Fe", "Mn", "Mg", "Ca", "Na", "K", "P",
           "Cl", "S", "F", "Br", "I"]
GAS_SPECIES = ["He", "Ne", "Ar", "Kr", "Xe", "CH4", "N2", "H2", "O2", "CO",
               "H2S", "NH3", "C2H6", "C3H8"]
ISOTOPE_GAS = {
    "He3_conc": ["3He", "³He"], "He4_conc": ["4He", "⁴He"],
    "Ne20_conc": ["20Ne", "²⁰Ne"], "Ne21_conc": ["21Ne", "²¹Ne"],
    "Ne22_conc": ["22Ne", "²²Ne"],
    "Ar36_conc": ["36Ar", "³⁶Ar"], "Ar38_conc": ["38Ar", "³⁸Ar"],
    "Ar40_conc": ["40Ar", "⁴⁰Ar"], "Ar40rad_conc": ["40Ar*", "⁴⁰Ar*", "40Ar rad"],
    "Kr84_conc": ["84Kr"], "Xe130_conc": ["130Xe"], "Xe132_conc": ["132Xe"],
    "Xe129_conc": ["129Xe"], "CH4_conc_iso": ["CH₄"],
}
EXTRA_ISOTOPE_RATIOS = {
    "Hf176_Hf177": ["176Hf/177Hf"], "Os187_Os188": ["187Os/188Os"],
    "Re187_Os188": ["187Re/188Os"], "Os186_Os188": ["186Os/188Os"],
    "Pb207_Pb206": ["207Pb/206Pb"], "Sr88_Sr86": ["88Sr/86Sr"],
    "Sm147_Nd144": ["147Sm/144Nd"], "Lu176_Hf177": ["176Lu/177Hf"],
    "Rb87_Sr86": ["87Rb/86Sr"], "U238_Pb204": ["238U/204Pb"],
    "Th232_Pb204": ["232Th/204Pb"], "He4_Ar40rad": ["4He/40Ar*", "4He/40Ar"],
    "Xe129_Xe130": ["129Xe/130Xe"], "Xe136_Xe130": ["136Xe/130Xe"],
    "Xe129_Xe132": ["129Xe/132Xe"], "N15_N14": ["15N/14N"],
}
REE_SUMS = {
    "REE_sum": ["REE", "ΣREE", "total REE", "sum REE", "REE total", "TREE"],
    "LREE_sum": ["LREE", "ΣLREE", "light REE"],
    "HREE_sum": ["HREE", "ΣHREE", "heavy REE"],
    "MREE_sum": ["MREE", "middle REE"],
}
ANOMALIES = {
    "Eu_anomaly": ["Eu/Eu*", "Eu/Eu", "Eu*", "(Eu/Eu*)"],
    "Ce_anomaly": ["Ce/Ce*", "Ce/Ce", "Ce*", "(Ce/Ce*)"],
}
MINERAL_INDICES = {
    "forsterite_content": ["Fo", "Fo#", "forsterite", "Fo content",
                           "Fo (forsterite content)", "Forsterite (Fo) content",
                           "Forsterite content (Fo)", "forsterite content"],
    "anorthite_content": ["An", "An#", "anorthite", "An content",
                          "An (anorthite content)", "anorthite content"],
    "enstatite_content": ["En"], "ferrosilite_content": ["Fs"],
    "wollastonite_content": ["Wo"], "orthoclase_content": ["Or"],
    "albite_content": ["Ab"], "Cr_number": ["Cr#", "Cr-number", "Cr number"],
}
PHYS_ALIASES = {
    "temperature_C": ["Temperature", "temperature", "Temp", "Temp.", "Temperature (T)"],
    "pressure_MPa": ["Pressure", "pressure", "P (MPa)"],
    "pH": ["pH"], "Eh": ["Eh"],
    "fO2": ["fO2", "oxygen fugacity", "f(O2)", "log fO2", "logfO2",
            "fO2 (oxygen fugacity)", "oxygen fugacity (fO2)", "oxygen fugacity fO2"],
    "Delta47": ["Δ47", "D47", "Delta47"], "Delta17O": ["Δ17O", "D17O", "Delta17O"],
    "crustal_thickness_km": ["crustal thickness", "Moho depth", "crust thickness"],
    "salinity": ["salinity", "S (psu)", "salinity (psu)"],
    "alkalinity": ["alkalinity", "total alkalinity", "TA", "Alkalinity"],
    "TDS": ["TDS", "total dissolved solids"],
    "conductivity": ["conductivity", "EC"],
    "Mg_number": ["Mg#", "Mg-number", "Mg number", "100Mg/(Mg+Fe)"],
}
# dissolved polyatomic anions (bare, no charge) -> {sp}_conc
POLYATOMIC_CONC = {
    "SO4": "SO4_conc", "HCO3": "HCO3_conc", "CO3": "CO3_conc",
    "NO3": "NO3_conc", "NO2": "NO2_conc", "PO4": "PO4_conc",
    "NH4": "NH4_conc", "HS": "HS_conc", "OH": "OH_conc",
}


def _build_l1_index() -> dict:
    idx: dict = {}

    def add(alias: str, vid: str):
        key = L0.ascii_fold(alias).strip()
        if key and key not in idx:
            idx[key] = vid

    for ox in MAJOR_OXIDES:
        add(ox, f"{ox}_wt_pct")
    for a in FE_TOTAL_ALIASES:
        add(a, "Fe_total_oxide_wt_pct")
    for vid, aliases in VOLATILES_OXIDE.items():
        for a in aliases:
            add(a, vid)
    for el in TRACE_ELEMENTS:
        add(el, f"{el}_conc")
    for el in REE:
        add(el, f"{el}_conc")
    for r in RATIOS:
        num, den = r.split("/")
        vid = f"{num}_{den}"
        add(r, vid)
        add(f"({r})N", f"{vid}_N")
        add(f"({r})_N", f"{vid}_N")
        add(f"{r}N", f"{vid}_N")
        add(f"{num}/{den}_N", f"{vid}_N")
    for r in OXIDE_RATIOS:
        num, den = r.split("/")
        add(r, f"{num}_{den}")
    for vid, aliases in EXTRA_ISOTOPE_ALIASES.items():
        for a in aliases:
            add(a, vid)
    for el in CATIONS:
        add(el, f"{el}_conc")
    for sp in GAS_SPECIES:
        add(sp, f"{sp}_conc")
    for vid, aliases in ISOTOPE_GAS.items():
        for a in aliases:
            add(a, vid)
    for vid, aliases in EXTRA_ISOTOPE_RATIOS.items():
        for a in aliases:
            add(a, vid)
    for vid, aliases in REE_SUMS.items():
        for a in aliases:
            add(a, vid)
    for vid, aliases in ANOMALIES.items():
        for a in aliases:
            add(a, vid)
    for vid, aliases in MINERAL_INDICES.items():
        for a in aliases:
            add(a, vid)
    for vid, aliases in PHYS_ALIASES.items():
        for a in aliases:
            add(a, vid)
    for sp, vid in POLYATOMIC_CONC.items():
        add(sp, vid)
    return idx


_L1_INDEX = _build_l1_index()


# ---------------------------------------------------------------------------
# Precision guards & corpus-specific pre-passes (Codex 006 verdict)
# ---------------------------------------------------------------------------
_ELEMENT_SET = set(CATIONS) | set(TRACE_ELEMENTS) | set(REE) | {"Br", "I", "H", "C", "N", "O"}
_POLYATOMIC = POLYATOMIC_CONC
_BLOCKLIST = {"x", "X", "f"}                 # too-generic placeholders (Codex #1)
_CORPUS_OVERRIDE = {"F": "F_conc"}           # element wins vs L0 fraction alias (Codex #2)

_CONC_UNIT_RE = re.compile(
    r"(ppm|ppb|ppt|mg\s*/\s*kg|mg\s*/\s*g|[µμu]g\s*/\s*g|ng\s*/\s*g|"
    r"mmol\s*/\s*kg|[µμu]mol\s*/\s*kg|nmol\s*/\s*kg|mol\s*/\s*kg|"
    r"mg\s*/\s*l|[µμu]g\s*/\s*l|mol\s*%)", re.IGNORECASE)
_CHARGE_TAIL = re.compile(r"(\d+)?\s*[+\-]{1,2}$")
_AGE_RE = re.compile(r"\bage\b", re.IGNORECASE)
_TIME_MARKER = re.compile(r"\s*\(\s*t\s*\)\s*$", re.IGNORECASE)


def _has_conc_unit(raw_label, unit):
    return bool(_CONC_UNIT_RE.search(f"{raw_label or ''} {unit or ''}"))


def _is_wt_pct_id(vid):
    return bool(vid) and vid.endswith("_wt_pct")


_CHARGE_FOLD = {"⁺": "+", "⁻": "-", "˗": "-"}


def _fold_charges(s):
    for k, v in _CHARGE_FOLD.items():
        s = s.replace(k, v)
    return s


def _try_ion(folded):
    if not re.search(r"[+\-]{1,2}$", folded):
        return None
    # two interpretations: strip trailing sign only, or charge-magnitude digit + sign
    # (HCO3- -> HCO3 ; SO42- -> SO4 ; Ca2+ -> Ca ; Cl- -> Cl)
    c1 = re.sub(r"\s*[+\-]{1,2}$", "", folded).strip()        # sign only: HCO3- -> HCO3
    c3 = re.sub(r"\s*\d\s*[+\-]{1,2}$", "", folded).strip()   # one charge digit: SO42- -> SO4
    for sp in (c1, c3):
        if sp in _ELEMENT_SET:
            return f"{sp}_conc"
        if sp in _POLYATOMIC:
            return _POLYATOMIC[sp]
    return None


def _try_age(folded):
    if not _AGE_RE.search(folded):
        return None
    low = folded.lower()
    pairs = [
        (("k-ar", "k/ar"), "age_KAr"),
        (("ar-ar", "ar/ar", "40ar/39ar"), "age_ArAr"),
        (("u-pb", "206pb/238u", "207pb/235u", "238u/206pb"), "age_UPb"),
        (("pb-pb", "207pb/206pb"), "age_PbPb"),
        (("rb-sr",), "age_RbSr"), (("sm-nd",), "age_SmNd"),
        (("re-os",), "age_ReOs"), (("th-pb", "208pb/232th"), "age_ThPb"),
        (("fission track", "ft age"), "age_FT"),
        (("(u-th)/he", "u-th/he", "he age"), "age_UThHe"),
        (("14c", "radiocarbon"), "age_14C"),
    ]
    for keys, vid in pairs:
        if any(k in low for k in keys):
            return vid
    return "age"


def _try_co2(raw_label, unit):
    f = L0.ascii_fold(raw_label).strip()
    base = re.sub(r"\b(concentrations?|contents?|conc\.?)\b", "", f, flags=re.IGNORECASE)
    base = re.sub(r"\s*[\(\[].*?[\)\]]\s*", "", base).strip()
    if base.lower() == "pco2":
        return "pCO2"
    if base != "CO2":
        return None
    if _has_conc_unit(raw_label, unit) or re.search(r"\bconcentration", f, re.IGNORECASE):
        return "CO2_conc"
    return "CO2_wt"   # bare CO2 / wt% context -> whole-rock volatile


# ---------------------------------------------------------------------------
# L2 — structural pre-clean (deterministic, presentation-only)
# ---------------------------------------------------------------------------
_UNIT_PAREN = re.compile(
    r"\s*[\(\[]\s*(wt\.?\s*%|ppm|ppb|ppt|wt|µg/g|ug/g|μg/g|mg/kg|mg/g|g/g|"
    r"mol\.?\s*%|at\.?\s*%|atom\s*%|%|‰|permil|per\s*mil|µmol/kg|umol/kg|"
    r"nmol/kg|mmol/kg|mg/l|µg/l|ug/l|ng/g|cps|psu)\s*[\)\]]\s*$",
    re.IGNORECASE,
)
# trailing descriptive words (incl. 'ratio'). NOTE: phase/context parens are NOT stripped.
_TRAILING_WORDS = re.compile(
    r"\b(concentrations?|contents?|abundances?|conc\.?|values?|ratios?)\b", re.IGNORECASE
)


def l2_clean(raw: str) -> str:
    s = L0.ascii_fold(raw).strip()
    s = _TIME_MARKER.sub("", s)                 # strip (t) epsilon time-marker
    prev = None
    for _ in range(2):
        if s == prev:
            break
        prev = s
        s = _UNIT_PAREN.sub("", s).strip()
        s = _TRAILING_WORDS.sub("", s).strip()
    s = re.sub(r"\s*/\s*", "/", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" :=-")
    return s


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def normalize_variable(raw_label, unit=None, phase=None):
    """Return (canonical_id_or_None, layer_tag)."""
    if not raw_label or not raw_label.strip():
        return None, "none"
    folded = _fold_charges(L0.ascii_fold(raw_label).strip())

    # 0. block too-generic placeholders
    if folded in _BLOCKLIST:
        return None, "blocked"
    # 1. ions BEFORE L0 (so F-/Cl-/Ca2+ are concentrations, not L0 derived aliases).
    #    also try after stripping a trailing 'concentration'/'content' word.
    ion = _try_ion(folded) or _try_ion(_fold_charges(_TRAILING_WORDS.sub("", folded).strip()))
    if ion:
        return ion, "ion"
    # 2. corpus override (element wins for colliding bare symbols)
    if folded in _CORPUS_OVERRIDE:
        return _CORPUS_OVERRIDE[folded], "ovr"
    # 3. geochronology age preemption (before any ratio/isotope rule)
    age = _try_age(folded)
    if age:
        return age, "age"
    # 4. CO2 unit/context split
    co2 = _try_co2(raw_label, unit)
    if co2:
        return co2, "co2"
    # 4b. REE-group sum by leading REE / rare-earth alias (Codex-approved, not paren-deletion)
    if re.match(r"^\s*(Σ?REE|TREE|rare\s*earth\s*element)s?\b", folded, re.IGNORECASE):
        return "REE_sum", "ree"

    conc = _has_conc_unit(raw_label, unit)

    def accept(vid):
        # oxide wt_pct guardrail: reject when explicit concentration unit present
        if _is_wt_pct_id(vid) and conc:
            return None
        return vid

    # 5. L0 isotope vocab
    vid = L0.normalize_axis(raw_label)
    if vid and accept(vid):
        return vid, "L0"
    # 6. L1 exact species lookup
    if folded in _L1_INDEX:
        v = accept(_L1_INDEX[folded])
        if v:
            return v, "L1"
    # 7. L2 structural clean, then retry L0 then L1
    cleaned = l2_clean(raw_label)
    if cleaned and cleaned != folded:
        vid = L0.normalize_axis(cleaned)
        if vid and accept(vid):
            return vid, "L0c"
        if cleaned in _L1_INDEX:
            v = accept(_L1_INDEX[cleaned])
            if v:
                return v, "L1c"
    return None, "none"


def l1_vocab_size() -> int:
    return len(set(_L1_INDEX.values()))


if __name__ == "__main__":
    tests = ["MgO", "SiO2 (wt%)", "SiO2 (mg/kg)", "Sr", "La/Yb", "(La/Yb)N",
             "La/Yb ratio", "CO2 concentration", "CO2", "CO₂ concentration (mmol/kg)",
             "F-", "Cl⁻", "Ca2+", "SO₄²⁻", "HCO3-", "x", "X",
             "³He/⁴He ratio", "pH", "FeOt", "εNd", "εNd(t)", "δ18O",
             "87Sr/86Sr", "Yb (ppm)", "K-Ar age", "40Ar/39Ar age", "CaO/Al2O3",
             "129Xe/130Xe", "fO2 (oxygen fugacity)", "Pressure"]
    for t in tests:
        print(f"{t!r:32} -> {normalize_variable(t)}")
    print(f"\nL1 distinct ids: {l1_vocab_size()}")
