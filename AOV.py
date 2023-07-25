from abc import *
from enum import Enum
import mtoa.aovs as aovs
import pymel.core as pm
from .AOVBehavior import *
from common.utils import *


class AOV(ABC):
    def __init__(self, name, order_group, aov_behaviors):
        """
        Constructor
        :param name:
        :param order_group:
        :param aov_behaviors:
        """
        self.__name = name
        self.__order_group = order_group
        self.__aov_behaviors = aov_behaviors
        self._aov = None

    def get_order_group(self):
        """
        Getter of the order group
        :return: order_group
        """
        return self.__order_group

    def create_aov(self, output_denoising, mono_driver):
        """
        Create the AOV
        :param output_denoising
        :return:
        """
        self._aov = aovs.AOVInterface().addAOV(self.__name)
        for aov_behavior in self.__aov_behaviors:
            aov_behavior.connect_driver_filter(self._aov.name, output_denoising, mono_driver)

    def update(self, aov_name, output_denoising, mono_driver):
        """
        Update the aov by connecting the right driver and filter
        :param aov_name
        :param output_denoising
        :return:
        """
        for aov_behavior in self.__aov_behaviors:
            aov_behavior.connect_driver_filter(aov_name, output_denoising, mono_driver)


class DefaultAOV(AOV):
    pass


class CryptomatteAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising, mono_driver):
        super(CryptomatteAOV, self).create_aov(output_denoising, mono_driver)

        if pm.objExists('aov_cryptomatte'):
            crypto_node = pm.ls("aov_cryptomatte", type="cryptomatte")[0]
        else:
            crypto_node = pm.createNode("cryptomatte", n="aov_cryptomatte")

        pm.connectAttr(crypto_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class OcclusionAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior()])

    def create_aov(self, output_denoising, mono_driver):
        super(OcclusionAOV, self).create_aov(output_denoising, mono_driver)

        occlusion_node = pm.createNode("aiAmbientOcclusion", n="occMtl")
        occlusion_node.falloff.set(0)
        pm.connectAttr(occlusion_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class UVAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [FullPrecisionBehavior()])

    def create_aov(self, output_denoising, mono_driver):
        super(UVAOV, self).create_aov(output_denoising, mono_driver)

        uv_node = pm.createNode("aiUtility", n="aiUtiliy_uv")
        uv_node.shadeMode.set(2)
        uv_node.colorMode.set(5)
        pm.connectAttr(uv_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class MotionVectorBlurAOV(AOV):
    def __init__(self, name, order_group, aov_behaviors):
        super().__init__(name, order_group, aov_behaviors)

    def create_aov(self, output_denoising, mono_driver):
        super(MotionVectorBlurAOV, self).create_aov(output_denoising, mono_driver)
        motion_vector_node = None
        if pm.objExists("aiMotionVector"):
            tmp_aimv = pm.ls("aiMotionVector", type="aiMotionVector")
            if len(tmp_aimv) > 0:
                motion_vector_node = tmp_aimv[0]
        if motion_vector_node is None:
            motion_vector_node = pm.createNode("aiMotionVector", n="aiMotionVector")
        motion_vector_node.raw.set(1)
        pm.connectAttr(motion_vector_node.name() + ".outColor", "aiAOV_" + self._aov.name + ".defaultValue")


class MotionVectorBlurGaussianAOV(MotionVectorBlurAOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [FullPrecisionBehavior()])


class MotionVectorBlurClosestAOV(MotionVectorBlurAOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [FullPrecisionClosestBehavior()])


class EmissionIndirectAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior(), AOVVarianceBehavior()])

    def create_aov(self, output_denoising, mono_driver):
        super(EmissionIndirectAOV, self).create_aov(output_denoising, mono_driver)
        pm.setAttr("aiAOV_" + self._aov.name + ".lightPathExpression", "C[DSV].*O")


class EmissionOSLAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior(), AOVVarianceBehavior()])

    def create_aov(self, output_denoising, mono_driver):
        super(EmissionOSLAOV, self).create_aov(output_denoising, mono_driver)
        pm.setAttr("aiAOV_" + self._aov.name + ".lightPathExpression", "C[DSV].*<O.'customEmit'>")


class LightGroupAOV(AOV):
    def __init__(self, name, order_group):
        super().__init__(name, order_group, [HalfPrecisionBehavior(), AOVVarianceBehavior()])
