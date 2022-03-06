import VisionApi, cv2


api = VisionApi.Instance()
image = cv2.imread("../../../test/output.png")

dur, result = api.upload(image,champions=["Xayah","Garen"])

print(result)
