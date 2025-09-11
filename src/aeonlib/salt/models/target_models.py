"""This module contains Pydantic models for targets to observe with SALT."""

from __future__ import annotations

from typing import Literal, Self

import astropy.units as u
from pydantic import BaseModel, NonNegativeFloat, model_validator

from aeonlib.models import SiderealTarget


Bandpass = Literal["U", "B", "V", "R", "I"]


class SaltSiderealTarget(SiderealTarget):
    """
    A sidereal target to observe with SALT.

    This model extends the `SiderealTarget` model by adding a target type and a
    magnitude range.

    Attributes
    ----------
    target_type
        Target type. This must be the label for SIMBAD object type (see
        http://simbad.cds.unistra.fr/guide/otypes.htx). Examples are "TTau*" and
        "StarburstG".
    magnitude_range
        Magnitude range for the range.
    """

    target_type: TargetType
    magnitude_range: MagnitudeRange

    @model_validator(mode="after")
    def check_target_viewable(self):
        if self.ra < -76 * u.deg or self.ra > 11 * u.deg:
            raise ValueError("ra not between -76 and 11 degrees.")

        return self


class MagnitudeRange(BaseModel):
    """
    A magnitude range.

    The minimum (brightest) and maximum (faintest) magnitude must be give for a
    particular bandpass filter.

    Attributes
    ----------
    min_magnitude
        Minimum (brightest) magnitude.
    max_magnitude
        Maximum (faintest) magnitude. This must be greater than or equal to the minimum
        magnitude.
    bandpass
        Bandpass filter for which the magnitude range is given.
    """

    min_magnitude: NonNegativeFloat

    max_magnitude: NonNegativeFloat

    bandpass: Bandpass

    @model_validator(mode="after")
    def check_max_magnitude_is_at_least_min_magnitude(self) -> Self:
        if self.min_magnitude > self.max_magnitude:
            raise ValueError(
                "max_magnitude must be greater than or equal to min_magnitude."
            )

        return self


TargetType = Literal[
    "Unknown",
    "Maser",
    "X",
    "SuperSoft",
    "gamma",
    "gammaBurst",
    "Inexistant",
    "Error",
    "Gravitation",
    "LensingEv",
    "Candidate_Lens",
    "Possible_lensImage",
    "GravLens",
    "GravLensSystem",
    "Candidates",
    "Possible_SClG",
    "Possible_ClG",
    "Possible_GrG",
    "Candidate_**",
    "Candidate_EB*",
    "Candidate_CV*",
    "Candidate_XB*",
    "Candidate_LMXB",
    "Candidate_HMXB",
    "Candidate_Pec*",
    "Candidate_YSO",
    "Candidate_pMS*",
    "Candidate_TTau*",
    "Candidate_C*",
    "Candidate_S*",
    "Candidate_OH",
    "Candidate_CH",
    "Candidate_WR*",
    "Candidate_Be*",
    "Candidate_HB*",
    "Candidate_RGB*",
    "Candidate_RSG*",
    "Candidate_AGB*",
    "Candidate_post-AGB*",
    "Candidate_BSS",
    "Candidate_WD*",
    "Candidate_NS",
    "Candidate_BH",
    "Candidate_SN*",
    "Candidate_low-mass*",
    "Candidate_brownD*",
    "multiple_object",
    "Region",
    "Void",
    "SuperClG",
    "ClG",
    "GroupG",
    "Compact_Gr_G",
    "Gr_QSO",
    "PairG",
    "IG",
    "GlCl?",
    "Cl*",
    "GlCl",
    "OpCl",
    "Assoc*",
    "**",
    "EB*",
    "EB*Algol",
    "EB*betLyr",
    "EB*WUMa",
    "EB*Planet",
    "SB",
    "CataclyV*",
    "DQHer",
    "AMHer",
    "Nova-like",
    "Nova",
    "DwarfNova",
    "XB",
    "LMXB",
    "HMXB",
    "***",
    "ISM",
    "PartofCloud",
    "PN?",
    "ComGlob",
    "Bubble",
    "EmObj",
    "Cloud",
    "GalNeb",
    "BrNeb",
    "DkNeb",
    "RfNeb",
    "MolCld",
    "Globule",
    "denseCore",
    "HVCld",
    "BiNeb",
    "GasNeb",
    "HII",
    "PN",
    "HIshell",
    "SNR?",
    "SNR",
    "Circumstellar",
    "outflow?",
    "Outflow",
    "OutflowJet",
    "HH",
    "Star",
    "*inCl",
    "*inNeb",
    "*inAssoc",
    "*in**",
    "V*?",
    "Pec*",
    "HB*",
    "YSO",
    "Em*",
    "Be*",
    "BlueStraggler",
    "RGB*",
    "AGB*",
    "C*",
    "S*",
    "RSG*",
    "post-AGB*",
    "WD*",
    "pulsWD*",
    "low-mass*",
    "brownD*",
    "OH/IR",
    "CH",
    "pMS*",
    "TTau*",
    "WR*",
    "NS*",
    "BH*",
    "PM*",
    "near*",
    "HV*",
    "V*",
    "Irregular_V*",
    "Orion_V*",
    "Rapid_Irreg_V*",
    "Eruptive*",
    "Flare*",
    "FUOr",
    "Erupt*RCrB",
    "RotV*",
    "RotV*alf2CVn",
    "RotV*Ell",
    "Pulsar",
    "BYDra",
    "RSCVn",
    "PulsV*",
    "RRLyr",
    "Cepheid",
    "PulsV*delSct",
    "PulsV*RVTau",
    "PulsV*WVir",
    "PulsV*bCep",
    "deltaCep",
    "gammaDor",
    "LPV*",
    "Mira",
    "semi-regV*",
    "SN",
    "Symbiotic*",
    "Sub-stellar",
    "Planet?",
    "ExG*",
    "Galaxy",
    "EllipticalG",
    "SpiralG",
    "DwarfG",
    "IrregG",
    "PartofG",
    "GinCl",
    "BClG",
    "GinGroup",
    "GinPair",
    "High_z_G",
    "AbsLineSystem",
    "Ly-alpha_ALS",
    "DLy-alpha_ALS",
    "metal_ALS",
    "Ly-limit_ALS",
    "Broad_ALS",
    "RadioG",
    "HII_G",
    "LSB_G",
    "AGN_Candidate",
    "QSO_Candidate",
    "Blazar_Candidate",
    "BLLac_Candidate",
    "EmG",
    "StarburstG",
    "BlueCompG",
    "LensedImage",
    "LensedG",
    "LensedQ",
    "AGN",
    "LINER",
    "Seyfert",
    "Seyfert_1",
    "Seyfert_2",
    "Blazar",
    "BLLac",
    "OVV",
    "QSO",
    "GSN",
    "Solar_System",
    "Planet",
    "Mercury",
    "Venus",
    "Earth",
    "Moon",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "PMoon",
    "PRing",
    "DwarfPlanet",
    "Pluto",
    "Asteroid",
    "Comet",
    "KBO",
    "Calib",
    "Calib_S",
    "Calib_aS",
    "Calib_phS",
    "Calib_sS",
    "Cal_polS",
    "Cal_spS",
    "Cal_rvS",
    "Cal_Flat",
    "Cal_SFlat",
    "Cal_DFlat",
    "Cal_Guide*",
]
