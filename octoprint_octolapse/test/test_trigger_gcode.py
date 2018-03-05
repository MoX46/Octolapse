import unittest
from tempfile import NamedTemporaryFile

from octoprint_octolapse.position import Position
from octoprint_octolapse.settings import OctolapseSettings
from octoprint_octolapse.trigger import GcodeTrigger


class Test_GcodeTrigger(unittest.TestCase):
    def setUp(self):
        self.Settings = OctolapseSettings(NamedTemporaryFile().name)
        self.Settings.current_printer().auto_detect_position = False
        self.Settings.current_printer().origin_x = 0
        self.Settings.current_printer().origin_y = 0
        self.Settings.current_printer().origin_z = 0
        self.OctoprintPrinterProfile = self.CreateOctoprintPrinterProfile()

    def tearDown(self):
        del self.Settings
        del self.OctoprintPrinterProfile

    def CreateOctoprintPrinterProfile(self):
        return {
            "volume": {
                "custom_box": False,
                "width": 250,
                "depth": 200,
                "height": 200
            }
        }

    def test_GcodeTrigger(self):
        """Test the gcode triggers"""
        self.Settings.current_snapshot().gcode_trigger_require_zhop = False

        position = Position(self.Settings, self.OctoprintPrinterProfile, False)
        trigger = GcodeTrigger(self.Settings)
        # test initial state
        self.assertFalse(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # send a command that is NOT the snapshot command using the defaults
        trigger.update(position, "NotTheSnapshotCommand")
        self.assertFalse(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # send a command that is the snapshot command without the axis being homes
        trigger.update(position, "snap")
        self.assertFalse(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # reset, set relative extruder and absolute xyz, home the axis, and resend the snap command, should wait since we require
        # the home command to complete (sent to printer) before triggering
        position.update("M83")
        position.update("G90")
        position.update("G28")
        trigger.update(position, "snap")
        self.assertFalse(trigger.is_triggered(0))
        self.assertTrue(trigger.is_waiting(0))

        # try again, Snap is encountered, but it must be the previous command to trigger
        position.update("G0 X0 Y0 Z0 E1 F0")
        trigger.update(position, "G0 X0 Y0 Z0 E1 F0")
        self.assertTrue(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # try again, but this time set RequireZHop to true
        trigger.RequireZHop = True
        trigger.update(position, "snap")
        self.assertFalse(trigger.is_triggered(0))
        self.assertTrue(trigger.is_waiting(0))
        # send another command to see if we are still waiting
        trigger.update(position, "NotTheSnapshotCommand")
        self.assertFalse(trigger.is_triggered(0))
        self.assertTrue(trigger.is_waiting(0))
        # fake a zhop
        position.is_zhop = lambda x: True
        trigger.update(position, "NotTheSnapshotCommand")
        self.assertTrue(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # send a command that is NOT the snapshot command using the defaults
        trigger.update(position, "NotTheSnapshotCommand")
        self.assertFalse(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))

        # change the snapshot triggers and make sure they are working
        self.Settings.current_snapshot().gcode_trigger_require_zhop = None
        self.Settings.current_snapshot().gcode_trigger_on_extruding = True
        self.Settings.current_snapshot().gcode_trigger_on_extruding_start = None
        self.Settings.current_snapshot().gcode_trigger_on_primed = None
        self.Settings.current_snapshot().gcode_trigger_on_retracting = None
        self.Settings.current_snapshot().gcode_trigger_on_partially_retracted = None
        self.Settings.current_snapshot().gcode_trigger_on_retracted = None
        self.Settings.current_snapshot().gcode_trigger_on_detracting_start = None
        self.Settings.current_snapshot().gcode_trigger_on_detracting = None
        self.Settings.current_snapshot().gcode_trigger_on_detracted = None
        trigger = GcodeTrigger(self.Settings)

        # send a command that is the snapshot command using the defaults
        trigger.update(position, "snap")
        self.assertFalse(trigger.is_triggered(0))
        self.assertTrue(trigger.is_waiting(0))
        # change the extruder state and test
        # should not trigger because trigger tests the previous command
        position.update("G0 X0 Y0 Z0 E10 F0")
        trigger.update(position, "NotTheSnapshotCommand")
        self.assertTrue(trigger.is_triggered(0))
        self.assertFalse(trigger.is_waiting(0))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_GcodeTrigger)
    unittest.TextTestRunner(verbosity=3).run(suite)
