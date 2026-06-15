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
# explicit total-iron OXIDE notation -> oxide wt%
FE_TOTAL_ALIASES = ["FeOt", "FeO*", "FeOT", "FeO(t)", "Fe2O3t", "Fe2O3*", "Fe2O3T",
                    "FeOtot", "Fe2O3tot", "TFe2O3", "TFeO", "Fe2O3(T)"]
# ambiguous "total Fe" (could be elemental) -> unit-agnostic total-Fe concentration (Codex 007)
FE_TOTAL_CONC_ALIASES = ["total Fe", "total iron", "FeO_total", "Fe2O3_total",
                         "Fe total", "Fetot", "Fe(total)", "FeT", "ΣFe", "Fe (total)"]
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
    "Ru", "Rh", "Pd", "Os", "Ir", "Pt", "Au", "Hg",
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
    "d34S": ["d34S", "δ34S"], "d33S": ["d33S", "δ33S"], "d36S": ["d36S", "δ36S"],
    "d17O": ["d17O", "δ17O"], "d2H": ["d2H", "δ2H"],
    # bare species-specific deltas (no permil unit) -> L0 species ids (Codex 012 tail recovery)
    "d13C_CO2": ["d13C-CO2", "d13C of CO2", "d13CO2", "d13C (CO2)", "d13C-CO₂"],
    "d13C_CH4": ["d13C-CH4", "d13C of CH4", "d13C (CH4)"],
    "dD_CH4": ["dD-CH4", "dD of CH4", "D-CH4"],
    "d13C_carbonate": ["d13C-carbonate", "d13C of carbonate", "d13Ccarb"],
    "d13C_DIC": ["d13C-DIC", "d13C of DIC", "d13CDIC"],
    "epsilon_Nd": ["eNd", "εNd", "epsilon Nd", "epsilon-Nd", "ENd", "epsilon_Nd",
                   "epsilon_Nd (εNd)", "epsilon Nd (εNd)"],
    "epsilon_Hf": ["eHf", "εHf", "epsilon Hf", "epsilon-Hf", "EHf", "epsilon_Hf"],
    "tritium": ["3H", "tritium", "3H (tritium)", "tritium (3H)"],
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
    "D_H": ["D/H"], "H2_H1": ["2H/1H"],   # hydrogen isotope ratios (Codex 007)
}
REE_SUMS = {
    "REE_sum": ["REE", "ΣREE", "total REE", "sum REE", "REE total"],
    "LREE_sum": ["LREE", "ΣLREE", "light REE"],
    "HREE_sum": ["HREE", "ΣHREE", "heavy REE"],
    "MREE_sum": ["MREE", "middle REE"],
}
ANOMALIES = {
    "Eu_anomaly": ["Eu/Eu*", "Eu/Eu", "Eu*", "(Eu/Eu*)"],
    "Ce_anomaly": ["Ce/Ce*", "Ce/Ce", "Ce*", "(Ce/Ce*)"],
    "Sr_anomaly": ["Sr/Sr*", "Sr*"], "Ti_anomaly": ["Ti/Ti*", "Ti*"],
    "Nb_anomaly": ["Nb/Nb*", "Nb*"], "Hf_anomaly": ["Hf/Hf*", "Hf*"],
    "Zr_anomaly": ["Zr/Zr*", "Zr*"], "W_anomaly": ["W/W*", "W*"],
    "Pb_anomaly": ["Pb/Pb*"], "Y_anomaly": ["Y/Y*"],
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
    "temperature": ["Temperature", "temperature", "Temp", "Temp.", "Temperature (T)",
                    "water temperature", "soil temperature", "sea temperature",
                    "bottom water temperature", "spring temperature", "fluid temperature",
                    "air temperature", "surface temperature"],
    "pressure": ["Pressure", "pressure", "P (MPa)", "P (GPa)", "P (kbar)"],
    "pH": ["pH"], "Eh": ["Eh"],
    "fO2": ["fO2", "oxygen fugacity", "f(O2)", "log fO2", "logfO2",
            "fO2 (oxygen fugacity)", "oxygen fugacity (fO2)", "oxygen fugacity fO2"],
    # cycle 5 — physical / geophysical (unit-agnostic ids; units stay in sidecar)
    "density": ["density", "bulk density", "rho", "grain density", "dry density"],
    "heat_flow": ["heat flow", "heat-flow", "surface heat flow", "heat flow density"],
    "heat_flux": ["heat flux"],
    "potential_temperature": ["potential temperature", "Tp", "mantle potential temperature"],
    "Vp": ["Vp", "P-wave velocity", "P wave velocity", "compressional velocity",
           "P-wave velocity (Vp)", "Rayleigh wave phase velocity"],
    "Vs": ["Vs", "S-wave velocity", "S wave velocity", "shear velocity",
           "shear-wave velocity", "S-wave velocity (Vs)"],
    "Vp_Vs_ratio": ["Vp/Vs", "Vp/Vs ratio", "vp/vs"],
    "gravity_anomaly": ["gravity anomaly", "Bouguer gravity anomaly", "Bouguer anomaly",
                        "free-air anomaly", "free air anomaly"],
    "magnetic_anomaly": ["magnetic anomaly", "magnetic anomalies"],
    "porosity": ["porosity"], "permeability": ["permeability"],
    "vesicularity": ["vesicularity", "vesicle content"],
    "viscosity": ["viscosity"], "DIC": ["DIC", "dissolved inorganic carbon",
                                        "DIC (dissolved inorganic carbon)"],
    "d_excess": ["d-excess", "deuterium excess"],
    # cycle 6 — water/field & physical clusters (Codex 012)
    "electrical_conductivity": ["electrical conductivity", "EC", "specific conductance"],
    "dissolved_oxygen": ["dissolved oxygen", "DO"],
    "DOC": ["DOC", "dissolved organic carbon"],
    "ORP": ["ORP", "oxidation-reduction potential", "redox potential"],
    "thermal_conductivity": ["thermal conductivity"],
    "magnetic_susceptibility": ["magnetic susceptibility", "susceptibility"],
    "heat_production": ["heat production", "radiogenic heat production"],
    "cooling_rate": ["cooling rate"], "water_content": ["water content"],
    "melt_fraction": ["melt fraction", "degree of melting", "partial melting degree"],
    "alkali_sum": ["Na2O + K2O", "Na2O+K2O", "K2O + Na2O", "K2O+Na2O", "total alkalis"],
    "LREE_HREE": ["LREE/HREE", "LREE/HREE ratio"],
    "Rn_activity": ["222Rn", "Rn", "radon", "222Rn activity"],
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
    for a in FE_TOTAL_CONC_ALIASES:
        add(a, "Fe_total_conc")
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
_JUNK_VALUES = {"not measured", "not determined", "not analyzed", "not analysed",
                "n.d.", "nd", "n/a", "na", "n.a.", "below detection limit", "bdl",
                "b.d.l.", "not detected", "no data", "-", "--", "---", "tbd"}
_CORPUS_OVERRIDE = {"F": "F_conc"}           # element wins vs L0 fraction alias (Codex #2)
# elements whose oxidation state is geochemically distinct (preserve charge for these; Codex 007)
_REDOX_MULTIVALENT = {"Fe", "Mn", "Cr", "Ce", "Eu", "U", "Cu", "V", "Ti",
                      "Co", "As", "Sb", "Sn", "Tl", "S", "N"}

_CONC_UNIT_RE = re.compile(
    r"(ppm|ppb|ppt|mg\s*/\s*kg|mg\s*/\s*g|[µμu]g\s*/\s*g|ng\s*/\s*g|"
    r"mmol\s*/\s*kg|[µμu]mol\s*/\s*kg|nmol\s*/\s*kg|mol\s*/\s*kg|"
    r"[mµμun]?mol\s*/\s*mol|mg\s*/\s*l|[µμu]g\s*/\s*l|mol\s*%)", re.IGNORECASE)
_CHARGE_TAIL = re.compile(r"(\d+)?\s*[+\-]{1,2}$")
_AGE_RE = re.compile(r"\bages?\b", re.IGNORECASE)   # singular + plural (Codex 011)
_TIME_MARKER = re.compile(r"\s*\(\s*t\s*\)\s*$", re.IGNORECASE)
# REE labels that are NOT an abundance/sum (block from REE_sum) — Codex 008
_REE_BLOCK = re.compile(
    r"\b(partition|coefficients?|distributions?|kd|patterns?|profiles?|normali[sz]ed|"
    r"anomal(y|ies)|ratios?|fractionation|spider|temperature|thermomet|d_[a-z])", re.IGNORECASE)


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
    # monatomic ion with explicit oxidation state: preserve state for redox-multivalent
    # (Fe3+ -> Fe3_conc ; Fe2+ -> Fe2_conc ; Ca2+ -> Ca_conc)
    mm = re.match(r"^([A-Z][a-z]?)(\d?)\s*[+\-]{1,2}$", folded)
    if mm and mm.group(1) in _ELEMENT_SET:
        el, mag = mm.group(1), mm.group(2)
        if mag and el in _REDOX_MULTIVALENT:
            return f"{el}{mag}_conc"
        return f"{el}_conc"
    # polyatomic / general: two interpretations (HCO3- -> HCO3 ; SO42- -> SO4)
    c1 = re.sub(r"\s*[+\-]{1,2}$", "", folded).strip()
    c3 = re.sub(r"\s*\d\s*[+\-]{1,2}$", "", folded).strip()
    for sp in (c1, c3):
        if sp in _ELEMENT_SET:
            return f"{sp}_conc"
        if sp in _POLYATOMIC:
            return _POLYATOMIC[sp]
    return None


_AGE_METHODS = [
    (("k-ar", "k/ar"), "age_KAr"),
    (("ar-ar", "ar/ar", "40ar/39ar", "39ar/40ar"), "age_ArAr"),
    (("u-pb", "206pb/238u", "207pb/235u", "238u/206pb"), "age_UPb"),
    (("pb-pb", "207pb/206pb"), "age_PbPb"),
    (("rb-sr",), "age_RbSr"), (("sm-nd",), "age_SmNd"),
    (("re-os", "re depletion", "re-depletion", "trd", "t_rd"), "age_ReOs"),
    (("th-pb", "208pb/232th"), "age_ThPb"),
    (("apatite fission", "aft", "fission track", "fission-track", "ft age"), "age_FT"),
    (("osl", "irsl", "luminescence", "pir-irsl"), "age_OSL"),
    (("exposure", "cosmogenic", "10be exposure", "26al/10be", "surface exposure"), "age_exposure"),
    (("3h/3he", "3h-3he", "tritium"), "age_3H3He"),
    (("(u-th)/he", "u-th/he", "(u-th)-he", "u,th-4he", "u-th-he"), "age_UThHe"),
    (("14c", "radiocarbon"), "age_14C"),
]
# generic 'age' only when 'age' is the trailing concept (ends with age, or age + unit/paren).
# rejects "Age grid misfit", "average", etc.
_AGE_TAIL_RE = re.compile(
    r"\bages?\b[\s)\]]*$"
    r"|\bages?\b\s*(\([^)]*\)|[:=]?\s*-?\d|\s+(ma|ka|ga|myr|kyr|gyr|yr|years?|b\.?p\.?))",
    re.IGNORECASE)


_ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7}
_VALENCE_RE = re.compile(r"^([A-Z][a-z]?)\s*\(\s*(VII|VI|IV|V|I{1,3})\s*\)")


