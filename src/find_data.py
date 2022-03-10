from get_stars import *
import datetime

class DataFinder:
    def __init__(self,org="StoneEdge",telescope="0.5meter"):
        self.prefix = "https://stars.uchicago.edu/images/" + org + "/" + telescope + "/"
        self.files_cache = []
        self.downloader = ImageDownloader(org=org,telescope=telescope)
        self.clear = self.downloader.clear_files
        self.reset()

    def reset(self):
        self.downloader.clear_files()
        files = [i for i in os.listdir() if ".fit" in i]
        for i in files:
            os.remove(i)

    def list_files(self,date,user,masks,limit=0):
        year = date.split("-")[0]
        self.downloader.cd("")
        self.downloader.cd(year + "/" + date + "/" + user + "/")
        files = self.downloader.ls()
        for i in masks + [".fit"]:
            files = [j for j in files if i in j]
        if limit > 0:
            files = files[:limit]
        return files

    def batch_find(self,date,user,masks=[],dark_masks=[],types=["original"],limit=0):
        year = date.split("-")[0]
        self.downloader.cd("")
        self.downloader.cd(year + "/" + date + "/" + user + "/")
        files = self.downloader.ls()
        for i in masks + [".fit"]:
            files = [j for j in files if i in j]
        if limit > 0:
            files = files[:limit]
        out = []
        for j in types:
            filenames = []
            #print("Downloading ",j+"s")
            if j == "original":
                for i in files:
                    filenames.append(self.downloader.download_file(i))
            else:
                filenames = self.find(filename=files[0],image_type=j,dark_masks=dark_masks,masks=masks)
            out.append(filenames)
        return out

    def find(self,filename=None,date=None,image_type="original",dark_masks=[],masks=[]):
        if not filename == None:
            temp = filename.split("_")
            date = temp[4]
            year = "20" + date[0:2]
            month = date[2:4]
            day = date[4:6]
            better_date = year + "-" + month + "-" + day
            user = temp[6]
        elif not date == None:
            year = date.split("-")[0]
            better_date = date
        else:
            return
        masters = year + "/" + "Masters-15C"
        if image_type == "dark":
            self.downloader.cd("")
            self.downloader.cd(masters + "/DARK")
            files = self.downloader.ls()
            for i in dark_masks:
                files = [j for j in files if i in j]
            out = []
            #print(files)
            for i in files:
                out.append(self.downloader.download_file(i,master=True))
            return out
        elif image_type == "bias":
            folder = masters + "/PFIT"
        elif image_type == "flat":
            self.downloader.cd("")
            self.downloader.cd(masters)
            days = [i.split("/")[0].split("FLAT_")[1] for i in self.downloader.ls() if "FLAT" in i]
            if better_date in days:
                folder = masters + "/FLAT_" + better_date
            else:
                min = float('inf')
                best = ""
                temp_date = datetime.datetime.strptime(better_date,"%Y-%m-%d")
                for i in days:
                    temp = abs(datetime.datetime.strptime(i,"%Y-%m-%d") - temp_date)
                    if temp.total_seconds() <= min:
                        min = temp.total_seconds()
                        best = i
                folder = masters + "/FLAT_" + best
            self.downloader.cd("")
            self.downloader.cd(folder)
            files = self.downloader.ls()
            for j in masks:
                files = [i for i in files if j in i]
            out = []
            for i in files:
                out.append(self.downloader.download_file(i,master=True))
            self.downloader.cd("")
            return out

        elif image_type == "original":
            return self.downloader.download_file(filename)

        self.downloader.cd("")
        self.downloader.cd(folder)
        return self.downloader.download_cd(master=True)
        #return self.downloader.download_cd()

if __name__ == "__main__":
    data_finder = DataFinder()
    hs = data_finder.batch_find("2022-02-18","hqureshi",masks=["g-band","RAW","bin1H"],limit=3,types=["original"])[0]
    ls = data_finder.batch_find("2022-02-18","hqureshi",masks=["g-band","RAW","bin1L"],limit=3,types=["original"])[0]
    data = hs + ls
    out = data_finder.batch_find("2022-02-18","hqureshi",dark_masks=["128.0s"],types=["dark","flat","bias"],masks=["g-band"])
    dark = out[0]
    flat = out[1]
    bias = out[2]

    print()
    print(data)
    print(dark)
    print(flat)
    print(bias)

    '''
    data = ['m51_g-band_128.0s_bin1H_220218_083635_hqureshi_seo_0_RAW.fits',
    'm51_g-band_128.0s_bin1H_220218_083907_hqureshi_seo_1_RAW.fits',
    'm51_g-band_128.0s_bin1H_220218_084137_hqureshi_seo_2_RAW.fits',
    'm51_g-band_128.0s_bin1L_220218_083635_hqureshi_seo_0_RAW.fits',
    'm51_g-band_128.0s_bin1L_220218_083907_hqureshi_seo_1_RAW.fits',
    'm51_g-band_128.0s_bin1L_220218_084137_hqureshi_seo_2_RAW.fits']

    dark = ['meandark_h-alpha_128.0s_bin1H_220112-220112_seo_MDARK.fits','meandark_h-alpha_128.0s_bin1L_220112-220112_seo_MDARK.fits']

    flat = ['mflat_g-band_bin1HDR_20220219_022331-022742_chultun_seo_MFLAT.fits']

    bias = ['darkpolyfit_bin1H_20220108-20220112_1.0-64.0s_PFIT.fits',
    'darkpolyfit_bin1H_20220108-20220117_1.0-64.0s_PFIT.fits',
    'darkpolyfit_bin1L_20220108-20220112_1.0-64.0s_PFIT.fits',
    'darkpolyfit_bin1L_20220108-20220117_1.0-64.0s_PFIT.fits']
    '''

    #out = batch_process(datapaths = [data], outfolder = '/out/', darkfolder = dark, biasfolder = bias, flatfolder = flat)

    #print(out)

    data_finder.clear()
