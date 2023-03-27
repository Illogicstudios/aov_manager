from abc import *
from pymel.core import *

import mtoa.aovs as aovs


# AOV Behaviors
class AOVBehavior(ABC):
    @abstractmethod
    def connect_driver_filter(self, aov, output_denoising):
        pass


class HalfPrecisionBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising):
        half_driver = ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        connectAttr(half_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)

class HalfPrecisionClosestBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising):
        half_driver = ls("defaultArnoldDriver", type="aiAOVDriver")[0]
        closest_filter = createNode("aiAOVFilter")
        closest_filter.aiTranslator.set("closest")
        connectAttr(half_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)
        connectAttr(closest_filter + ".message", "aiAOV_" + aov_name + '.outputs[0].filter', f=True)


class FullPrecisionBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising):
        full_driver = ls("aov_full_driver", type="aiAOVDriver")[0]
        connectAttr(full_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)


class ClosestGaussianBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising):
        full_driver = ls("aov_full_driver", type="aiAOVDriver")[0]
        closest_filter = createNode("aiAOVFilter")
        closest_filter.aiTranslator.set("closest")
        connectAttr(full_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[0].driver", f=True)
        connectAttr(closest_filter + ".message", "aiAOV_" + aov_name + '.outputs[0].filter', f=True)
        connectAttr(full_driver.name() + ".message", "aiAOV_" + aov_name + ".outputs[1].driver", f=True)
        connectAttr("defaultArnoldFilter.message", "aiAOV_" + aov_name + '.outputs[1].filter', f=True)


class AOVVarianceBehavior(AOVBehavior):
    def connect_driver_filter(self, aov_name, output_denoising):
        variance_driver = ls("variance_driver", type="aiAOVDriver")[0]
        driver_field = "aiAOV_" + aov_name + ".outputs[1].driver"
        filter_field = "aiAOV_" + aov_name + ".outputs[1].filter"
        if output_denoising:
            variance_filter = createNode('aiAOVFilter', n="variance_filter")
            setAttr(variance_filter + '.ai_translator', "variance", type="string")
            connectAttr(variance_driver + ".message", driver_field, f=True)
            connectAttr(variance_filter + ".message", filter_field, f=True)
        else:
            try:
                disconnectAttr(variance_driver + ".message", driver_field)
                variance_filter = listConnections(filter_field)[0]
                disconnectAttr(variance_filter + ".message", filter_field)
                delete(variance_filter)
            except Exception:
                pass