def _try_valence(folded):
    """Fe(III)/Mn(IV)/ferric/ferrous -> oxidation-state-preserving conc (Codex 008)."""
    low = folded.lower()
    # total-iron OXIDE phrases ("total iron as ferrous oxide", FeOT) are not valence ions (Codex 010/011)
    if "oxide" in low or "total iron" in low or re.search(r"feo[t*]|fe2o3", low.replace(" ", "")):
        return None
    # ratio context (Fe(III)/ΣFe ratio) is a redox ratio, not a valence concentration (self-audit c5)
    if "/" in folded or "ratio" in low:
        return None
    m = _VALENCE_RE.match(folded)
    if m and m.group(1) in _REDOX_MULTIVALENT:
        n = _ROMAN.get(m.group(2).lower())
        if n:
            return f"{m.group(1)}{n}_conc"
    low = folded.lower()
    if "ferric" in low:
        return "Fe3_conc"
    if "ferrous" in low:
        return "Fe2_conc"
    return None


def _try_age(folded):
    if not _AGE_RE.search(folded):
        return None
    low = re.sub(r"[${}\\^]", "", folded).lower()   # strip LaTeX so $^{14}C$ -> 14c (Codex 011)
    for keys, vid in _AGE_METHODS:
        if any(k in low for k in keys):
            return vid
    if _AGE_TAIL_RE.search(folded):
        return "age"
    return None


