# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module containing builders intended for testing cbuildbot behaviors."""

from __future__ import print_function

import os

from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import osutils

from chromite.cbuildbot.builders import generic_builders
from chromite.cbuildbot.stages import generic_stages
from chromite.cbuildbot.stages import sync_stages


class SuccessStage(generic_stages.BuilderStage):
  """Build stage declares success!"""

  def PerformStage(self):
    logging.info('!!!SuccessStage, FTW!!!')


class ArtifactStage(generic_stages.BuilderStage,
                    generic_stages.ArchivingStageMixin):
  """Build stage that creates/uploads a build artifact."""

  def PerformStage(self):
    working_root = osutils.GetGlobalTempDir()
    stuffs_dir = os.path.join(working_root, 'stuffs')
    tar_file = os.path.join(working_root, 'stuffs.tar.xz')

    # Create some stuff to tar up.
    osutils.Touch(os.path.join(stuffs_dir, 'a'), makedirs=True)
    osutils.Touch(os.path.join(stuffs_dir, 'b'), makedirs=True)
    osutils.Touch(os.path.join(stuffs_dir, 'c'), makedirs=True)

    # Files will be added as 'stuffs/a',  'stuffs/b',  'stuffs/c'
    cros_build_lib.CreateTarball(tar_file, working_root, inputs=['stuffs'])

    # This actually uploads the artifact to GS. It will be listed in the build's
    # artifacts linked from the final report stage.
    self.UploadArtifact(tar_file, archive=True)


class SyncBuilder(generic_builders.Builder):
  """Builder that performs sync, then exits."""

  def GetSyncInstance(self):
    """Returns an instance of a SyncStage that should be run."""
    return self._GetStageInstance(sync_stages.SyncStage)

  def RunStages(self):
    """Run something after sync/reexec."""
    self._RunStage(SuccessStage)


class ArchiveBuilder(generic_builders.Builder):
  """Builder that performs sync, then exits."""

  def GetSyncInstance(self):
    """Returns an instance of a SyncStage that should be run."""
    return self._GetStageInstance(sync_stages.SyncStage)

  def RunStages(self):
    """Run something after sync/reexec."""
    self._RunStage(ArtifactStage)
