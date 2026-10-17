"""Build a complete release candidate, never publish it or create Git state."""
import argparse
from pathlib import Path

from tools import build_addon

# Explicit ABI/version intervals. Untested intervening minors are not inferred.
TARGETS = {
    '3.0': dict(kind='legacy', python='3.9'),
    '3.6': dict(kind='legacy', python='3.10'),
    '4.2': dict(kind='extension', python='3.11', blender_min='4.2.0', blender_max='4.3.0'),
    '4.5': dict(kind='extension', python='3.11', blender_min='4.5.0', blender_max='4.6.0'),
    '5.2': dict(kind='extension', python='3.13', blender_min='5.2.0', blender_max='5.3.0'),
}


def build(target, platform, cache, output, download=False):
    options = TARGETS[target]
    output = Path(output)
    archive = build_addon.build(**options, platform=platform, cache=Path(cache), output=output, download=download)
    # Distinguish 4.2 and 4.5, which share an ABI but have separate manifests.
    destination = output / ('freemocap-{}-blender{}-py{}-{}.zip'.format(
        options['kind'], target, options['python'], platform))
    archive.replace(destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=TARGETS, required=True)
    parser.add_argument('--platform', choices=build_addon.PLATFORMS, required=True)
    parser.add_argument('--cache', type=Path, default=build_addon.ROOT / '.test-artifacts/wheels')
    parser.add_argument('--output', type=Path, default=build_addon.ROOT / 'dist')
    parser.add_argument('--download', action='store_true')
    print(build(**vars(parser.parse_args())))
