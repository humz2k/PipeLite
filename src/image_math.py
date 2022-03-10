from setup import *
def quickpic4(image,titlestring='',madfactor=(3.,10.),mask=([0],[0]),mask2=([0],[0]) ,csize=100,edgecolor='r',\
               edgecolor2='b', figlims=(10,10), ilims=(0.,0.), cmap='gray', plotmasks=False):
    '''
    A simple image display tool with initial autoscaling based on image median and mad_std.
    It also includes the option to plot circles around positions defined in one or two image masks.
    Arguments:
        image:       A 2D image.
        titlestring: A text string for the figure title. Default is empty string.
        madfactor:   A tuple with multipliers for mad_std to subtract or add to median to get vmin and vmax for imshow.
        mask:        A tuple of ndarrays with lists of the row and column coordinates of the circles to plot.
        mask2:       Another mask array for a second set of circles with twice the radius and different color.
        csize:       Sets size of circles for mask positions. Circles for mask2 positions are two times larger.
        edgecolor:   The color for the mask circles.
        edgecolor2:  The color for the mask2 circles.
        figlims:     Tuple to determine figsize.
        cmap:        Color map. Default = 'gray'
        plotmasks:   If True, plot circles around mask positions. Default = False.
    Author(s) = Al Harper
    Created: 190818.
    Modified: 210705, 210728, 210805.
    Version = 1.1
    '''

    pic = image.copy()
    rows, cols = pic.shape
    med, mad = np.nanmedian(pic), mad_std(pic,ignore_nan=True)
    if ilims == (0.,0.):
        vmn, vmx = med - mad * madfactor[0], med + mad * madfactor[1]
    else:
        vmn, vmx = ilims
    plt.figure(figsize = (figlims))
    plt.title(titlestring)
    plt.imshow(pic, cmap, interpolation='nearest', vmin = vmn, vmax = vmx)
    plt.colorbar(orientation = 'vertical',shrink = 0.8)
    if plotmasks == True:
        for i in mask:
            plt.scatter(mask[1],mask[0],s=csize, facecolors='none', edgecolors=edgecolor)
        for i in mask2:
            plt.scatter(mask2[1],mask2[0],s=2*csize, facecolors='none', edgecolors=edgecolor2)


def timesort(filelist, datapath, date_key = 'DATE-OBSd', print_list = False):
    '''
    Sorts a list of fits files by a header keyword with a date/time value.
    Arguments:
        filelist   = a list of fits files
        datapath   = the path to the files
        date_key   = the header keyword containing the time/date data
        print_list = if True, print the sorted file list
    Returns:
        tfiles     = the sorted file list
        utime      = a list of the unix times of the observations
    Author(s): Al Harper
    Modified: 210807
    Version: 1.0
    '''
    date_obs = []                                           # Make a list to hold the date-obs keyword strings.
    fd = DataFits(config=config)                            # Make a PipeData object.
    for i in range(len(filelist)):                          # Make a PipeData object.
        fd.loadhead(os.path.join(datapath,filelist[i]))
        date_obs.append(fd.header.get('date-obs','None'))   # Add date information to list. of string objects.
    t = Time(date_obs, format='isot', scale='utc')          # Make an astropy time object in 'isot' format.
    tsort = np.argsort(t)                                   # Make a list of indices that will sort by date_obs.
    tfiles = []
    utime = []
    for i in tsort:
        tfiles.append(filelist[i])
        utime.append(t[i].unix)
    if print_list == True:
        for i in range(len(filelist)):
            print( i, tfiles[i], utime[i])
    return tfiles, utime

