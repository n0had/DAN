import os
import sys
import cv2
import numpy as np
import torch

try:
    sys.path.append("/content/DAN/codes")  # was "..'
    from data.util import imresize
    import utils as util
except ImportError:
    pass


def downsizeimages_forceful():
    # set parameters
    up_scale = 4  # was 4
    mod_scale = 4  # was 4
    # set data dir
    #sourcedir = "/content/drive/MyDrive/tapmobileTestProj/trainData/united_noVal/source"  # why /? was "/data/Set5/source/"
    #sourcedir = "/content/drive/MyDrive/tapmobileTestProj/trainData/united_noVal/LR/x2"
    #savedir = "/content/drive/MyDrive/tapmobileTestProj/trainData/data_resized"  # was "/data/Set5/"    extra / ?
    sourcedir = "/content/drive/MyDrive/tapmobileTestProj/valData/DIV2K_valid/source"
    savedir = "/content/drive/MyDrive/tapmobileTestProj/valData"

    # load PCA matrix of enough kernel
    print("load PCA matrix")
    pca_matrix = torch.load(
         "/content/DAN/pca_matrix/DANv2/pca_matrix.pth",
        map_location=lambda storage, loc: storage  # was "../../pca_matrix.pth"
    )
    print("PCA matrix shape: {}".format(pca_matrix.shape))

    degradation_setting = {
        "random_kernel": False,
        "code_length": 10,
        "ksize": 21,
        "pca_matrix": pca_matrix,
        "scale": up_scale,
        "cuda": True,
        "rate_iso": 1.0  # was ""rate_iso", 1.0" for some reason
    }

    # set random seed
    util.set_random_seed(0)

    #saveHRpath = os.path.join(savedir, "HR", "x" + str(mod_scale))
    saveLRpath = os.path.join(savedir, "LR", "x" + str(up_scale))



    if not os.path.isdir(sourcedir):
        print("Error: No source data found")
        exit(0)
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    #if not os.path.isdir(os.path.join(savedir, "HR")):
    #    os.mkdir(os.path.join(savedir, "HR"))
    if not os.path.isdir(os.path.join(savedir, "LR")):
        os.mkdir(os.path.join(savedir, "LR"))



    #if not os.path.isdir(saveHRpath):
    #    os.mkdir(saveHRpath)
    #else:
    #    print("It will cover " + str(saveHRpath))

    if not os.path.isdir(saveLRpath):
        os.mkdir(saveLRpath)
    else:
        print("It will cover " + str(saveLRpath))






    filepaths = sorted([f for f in os.listdir(sourcedir) if f.endswith(".png")])
    print(filepaths)
    num_files = len(filepaths)

    #kernel_map_tensor = torch.zeros((num_files, 1, 10))  # each kernel map: 1*10

    # prepare data with augementation

    #kernelPath="C:/tapMobileProj/dataset/united_noVal/Kernels" # / ?

    for i in range(num_files):
        filename = filepaths[i]
        print("No.{} -- Processing {}".format(i, filename))
        # read image
        image = cv2.imread(os.path.join(sourcedir, filename))

        width = int(np.floor(image.shape[1] / mod_scale))
        height = int(np.floor(image.shape[0] / mod_scale))
        # modcrop
        if len(image.shape) == 3:
            image_HR = image[0: mod_scale * height, 0: mod_scale * width, :]
        else:
            image_HR = image[0: mod_scale * height, 0: mod_scale * width]
        # LR_blur, by random gaussian kernel
        img_HR = util.img2tensor(image_HR)
        C, H, W = img_HR.size()


        # LR
        image_LR = imresize(image_HR, 1 / up_scale, True)


        #cv2.imwrite(os.path.join(saveHRpath, filename), image_HR)
        cv2.imwrite(os.path.join(saveLRpath, filename), image_LR)

        #kernel_map_tensor[i] = ker_map
    # save dataset corresponding kernel maps
    #torch.save(kernel_map_tensor,
    #           "C:/tapMobileProj/dataset/united_noVal/Kernels/unitedKermap.pth")  # was ./Set5_sig2.6_kermap.pth
    print("Image Blurring & Down smaple Done: X" + str(up_scale))


if __name__ == "__main__":
    downsizeimages_forceful()
