from abc import *
import pymel.core as pm

import mtoa.aovs as aovs


class AOVBehavior(ABC):
    """
    AOV Behaviors
    """
    @abstractmethod
    def connect_driver_filter(self, aov, output_denoising, mono_driver):
        """
        Connect the right driver and the right filter
        :param aov
        :param output_denoising
        :param mono_driver
        :return:
        """
        pass


class HalfPrecisionBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        half_driver = pm.ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        pm.connectAttr(half_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)


class HalfPrecisionClosestBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        half_driver = pm.ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        closest_filter = pm.createNode("aiAOVFilter")
        closest_filter.aiTranslator.set("closest")
        pm.connectAttr(half_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)
        pm.connectAttr(closest_filter + ".message", "aiAOV_" + aov_name + '.outputs[0].filter', f=True)


class FullPrecisionClosestBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        if mono_driver:
            driver = pm.ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        else:
            driver = pm.ls("aov_full_driver", type="aiAOVDriver")[0]
        closest_filter = pm.createNode("aiAOVFilter")
        closest_filter.aiTranslator.set("closest")
        pm.connectAttr(driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)
        pm.connectAttr(closest_filter + ".message", "aiAOV_" + aov_name + '.outputs[0].filter', f=True)


class FullPrecisionBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        if mono_driver:
            driver = pm.ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        else:
            driver = pm.ls("aov_full_driver", type="aiAOVDriver")[0]
        pm.connectAttr(driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)


class ClosestGaussianBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        if mono_driver:
            driver = pm.ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        else:
            driver = pm.ls("aov_full_driver", type="aiAOVDriver")[0]
        closest_filter = pm.createNode("aiAOVFilter")
        closest_filter.aiTranslator.set("closest")
        pm.connectAttr(driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)
        pm.connectAttr(closest_filter + ".message", "aiAOV_" + aov_name + '.outputs[0].filter', f=True)
        pm.connectAttr(driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[1].driver", f=True)
        pm.connectAttr("defaultArnoldFilter.message", "aiAOV_" + aov_name + '.outputs[1].filter', f=True)


class AOVVarianceBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising, mono_driver):
        driver = pm.ls("variance_driver", type="aiAOVDriver")[0]
        driver_field = "aiAOV_" + aov_name + ".outputs[1].driver"
        filter_field = "aiAOV_" + aov_name + ".outputs[1].filter"
        if output_denoising and not mono_driver:
            variance_filter = pm.createNode('aiAOVFilter', n="variance_filter")
            pm.setAttr(variance_filter + '.ai_translator', "variance", type="string")
            pm.connectAttr(driver + ".message", driver_field, f=True)
            pm.connectAttr(variance_filter + ".message", filter_field, f=True)
        else:
            try:
                pm.disconnectAttr(driver + ".message", driver_field)
                variance_filter = pm.listConnections(filter_field)[0]
                pm.disconnectAttr(variance_filter + ".message", filter_field)
                pm.delete(variance_filter)
            except Exception:
                pass