_PHASE_CTX_RE = re.compile(
    r"\b(dissolved|aqueous|gas|gaseous|fluid|soil\s*gas|vapou?r|porewater|"
    r"pore\s*water|seawater|melt|fluid\s*inclusion)\b", re.IGNORECASE)


def _try_co2(raw_label, unit):
    f = L0.ascii_fold(raw_label).strip()
    low = f.lower()
    base = re.sub(r"\b(concentrations?|contents?|conc\.?)\b", "", f, flags=re.IGNORECASE)
    base = re.sub(r"\s*[\(\[].*?[\)\]]\s*", " ", base).strip()
    base = re.sub(r"\s+", " ", base).strip()
    if base.lower() == "pco2":
        return "pCO2"
    if base != "CO2":
        return None
    # phase/concentration context -> CO2_conc ; only bare CO2 / wt% -> CO2_wt (Codex 008)
    if (_has_conc_unit(raw_label, unit) or "concentration" in low
            or _PHASE_CTX_RE.search(low)):
        return "CO2_conc"
    return "CO2_wt"


# cycle 5 — flux & dissolved-oxide (Codex 011 greenlight)
_FLUX_SPECIES = {"CO2", "SO2", "HCl", "HF", "H2S", "CH4", "He", "CO", "H2O",
                 "N2", "Hg", "SO3", "H2", "O2"} | {"3He", "4He"}