def timesortHDR(filelist, datapath, date_key = 'date-obs', print_list = False):
    '''
    Sorts a list of fits files by a header keyword with a date/time value. In the case of an
    SBIG CMOS camera RAW file, the date/time is read from the second HDU.
    Arguments:
        filelist   = a list of fits files
        datapath   = the path to the files
        date_key   = the header keyword containing the time/date data
        print_list = if True, print the sorted file list
    Returns:
        tfiles     = the sorted file list
        utime      = a list of the unix times of the observations
    Author(s): Al Harper
    Modified: 210807, 210815
    Version: 1.1
    '''

    date_obs = []                                                # Make a list to hold the date-obs keyword strings.
    fd = DataFits(config=config)                                 # Make a PipeData object.
    for i in range(len(filelist)):
        fname = os.path.join(datapath,filelist[i])
        if '_bin1L' in filelist[i] and '_RAW.' in filelist[i]:
            fd.load(fname)                                       # Load the fits file into the PipeData object.
            head = fd.getheader(fd.imgnames[1])                  # Get the header of the second HDU (index = [1]).
            date_obs.append(head[date_key])                      # Add date information to list. of string objects.
        else:
            fd.load(fname)                                       # Load the fits file.                                       # Load the fits file.
            head = fd.getheader()                                # Get the header of the primary HDU (index = [0]).
            date_obs.append(head[date_key])                      # Add date information to list. of string objects.
    t = Time(date_obs, format='isot', scale='utc')               # Make an astropy time object in 'isot' format.
    tsort = np.argsort(t)                                        # Make a list of indices that will sort by date_obs.
    tfiles = []
    utime = []
    for i in tsort:
        tfiles.append(filelist[i])
        utime.append(t[i].unix)
    if print_list == True:
        for i in range(len(filelist)):
            print( i, tfiles[i], utime[i])
    return tfiles, utime


def expsortHDR(filelist, datapath, print_list = False):
    '''
    Sorts a list of fits files by a header keyword with an exposure time value. In the case of an
    SBIG CMOS camera RAW file, the exposure time is read from the second HDU.
    Arguments:
        filelist   = a list of fits files
        datapath   = the path to the files
        print_list = if True, print the sorted file list
    Returns:
        expfiles     = the sorted file list
        exp          = a sorted list of the exposure times
    Author(s): Carmen Choza
    Modified: 210812
    Version: 1.0
    '''

    exptime = []
    df = DataFits()
    for i in range(len(filelist)):
        fname = os.path.join(datapath, filelist[i])
        if '_bin1L' in filelist[i] and '_RAW.' in filelist[i]:
            df.load(fname)
            head = df.getheader(df.imgnames[1])
            exptime.append(head['exptime'])
        else:
            df.loadhead(os.path.join(datapath, filelist[i]))
            exptime.append(df.header.get('exptime', 'None'))
        expsort = np.argsort(exptime)
        expfiles = []
        exp = []
    for i in expsort:
            expfiles.append(filelist[i])
            exp.append(exptime[i])
    if print_list == True:
            for i in range(len(filelist)):
                print(i, expfiles[i], exp[i])
    return expfiles, exp



def histogram2(img, titlestring = '', NBINS=800, percent=(.05,.05), figsize=(18,8), display_lims=(0,1000), \
               mask_lims=[0,3500], use_percent=True):
    '''
    Makes two histograms of an image. One includes all points and one includes all points within specified
    limits. If there are nans in the image, they are set to a value just smaller than the minimum value of
    the image and then eliminated from the flattened image before computing the histograms.
    Returns:
        undermask = mask identifying pixels with values less than mask_lims[0]
        overmask  = mask identifying pixels with values greater than mask_lims[1]
        mask_lims = list with the upper and lower limits, respectively, of undermask and overmask
    Arguments:
        img             = image to be analyzed
        titlestring     = title of output graph
        percent         = limit percentiles for masks to be applied by default to the second plot
        figsize         = figure size
        display_lims    = lower and upper limits of display of second histogram
        mask_lims       = lower and upper limits used to create undermask and overmask
        use_percent     = True if mask_lims is to be set automatically to the value of the "percent" kwarg
                          and False if undermask and overmask limits are to be set by the mask_lims kwarg
    Author(s): Al Harper
    Modified: 210806, 210811
    Version 1.1
    '''

    # plt.figure(figsize = figsize)

    ## Set any nans to a value just smaller than img minimum so the histogram won't get confused.
    newimg = img.copy()
    imgmin = np.nanmin(img)
    newmin = imgmin - 0.000001 * imgmin
    oldmin_bool = newimg == imgmin
    oldmin = np.sum(oldmin_bool)
    nanmask = np.isnan(img)
    newimg[nanmask] = newmin
    ## Flatten the image, sort it, exclude formerly nan values, and find indices and image values
    ## corresponding to the percent kwarg values.
    flatpic = newimg.flatten()
    sortpic = sorted(flatpic)
    nans = np.sum(sortpic == newmin)
    newsortpic = sortpic[nans:]
    b = int(len(newsortpic)*(1 - percent[1]/100.0))
    a = int(len(newsortpic)*(percent[0]/100.0))

    upper_value = newsortpic[b]
    lower_value = newsortpic[a]
    fpic = newsortpic[a:b]

    ## Make masks and calculate how many pixels fall below and above limits.
    if use_percent == True:
        mask_lims[0], mask_lims[1] = lower_value, upper_value

    ## Create some masks for pixels below and above
    undermask, overmask = np.where(newimg < mask_lims[0]), np.where(newimg > mask_lims[1])
    return undermask, overmask, mask_lims

