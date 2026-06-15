"""
VP-NORM-1 corpus variable normalizer (layered, deterministic, non-destructive).

Maps a sidecar `variables_measured[].raw_label` to a canonical variable id.
Returns None (-> stays `raw_label_only`) when no confident match — NEVER force.

Layers (PR#16 §0.7):
  L0  isotope vocab    -- reuse geochem normalize.py (He/Ne/Ar/Sr/Nd/Pb ratios, delta isotopes)
  L1  standard geochem -- major oxides, trace elements, REE, common element ratios (the 87% bulk)
  L2  structural clean  -- strip unit-parens / 'concentration' words / normalize ratio slashes, then retry L0+L1
  (L3 phase/species disambiguation: later cycle)

Precision-first: element-symbol matches are EXACT (case-sensitive) to avoid fuzzy false hits.
The coverage/precision loop (with Codex audit) refines aliases each cycle.
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
# id convention (cycle-1 default — flagged to Codex for ratification):
#   oxide  X      -> {X}_wt_pct        (oxides are ~always wt%)
#   trace/REE El  -> {El}_conc         (unit-agnostic; unit lives in sidecar field)
#   ratio  A/B    -> {A}_{B}           (normalized (A/B)N -> {A}_{B}_N)

MAJOR_OXIDES = [
    "SiO2", "TiO2", "Al2O3", "Fe2O3", "FeO", "MnO", "MgO", "CaO",
    "Na2O", "K2O", "P2O5", "Cr2O3", "NiO", "SO3", "BaO", "SrO", "CoO",
]
# total-iron forms collapse to one id
FE_TOTAL_ALIASES = ["FeOt", "FeO*", "FeOT", "FeO(t)", "Fe2O3t", "Fe2O3*", "Fe2O3T",
                    "FeOtot", "Fe2O3tot", "total Fe", "total iron", "FeO_total", "Fe2O3_total",
                    "TFe2O3", "TFeO", "Fe2O3(T)"]
VOLATILES_OXIDE = {  # special wt% volatiles
    "LOI": ["LOI", "L.O.I.", "loss on ignition"],
    "H2O_plus": ["H2O+", "H2O(+)"],
    "H2O_minus": ["H2O-", "H2O(-)"],
    "H2O_total": ["H2O", "H2O total", "total H2O", "H2Ot"],
    "CO2_wt": ["CO2"],  # as wt% volatile (distinct from CO2/3He ratio in L0)
}

TRACE_ELEMENTS = [
    "Li", "Be", "B", "Sc", "V", "Cr", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",
    "As", "Se", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "Cs", "Ba", "Hf", "Ta", "W", "Re", "Tl", "Pb", "Bi", "Th", "U",
]
REE = ["La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]

# common element / oxide ratios (numerator/denominator). normalized (…)N handled separately.
RATIOS = [
    "La/Yb", "La/Sm", "Sm/Nd", "Ce/Pb", "Nb/Ta", "Zr/Hf", "Th/U", "Ba/Nb",
    "Ba/La", "Ba/Th", "Nb/U", "Rb/Sr", "Sr/Y", "La/Nb", "Th/Yb", "Nb/Yb",
    "Gd/Yb", "Dy/Yb", "Ce/Y", "Zr/Nb", "K/Ti", "Ti/V", "Y/Nb", "Th/Nb",
    "La/Ce", "Sr/Ba", "Zr/Y", "Nb/La", "Ce/Yb", "Tb/Yb", "U/Th", "Nb/Zr",
    "La/Lu", "Lu/Hf", "Sm/Yb",
]

# delta (rock/mineral) stable isotopes NOT already in L0, plus epsilon notations
EXTRA_ISOTOPE_ALIASES = {
    "d18O_rock": ["d18O", "δ18O", "d18O rock", "d18O mineral"],   # rock context (L0 has d18O_water)
    "d11B": ["d11B", "δ11B"],
    "d7Li": ["d7Li", "δ7Li"],
    "d26Mg": ["d26Mg", "δ26Mg"],
    "d44Ca": ["d44Ca", "δ44Ca"],
    "d56Fe": ["d56Fe", "δ56Fe"],
    "d30Si": ["d30Si", "δ30Si"],
    "d98Mo": ["d98Mo", "δ98Mo"],
    "d66Zn": ["d66Zn", "δ66Zn"],
    "d37Cl": ["d37Cl", "δ37Cl"],
    "epsilon_Nd": ["eNd", "εNd", "epsilon Nd", "epsilon-Nd", "ENd"],
    "epsilon_Hf": ["eHf", "εHf", "epsilon Hf", "epsilon-Hf", "EHf"],
}

# --- cycle 2 additions ---------------------------------------------------
# bare major-element cations (element form, not oxide) -> {El}_conc
CATIONS = ["Si", "Ti", "Al", "Fe", "Mn", "Mg", "Ca", "Na", "K", "P",
           "Cl", "S", "F", "Br", "I"]
# molecular / noble gas species (bulk) -> {sp}_conc
GAS_SPECIES = ["He", "Ne", "Ar", "Kr", "Xe", "CH4", "N2", "H2", "O2", "CO",
               "H2S", "NH3", "H2O_gas", "C2H6", "C3H8"]
# mass-prefixed isotope-specific gas concentrations -> {El}{mass}_conc
ISOTOPE_GAS = {
    "He3_conc": ["3He", "³He"], "He4_conc": ["4He", "⁴He"],
    "Ne20_conc": ["20Ne", "²⁰Ne"], "Ne21_conc": ["21Ne", "²¹Ne"],
    "Ne22_conc": ["22Ne", "²²Ne"],
    "Ar36_conc": ["36Ar", "³⁶Ar"], "Ar38_conc": ["38Ar", "³⁸Ar"],
    "Ar40_conc": ["40Ar", "⁴⁰Ar"], "Ar40rad_conc": ["40Ar*", "⁴⁰Ar*", "40Ar rad"],
    "Kr84_conc": ["84Kr"], "Xe130_conc": ["130Xe"], "Xe132_conc": ["132Xe"],
    "Xe129_conc": ["129Xe"], "CH4_conc": ["CH4", "CH₄"], "CO2_conc_gas": ["pCO2"],
}
# additional radiogenic / stable isotope ratios not in L0
EXTRA_ISOTOPE_RATIOS = {
    "Hf176_Hf177": ["176Hf/177Hf"], "Os187_Os188": ["187Os/188Os"],
    "Re187_Os188": ["187Re/188Os"], "U238_Pb204": ["238U/204Pb", "mu", "238U/204Pb (mu)"],
    "Th232_Pb204": ["232Th/204Pb"], "Pb207_Pb206": ["207Pb/206Pb"],
    "Sr88_Sr86": ["88Sr/86Sr"], "Os186_Os188": ["186Os/188Os"],
    "He4_Ar40rad": ["4He/40Ar*", "4He/40Ar"],
}
# REE-group sums / fractions
REE_SUMS = {
    "REE_sum": ["REE", "ΣREE", "total REE", "sum REE", "REE total", "TREE"],
    "LREE_sum": ["LREE", "ΣLREE", "light REE"],
    "HREE_sum": ["HREE", "ΣHREE", "heavy REE"],
    "MREE_sum": ["MREE", "middle REE"],
}
# anomalies (deviation from chondrite-normalized neighbours)
ANOMALIES = {
    "Eu_anomaly": ["Eu/Eu*", "Eu/Eu", "Eu*", "(Eu/Eu*)"],
    "Ce_anomaly": ["Ce/Ce*", "Ce/Ce", "Ce*", "(Ce/Ce*)"],
}
# mineral end-member / composition indices
MINERAL_INDICES = {
    "forsterite_content": ["Fo", "Fo#", "forsterite", "Fo content"],
    "anorthite_content": ["An", "An#", "anorthite", "An content"],
    "enstatite_content": ["En"], "ferrosilite_content": ["Fs"],
    "wollastonite_content": ["Wo"], "orthoclase_content": ["Or"],
    "albite_content": ["Ab"], "Cr_number": ["Cr#", "Cr-number", "Cr number"],
}

# physical / chemical scalars
PHYS_ALIASES = {
    "temperature_C": ["Temperature", "temperature", "Temp", "Temp."],
    "pH": ["pH"],
    "Eh": ["Eh"],
    "salinity": ["salinity", "S (psu)", "salinity (psu)"],
    "alkalinity": ["alkalinity", "total alkalinity", "TA"],
    "TDS": ["TDS", "total dissolved solids"],
    "conductivity": ["conductivity", "EC"],
    "Mg_number": ["Mg#", "Mg-number", "Mg number", "100Mg/(Mg+Fe)"],
    "loss_on_ignition_dup": [],  # placeholder (LOI handled in volatiles)
}


def _build_l1_index() -> dict[str, str]:
    """alias(folded) -> canonical id. Exact (case-sensitive ASCII-fold) lookup."""
    idx: dict[str, str] = {}

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
        add(r, vid)                 # La/Yb
        add(f"({r})N", f"{vid}_N")  # (La/Yb)N
        add(f"({r})_N", f"{vid}_N")
        add(f"{r}N", f"{vid}_N")    # La/YbN
        add(f"{num}/{den}_N", f"{vid}_N")
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
    return idx


_L1_INDEX = _build_l1_index()


# ---------------------------------------------------------------------------
# L2 — structural pre-clean (deterministic, presentation-only)
# ---------------------------------------------------------------------------
_UNIT_PAREN = re.compile(
    r"\s*[\(\[]\s*(wt\.?\s*%|ppm|ppb|ppt|wt|µg/g|ug/g|μg/g|mg/kg|mg/g|g/g|"
    r"mol\.?\s*%|at\.?\s*%|atom\s*%|%|‰|permil|per\s*mil|µmol/kg|umol/kg|"
    r"nmol/kg|mmol/kg|mg/l|µg/l|ug/l|ng/g|cps|psu)\s*[\)\]]\s*$",
    re.IGNORECASE,
)
_TRAILING_WORDS = re.compile(
    r"\b(concentrations?|contents?|abundances?|conc\.?|values?)\b", re.IGNORECASE
)


def l2_clean(raw: str) -> str:
    s = L0.ascii_fold(raw).strip()
    prev = None
    # iterate: strip a trailing unit-paren then trailing words, repeat once
    for _ in range(2):
        if s == prev:
            break
        prev = s
        s = _UNIT_PAREN.sub("", s).strip()
        s = _TRAILING_WORDS.sub("", s).strip()
    s = re.sub(r"\s*/\s*", "/", s)          # normalize ratio slash spacing
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" :=-")
    return s


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def normalize_variable(raw_label: str | None, unit: str | None = None,
                       phase: str | None = None) -> tuple[str | None, str]:
    """Return (canonical_id_or_None, layer_tag). layer_tag in {L0,L0c,L1,L1c,none}."""
    if not raw_label or not raw_label.strip():
        return None, "none"

    # L0 — isotope vocab on raw
    vid = L0.normalize_axis(raw_label)
    if vid:
        return vid, "L0"

    # L1 — exact species lookup on raw (folded)
    folded = L0.ascii_fold(raw_label).strip()
    if folded in _L1_INDEX:
        return _L1_INDEX[folded], "L1"

    # L2 — structural clean, then retry L0 then L1
    cleaned = l2_clean(raw_label)
    if cleaned and cleaned != folded:
        vid = L0.normalize_axis(cleaned)
        if vid:
            return vid, "L0c"
        if cleaned in _L1_INDEX:
            return _L1_INDEX[cleaned], "L1c"

    return None, "none"


def l1_vocab_size() -> int:
    return len(set(_L1_INDEX.values()))


if __name__ == "__main__":
    # quick smoke
    tests = ["MgO", "SiO2 (wt%)", "Sr", "La/Yb", "(La/Yb)N", "CO2 concentration",
             "³He/⁴He ratio", "pH", "FeOt", "εNd", "δ18O", "87Sr/86Sr", "Yb (ppm)"]
    for t in tests:
        print(f"{t!r:28} -> {normalize_variable(t)}")
    print(f"\nL1 distinct ids: {l1_vocab_size()}")
