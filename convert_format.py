import pandas as pd


def main():
    args = getCommandLineArguments()
    df = pd.read_csv(args.filename)
    convert_file(df, args.family_id)

def getCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("pedigree_file",
                        help="CSV to convert. Contains a pedigree in TODO \
                        format.")
    parser.add_argument("--family_id",
                        help="Name of the pedigree. Default value is 1.")
    parser.add_argument("--output",
                        help="Filename to write Plink (.map, .ped) and \
                        visualization (.pdf) files to.")
    # TODO: default value
    return args


def convert_file(df, family_id, output_filename):

    df.insert(loc=0, column='FAMILY_ID', value=family_id)
    ancestors = pd.DataFrame(columns=["FAMILY_ID","ID","FATHER","MOTHER","SEX"])
    print("Pedigree size before ancestors: {}".format(df.shape[0]))

    for i, row in df.iterrows():
        if row['FATHER'] not in df['ID']:
            ancestor = pd.DataFrame([[family_id, row['FATHER'], 0, 0, 1]], columns=["FAMILY_ID","ID","FATHER","MOTHER","SEX"])
            ancestors = ancestors.append(ancestor, ignore_index=True)
        elif row['MOTHER'] not in df['ID']:
            ancestor = pd.DataFrame([[family_id, row['MOTHER'], 0, 0, 2]], columns=["FAMILY_ID","ID","FATHER","MOTHER","SEX"])
            ancestors = ancestors.append(ancestor, ignore_index=True)

    ancestors = ancestors.drop_duplicates()
    print("Number of ancestors: {}".format(ancestors.shape[0]))
    ancestors = ancestors.append(df, ignore_index=True)
    ancestors.to_csv(output_filename, sep=' ', header=False, index=False)
    print("Pedigree after ancestors: {}".format(ancestors.shape[0]))


main()
