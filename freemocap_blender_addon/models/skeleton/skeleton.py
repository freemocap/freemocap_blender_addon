@dataclass
class Skeleton:
    body: CompoundLinkageABC
    hands: Optional[HandsLinkageABC]