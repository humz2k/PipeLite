import wget
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

class ImageDownloader:
    def __init__(self,org="StoneEdge",telescope="0.5meter"):
        self.prefix = "https://stars.uchicago.edu/images/" + org + "/" + telescope + "/"
        self.files_cache = []
        self.current_dir = ""

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

    def download_file(self,file):
        filename = wget.download(self.get_url(file))
        self.files_cache.append(filename)
        return filename

    def download_cd(self):
        files = [i for i in self.ls() if ".fit" in i]
        filenames = []
        for i in files:
            filenames.append(self.download_file(i))
        return filenames

    def ls(self):
        #print(self.prefix + self.current_dir)
        filename = wget.download(self.prefix + self.current_dir)
        print("\n")
        with open(filename,"r") as f:
            raw = f.read()
        os.remove(filename)
        raw = raw.split("<table>")[1].split("</table>")[0]
        dirs = []
        for i in raw.split("<tr>")[4:]:
            try:
                dirs.append(i.split('href="')[1].split('"')[0])
            except:
                pass

        return dirs

    def cd(self,inp):
        if inp == "..":
            temp = self.current_dir[:-1].split("/")
            if len(temp) > 1:
                self.current_dir = "/".join(temp[:-1])
            if len(temp) == 1:
                self.current_dir = ""
        else:
            self.current_dir += inp
            if self.current_dir[-1] != "/":
                self.current_dir += "/"
        print(self.current_dir)

    '''
    def directory_download(self,date,name=""):
        temp = date.split("-")
        year = temp[0]
        if name != "":
            name += "/"
        url = self.prefix + year + "/" + date + "/" + name
        filename = wget.download(url)
        return filename
    '''

    def clear_files(self):
        for i in self.files_cache:
            os.remove(i)

downloader = ImageDownloader()
#print(downloader.directory_download("2022-02-18","hqureshi"))
downloader.cd("2022/2022-02-18/al")
print(downloader.ls())
downloader.download_cd()
downloader.clear_files()

#url = "https://stars.uchicago.edu/images/StoneEdge/0.5meter/2022/2022-02-18/hqureshi/m51_g-band_128.0s_bin1H_220218_083635_hqureshi_seo_0_FCAL.fits"

#filename = wget.download(url)

#print(filename)

#os.remove(filename)
