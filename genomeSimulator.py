from helper import Simulation
import argparse

def main():
    args = getCommandLineArguments()
    sim = Simulation(verbose=args.verbose)
    sim.addPedigree(args.pedigree_file, args.pedigree_name)
    sim.runSimulation()
    sim.populateGenomes()
    sim.writePedigreeToPlink("test")
    sim.visualizePedigree("vis")

def getCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("pedigree_file",
                        help="Filename that specifies the pedigree structure \
                        used in the simulation.")
    parser.add_argument("pedigree_name",
                        help="Name of the pedigree in the pedigree file to use \
                        for simulation.")
    parser.add_argument("--verbose",
                        help="Increase output verbosity.",
                        action="store_true")
    args = parser.parse_args()
    return args



main()
