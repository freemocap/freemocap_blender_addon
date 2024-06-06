from freemocap_blender_addon.models.skeleton_model.keypoint_rigidbody_linkage_chain_abc import ChainABC
from freemocap_blender_addon.models.skeleton_model.body.b_rigid_bodies.right_body_rigid_bodies import RightForearmRigidBody, \
    RightPalmRigidBody, RightFootRigidBody
from freemocap_blender_addon.models.skeleton_model.body.c_linkages.right_body_linkages import RightShoulderLinkage, \
    RightElbowLinkage, RightAnkleLinkage, RightKneeLinkage, RightHipLinkage


class RightArmChain(ChainABC):
    parent = RightShoulderLinkage
    children = [RightElbowLinkage,
                RightForearmRigidBody,
                RightPalmRigidBody
                ]

class RightLegChain(ChainABC):
    parent = RightHipLinkage
    children = [RightKneeLinkage,
                RightAnkleLinkage,
                RightFootRigidBody
                ]