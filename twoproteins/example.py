from pymol import cmd
from getpass import getuser

username = getuser()

# set a path to your data
PATH_data = '/home/{0}/repo/github/chmnk/pymol-examples/twoproteins/'.format(username)


# pymol requires python2
# to run this, try pymol example.py to see the pymol window, or
# to run this, try pymol -c example.py for terminal mode


def compare_10gs_11gs():
    # it is possible to download proteins from RCSB (Protein Data Bank) to fetch_path, which is current working
    # directory by default
    cmd.set('fetch_path', cmd.exp_path(PATH_data))
    cmd.fetch('10gs')
    cmd.fetch('11gs')

    cmd.load('{0}10gs.cif'.format(PATH_data), '10gs')
    cmd.load('{0}11gs.cif'.format(PATH_data), '11gs')

    # proteins
    # pymol has several options for proteins alignment, align is better for proteins with high homology
    align_command = cmd.align  # or super, or cealign
    align_res = align_command('10gs', '11gs')
    if align_command == cmd.align:
        print('aligned with rmsd {0}'.format(align_res[0]))
    # cmd.create creates a separate object (copies everything to it)
    # het stands for heteroatoms (non-protein)
    cmd.create('10gs_protein', '10gs and not het')
    cmd.create('11gs_protein', '11gs and not het')
    # print protein sequences for fun
    fasta_10gs = cmd.get_fastastr(selection='10gs_protein')
    fasta_11gs = cmd.get_fastastr(selection='11gs_protein')
    print('10gs sequence:{0}'.format(fasta_10gs))
    print('11gs sequence:{0}'.format(fasta_11gs))
    cmd.delete('*_protein')  # delete objects

    # ligands
    cmd.select('10gs_ligands', '10gs and not resname HOH and het')
    cmd.select('11gs_ligands', '11gs and not resname HOH and het')
    space_10gs = {'lig_names': []}  # or simpy lig_names = []
    space_11gs = {'lig_names': []}
    # strange pymol interface to iterate over atoms
    cmd.iterate('10gs_ligands', 'lig_names.append(resn)', space=space_10gs)
    cmd.iterate('11gs_ligands', 'lig_names.append(resn)', space=space_11gs)
    ligs_10gs = set(space_10gs['lig_names'])
    ligs_11gs = set(space_11gs['lig_names'])
    # by the way, in both 10gs and 11gs we have MSE, which is actually a modified residue and not a ligand
    print('ligands found in 10gs: {0}'.format(ligs_10gs))
    print('ligands found in 11gs: {0}'.format(ligs_11gs))
    for ligand_unique in ligs_10gs.symmetric_difference(ligs_11gs):
        cmd.save('{0}{1}_{2}_ligand.sdf'.format(PATH_data, '10gs' if ligand_unique in ligs_10gs else '11gs', ligand_unique),
                 'resname {0}'.format(ligand_unique))
    # deleting selection, objects remain unchanged
    cmd.delete('ligs*')

    print('drawing a figure (this will take some time)')
    cmd.set('transparency_mode', 1)
    cmd.bg_color('white')
    cmd.show('sticks', 'het and not resname HOH')
    cmd.color('white', 'not het')
    cmd.show('surface', 'not het')
    cmd.hide('lines')
    cmd.set('transparency', '0.7')
    cmd.show('spheres', 'resname HOH')
    cmd.color('palecyan', 'resname HOH')
    cmd.hide('nonbonded', 'resname HOH')
    cmd.set('sphere_transparency', '0.7')
    cmd.ray()
    cmd.png('{0}fig.png'.format(PATH_data))
    # cmd.delete('all')


compare_10gs_11gs()

