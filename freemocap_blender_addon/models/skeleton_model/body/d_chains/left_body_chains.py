from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.left_body_rigid_bodies import LeftForearmRigidBody, \
    LeftPalmRigidBody, LeftFootRigidBody
from freemocap_blender_addon.models.skeleton_model.body.c_linkages.left_body_linkages import LeftShoulderLinkage, \
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