def read_oneDF(whichfiles, whichfile, whichpath, convert_raw=False):
    '''
    Read one fits file into a DataFits object. If the file is an SBIG CMOS camera RAW file,
    strip the overscan rows from the image and create a header keyword with value equal to
    the mean value of the overscan region.
    Returns:
        df:              DataFits object
    Arguments:
        whichfiles:      List of fits files
        whichfile:       Index number of file to be selected from list
        whichpath:       Path to directory where files are stored
        convert_raw:     If True, strip overscan columns from SBIG CMOS camera images
                         and add overscan mean to header. Default = False
    Author(s): Al Harper
    Modified: 210805
              211125: Modified to read bin2 as well as bin1 images.
    Version 1.1
    '''
    #fitsfilename = os.path.join(whichpath,whichfiles[whichfile])
    fitsfilename = whichfiles[whichfile]
    if 'bin1L' in fitsfilename and '_RAW.fit' in whichfiles[whichfile]:
        ddf = DataFits(config=config)
        ddf.load(fitsfilename)
        df = DataFits(config=config)
        df.header = ddf.getheader(ddf.imgnames[1]).copy()
        del df.header['xtension']
        df.header.insert(0,('simple',True,'file does conform to FITS standard'))
        df.imageset(ddf.imageget(ddf.imgnames[1]))
    else:
        df = DataFits(config=config)                # Create a DataPype DataFits io object.
        df.load(fitsfilename)                       # Loads the file.

    ## Crop over-scan columns from image and create over-scan image (only for bin=1L SBIG CMOS camera images).
    if camera == 'SBIG' and '_RAW.fit' and '_bin1' in whichfiles[whichfile] and convert_raw == True:
        osimg = df.image[:,4096:]
        df.image = df.image[:,:4096]
        oscnmean = np.nanmean(osimg)
        df.header['oscnmean'] = oscnmean
    if camera == 'SBIG' and '_RAW.fit' and '_bin2' in whichfiles[whichfile] and convert_raw == True:
        osimg = df.image[:,2048:]
        df.image = df.image[:,:2048]
        oscnmean = np.nanmean(osimg)
        df.header['oscnmean'] = oscnmean

    return df


def make_stackDF(whichfiles, whichpath):
    '''
    Make a stack of images, a list of headers from those images, and calculate some medians and stds
    that will help set autoscaling parameters. If camera == 'SBIG', crop the overscan columns and create
    an overscan image. If the data were taken in low-gain mode, fix the FITS format of the low-gain image.

    Returns:
        image    =  a 3-dimensional image (an "image stack")
        headlist =  a list of the primary headers of the imaes in the stack
        stats    =  {'median':median,'std':std,'mad':mad}
    Author(s): Al Harper
    Modified: 210805, 210817
    Version 1.1
    '''

    # Read one file to determine numbers of rows and columns.
    ff = read_oneDF(whichfiles, 0, whichpath, convert_raw = True)
    rows, cols = ff.image.shape[0], ff.image.shape[1]

    image = np.zeros((len(whichfiles), rows,cols))  # 3D numpy array to hold the stack of images.
    median = np.zeros((len(whichfiles)))            # 1D numpy array to hold array medians.
    mean = np.zeros((len(whichfiles)))            # 1D numpy array to hold array medians.
    std = np.zeros((len(whichfiles)))               # 1D numpy array to hold array stds.
    mad = np.zeros((len(whichfiles)))            # 1D numpy array to hold median absolute deviations.

    headlist = []                                   # Empty list to hold the headers.
    for i in range(len(whichfiles)):
        df = read_oneDF(whichfiles, i, whichpath, convert_raw = True)
        image[i] = df.image
        headlist.append(df.header.copy())
        # Calculate some statistical information.
        mad[i] = mad_std(image[i],ignore_nan=True)
        median[i] = np.nanmedian(image[i])
        mean[i] = np.nanmean(image[i])
        std[i] = np.nanstd(image[i])

    stats = {'median':median, 'mean':mean, 'std':std, 'mad':mad}

    return image, headlist, stats

