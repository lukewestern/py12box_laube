"""
Runs the inversion code over the AGAGE species as an array job.
Need to pass the species and nthreads you want to use.

The species can either be a number, corresponding to its entry 
in the species_list or as a string naming the species of interest.

Call as:
python run_py12box_noaa.py $include $species_index $nthreads
"""
import numpy as np
import sys

from py12box_invert.invert import Invert
from py12box_laube import get_data
from py12box_agage.utils import get_inversion_params

species_search_string = sys.argv[1]
species_index = int(sys.argv[2])
nthreads = int(sys.argv[3])

print(f"Running {species_search_string}, index {species_index} on {nthreads} threads")

# Hardwire Martin's species list
# species_list = ["HCFC-133a", "HCFC-31","HCFC-132b"]
# species_list = ["CFC-112", "CFC-112a", "CFC-113","CFC-113a", "CFC-114", "CFC-114a"]
species_list = ["H-1202"]

if species_search_string != "all":
    species_list = [s for s in species_list if species_search_string in s]
    
# Check if array index is too high
if species_index > len(species_list):
    raise SystemExit
else:
    species = species_list[species_index-1]

# if species not in species_list:
#     raise Exception(f"{species} not in Vollmer species list\n It may just have to be added to hardwired list or not formatted the same way\n possible species are {species_list}")


print(f"... {species}")

# Work out paths
project_path = get_data(f"{species}")
obs_path = project_path / f"inputs/{species}_obs_laube.csv"
output_path = project_path / f"outputs/{species}_out.p"

if not output_path.parent.exists():
    output_path.parent.mkdir()

# Get inversion parameters
inversion_params = get_inversion_params(species)

# Set up inversion
inv = Invert(project_path / "inputs", species,
            obs_path = obs_path,
            method="iterative_rigby14",
            n_threads=nthreads,
            sensitivity_freq=inversion_params.loc["Sensitivity frequency"],
            end_year=2024.)


# Calculate emissions uncertainty
emissions_box = inv.mod.emissions.mean(axis=0)

invert_uncertainty = inv.mod.emissions.sum(axis=1).max() * inversion_params.loc["Growth uncertainty (%)"]/100.
invert_uncertainty_box = np.sqrt(invert_uncertainty**2 * emissions_box / emissions_box.sum())
invert_uncertainty_min = invert_uncertainty*0.01

invert_uncertainty_box[invert_uncertainty_box < invert_uncertainty_min] = invert_uncertainty_min

# Run inversion
inv.run_inversion(invert_uncertainty_box,
                lifetime_error=inversion_params.loc["Overall lifetime uncertainty (%)"]/100.,
                scale_error=np.mean([inversion_params.loc["Scale error plus (%)"]/100.,
                    inversion_params.loc["Scale error minus (%)"]/100.]))

# Save outputs
inv.save(output_path)

# Write to csv
inv.to_csv(project_path / "outputs/")


