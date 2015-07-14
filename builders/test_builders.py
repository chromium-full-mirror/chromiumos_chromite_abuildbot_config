# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module containing builders intended for testing cbuildbot behaviors."""

from __future__ import print_function

from chromite.lib import cros_logging as logging

from chromite.cbuildbot import manifest_version
from chromite.cbuildbot.builders import generic_builders
from chromite.cbuildbot.stages import generic_stages
from chromite.cbuildbot.stages import sync_stages


class SuccessStage(generic_stages.BuilderStage):
  """Build stage declares success!"""
  def Run(self):
    logging.info('!!!SuccessStage, FTW!!!')


class SyncBuilder(generic_builders.Builder):
  """Builder that performs sync, then exits."""

  def GetVersionInfo(self):
    """This version isn't very meaningful, just pin it."""
    return manifest_version.VersionInfo('1.0.0')

  def GetSyncInstance(self):
    """Returns an instance of a SyncStage that should be run."""
    return self._GetStageInstance(sync_stages.SyncStage)

  def RunStages(self):
    """Run something after sync/reexec."""
    self._RunStage(SuccessStage)