def make_hotpix_mask(darkfolder, exposure = "128"):
    if type(darkfolder) is list:
        darkfiles = darkfolder
    else:
        darkfiles = sorted([f for f in os.listdir(darkfolder) if '.fit' in f and 'MDARK' in f and exposure in f])
    darkH_df = read_oneDF(darkfiles,0,darkfolder)
    global darkH
    darkH = darkH_df.image
    global darknameH
    darknameH = darkfiles[0]
    darkL_df = read_oneDF(darkfiles,1,darkfolder)
    global darkL
    darkL = darkL_df.image
    global darknameL
    darknameL = darkfiles[1]

    ## Make a hot pixel mask.
    darkHPX_df = read_oneDF(darkfiles, 0, darkfolder)
    global darknameHPX
    darknameHPX = darkfiles[0]
    ## Then make a histogram and a "hot pixel" mask.
    img = darkHPX_df.image
    titlestring = darkfiles[0]
    global hotpix
    undermask, hotpix, mask_lims = histogram2(img, titlestring, percent=[0.0, 0.5], \
                    display_lims=(19.9, 21.9), mask_lims=[19.9, 21.9], use_percent=True)
    print("made hotpixel mask")

def find_band(filepath):
    '''
    Find the band of the images.
    Returns:
        band:    string containing the band name
    '''
    unknown = ''
    for b in ["h-alpha", "g-band", "i-band", "r-band", "oiii", "sii", "clear"]:
        if b in filepath:
            print("Found band:", b)
            return b
    return unknown

def load_bias(biasfolder):
    ## List the files in biaspath.
    if type(biasfolder) is list:
        biasfiles = biasfolder
    else:
        biasfiles = [f for f in os.listdir(biasfolder) if 'PFIT' in f]    #  and 'dark' in f]
    biasH_df = read_oneDF(biasfiles,0,biasfolder)
    global biasH
    biasH = biasH_df.image[1]
    biasL_df = read_oneDF(biasfiles,1,biasfolder)
    global biasL
    biasL = biasL_df.image[1]
    print("loaded bias")

def load_flat(flatfolder, band_string = "", curr_date = np.datetime64('today', 'D')):
    if type(flatfolder) is list:
        flatfiles = flatfolder
    else:
        flatfiles = [f for f in os.listdir(flatfolder) if '.fit' in f and 'MFLAT' in f]
    whichfile = -1
    filecandidates = set()
    if band_string == "":
        print("Warning: no band specified. Using first flat file.")
    for i,val in enumerate(flatfiles):
        if band_string in val:
            filecandidates.add((i, get_header(val, flatfolder, 'DATE-OBS')[:10]))
    # get index of flat with closest date
    closest = min(filecandidates, key=lambda x: abs(np.datetime64(x[1]) - np.datetime64(curr_date)))
    print(f"Closest flat: {closest}")
    whichfile = closest[0]
    if whichfile == -1:
        print(f"ERROR: Could not find flat file with band_string = {band_string}")
        return
    ## Load flat files and create names for titles of flat-frame images
    flat_df = read_oneDF(flatfiles,whichfile,flatfolder)
    global flatH
    flatH = flat_df.image[0]
    global flatL
    flatL = flat_df.image[1]
    global flat_date
    flat_date = flat_df.getheader()['DATE-OBS'][:10]
    gain_df = read_oneDF(flatfiles, whichfile, flatfolder)
    global gain
    gain = gain_df.imageget('gain ratio')
    print(f"loaded flats for band {band_string}")

