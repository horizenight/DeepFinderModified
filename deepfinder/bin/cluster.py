#!/usr/bin/env python

# =============================================================================================
# DeepFinder - a deep learning approach to localize macromolecules in cryo electron tomograms
# =============================================================================================
# Copyright (C) Inria,  Emmanuel Moebel, Charles Kervrann, All Rights Reserved, 2015-2021, v1.0
# License: GPL v3.0. See <https://www.gnu.org/licenses/>
# =============================================================================================

import os
import sys
from os.path import dirname, abspath, join, basename
import argparse


def main():
    # Set deepfindHome to the location of this file
    deepfindHome = dirname(abspath(__file__))
    deepfindHome = os.path.split(deepfindHome)[0] + '/'
    sys.path.append(deepfindHome)

    # Define arguments:
    parser = argparse.ArgumentParser(description='Segment a tomogram.')
    parser.add_argument('-l', action='store', dest='path_lmap', help='path to label map')
    parser.add_argument('-r', action='store', dest='cradius', type=int, help='clustering radius (in voxels)')
    parser.add_argument('-o', action='store', dest='path_output', help='output path')
    args = parser.parse_args()

    no_args = args.path_lmap == None and args.cradius == None and args.path_output == None
    incomplete_args = args.path_lmap == None or args.cradius == None or args.path_output == None

    if no_args:  # if no args are passed, then open GUI
        gui_folder = 'pyqt.clustering.'
        gui_script = 'gui_clustering'

        cmd = 'python -m ' + 'deepfinder.' + gui_folder+gui_script
        print(cmd)

        os.system(cmd)

    elif incomplete_args:
        print('DeepFinder message: an argument is missing. All arguments need to be addressed: -l, -r, -o')

    else:
        from deepfinder.inference import Cluster
        import deepfinder.utils.common as cm
        import deepfinder.utils.objl as ol

        # Load data:
        lmap = cm.read_array(args.path_lmap)

        # Initialize clustering task:
        clust = Cluster(clustRadius=args.cradius)

        # Launch clustering (result stored in objlist)
        objlist = clust.launch(lmap)

        # Save object lists:
        ol.write_xml(objlist, args.path_output)


if __name__ == "__main__":
    main()
