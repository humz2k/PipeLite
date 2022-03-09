import wget
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

class ImageDownloader:
    def __init__(self,org="StoneEdge",telescope="0.5meter"):
        self.prefix = "https://stars.uchicago.edu/images/" + org + "/" + telescope + "/"
        self.files_cache = []

    def get_url(self,file):
        filename = file
        temp = file.split("_")
        date = temp[4]
        year = "20" + date[0:2]
        month = date[2:4]
        day = date[4:6]
        user = temp[6]
        url = self.prefix + year + "/" + year + "-" + month + "-" + day + "/" + user + "/" + filename
        return url

    def download(self,file):
        filename = wget.download(self.get_url(file))
        self.files_cache.append(filename)
        return filename

    def directory_download(self,date,name=""):
        temp = date.split("-")
        year = temp[0]
        if name != "":
            name += "/"
        url = self.prefix + year + "/" + date + "/" + name
        print(url)

    def clear_files(self):
        for i in self.files_cache:
            os.remove(i)

downloader = ImageDownloader()
print(downloader.directory_download("m51_g-band_128.0s_bin1H_220218_083635_hqureshi_seo_0_FCAL.fits"))
downloader.clear_files()

#url = "https://stars.uchicago.edu/images/StoneEdge/0.5meter/2022/2022-02-18/hqureshi/m51_g-band_128.0s_bin1H_220218_083635_hqureshi_seo_0_FCAL.fits"

#filename = wget.download(url)

#print(filename)

#os.remove(filename)