def load_datafiles(datapath, object_name = "", band_string = ""):
    if type(datapath) is list:
        files = datapath
        files_L = sorted([f for f in files if 'bin1L' in f],
                            key = lambda x : fits.open(x)[1].header['DATE-OBS'])
        files_H = sorted([f for f in files if 'bin1H' in f],
                            key = lambda x: fits.open(x)[0].header['DATE-OBS'])
    else:
        files = [f for f in os.listdir(datapath) if '.fit' and 'RAW' in f\
                and '_bin1_' not in f and 'dark' not in f and object_name in f and band_string in f]
        files_L = sorted([f for f in files if 'bin1L' in f],
                            key = lambda x : fits.open(os.path.join(datapath,x))[1].header['DATE-OBS'])
        files_H = sorted([f for f in files if 'bin1H' in f],
                            key = lambda x: fits.open(os.path.join(datapath,x))[0].header['DATE-OBS'])
    print("Processing the following files:")
    for i in range(len(files_L)):
        print(i, files_L[i])
        print(i, files_H[i])
    return files_L, files_H

#### Load data files.
# Processes index of filelist, outputs dataH and dataL
def process_one(index, files_L, files_H):
    dataH_df = read_oneDF(files_H, index, datapath, convert_raw=True)
    dataH = dataH_df.image
    datanameH = files_H[index]
    dataL_df = read_oneDF(files_L, index, datapath, convert_raw=True)
    dataL = dataL_df.image
    datanameL = files_L[index]
    dataH.shape
    return dataH, dataH_df, dataL, dataL_df

'''cosmic_file: takes a DataFits object and returns the cosmic ray cleaned image.'''
def cosmic_file(a, log = ""):
    cosmics = detect_cosmics(a, cleantype='medmask')
    # print(f"LOG: {log} || Detected {count} pixels of cosmic rays.")
    return cosmics[1]

'''Process HDR images through bias-dark-flat, HDR combination, and downsampling stages'''
# Returns outdata
def process_hdr_images(dataH, dataL):
    kernel = Gaussian2DKernel(x_stddev=2)  # Prepare kernel for nan-replacement
    '''Process high-gain data'''
    # bias-dark-flat processing
    dataHbdf = ((dataH - biasH) - (darkH - biasH))/flatH
    # Apply hotpix mask (in case not all hot pixels captured in flat above)
    dataHbdfx = dataHbdf.copy()
    dataHbdfx[hotpix] = np.nan
    # Replace nans with Gaussian-weighted average of adjacent pixels
    dataHbdfx = interpolate_replace_nans(dataHbdfx, kernel)
    '''Process low-gain data'''
    dataLbdf = (((dataL - biasL) - (darkL - biasL))/flatL) * gain
    dataLbdfx = dataLbdf.copy()
    dataLbdfx[hotpix] = np.nan
    dataLbdfx = interpolate_replace_nans(dataLbdfx, kernel)
    '''Combine high and low gain data into HDR image'''
    upperL = np.where(dataLbdfx > 3000.0)   # Crossover threshold is currently hard-coded. Could be a parameter in future.
    Ldata = dataLbdfx.copy()
    HDRdata = dataHbdfx.copy()
    HDRdata[upperL] = Ldata[upperL]
    '''Downsample image by factor of two'''
    outdata = nd.zoom(HDRdata,0.5)
    return outdata

def construct_output_name(index, files_H):
    datanameH = files_H[index]
    a = datanameH.split('_')
    b = '_'
    # print(a)
    newname = a[0]+b+a[1]+b+a[2]+b+a[3][:-1]+b+a[4]+b+a[5]+b+a[6]+b+a[7]+b+str(index)+'_HDR'+'.fits'
    # print(newname)
    return newname

def get_header(file, datapath, header = 'DEWTEM1'):
    if type(datapath) is list:
        if(any([a in file for a in ['bin1H', 'MFLAT', 'MDARK', 'PFIT']])):
            return fits.open(file)[0].header[header]
        else:
            return fits.open(file)[1].header[header]
    else:

        if(any([a in file for a in ['bin1H', 'MFLAT', 'MDARK', 'PFIT']])):
            return fits.open(os.path.join(datapath,file))[0].header[header]
        else:
            return fits.open(os.path.join(datapath,file))[1].header[header]

## Set output path, output file name, and image name.
def create_output(newname, outdata, dataH_df, outfolder):
    outname = newname
    outfile = os.path.join(outfolder, outname)
    ## Set content of output file.
    outimage = outdata
    outheader = dataH_df.header.copy()
    ## Create output data object.
    outd = DataFits()
    ## Load image data in output object.
    outd.image = outimage
    return outheader, outd, outname, outfile

