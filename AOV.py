from abc import *
from enum import Enum
import mtoa.aovs as aovs
from pymel.core import *
from AOVBehavior import *
from utils import *


class AOV(ABC):
    def __init__(self, name, order_group, aov_behaviors):
        self.__name = name
        self.__order_group = order_group
        self.__aov_behaviors = aov_behaviors
        self._aov = None

    def get_order_group(self):
        return self.__order_group

    def create_aov(self, output_denoising):
        self._aov = aovs.AOVInterface().addAOV(self.__name)
        for aov_behavior in self.__aov_behaviors:
            aov_behavior.connect_driver_filter(self._aov.name, output_denoising)

    def update(self, aov_name, output_denoising):
        for aov_behavior in self.__aov_behaviors:
            aov_behavior.connect_driver_filter(aov_name, output_denoising)


class DefaultAOV(AOV):
    pass


class CryptomatteAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(CryptomatteAOV, self).create_aov(output_denoising)

        if objExists('aov_cryptomatte'):
            crypto_node = ls("aov_cryptomatte", type="cryptomatte")[0]
        else:
            crypto_node = createNode("cryptomatte", n="aov_cryptomatte")

        cmds.connectAttr(crypto_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class OcclusionAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(OcclusionAOV, self).create_aov(output_denoising)

        occlusion_node = createNode("aiAmbientOcclusion", n="occMtl")
        occlusion_node.falloff.set(0)
        cmds.connectAttr(occlusion_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class UVAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [FullPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(UVAOV, self).create_aov(output_denoising)

        uv_node = createNode("aiUtility", n="aiUtiliy_uv")
        uv_node.shadeMode.set(2)
        uv_node.colorMode.set(5)
        cmds.connectAttr(uv_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class MotionVectorBlurAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [FullPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(MotionVectorBlurAOV, self).create_aov(output_denoising)

        motion_vector_node = createNode("aiMotionVector", n="aiMotionVector")
        motion_vector_node.raw.set(1)
        cmds.connectAttr(motion_vector_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class EmissionIndirectAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(EmissionIndirectAOV, self).create_aov(output_denoising)
        setAttr("aiAOV_" + self._aov.name+".lightPathExpression","C<R>.*O")


class EmissionOSLAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising):
        super(EmissionOSLAOV, self).create_aov(output_denoising)
        setAttr("aiAOV_" + self._aov.name+".lightPathExpression","C<R><O.'customEmit'>")


class LightGroupAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior(), AOVVarianceBehavior()])
