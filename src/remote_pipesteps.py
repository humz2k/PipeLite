from find_data import *
from image_math import batch_process
from setup import *
from pipeline import run_pipeline, run_local_astrometry
from image_combine import drizzle, display_images, datain

class Remote:
    def __init__(self,org="StoneEdge",telescope="0.5meter"):
        self.datafinder = DataFinder(org=org,telescope=telescope)

    def image_math(self,date,user,exposures,filters,limit=0):

        expo = []
        for i in exposures:
            if i == 128 or i == 256 or i == 64:
                expo.append(str(i) + ".0s")

        hs = self.datafinder.batch_find(date,user,masks=["RAW","bin1H"] + filters,limit=limit,types=["original"])[0]
        ls = self.datafinder.batch_find(date,user,masks=["RAW","bin1L"] + filters,limit=limit,types=["original"])[0]
        data = hs + ls
        out = self.datafinder.batch_find(date,user,dark_masks=expo,types=["dark","flat","bias"],masks=filters)
        dark = out[0]
        flat = out[1]
        bias = out[2]

        out = batch_process(datapaths = [data], outfolder = '/out/', darkfolder = dark, biasfolder = bias, flatfolder = flat)
        self.datafinder.clear()

        return out

remote = Remote()
outs = remote.image_math("2022-02-18","hqureshi",[128],["g-band"])
print(outs)
