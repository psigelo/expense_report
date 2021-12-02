import os
import time
import numpy as np

import torch
from torch.autograd import Variable
import cv2

from ai.CRAFT.craft import CRAFT
import ai.CRAFT.imgproc as imgproc
import ai.CRAFT.craft_utils as craft_utils
import ai.CRAFT.file_utils as file_utils

from collections import OrderedDict

# Parameters
trained_model = 'craft_mlt_25k.pth'
text_threshold =0.7
low_text =0.4
link_threshold =0.4
cuda = False
canvas_size = 1280
mag_ratio =1.5
poly = False
show_time = False
test_folder = '/home/anonimo/Documents/MIA/Capstone/imagenes_prueba/'
refine = False
refiner_model = None #'weights/craft_refiner_CTW1500.pth'
refine_net = None

def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def crop_sections(image, polys, result_folder, filename):
    for i in range(len(polys)):
        mask = np.zeros(image.shape[0:2], dtype=np.uint8)
        points = polys[i].reshape(1,4,2).astype(int)
        #method 1 smooth region
        cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        #method 2 not so smooth region
        # cv2.fillPoly(mask, points, (255))
        res = cv2.bitwise_and(image,image,mask = mask)
        rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
        ## crate the white background of the same size of original image
        #wbg = np.ones_like(image, np.uint8)*255
        #cv2.bitwise_not(wbg,wbg, mask=mask)
        # overlap the resulted cropped image on the white background
        #dst = wbg+res

        mask_file_path = result_folder + "/res_" + filename + '_crop_' + str(i) + '.jpg'
        cv2.imwrite(mask_file_path, cropped)

result_folder = './result/'
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)

# Load model
#net = CRAFT()
#net.load_state_dict(copyStateDict(torch.load(trained_model, map_location='cpu')))
#net.eval()


def load_model(trained_model):
    net = CRAFT()
    net.load_state_dict(copyStateDict(torch.load(trained_model, map_location='cpu')))
    net.eval()
    return net


def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None):
    t0 = time.time()

    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image,  canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio= mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0,:,:,0].cpu().data.numpy()
    score_link = y[0,:,:,1].cpu().data.numpy()

    # refine link
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0,:,:,0].cpu().data.numpy()

    t0 = time.time() - t0
    t1 = time.time()

    # Post-processing
    boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None: polys[k] = boxes[k]

    t1 = time.time() - t1

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    if  show_time : print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

    return boxes, polys, ret_score_text

""" For test images in a folder """
image_list, _, _ = file_utils.get_files(test_folder)

# Evaluate images and return results

# for k, image_path in enumerate(image_list):
#     print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path), end='\r')
#     image = imgproc.loadImage(image_path)
#
#     bboxes, polys, score_text = test_net(net, image,  text_threshold,  link_threshold,  low_text,  cuda,  poly, refine_net)
#
#     # save score text
#     filename, file_ext = os.path.splitext(os.path.basename(image_path))
#     mask_file = result_folder + "/res_" + filename + '_mask.jpg'
#     cv2.imwrite(mask_file, score_text)
#
#     file_utils.saveResult(image_path, image[:,:,::-1], polys, dirname=result_folder)
#     crop_sections(image, polys, result_folder, filename)
#





