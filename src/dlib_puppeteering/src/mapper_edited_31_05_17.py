#!/usr/bin/env python3
import sys
import rospy

import roslib
#import cv2

from pau2motors.msg import pau
from dlib_puppeteering.msg import lm_points
roslib.load_manifest('dlib_puppeteering')

import random
import numpy
import numpy as np
from sklearn.linear_model import Ridge

class dlib_puppeteering:
  
  # declare publishers, subscribers, and other important static variables
  def __init__(self):
  
    self.once = 0
    self.dlibX = []
    self.dlibY = []

    self.dlibFaceIndex = []
    self.indexes = [0, 1, 2, 3, 4]  # shapekey indexes tobe mapped

    self.pub_pau = rospy.Publisher('/blender_api/set_pau', pau, queue_size=10)
    self.image_sub = rospy.Subscriber("/dlib_values", lm_points, self.dlib_callback)

    self.blendshape_names = ['brow_center_UP', 'brow_center_DN', 'brow_inner_UP.L', 'brow_inner_DN.L', 'brow_inner_UP.R',
                          'brow_inner_DN.R', 'brow_outer_UP.L', 'brow_outer_DN.L', 'brow_outer_up.R', 'brow_outer_DN.R',
                          'eye-flare.UP.L', 'eye-blink.UP.L', 'eye-flare.UP.R', 'eye-blink.UP.R', 'eye-blink.LO.L',
                          'eye-flare.LO.L', 'eye-blink.LO.R', 'eye-flare.LO.R', 'wince.L', 'wince.R', 'sneer.L',
                          'sneer.R', 'eyes-look.dn', 'eyes-look.up', 'lip-UP.C.UP', 'lip-UP.C.DN', 'lip-UP.L.UP',
                          'lip-UP.L.DN', 'lip-UP.R.UP', 'lip-UP.R.DN', 'lips-smile.L','lips-smile.R', 'lips-wide.L',
                          'lips-narrow.L', 'lips-wide.R', 'lips-narrow.R', 'lip-DN.C.DN', 'lip-DN.C.UP', 'lip-DN.L.DN',
                          'lip-DN.L.UP', 'lip-DN.R.DN', 'lip-DN.R.UP', 'lips-frown.L', 'lips-frown.R','lip-JAW.DN']
    
    #x_normalized = 'hello'
    '''y_normalized = normalize(self.dlibY)
    xy = x_normalized + y_normalized
    xy = np.array(xy)
    browsup_model = Ridge(alpha = alpha)
    browsup_model.coeff_ = coeff_brows_up
    browsup_model.intercept_ = intercept_brows_up
    alpha = 0.1
    ridge = Ridge(alpha = alpha)''' 
  
  # callback: gets relative distance of DLIB's land marks per their corresponding shapekey
  def dlib_callback(self, data):

      coeff_brows_up = ([-0.03994529,  0.05965983,  0.26604942, -0.10001976,  0.02571235,
       -0.15743366, -0.15107966,  0.05932797, -0.04445027, -0.00051184,
       -0.01794235,  0.08205211, -0.02737744, -0.04503058,  0.00097107,
        0.03430173,  0.00135388,  0.12086409,  0.24367876,  0.12423624,
        0.12427326, -0.12390761,  0.16738411, -0.03294159, -0.02225945,
       -0.09150146, -0.05671128,  0.00994966, -0.0041362 ,  0.11825082,
       -0.07925411, -0.08126947, -0.05907555, -0.09782393,  0.04432068,
       -0.0397211 , -0.09751762, -0.17953067,  0.06043592,  0.10127657,
        0.02658325, -0.07335536, -0.21000558,  0.04144996, -0.01290343,
        0.06514291,  0.00780998,  0.01651065,  0.19827989, -0.00394886,
        0.00552164, -0.20197584,  0.02243605, -0.0724711 , -0.15828425,
        0.00535809,  0.10761565, -0.02992744,  0.07518744,  0.13417684,
        0.00995507,  0.08043928,  0.14559729, -0.07282683, -0.01328051,
        0.0701037 ,  0.01477559,  0.0152705 , -0.14343098,  0.15201524,
       -0.14463469,  0.02412382,  0.0697816 ,  0.00741937,  0.00819093,
       -0.03161338, -0.11183878, -0.00521626, -0.0349472 ,  0.08937093,
        0.02370157,  0.05277089, -0.0681871 ,  0.02369042, -0.05190085,
        0.05925793,  0.1404831 ,  0.05088367, -0.29246621, -0.09831926,
       -0.10359141, -0.04927141, -0.04304857,  0.18312706,  0.13543494,
       -0.18588968, -0.02794997, -0.13353171, -0.00807263, -0.1083353 ,
        0.12407571,  0.02983456,  0.16133227, -0.15397156, -0.12894383,
       -0.08374003, -0.03608447, -0.03653539, -0.08866398, -0.05310818,
       -0.08937821,  0.03761951,  0.13386111, -0.11045425,  0.03025596,
        0.047111  ,  0.060447  , -0.01068462,  0.0219471 , -0.01606329,
        0.14224367,  0.16036216, -0.03929058,  0.06096333, -0.06239731,
        0.07814062,  0.07903677,  0.10244747,  0.04471812, -0.04535393,
        0.01450537,  0.01261773,  0.0079287 , -0.09126498,  0.00105649,
       -0.10070298])
      coeff_brows_up = numpy.array(coeff_brows_up)

      intercept_brows_up = 0.24949174560098603

      self.dlibX = data.dlib_X
      self.dlibY = data.dlib_Y
      self.dlibFaceIndex = data.dlib_face_index

      head_pau = pau()

      head_pau.m_headRotation.x = 0.9
      head_pau.m_headRotation.y = 0.5
      head_pau.m_headRotation.z = 0.7
      head_pau.m_headRotation.w = 0.9

      head_pau.m_headTranslation.x =0.9
      head_pau.m_headTranslation.y =0.7
      head_pau.m_headTranslation.z =0.8

      head_pau.m_neckRotation.x= -0.9
      head_pau.m_neckRotation.y= -0.5
      head_pau.m_neckRotation.z= 0.5
      head_pau.m_neckRotation.w= 0.9

      head_pau.m_eyeGazeLeftPitch = 0.01
      head_pau.m_eyeGazeLeftYaw = 0.1
      head_pau.m_eyeGazeRightPitch = 0.01
      head_pau.m_eyeGazeRightYaw = 0.1

      head_pau.m_shapekeys = self.blendshape_names
      head_pau.m_coeffs = self.doMapping()

      self.pub_pau.publish(head_pau) # publish to "/blender_api/set_pau"

      

  '''def ridge_mouthleft(self):

      dlib = numpy.loadtxt('' + "/home/meareg/dlib_ws/src/dlib_puppeteering/src/mouthright_dlib.csv", delimiter=",", skiprows=1)
      fs = numpy.loadtxt('' + "/home/meareg/dlib_ws/src/dlib_puppeteering/src/mouthright_only_fs.csv", delimiter=",", skiprows=1)
      
      dlib_array = numpy.array(dlib)
      fs_array = numpy.array(fs)
      
      alpha = 0.1
      ridge = Ridge(alpha = alpha)
      ridge.fit(dlib_array[0:200], fs_array[0:200])
      #ridge.fit(dd[100:450], fs[100:450])
      #ridge.fit(dd[100:450], fs[100:450])
      #ridge.fit(ddxy[100:450], fs[100:450])
      #ridge.score(ddxy[0:100], fs[0:100])
      #ridge.score(ddxy[450:595], fs[450:595])


   
      #ridge = Ridge(0.1)
      #ridge.fit(ddxy[0:2], fs[0:2])
      #ridge.fit(brow_sel[0:2], fs[0:2])
      #ridge._coeff = coeff_brows_up
      #ridge._coeff = coeff_brows_up_2
      #ridge._intercept = intercept_brows_up
      #ridge._coeff = coeff_brows_up_fake
      #ridge._intercept = intercept_brows_up_2
      return ridge'''
      


  def ridge_brow_model(self):
      dlib_xy = numpy.loadtxt('' + "/home/meareg/dlib_ws/src/dlib_puppeteering/src/browsup_unnormalized1.csv", delimiter=",", skiprows=1)
      fs = numpy.loadtxt('' + "/home/meareg/dlib_ws/src/dlib_puppeteering/src/fs_browsup_eyeblink.csv", delimiter=",", skiprows=1)
      dlib_xy_array = numpy.array(dlib_xy)
      fs_array = numpy.array(fs)
      #print(dlib_xy)
      
      alpha = 0.1
      ridge = Ridge(alpha = alpha)
      #ridge.fit(dlib_xy_array[100:450], fs_array[100:450])
      #ridge.fit(dd[100:450], fs[100:450])
      #ridge.fit(dd[100:450], fs[100:450])
      #ridge.fit(ddxy[100:450], fs[100:450])
      ridge.fit(dlib_xy_array[0:100], fs_array[0:100])
      #ridge.score(ddxy[450:595], fs[450:595])

      #ridge = Ridge(0.1)
      #ridge.fit(ddxy[0:2], fs[0:2])
      #ridge.fit(brow_sel[0:2], fs[0:2])
      #ridge._coeff = coeff_brows_up
      #ridge._coeff = coeff_brows_up_2
      #ridge._intercept = intercept_brows_up
      #ridge._coeff = coeff_brows_up_fake
      #ridge._intercept = intercept_brows_up_2
      return ridge

  def doMapping(self):
      xy_normalized = []
      x_new = []
      
      # brows up 256x256 neutral expressions of dlib points from x[0], x[17:27] to y[0], y[17:27] (points most important during brows up)
      #neutral_brows = ([72, 82, 95, 108, 121, 139, 151, 163, 175, 183, 87, 79, 76, 78, 83, 83, 78, 76, 79, 87])
      # brows up 256x256 neutral expressions of dlib points from x[0], x[17:27] to y[8], y[17:27](points most important during brows up and x[0] and y[0] are static reference points for the brow lines)#index 89
      neutral_brows_scaled = ([57, 67, 75, 87, 99, 110, 129, 140, 151, 162, 169, 203, 84 ,76, 74, 77, 81, 81, 77, 75, 78, 86]) # index 89


      #neutral_brows_scaled = ([70, 79, 93, 107, 120, 138, 150, 163, 175, 184, 90, 81, 78, 80, 85, 85, 80, 79, 81, 90])
      #neutral_mouthleft_import_landmarks  = ([X52, X53, X54, X55, X56, X57, X60, X61, X62, X63, X64, X65, X66, X67])

      #neutral_mouthleft = ([140, 150, 159, 150, 140, 132, 110, 124, 132, 140, 154, 140, 132, 124])


      
      # convert the 256x256 to its 640x480 resolution equivalent. Doing this increases the gaps between numbers which in return would be good give chance of delicate numbers being detected during prediction correctly.
      # Use the formula below for conversion:
      ''' neutral_brows_scaled = []
          for i in range(0, len(neutral_brows)):
              neutral_brows_scaled.append(neutral_pose_brows_up[i]*604/256)'''


      #neutral_brows_scaled = ([169.875, 193.46875, 224.140625, 254.8125, 285.484375, 327.953125, 356.265625, 384.578125, 412.890625, 431.765625, 205.265625, 186.390625, 179.3125, 184.03125, 195.828125, 195.828125, 184.03125, 179.3125, 186.390625, 205.265625])
      
      # Map any corresponding landmark input points (x[17:27], y[17:27]) from dlib relative to the given neutral pose landmarks on the above line.
      # sample dlib values of a single frame

      #x_brow = ([321, 332, 347, 364, 379, 408, 424, 441, 458, 472])	
      #y_brow= ([176, 165, 162, 164, 169, 168, 161, 158, 160, 171])
      #x = x/640 * 256
      #y = y/480 * 256

      x = self.dlibX[0:67]
      y = self.dlibY[0:67]


      x_brow = []
      y_brow = []

      x_brow_i = x[17:27]
      y_brow_i = y[17:27]

      x_brow.append(x[0])
      y_brow.append(y[8])

      for i in range(0, len(x_brow_i)):
          x_brow.append(x_brow_i[i])
          
      for i in range(0, len(y_brow_i)):
          y_brow.append(y_brow_i[i])

      x_neutral = neutral_brows_scaled[0:11]
      y_neutral = neutral_brows_scaled[11:22]

      '''x_brows_scaled = []
      for i in range(0, len(x_brow)):
          x_brows_scaled.append(x_brow[i]*256/640)

      y_brows_scaled = []
      for i in range(0, len(y_brow)):
          y_brows_scaled.append(y_brow[i]*256/480)

      x_brow = x_brows_scaled 
      y_brow = y_brows_scaled'''

      print('xy_brow')
      print(x_brow + y_brow)
      print('length of xy_brow')
      print(len(x_brow + y_brow))



      '''x_i_mouthleft = x[52:57]
      x_ii_mouthleft = x[60:67]
      x_mouthleft = [x_i_mouthleft, x_ii_mouthleft]



      x_mouthleft_new = [x_mouthleft[0], x_mouthleft[1]]
      j = 0      
      for i in range(2, len(x_mouthleft)):

          x_mouthleft_new.append(x_mouthleft_new[j] + ((x_mouthleft[i] - x_mouthleft[0]) * (neutral_mouthleft[i-1] - neutral_mouthleft[0])/(x_mouthleft[i-1] - x_mouthleft[0])))
          j = j + 1


      x_brow_new = [x_neutral[0], x_neutral[1]]

      #x_brow_new.append(neutral_brows_scaled[0] + (x_brow[1] - x_brow[0]))

      y_brow_new = [y_neutral[0], y_neutral[1]]
      #y_brow_new.append(neutral_brows_scaled[0] + (y_brow[1] - y_brow[0]))

      x_mouthleft_numpy = numpy.array(mouthleft_new)
      ridge_mouthleft = self.ridge_mouthleft()
      predicted_mouthleft = ridge_mouthleft.predict(x_mouthleft_numpy)
      print('predicted_mouthleft')
      print(predicted_mouthleft)'''

      x_brow_new = [neutral_brows_scaled[0], neutral_brows_scaled[1]]
      #x_brow_new.append(neutral_brows_scaled[0] + (x_brow[1] - x_brow[0]))

      y_brow_new = [neutral_brows_scaled[11], neutral_brows_scaled[12]]
      #y_brow_new.append(neutral_brows_scaled[0] + (y_brow[1] - y_brow[0]))
      #x_brow_new = [x_neutral[0], x_neutral[1]]

      for i in range(2, len(x_brow)):
          j = 0
          x_brow_new.append(x_brow_new[0] + ((x_brow[i] - x_brow[0]) * (x_neutral[1] - x_neutral[0])/(x_brow[1] - x_brow[0])))

      # try it out how good this approach is when it comes to y too.
      for i in range(2, len(y_brow)):
          y_brow_new.append(y_brow_new[0] + ((y_brow[i] - y_brow[0]) * (y_neutral[1] - y_neutral[0])/(y_brow[1] - y_brow[0])))
    
      #to be fed to the ridge model
      xy_brow_new = x_brow_new + y_brow_new

      print('xy_brow_new')
      print(xy_brow_new)
      print('length of xy_brow_new')
      print(len(xy_brow_new))      

      brow_numpy = numpy.array(xy_brow_new)
      ridge_brow = self.ridge_brow_model()
      predicted_brow = ridge_brow.predict(brow_numpy)
      predicted_brow = predicted_brow - 2 
      print(predicted_brow)
      '''if self.once == 0:
          self.once = 1
          self.ridge = self.ridge_model()
          predicted_brow  = self.ridge.predict(ddxy[0:100])
          predicted_brow  = self.ridge.predict(ddxy[450:590])
          print(predicted_brow)
          print(predicted_brow)'''
      #else:
      #predicted_shapekey = ridge.predict(xy_normalized)

      blendshape_values = []
      for i in range(0, 45): # modify this block to include the machine learning approach
          if i in self.indexes:
              #random_val= random.random() # generate some random values between 0 and 1
              #blendshape_values.append(random_val)
              blendshape_values.append(predicted_brow) 
              #blendshape_values.append(predicted_shapekey[i])
              #print('random on print')
              #if i == 28:
              #    blendshape_values.append(predicted_mouthleft)
          else:
              blendshape_values.append(0.0)
          #if i == 44:
          #    i = 0
      print(blendshape_values)
      return blendshape_values

def main(args):
  rospy.init_node('dlib2blender_mapper', anonymous=True)
  dlib_puppeteering()
  try:
      rospy.spin()
  except KeyboardInterrupt:
      print("Dlib-Puppeteering Exiting...")
      #cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)