_DISSOLVED_RE = re.compile(r"\b(dissolved|aqueous|in\s+solution|porewater|seawater)\b",
                           re.IGNORECASE)


def _try_flux(folded):
    m = re.match(r"^(.+?)\s+flux(es)?\b", folded, re.IGNORECASE)
    if not m:
        return None
    sp = m.group(1).strip()
    if sp in _FLUX_SPECIES or sp in GAS_SPECIES:
        return f"{sp}_flux"
    if sp.lower() == "heat":
        return "heat_flux"
    return None


def _try_dissolved_oxide(folded):
    """dissolved/aqueous SiO2 etc. -> {ox}_conc, never wt_pct (Codex 011)."""
    if not _DISSOLVED_RE.search(folded):
        return None
    for ox in MAJOR_OXIDES:
        if re.search(rf"(?<![A-Za-z]){re.escape(ox)}(?![A-Za-z0-9])", folded):
            return f"{ox}_conc"
    return None


# cycle 6 — partial pressure & bracket-concentration (Codex 012)
_PP_SPECIES = {"co2": "CO2", "h2o": "H2O", "o2": "O2", "h2": "H2", "n2": "N2",
               "ch4": "CH4", "so2": "SO2", "h2s": "H2S", "he": "He", "ar": "Ar"}
_PP_RE = re.compile(r"^p\s*\(\s*([A-Za-z0-9]+)\s*\)$", re.IGNORECASE)


def _try_partial_pressure(folded):
    m = _PP_RE.match(folded)
    if not m:
        return None
    sp = _PP_SPECIES.get(m.group(1).lower())
    return f"p{sp}" if sp else None


def _try_bracket(folded):
    m = re.match(r"^\[\s*([A-Za-z0-9+\-]+)\s*\]$", folded)
    if not m:
        return None
    inner = m.group(1).strip()
    if inner in _ELEMENT_SET or inner in _ISO_GAS_LABELS or inner in GAS_SPECIES:
        return f"{inner}_conc"
    return None


