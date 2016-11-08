import MySQLdb as Mdb
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Hardcoded
DB_HOST = "localhost"
DB_USER = "frav"
DB_PASS = "VXxL4UOLvB6wc01Y3Cxi"
DB_NAME = "frav_ABC"
FOLDER = "/media/alberto/Datos/FRAV_ALBERTO/"

con = Mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
cur = con.cursor()

# attributes = ["locateFace", "faceConfidence", "locateEyes", "eye0Confidence", "eye1Confidence", "age",
#         "backgroundUniformity", "chin", "crown", "deviationFromFrontalPose", "deviationFromUniformLighting", "ear0",
#         "ear1", "ethnicityAsian", "ethnicityBlack", "ethnicityWhite", "exposure", "eye0X", "eye0Y", "eye0GazeFrontal",
#         "eye0Open", "eye0Red", "eye0Tinted", "eye1X", "eye1Y", "eye1GazeFrontal", "eye1Open", "eye1Red", "eye1Tinted",
#         "eyeDistance", "faceCenterX", "faceCenterY", "glasses", "grayScaleDensity", "height", "hotSpots", "isColor",
#         "isMale", "lengthOfHead", "mouthClosed", "naturalSkinColour", "numberOfFaces", "poseAngleRoll", "sharpness",
#         "width", "widthOfHead", "ISO_19794_5_EyesGazeFrontalBestPractice", "ISO_19794_5_EyesNotRedBestPractice",
#         "ISO_19794_5_EyesOpenBestPractice", "ISO_19794_5_GoodExposure", "ISO_19794_5_GoodGrayScaleProfile",
#         "ISO_19794_5_GoodVerticalFacePosition", "ISO_19794_5_HasNaturalSkinColour",
#         "ISO_19794_5_HorizontallyCenteredFace", "ISO_19794_5_ImageWidthToHeightBestPractice",
#         "ISO_19794_5_IsBackgroundUniformBestPractice", "ISO_19794_5_IsBestPractice", "ISO_19794_5_IsCompliant",
#         "ISO_19794_5_IsFrontal", "ISO_19794_5_IsFrontalBestPractice", "ISO_19794_5_IsLightingUniform",
#         "ISO_19794_5_IsSharp", "ISO_19794_5_LengthOfHead", "ISO_19794_5_LengthOfHeadBestPractice",
#         "ISO_19794_5_MouthClosedBestPractice", "ISO_19794_5_NoHotSpots", "ISO_19794_5_NoTintedGlasses",
#         "ISO_19794_5_OnlyOneFaceVisible", "ISO_19794_5_Resolution", "ISO_19794_5_ResolutionBestPractice",
#         "ISO_19794_5_WidthOfHead", "ISO_19794_5_WidthOfHeadBestPractice", "Features_Ethnicity", "Features_Gender",
#         "Features_WearsGlasses"]

attributes = ["ISO_19794_5_EyesGazeFrontalBestPractice", "ISO_19794_5_EyesNotRedBestPractice",
         "ISO_19794_5_EyesOpenBestPractice", "ISO_19794_5_GoodExposure", "ISO_19794_5_GoodGrayScaleProfile",
         "ISO_19794_5_GoodVerticalFacePosition", "ISO_19794_5_HasNaturalSkinColour",
         "ISO_19794_5_HorizontallyCenteredFace", "ISO_19794_5_ImageWidthToHeightBestPractice",
         "ISO_19794_5_IsBackgroundUniformBestPractice", "ISO_19794_5_IsBestPractice", "ISO_19794_5_IsCompliant",
         "ISO_19794_5_IsFrontal", "ISO_19794_5_IsFrontalBestPractice", "ISO_19794_5_IsLightingUniform",
         "ISO_19794_5_IsSharp", "ISO_19794_5_LengthOfHead", "ISO_19794_5_LengthOfHeadBestPractice",
         "ISO_19794_5_MouthClosedBestPractice", "ISO_19794_5_NoHotSpots", "ISO_19794_5_NoTintedGlasses",
         "ISO_19794_5_OnlyOneFaceVisible", "ISO_19794_5_Resolution", "ISO_19794_5_ResolutionBestPractice",
         "ISO_19794_5_WidthOfHead", "ISO_19794_5_WidthOfHeadBestPractice", "Features_Ethnicity", "Features_Gender",
         "Features_WearsGlasses"]

bins = np.linspace(0, 1, 11)
for attr in attributes:
    plt.figure()
    for i in np.arange(2):
        cur.execute("SELECT p.clase, i.clase, s.score FROM score_data s INNER JOIN imgs_data i ON s.id_img = i.id INNER JOIN pass_data p ON s.id_pass = p.id WHERE i.camera = 1 AND i.light = 1 AND i." + attr + "=" + str(i))
        data = cur.fetchall()
        # data = random.sample(data, 200000)
        data = np.asarray(data)
        data = [x for x in data if x[2] >= 0]
        data = [x for x in data if x[2] <= 1]
        scores_true = [x[2] for x in data if x[0] == x[1]]
        scores_false = [x[2] for x in data if x[0] != x[1]]
        scores_false = random.sample(scores_false, len(scores_true))
        i_plot = 1 if i == 0 else 2
        plt.subplot(210 + i_plot)
        plt.hist(scores_true, bins, alpha=0.5, label='true')
        plt.hist(scores_false, bins, alpha=0.5, label='false')
        plt.title(attr + "_" + str(i))
        plt.xlabel("score")
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig(attr + ".png")
    plt.close()

