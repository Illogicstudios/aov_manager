from abc import *
from enum import Enum
import mtoa.aovs as aovs
from pymel.core import *


class PrecisionMode(Enum):
    FullPrecision = 0
    Halfprecision = 1
    FullAndHalfPrecision = 2


class AOV(ABC):
    def __init__(self, name, order_group, precision=PrecisionMode.Halfprecision):
        self.__name = name
        self.__precision = precision
        self.__order_group = order_group

    def get_order_group(self):
        return self.__order_group

    def create_aov(self, half_driver, full_driver):
        aov = aovs.AOVInterface().addAOV(self.__name)

        if self.__precision == PrecisionMode.FullPrecision:
            connectAttr(full_driver.name() + ".message", "aiAOV_" + aov.name + ".outputs[0].driver", f=True)
        elif self.__precision == PrecisionMode.Halfprecision:
            connectAttr(half_driver.name() + ".message", "aiAOV_" + aov.name + ".outputs[0].driver", f=True)
        else:
            connectAttr(full_driver.name() + ".message", "aiAOV_" + aov.name + ".outputs[0].driver", f=True)
            connectAttr(full_driver.name() + ".message", "aiAOV_" + aov.name + ".outputs[1].driver", f=True)
            connectAttr("defaultArnoldFilter.message", "aiAOV_" + aov.name +'.outputs[0].filter', f=True)
            closest_filter = createNode("aiAOVFilter")
            closest_filter.aiTranslator.set("closest")
            connectAttr(closest_filter+".message", "aiAOV_" + aov.name +'.outputs[1].filter', f=True)

        return aov


class DefaultAOV(AOV):
    def __init__(self, name, order_group, precision=PrecisionMode.Halfprecision):
        super().__init__(name, order_group, precision)


class CryptomatteAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, PrecisionMode.FullPrecision)

    def create_aov(self, half_driver, full_driver):
        aov = super(CryptomatteAOV, self).create_aov(half_driver,full_driver)

        if objExists('aov_cryptomatte'):
            crypto_node = ls("aov_cryptomatte", type="cryptomatte")[0]
        else:
            crypto_node = createNode("cryptomatte", n="aov_cryptomatte")

        cmds.connectAttr(crypto_node.name()+".outColor", "aiAOV_" + aov.name + ".defaultValue")
        return aov


class OcclusionAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group)

    def create_aov(self, half_driver, full_driver):
        aov = super(OcclusionAOV, self).create_aov(half_driver,full_driver)

        occlusion_node = createNode("aiAmbientOcclusion", n="occMtl")
        occlusion_node.falloff.set(0)
        cmds.connectAttr(occlusion_node.name()+".outColor", "aiAOV_" + aov.name + ".defaultValue")
        return aov


class UVAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, PrecisionMode.FullPrecision)

    def create_aov(self, half_driver, full_driver):
        aov = super(UVAOV, self).create_aov(half_driver,full_driver)

        uv_node = createNode("aiUtility", n="aiUtiliy_uv")
        uv_node.shadeMode.set(2)
        uv_node.colorMode.set(5)
        cmds.connectAttr(uv_node.name()+".outColor", "aiAOV_" + aov.name + ".defaultValue")
        return aov


class MotionVectorBlurAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, PrecisionMode.FullPrecision)

    def create_aov(self, half_driver, full_driver):
        aov = super(MotionVectorBlurAOV, self).create_aov(half_driver,full_driver)

        motion_vector_node = createNode("aiMotionVector", n="aiMotionVector")
        motion_vector_node.raw.set(1)
        cmds.connectAttr(motion_vector_node.name()+".outColor", "aiAOV_" + aov.name + ".defaultValue")
        return aov


class LightGroupAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group)