# ---------------------------------------------------------------------------
# L2 — structural pre-clean (deterministic, presentation-only)
# ---------------------------------------------------------------------------
_UNIT_PAREN = re.compile(
    r"\s*[\(\[]\s*(wt\.?\s*%|ppm|ppb|ppt|wt|µg/g|ug/g|μg/g|mg/kg|mg/g|g/g|"
    r"mol\.?\s*%|at\.?\s*%|atom\s*%|%|‰|permil|per\s*mil|µmol/kg|umol/kg|"
    r"nmol/kg|mmol/kg|mg/l|µg/l|ug/l|ng/g|cps|psu|"
    r"gpa|mpa|kbar|kbars|kb|bar|deg\s*c|°c|degc|km/s|km|"
    r"mw/m\^?2|g/cm\^?3|kg/m\^?3)\s*[\)\]]\s*$",
    re.IGNORECASE,
)
# trailing descriptive words (incl. 'ratio'). NOTE: phase/context parens are NOT stripped.
_TRAILING_WORDS = re.compile(
    r"\b(concentrations?|contents?|abundances?|conc\.?|values?|ratios?)\b", re.IGNORECASE
)


def l2_clean(raw: str) -> str:
    s = _fold_charges(L0.ascii_fold(raw).strip()).replace("^", "")   # strip caret (^87Sr/^86Sr)
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
# cycle 4 (PENDING Codex 007 greenlight) — generic ratio / isotope ratio / gloss / CI.
# Wired into normalize_variable as fallback steps, gated by CYCLE4_ENABLED.
# These only resolve currently-unmatched labels (never override existing matches).
# ---------------------------------------------------------------------------
CYCLE4_ENABLED = True   # activated cycle-4 wake (self-audit clean; Codex retroactive gate)

_ISO_GAS_LABELS = {"3He", "4He", "20Ne", "21Ne", "22Ne", "36Ar", "38Ar", "40Ar",
                   "84Kr", "129Xe", "130Xe", "132Xe", "136Xe"}
_RATIO_TOKENS = (_ELEMENT_SET | set(MAJOR_OXIDES) | set(GAS_SPECIES) | set(REE)
                 | _ISO_GAS_LABELS | {"CO2", "H2O", "CH4"})
_ISO_ELEMENTS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si",
    "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",
    "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb",
    "Mo", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs",
    "Ba", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm",
    "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb",
    "Bi", "Th", "U",
}
_PHASE_UNIT_WORDS = {
    "water", "rock", "mineral", "fluid", "gas", "seawater", "porewater", "pore water",
    "carbonate", "olivine", "clinopyroxene", "orthopyroxene", "cpx", "opx",
    "plagioclase", "plag", "glass", "melt", "whole rock", "wr", "bulk", "groundmass",
    "matrix", "vapor", "liquid", "aqueous", "dissolved", "smow", "vsmow", "pdb",
    "vpdb", "cdt", "permil", "per mil", "r/ra", "ra", "n",
}
_UNIT_SLASH_RE = re.compile(
    r"^(mg|µg|μg|ug|ng|pg|g|kg|mol|mmol|µmol|umol|nmol|pmol|cm|km|m|l|ml)\s*/\s*"
    r"(kg|g|mg|l|ml|s|m|cm|yr|a|mol)$", re.IGNORECASE)
_PHYS_RATIO = {"vp/vs", "vs/vp", "p/s", "s/p"}
_ISO_RATIO_RE = re.compile(r"^(\d{1,3})([A-Z][a-z]?)\s*/\s*(\d{1,3})([A-Z][a-z]?)$")


def _try_isotope_ratio(folded):
    m = _ISO_RATIO_RE.match(folded)
    if not m:
        return None
    m1, e1, m2, e2 = m.groups()
    if e1 in _ISO_ELEMENTS and e2 in _ISO_ELEMENTS:
        return f"{e1}{m1}_{e2}{m2}"
    return None


def _try_generic_ratio(folded):
    if folded.count("/") != 1:
        return None
    if _UNIT_SLASH_RE.match(folded) or folded.lower() in _PHYS_RATIO:
        return None
    a, b = (t.strip() for t in folded.split("/"))
    if a in _RATIO_TOKENS and b in _RATIO_TOKENS:
        return f"{a}_{b}"
    return None


