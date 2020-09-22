# Copyright 2018 RethinkDB
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import imp

from rethinkdb import errors, version
from rethinkdb import net
import pkg_resources


# The builtins here defends against re-importing something obscuring `object`.
try:
    import __builtin__ as builtins  # Python 2
except ImportError:
    import builtins  # Python 3


__all__ = ['RethinkDB'] + errors.__all__
__version__ = version.VERSION


class RethinkDB(builtins.object):
    def __init__(self):
        super(RethinkDB, self).__init__()

        from rethinkdb import _dump, _export, _import, _index_rebuild, _restore, ast, query, net

        self._dump = _dump
        self._export = _export
        self._import = _import
        self._index_rebuild = _index_rebuild
        self._restore = _restore

        net.Connection._r = self

        for module in (net, query, ast, errors):
            for function_name in module.__all__:
                setattr(self, function_name, getattr(module, function_name))

        self.set_loop_type(None)

    def set_loop_type(self, library=None):
        if library is None:
            self.connection_type = net.DefaultConnection
            return

        # find module file
        manager = pkg_resources.ResourceManager()
        libPath = '%(library)s_net/net_%(library)s.py' % {'library': library}
        if not manager.resource_exists(__name__, libPath):
            raise ValueError('Unknown loop type: %r' % library)

        # load the module
        modulePath = manager.resource_filename(__name__, libPath)
        moduleName = 'net_%s' % library
        moduleFile, pathName, desc = imp.find_module(moduleName, [os.path.dirname(modulePath)])
        module = imp.load_module('rethinkdb.' + moduleName, moduleFile, pathName, desc)

        # set the connection type
        self.connection_type = module.Connection

        # cleanup
        manager.cleanup_resources()

    def connect(self, *args, **kwargs):
        return self.make_connection(self.connection_type, *args, **kwargs)
