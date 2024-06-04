from freemocap_blender_addon.models.skeleton.abstract_base_classes import ChainABC
from freemocap_blender_addon.models.skeleton.body.b_rigid_bodies.left_body_rigid_bodies import LeftForearmRigidBody, \
    LeftPalmRigidBody, LeftFootRigidBody
from freemocap_blender_addon.models.skeleton.body.c_linkages.left_body_linkages import LeftShoulderLinkage, \
    LeftElbowLinkage, LeftAnkleLinkage, LeftKneeLinkage, LeftHipLinkage


class LeftArmChain(ChainABC):
    parent = LeftShoulderLinkage
    children = [LeftElbowLinkage,
                LeftForearmRigidBody,
                LeftPalmRigidBody
                ]

class LeftLegChain(ChainABC):
    parent = LeftHipLinkage
    children = [LeftKneeLinkage,
                LeftAnkleLinkage,
                LeftFootRigidBody
                ]