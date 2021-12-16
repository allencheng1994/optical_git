class LensUnit(object):
    def __init__(self, piece, mid=0):
        self.__partID = self.__genPartID(piece, mid)
        self.__surfaceID, self.__materialID = self.__genSurfaceID(piece, mid)

    def __genPartID(self, part, mid):
        partID = []
        if mid == 0:
            for i in range(2, 2 * (part + 1), 2):
                surfaceID = i
                partID.append("S" + str(surfaceID) + ".." + str(surfaceID + 1))
        else:
            mid = mid * 2 + 2
            for i in range(2, 2 * (part + 1), 2):
                surfaceID = i
                if i < mid:
                    partID.append("S" + str(surfaceID) + ".." + str(surfaceID + 1))
                else:
                    partID.append("S" + str(surfaceID + 1) + ".." + str(surfaceID + 2))
        return partID

    def __genSurfaceID(self, part, mid):
        surfaceID_list = []
        materialID_list = []
        if mid == 0:
            for i in range(2, 2 * (part + 1), 2):
                surfaceID = i
                surfaceID_list.append("S" + str(surfaceID))
                materialID_list.append("S" + str(surfaceID))
                surfaceID_list.append("S" + str(surfaceID + 1))
        else:
            mid = mid * 2 + 2
            for i in range(2, 2 * (part + 1), 2):
                surfaceID = i
                if i < mid:
                    surfaceID_list.append("S" + str(surfaceID))
                    materialID_list.append("S" + str(surfaceID))
                    surfaceID_list.append("S" + str(surfaceID + 1))
                else:
                    surfaceID_list.append("S" + str(surfaceID + 1))
                    materialID_list.append("S" + str(surfaceID + 1))
                    surfaceID_list.append("S" + str(surfaceID + 2))
        return surfaceID_list, materialID_list

    def get_partID(self):
        return self.__partID

    def get_surfaceID(self):
        return self.__surfaceID

    def get_materialID(self):
        return self.__materialID


if __name__ == "__main__":
    pass
