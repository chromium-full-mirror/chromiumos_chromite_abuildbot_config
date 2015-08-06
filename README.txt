This repository exists to help prove out site specific cbuildbot configurations.

To check this out as a repo checkout:

  repo init -u https://chromium.googlesource.com/chromiumos/chromite/abuildbot_config

To perform a local build:

  bin/cbuildbot --buildroot /tmp/test_buildroot \
    --buildbot --debug --config_repo  \
    https://chromium.googlesource.com/chromiumos/chromite/abuildbot_config \
    sync-test-abuildbot
