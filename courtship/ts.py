# -*- coding: utf-8 -*-

"""
.. module:: courtship
   :synopsis: Class to hold tracking summaries (ts). 

.. moduleauthor:: Ross McKinney
"""
import os
import pickle
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
from mpl_toolkits.mplot3d import Axes3D

import motmot.FlyMovieFormat.FlyMovieFormat as FMF

import numpy as np
import pandas as pd

import pycircstat.descriptive as pysum
import pycircstat.tests as pytest
import pytz

from .fly import Fly
from .meta import (
    VideoMeta,
    ArenaMeta,
    SoftwareTrackingMeta
)


class TrackingSummary(object):
    """Holds information about a particular tracked video.

    Attributes
    ----------
    video_file : string or None (default=None)
        Path to video from which objects were tracked.

    fps : float or None (default=None)
        Frames per second within tracked video.

    start_time : string or None (default=None)
        Datetime at which video recording was started.

    end_time : string or None (default=None)
        Datetime at which video recording was ended.

    arena_type : string or None (default=None)
        String describing the type of arena used in video.

    pixels_per_mm : int or None (default=None)
        Conversion factor so we know the absolute size of things in the video.

    group : string or None (default=None)
        String denoting to which group tracked objects belong.

    tight_threshold : int or None (default=None)
        Tight threshold used to locate object in video.

    loose_threshold : int or None (default=None)
        Loose threshold used to locate object in video.

    date_tracked : string or None (default=None)
        Datetime at which tracking of video took place
        (this is tracking, not recording)

    tracking_software : string or None (default=None)
        String containing version of software used for tracking.

    arena_size_mm : int or None (default=None)
        Size of arena. Diameter if circular.

    behaviors : dictionary (default={})
        Dictionary containing any behaviors observed within tracked video.
        This should be used to store behaviors determined using classifiers.
        Each key should be a string describing the behavior, and
        each value should be a binary, 1D array stating whether or
        not that behavior was observed in a each frame.
    """
    def __init__(self):
        self.video_file = None
        self.fps = None
        self.start_time = None
        self.end_time = None
        self.arena_type = None
        self.arena_size_mm = None
        self.pixels_per_mm = None
        self.group = None
        self.tight_threshold = None
        self.loose_threshold = None
        self.date_tracked = None
        self.tracking_software = None
        self.behaviors = {}

    def __str__(self):
        """Pretty print of class properties."""
        params = self.get_meta_data()
        class_description = 'Tracking Summary\n----------------'
        for key in sorted(params.keys()):
            class_description += '\n{}: {}'.format(key, params[key])
        return class_description

    def get_meta_data(self):
        """Returns a dictionary of all meta data associated with this object.

        Meta data is everything except for any flies and/or behaviors.

        Returns
        -------
        meta : dictionary
        """
        meta = {}
        for k, v in self.__dict__.iteritems():
            if k in ['male', 'female', 'behaviors']:
                continue
            meta[k] = v

        return meta

    def get_video_statistics(self):
        """Gets summary statistics about a this classes' associated video file.

        Returns
        -------
        fps : float
            Number of frames per second.

        start_time : string
            Date and time that video recording started.

        end_time : string
            Date and time that video recording ended.
        """
        video = FMF.FlyMovie(self.video_file)
        timestamps = video.get_all_timestamps()
        fps = 1. / np.mean(np.diff(timestamps))
        start_time = datetime.fromtimestamp(timestamps[0]).strftime(
            '%Y-%m-%d %H:%M:%S')
        end_time = datetime.fromtimestamp(timestamps[-1]).strftime(
            '%Y-%m-%d %H:%M:%S')
        return fps, start_time, end_time

    def set_attributes(self, **kwargs):
        """Sets some - or all - attributes of this class.

        Parameters
        ----------
        kwargs : dictionary
            Keys should be attribute names, and values should be data
            associated with that attribute.
        """
        available_attributes = self.__dict__.keys()
        for k, v in kwargs.iteritems():
            if k in available_attributes:
                setattr(self, k, v)
            else:
                raise NameError(
                    "Key <{}> is not a valid attribute name.".format(k))

        if self.video_file is not None and os.path.exists(self.video_file):
            self.fps, self.start_time, self.end_time = \
                self.get_video_statistics()
