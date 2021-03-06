# -*- coding: utf-8 -*-

import os
import sys
import pickle
sys.path.insert(0, os.path.abspath('..'))

import courtship.fly as fly
import courtship.behavior as behavior
import courtship.experiment as experiment
import courtship.ts as ts

import courtship.app.arena as trk_arena
import courtship.app.female as trk_female
import courtship.app.tracking as trk_track
import courtship.app.entry as entry

import courtship.stats.centroid as centroid
import courtship.stats.spatial as spatial
import courtship.stats.transforms as transforms
import courtship.stats.behaviors as behaviors
import courtship.stats.markov as markov

import courtship.ml.features as features
import courtship.ml.classifiers as classifiers

import courtship.plots as plots
import courtship.plots.misc as misc_plots
import courtship.plots.utils as plot_utils