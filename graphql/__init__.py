import collections

from graphql import client


__all__ = []


_VersionInfo = collections.namedtuple('_VersionInfo', 'major minor micro release serial')

__version__ = '0.1.0a'
version_info = _VersionInfo(0, 1, 0, 'alpha', 0)
