from helper import Simulation
import argparse


def main():
    args = getCommandLineArguments()
    sim = Simulation(verbose=args.verbose)
    sim.addPedigree(args.pedigree_file, args.family_id)
    sim.runSimulation(chromLength=int(args.length))
    sim.populateGenomes()
    sim.writePedigreeToPlink(args.output)
    sim.visualizePedigree(args.output)

def getCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("pedigree_file",
                        help="Filename that specifies the pedigree structure \
                        used in the simulation.")
    parser.add_argument("family_id",
                        help="FAMILY_ID of the pedigree in pedigree_file.")
    parser.add_argument("--verbose",
                        help="Increase output verbosity.",
                        action="store_true")
    parser.add_argument("--output",
                        help="Filename to write Plink (.map, .ped) and \
                        visualization (.pdf) files to.")
    parser.add_argument("--length",
                        help="Length in base pairs of chromosome to simulate. \
                        Default value is 5000.") #TODO: make sure this is optional
    args = parser.parse_args()
    if not args.output: #TODO see if there's a better way to default
        args.output = "output"
    if not args.length:
        args.length = 5000
    return args



main()
