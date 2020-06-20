import os
import unittest
import tempfile

import gourmet.gglobals

import gourmet.GourmetRecipeManager
import gourmet.backends.db

from gourmet.plugin_loader import get_master_loader

class Test (unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self._prev_gourmetdir = gourmet.gglobals.gourmetdir
        gourmet.gglobals.gourmetdir = td.name

        # Switch to a temporary database for these tests
        self.db = gourmet.backends.db.get_database()
        self._db_plugins_prev = self.db.plugins[:]
        self._db_prev = self.db._switch_to(os.path.join(td.name, 'recipes.db'))

        gourmet.GourmetRecipeManager.GourmetApplication.__single = None

    def tearDown(self) -> None:
        self.db.plugins[:] = self._db_plugins_prev
        self.db._switch_to(*self._db_prev)
        gourmet.gglobals.gourmetdir = self._prev_gourmetdir

    def testDefaultPlugins (self):
        ml = get_master_loader()
        ml.load_active_plugins()
        print('active:',ml.active_plugins)
        print('instantiated:',ml.instantiated_plugins)
        assert(not ml.errors)

    def testAvailablePlugins (self):
        ml = get_master_loader()
        for module_name, plugin_set in ml.available_plugin_sets.items():
            if module_name not in ml.active_plugin_sets:
                ml.activate_plugin_set(plugin_set)

if __name__ == '__main__':
    unittest.main()