ELEMENT_NAMES = {
    "hydrogen": "H", "helium": "He", "lithium": "Li", "beryllium": "Be", "boron": "B",
    "carbon": "C", "nitrogen": "N", "oxygen": "O", "fluorine": "F", "neon": "Ne",
    "sodium": "Na", "magnesium": "Mg", "aluminium": "Al", "aluminum": "Al",
    "silicon": "Si", "phosphorus": "P", "sulfur": "S", "sulphur": "S", "chlorine": "Cl",
    "argon": "Ar", "potassium": "K", "calcium": "Ca", "scandium": "Sc", "titanium": "Ti",
    "vanadium": "V", "chromium": "Cr", "manganese": "Mn", "iron": "Fe", "cobalt": "Co",
    "nickel": "Ni", "copper": "Cu", "zinc": "Zn", "gallium": "Ga", "germanium": "Ge",
    "arsenic": "As", "selenium": "Se", "bromine": "Br", "krypton": "Kr", "rubidium": "Rb",
    "strontium": "Sr", "yttrium": "Y", "zirconium": "Zr", "niobium": "Nb",
    "molybdenum": "Mo", "ruthenium": "Ru", "rhodium": "Rh", "palladium": "Pd",
    "silver": "Ag", "cadmium": "Cd", "indium": "In", "tin": "Sn", "antimony": "Sb",
    "tellurium": "Te", "iodine": "I", "xenon": "Xe", "caesium": "Cs", "cesium": "Cs",
    "barium": "Ba", "lanthanum": "La", "cerium": "Ce", "praseodymium": "Pr",
    "neodymium": "Nd", "samarium": "Sm", "europium": "Eu", "gadolinium": "Gd",
    "terbium": "Tb", "dysprosium": "Dy", "holmium": "Ho", "erbium": "Er", "thulium": "Tm",
    "ytterbium": "Yb", "lutetium": "Lu", "hafnium": "Hf", "tantalum": "Ta",
    "tungsten": "W", "rhenium": "Re", "osmium": "Os", "iridium": "Ir", "platinum": "Pt",
    "gold": "Au", "mercury": "Hg", "thallium": "Tl", "lead": "Pb", "bismuth": "Bi",
    "thorium": "Th", "uranium": "U",
}
# paren that re-qualifies the meaning -> outer is NOT the bare element/variable
_QUALIFIER_WORDS = re.compile(
    r"\b(coefficient|partition|polydispersity|amplitude|kappa|model|parameter|"
    r"index|excess|normali[sz]ed|fraction|misfit|grid|enrichment|disequilibrium|"
    r"deficit|apparent|stage|two-stage)\b", re.IGNORECASE)


def _try_gloss(folded):
    m = re.match(r"^(.*?)\s*\(([^()]+)\)\s*$", folded)   # single, non-nested paren at end
    if not m:
        return None
    outer, inner = m.group(1).strip(), m.group(2).strip()
    il, ol = inner.lower(), outer.lower()
    # never strip phase/unit/context parens
    if (il in _PHASE_UNIT_WORDS or _has_conc_unit(inner, None)
            or _UNIT_PAREN.search(f"({inner})") or "permil" in il or "%" in inner):
        return None
    # normalized-ratio restatement -> produce {A}_{B}_N instead of plain ratio (Codex 009/012)
    if re.search(r"[a-z]+n\s*/\s*[a-z]+n|normali[sz]ed|chondrite|primitive\s*mantle"
                 r"|n-morb|e-morb|pm-normal", il):
        rid = _try_generic_ratio(outer)
        if not rid and "/" in outer:
            rid = _L1_INDEX.get(L0.ascii_fold(outer).strip())
        if rid and not rid.endswith("_N"):
            return rid + "_N"
        return None
    # (1) high-precision: full element name <-> its symbol
    if ol in ELEMENT_NAMES and inner == ELEMENT_NAMES[ol]:
        return f"{inner}_conc"
    if il in ELEMENT_NAMES and outer == ELEMENT_NAMES[il]:
        return f"{outer}_conc"
    # (2) outer IS the variable and the paren is a plain gloss (no meaning-changing qualifier)
    if not _QUALIFIER_WORDS.search(folded):
        if outer in _L1_INDEX:
            return _L1_INDEX[outer]
        v = L0.normalize_axis(outer)
        if v:
            return v
        ci = _L1_CI.get(outer.lower())   # case-insensitive descriptive (Forsterite, TDS, conductivity)
        if ci:
            return ci
    return None


_L1_CI = {k.lower(): v for k, v in _L1_INDEX.items()
          if (" " in k or (len(k) >= 5 and k.isalpha()))}


def _try_ci(folded):
    return _L1_CI.get(folded.lower())


