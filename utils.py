from typing import List


from plane import Plane


def Sort(Planes: List[Plane]):
    Planes.sort(key=lambda plane_: plane_.GetAverageZ(), reverse=True)
    return Planes