def prepare_header(outheader, outd):
    add_keywords = True
    filestring = ''
    notestring = 'HDR image reduced with Jupyter notebook ' + reduced_by
    if add_keywords == True:
        outheader['notes'] = notestring
        outheader['filelist'] = filestring
        outheader['bzero'] = 0.0
    ## Load header in output object.
    outd.header = outheader
    return outd

def save_file(outd, outfile, outname):
    print("CALLING ME")
    outd.save(outname)
    return outname
    '''
    if os.path.exists(os.path.join(outfile)) == True:
        print(f"File {outfile} already exists!")
    else:
        outd.save(outname)
        print(f"File {outname} was saved.")
    '''
"""
Batch_process
    Batch process HDR images.
    Inputs:
        datapaths (optional list str): list of paths to data files (default: datapath from input.py)
        outfolder (optional str): path to output folder (default: outpath from input.py)
        darkfolder (optional str): path to dark folder (default: darkpath from input.py)
        flatfolder (optional str): path to flat folder (default: flatpath from input.py)
        biasfolder (optional str): path to bias folder (default: biaspath from input.py)
    Outputs:
        Saves HDR images to output path.

"""
def batch_process(datapaths = [datapath], outfolder = outpath, darkfolder = darkpath, biasfolder = biaspath, flatfolder = flatpath, detect_cosmics = False):
    # Batch process many files
    out = []
    load_bias(biasfolder)
    if isinstance(datapaths, str):
      print("Error: datapaths must be list of strings, not string")
      return

    for curr_path in datapaths:
        global datapath
        datapath = curr_path
        files_L, files_H = load_datafiles(datapath)
        old_curr_date = 0
        old_exposure_time = 0
        old_band = ''
        for index in range(len(files_L)):
            output_name = construct_output_name(index, files_H)
            #print("OUT",output_name)
            print(f"\nProcessing file {output_name}")
            # If already processed, skip
            if os.path.exists(os.path.join(outfolder, output_name)) == True:
                print(f"File {construct_output_name(index, files_H)} already exists!")
                continue
            curr_date = get_header(files_L[index], datapath, 'DATE-OBS')[:10]
            curr_band = find_band(files_L[index])
            # Load new flat if necessary
            if curr_date != old_curr_date or curr_band != old_band:
                old_curr_date = curr_date
                old_band = curr_band
                print("Date/string mismatch: Getting new flat")
                load_flat(flatfolder, curr_band, curr_date)
            # Load new dark if necessary
            curr_exposure_time = get_exposure_time(files_L[index])
            if curr_exposure_time != old_exposure_time:
                old_exposure_time = curr_exposure_time
                print("Exposure time mismatch: Getting new dark")
                make_hotpix_mask(darkfolder, curr_exposure_time)

            dataH, dataH_df, dataL, dataL_df = process_one(index, files_L, files_H)
            outdata = process_hdr_images(dataH, dataL)
            #print("AFTER PROCESS")
            outheader, outd, outname, outfile = create_output(output_name, outdata, dataH_df, outfolder)
            prepare_header(outheader, outd)
            #print("AFTER HEADER")
            if(detect_cosmics):
                outd.image = cosmic_file(outd.image)
            #print(outd,outfile,outname)
            out.append(save_file(outd, outfile, outname))
    return out

def get_exposure_time(filename):
    if '128' in filename:
        return "128"
    else:
        return "256"

def sort_dewtemp(datapaths = [datapath]):
    for datapath in datapaths:
        os.makedirs('-15', exist_ok=True)
        os.makedirs('0', exist_ok=True)
        if type(datapaths[0]) is list:
            for file in datapath:
                if file.endswith('.fits'):
                    try:
                        if get_header(file, datapath) == -15:
                            # move to folder
                            os.rename(file, os.path.join("-15", file))
                        else:
                            os.rename(file, os.path.join("0", file))
                    except:
                        print(f"Could not find dewtemp for {file}")
        else:
            for file in os.listdir(datapath):
                if file.endswith('.fits'):
                    try:
                        if get_header(file, datapath) == -15:
                            # move to folder
                            os.rename(os.path.join(datapath, file), os.path.join(datapath, "-15", file))
                        else:
                            os.rename(os.path.join(datapath, file), os.path.join(datapath, "0", file))
                    except:
                        print(f"Could not find dewtemp for {file}")