def _cycle4(folded):
    """Fallback resolution (cycle 4). Returns (id, tag) or (None, None)."""
    v = _try_isotope_ratio(folded)
    if v:
        return v, "isorat"
    v = _try_generic_ratio(folded)
    if v:
        return v, "genrat"
    v = _try_gloss(folded)
    if v:
        return v, "gloss"
    v = _try_ci(folded)
    if v:
        return v, "ci"
    return None, None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def normalize_variable(raw_label, unit=None, phase=None):
    """Return (canonical_id_or_None, layer_tag)."""
    if not raw_label or not raw_label.strip():
        return None, "none"
    folded = _fold_charges(L0.ascii_fold(raw_label).strip()).replace("^", "")

    # 0. block too-generic placeholders / non-value junk
    if folded in _BLOCKLIST:
        return None, "blocked"
    if folded.lower() in _JUNK_VALUES:
        return None, "junk"
    # 1. ions BEFORE L0 (so F-/Cl-/Ca2+ are concentrations, not L0 derived aliases).
    #    also try after stripping a trailing 'concentration'/'content' word.
    ion = _try_ion(folded) or _try_ion(_fold_charges(_TRAILING_WORDS.sub("", folded).strip()))
    if ion:
        return ion, "ion"
    # 2. corpus override (element wins for colliding bare symbols)
    if folded in _CORPUS_OVERRIDE:
        return _CORPUS_OVERRIDE[folded], "ovr"
    # 2b. valence/speciation (Fe(III), ferric…) before bulk-element routing
    val = _try_valence(folded)
    if val:
        return val, "val"
    # 2c. partial pressure P(CO2)->pCO2 (not phosphorus) ; bracket [He]->He_conc — cycle 6
    pp = _try_partial_pressure(folded)
    if pp:
        return pp, "pp"
    brk = _try_bracket(folded)
    if brk:
        return brk, "brk"
    # 3. geochronology age preemption (before any ratio/isotope rule)
    age = _try_age(folded)
    if age:
        return age, "age"
    # 3b. flux (never route flux to concentration/wt%) — cycle 5
    flux = _try_flux(folded)
    if flux:
        return flux, "flux"
    # 4. CO2 unit/context split
    co2 = _try_co2(raw_label, unit)
    if co2:
        return co2, "co2"
    # 4a. dissolved/aqueous oxide -> {ox}_conc (not wt_pct) — cycle 5
    dox = _try_dissolved_oxide(folded)
    if dox:
        return dox, "dox"
    # 4b. REE group — but NOT coefficient/pattern/anomaly/ratio/temperature labels (Codex 008/010)
    if not _REE_BLOCK.search(folded):
        if re.match(r"^\s*(Σ?REE|rare\s*earth\s*element)s?\b", folded, re.IGNORECASE):
            # explicit yttrium in the list/name -> REE_Y_sum (Codex 011)
            if re.search(r"\bY\b|yttrium|REE[\s\-+]*Y\b", folded, re.IGNORECASE):
                return "REE_Y_sum", "ree"
            return "REE_sum", "ree"

    conc = _has_conc_unit(raw_label, unit)

    def accept(vid):
        # oxide wt_pct + explicit concentration unit -> route to {ox}_conc (Codex 011)
        if _is_wt_pct_id(vid) and conc:
            return vid[:-7] + "_conc"   # strip "_wt_pct"
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
        # re-apply pre-passes on cleaned so unit-stripped "F (ppm)"->"F" can't hit L0 fraction alias
        if cleaned in _BLOCKLIST:
            return None, "blocked"
        if cleaned in _CORPUS_OVERRIDE:
            return _CORPUS_OVERRIDE[cleaned], "ovr"
        vid = L0.normalize_axis(cleaned)
        if vid and accept(vid):
            return vid, "L0c"
        if cleaned in _L1_INDEX:
            v = accept(_L1_INDEX[cleaned])
            if v:
                return v, "L1c"
    # 8. cycle 4 fallbacks (only when greenlit; never overrides existing matches)
    if CYCLE4_ENABLED:
        v, tag = _cycle4(folded)
        if v:
            return v, tag
        if cleaned and cleaned != folded:
            v, tag = _cycle4(cleaned)
            if v:
                return v, tag
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
